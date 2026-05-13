import os
import tempfile
import unittest

from werkzeug.security import generate_password_hash

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
