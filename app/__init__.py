import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.game import game
    from app.routes.scenario import scenario
    from app.routes.campaign import campaign
    from app.routes.chat import chat

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(game)
    app.register_blueprint(scenario, url_prefix='/scenario')
    app.register_blueprint(campaign)
    app.register_blueprint(chat)

    os.makedirs(
        os.path.join(app.config['UPLOAD_FOLDER'], 'profile_photos'),
        exist_ok=True
    )

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
