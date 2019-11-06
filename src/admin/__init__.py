import os

from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import flask_restplus
from werkzeug.contrib import fixers

from admin import settings

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def register_api(_app):
    from admin.api.users import users_blueprint
    from admin.api.auth import auth_blueprint
    from admin.api.shows import ns as shows_ns
    # _app.register_blueprint(auth_blueprint)
    # _app.register_blueprint(users_blueprint)

    blueprint = Blueprint('api', __name__)
    api = flask_restplus.Api(
        app=blueprint,
        doc=settings.SWAGGER_PATH,
        version=settings.API_VERSION,
        title='Shows On Demand - Admin Service REST API',
        description='Shows on deman Admin service API for the administration of shows.',
        validate=settings.RESTPLUS_VALIDATE
    )
    api.add_namespace(shows_ns, path='/{}/shows'.format(settings.API_VERSION))
    _app.register_blueprint(blueprint)


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    # app.config.from_pyfile(settings.__file__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    app.wsgi_app = fixers.ProxyFix(app.wsgi_app)

    # register blueprints
    register_api(app)
    return app