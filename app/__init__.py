import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def ensure_profile_photo_column(app):
    """
    Small SQLite helper for this student project.

    db.create_all() creates new tables, but it does not add new columns to an
    existing table. This keeps older local xenotype.db files working after the
    profile_photo field was added.
    """
    with app.app_context():
        if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite"):
            from sqlalchemy import text

            columns = db.session.execute(text("PRAGMA table_info(user)")).fetchall()
            column_names = {column[1] for column in columns}

            if "profile_photo" not in column_names:
                db.session.execute(
                    text("ALTER TABLE user ADD COLUMN profile_photo VARCHAR(255)")
                )
                db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.game import game
    from app.routes.scenario import scenario
    from app.routes.campaign import campaign
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(game)
    app.register_blueprint(scenario,url_prefix='/scenario')
    app.register_blueprint(campaign)

    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_photos'), exist_ok=True)
    ensure_profile_photo_column(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
