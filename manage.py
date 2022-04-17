import os 

import click
from flask_migrate import Migrate
from app import create_app, db, socketio
from flask_cors import CORS, cross_origin
# from flask_script import Manager

# Import models
from app.models.user import User
from app.models.roles import Role
from app.models.permissions import Permissions
from app.models.roles_permissions import RolesPermissions


app = create_app(os.getenv("FLASK_CONFIG") or "development")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

migrate = Migrate(app, db)

# manager = Manager(app)
# @manager.command
def run():
    # app.run(host='0.0.0.0', port=5500, debug=True)
    socketio.run(app, host="0.0.0.0",port=5500)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
     User=User,
      Role=Role,
      RolesPermissions=RolesPermissions,
       Permissions=Permissions
        )

@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """ Run unit tests """
    import unittest

    if test_names:
        """ Run specific unit tests.

        Example:
        $ flask test tests.test_auth_api tests.test_user_model ...
        """
        tests = unittest.TestLoader().loadTestsFromNames(test_names)

    else:
        tests = unittest.TestLoader().discover("tests", pattern="test*.py")

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0

    # Return 1 if tests failed, won't reach here if succeeded.
    return 1
