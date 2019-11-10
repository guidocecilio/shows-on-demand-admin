import os

from flask import Flask, jsonify, Blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import flask_restplus
from werkzeug.contrib import fixers

from app import config

app = Flask(__name__)

# instantiate the extensions
db = SQLAlchemy()
# migrate = Migrate()
bcrypt = Bcrypt()

def register_api(_app):
    from app.api.users import users_blueprint
    from app.api.auth import auth_blueprint
    from app.api.shows import ns as shows_ns
    _app.register_blueprint(auth_blueprint)
    _app.register_blueprint(users_blueprint)

    blueprint = Blueprint('api', __name__)
    api = flask_restplus.Api(
        app=blueprint,
        doc=_app.config['SWAGGER_PATH'],
        version=_app.config['API_VERSION'],
        title='Shows On Demand - Admin Service REST API',
        description='Shows on deman Admin service API for the administration of shows.',
        validate=_app.config['RESTPLUS_VALIDATE']
    )
    api.add_namespace(shows_ns, path='/{}/shows'.format(_app.config['API_VERSION']))
    _app.register_blueprint(blueprint)


def create_app():
    # instantiate the app

    # enable CORS
    CORS(app)

    # set config
    app.config.from_object(os.getenv('APP_SETTINGS', 'app.config.ProductionConfig'))
    
    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    # migrate.init_app(app, db)
    _manager = Manager(app)
    _manager.add_command('db', MigrateCommand)

    

    app.wsgi_app = fixers.ProxyFix(app.wsgi_app)

    # register blueprints
    with app.app_context():
        register_api(app)
    return app, _manager, db

current_app, manager, database = create_app()
