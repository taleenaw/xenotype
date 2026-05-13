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
