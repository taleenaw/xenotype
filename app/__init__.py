import os

from flask_wtf.csrf import CSRFProtect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    #-----------------------------------------------------

    if test_config:

        app.config.update(test_config)

    #-----------------------------------------------------

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.game import game
    from app.routes.scenario import scenario
    from app.routes.campaign import campaign
    from app.routes.chat import chat
    from app.routes.bot import bot

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(game)
    app.register_blueprint(scenario, url_prefix='/scenario')
    app.register_blueprint(campaign)
    app.register_blueprint(chat)
    app.register_blueprint(bot)

    os.makedirs(
        os.path.join(app.config['UPLOAD_FOLDER'], 'profile_photos'),
        exist_ok=True
    )

    from flask import flash, redirect, request, url_for

    @app.errorhandler(413)
    def too_large(e):
        flash('File too large. Maximum size is 2 MB. Please choose a smaller image.')
        return redirect(request.referrer or url_for('main.lobby'))

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
