import unittest
import coverage

from flask_migrate import stamp

from app import manager
from app import current_app as app
from app.models import db
from app.models.user import User
from app.models.show import Show
from app.api.helpers.db import get_or_create
from populate_db import populate


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*'
    ]
)
COV.start()


@manager.command
def list_routes():
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(
            rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('admin/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('admin/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def initialize_db():
    with app.app_context():
        populate_data = True
        try:
            db.drop_all()
            db.create_all()
            stamp()
        except Exception:
            populate_data = False
            print("[LOG] Could not create tables. Either database does not exist or tables already created")
        if populate_data:
            populate()


@manager.command
def reset_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()