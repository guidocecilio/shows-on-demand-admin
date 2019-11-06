import os
import argparse

# import flask
# import flask_restplus
# from flask import Blueprint
# from werkzeug.contrib import fixers

from flask import Flask, jsonify
from flask_cors import CORS
import flask_restplus
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from werkzeug.contrib import fixers

from admin import settings

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def register_api(_app):
    # from admin.api.predictors import ns as predictors_ns

    # blueprint = Blueprint('api', __name__)
    # api = flask_restplus.Api(
    #     app=blueprint,
    #     doc=settings.SWAGGER_PATH,
    #     version=settings.API_VERSION,
    #     title='Shows On Demand - Admin Service REST API',
    #     description="""Shows on deman Admin service API for the administration
    #     of shows.""",
    #     validate=settings.RESTPLUS_VALIDATE
    # )
    # api.add_namespace(predictors_ns, path='/{}/organizations/<organization_id>/predictors'.format(settings.API_VERSION))
    # _app.register_blueprint(blueprint)

    from admin.api.users import users_blueprint
    from admin.api.auth import auth_blueprint
    _app.register_blueprint(auth_blueprint)
    _app.register_blueprint(users_blueprint)

    # @api.errorhandler
    # def default_error_handler(error):
    #     return exceptions.APIException(str(error)).to_dict()


def bootstrap_application():
    _app = Flask('admin')
    _app.config.from_pyfile(settings.__file__)
    # _app_settings = os.getenv('APP_SETTINGS')
    # _app.config.from_object(_app_settings)

    # set up extensions
    db.init_app(_app)
    bcrypt.init_app(_app)
    migrate.init_app(_app, db)

    _app.wsgi_app = fixers.ProxyFix(_app.wsgi_app)

    # add_health_check(_app)
    register_api(_app)
    return _app


app = bootstrap_application()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Running bottle application.')
    parser.add_argument('--listen', type=str, default='0.0.0.0', help='bind address.')
    parser.add_argument('--port', type=int, default=3031, help='Webserver port')
    parser.add_argument('--mode', type=str, default='dev', help='Mode of application. Possible values: dev, prod.')
    parser.add_argument('--ssl', type=bool, default=False, help='Run app with https.')
    parser.add_argument('--debug', type=bool)
    args = parser.parse_args()

    if args.ssl and args.mode == 'dev':
        from OpenSSL import SSL
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file('ssl.key')
        ctx.use_certificate_file('ssl.cert')
        ssl_ctx = ctx
    else:
        ssl_ctx = None

    app = bootstrap_application()
    app.run(
        app.config.get('HOST', args.listen),
        args.port,
        ssl_context=ssl_ctx,
        use_reloader=True
    )