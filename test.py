import os
import tempfile
import threading
import time
import unittest

from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server

from app import create_app, db
from app.models import User, Scenario, Run


def make_test_app(database_path=None):
    app = create_app()

    if database_path is None:
        database_path = tempfile.mktemp(suffix=".db")

    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
        SERVER_NAME=None,
    )

    return app


def create_test_user(username="alice", email="alice@example.com", password="password123"):
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return user


def create_test_scenario():
    scenario = Scenario(
        title="Test Scenario",
        genre="Sci-Fi",
        difficulty="Easy",
        intro_text="Decode the test signal.",
        passage="abc",
        outcome_high="Excellent signal recovery.",
        outcome_mid="Partial signal recovery.",
        outcome_low="Signal failed.",
        is_official=True,
    )
    db.session.add(scenario)
    db.session.commit()
    return scenario


class XenotypeUnitTests(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_file.close()

        self.app = make_test_app(self.db_file.name)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

        if os.path.exists(self.db_file.name):
            os.unlink(self.db_file.name)

    def test_register_creates_user(self):
        response = self.client.post(
            "/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            user = User.query.filter_by(username="newuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "newuser@example.com")

    def test_register_duplicate_username_redirects(self):
        with self.app.app_context():
            create_test_user(username="duplicate", email="first@example.com")

        response = self.client.post(
            "/register",
            data={
                "username": "duplicate",
                "email": "second@example.com",
                "password": "password123",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Username already exists", response.data)

    def test_login_and_logout_flow(self):
        with self.app.app_context():
            create_test_user(username="loginuser", email="login@example.com")

        login_response = self.client.post(
            "/login",
            data={
                "username": "loginuser",
                "password": "password123",
            },
            follow_redirects=True,
        )

        self.assertEqual(login_response.status_code, 200)

        logout_response = self.client.get("/logout", follow_redirects=True)

        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b"Login", logout_response.data)

    def test_play_route_requires_login(self):
        with self.app.app_context():
            scenario = create_test_scenario()
            scenario_id = scenario.id

        response = self.client.get(f"/play/{scenario_id}", follow_redirects=False)

        self.assertIn(response.status_code, [302, 401])

    def test_submit_run_creates_run_for_logged_in_user(self):
        with self.app.app_context():
            user = create_test_user(username="runner", email="runner@example.com")
            scenario = create_test_scenario()
            scenario_id = scenario.id

        self.client.post(
            "/login",
            data={
                "username": "runner",
                "password": "password123",
            },
            follow_redirects=True,
        )

        response = self.client.post(
            f"/submit_run/{scenario_id}",
            data={
                "wpm": "55",
                "accuracy": "91",
                "time_remaining": "12",
                "errors": "2",
                "grade": "A",
                "wpm_history": "[10, 20, 30]",
            },
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            run = Run.query.filter_by(user_id=user.id, scenario_id=scenario_id).first()
            self.assertIsNotNone(run)
            self.assertEqual(run.wpm, 55)
            self.assertEqual(run.accuracy, 91)
            self.assertEqual(run.grade, "A")

    def test_model_helper_methods(self):
        with self.app.app_context():
            user = create_test_user(username="modeluser", email="model@example.com")
            scenario = create_test_scenario()

            run = Run(
                user_id=user.id,
                scenario_id=scenario.id,
                wpm=80,
                accuracy=95,
                time_remaining=20,
                errors=0,
                grade="S",
                wpm_history="[70, 75, 80]",
            )

            db.session.add(run)
            db.session.commit()

            self.assertEqual(user.get_best_wpm(), 80)
            self.assertEqual(user.get_total_runs(), 1)
            self.assertEqual(run.get_outcome_label(), "Perfect Transmission")
            self.assertTrue(run.is_passing())


class ServerThread(threading.Thread):
    def __init__(self, app, host="127.0.0.1", port=5001):
        super().__init__()
        self.server = make_server(host, port, app)
        self.context = app.app_context()
        self.host = host
        self.port = port

    def run(self):
        self.context.push()
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.context.pop()


class XenotypeSeleniumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
        except ImportError:
            raise unittest.SkipTest("Selenium is not installed. Install it with: pip install selenium")

        cls.webdriver = webdriver
        cls.Options = Options
        cls.By = By
        cls.Keys = Keys
        cls.WebDriverWait = WebDriverWait
        cls.EC = EC

        cls.db_file = tempfile.NamedTemporaryFile(delete=False)
        cls.db_file.close()

        cls.app = make_test_app(cls.db_file.name)

        with cls.app.app_context():
            db.drop_all()
            db.create_all()
            create_test_scenario()

        cls.server = ServerThread(cls.app, port=5001)
        cls.server.daemon = True
        cls.server.start()
        time.sleep(1)

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,900")

        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except Exception as error:
            cls.server.shutdown()
            raise unittest.SkipTest(f"Chrome WebDriver could not start: {error}")

        cls.base_url = "http://127.0.0.1:5001"

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()

        if hasattr(cls, "server"):
            cls.server.shutdown()

        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

        if os.path.exists(cls.db_file.name):
            os.unlink(cls.db_file.name)

    def setUp(self):
        self.driver.delete_all_cookies()

    def register_user(self, username, email, password="password123"):
        self.driver.get(f"{self.base_url}/register")

        self.driver.find_element(self.By.NAME, "username").send_keys(username)
        self.driver.find_element(self.By.NAME, "email").send_keys(email)
        self.driver.find_element(self.By.NAME, "password").send_keys(password)
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()

    def login_user(self, username, password="password123"):
        self.driver.get(f"{self.base_url}/login")

        self.driver.find_element(self.By.NAME, "username").send_keys(username)
        self.driver.find_element(self.By.NAME, "password").send_keys(password)
        self.driver.find_element(self.By.CSS_SELECTOR, "button[type='submit']").click()

    def test_selenium_user_registration_flow(self):
        self.register_user("selenium_register", "selenium_register@example.com")

        self.WebDriverWait(self.driver, 5).until(
            self.EC.url_contains("/login")
        )

        self.assertIn("/login", self.driver.current_url)

    def test_selenium_login_flow(self):
        with self.app.app_context():
            create_test_user(username="selenium_login", email="selenium_login@example.com")

        self.login_user("selenium_login")

        self.WebDriverWait(self.driver, 5).until(
            self.EC.url_to(f"{self.base_url}/")
        )

        self.assertEqual(self.driver.current_url.rstrip("/"), self.base_url)

    def test_selenium_scenarios_page_loads(self):
        with self.app.app_context():
            create_test_user(username="selenium_scenarios", email="selenium_scenarios@example.com")

        self.login_user("selenium_scenarios")
        self.driver.get(f"{self.base_url}/scenarios")

        self.assertIn("Test Scenario", self.driver.page_source)

    def test_selenium_typing_game_flow(self):
        with self.app.app_context():
            create_test_user(username="selenium_typing", email="selenium_typing@example.com")
            scenario = Scenario.query.first()
            scenario_id = scenario.id

        self.login_user("selenium_typing")
        self.driver.get(f"{self.base_url}/play/{scenario_id}")

        self.WebDriverWait(self.driver, 5).until(
            self.EC.presence_of_element_located((self.By.ID, "hidden-input"))
        )

        self.driver.execute_script("document.getElementById('hidden-input').focus();")
        active = self.driver.switch_to.active_element
        active.send_keys("abc")

        self.WebDriverWait(self.driver, 8).until(
            self.EC.url_contains("/outcome/")
        )

        self.assertIn("/outcome/", self.driver.current_url)

    def test_selenium_leaderboard_navigation(self):
        with self.app.app_context():
            user = create_test_user(username="selenium_leaderboard", email="selenium_leaderboard@example.com")
            scenario = Scenario.query.first()

            run = Run(
                user_id=user.id,
                scenario_id=scenario.id,
                wpm=75,
                accuracy=96,
                time_remaining=10,
                errors=1,
                grade="A",
                wpm_history="[60, 70, 75]",
            )

            db.session.add(run)
            db.session.commit()

        self.driver.get(f"{self.base_url}/leaderboard")

        self.assertIn("selenium_leaderboard", self.driver.page_source)

        profile_link = self.driver.find_element(
            self.By.LINK_TEXT,
            "selenium_leaderboard",
        )

        profile_link.click()

        self.WebDriverWait(self.driver, 5).until(
            self.EC.url_contains("/profile/selenium_leaderboard")
        )

        self.assertIn("/profile/selenium_leaderboard", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)
