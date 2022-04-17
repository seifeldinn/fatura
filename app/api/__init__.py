from flask_restx import Api
from flask import Blueprint

from .user.controller import api as user_ns
from .auth.controller import api as auth_ns
from .roles.controller import api as role_ns
from .permissions.controller import api as permission_ns

    # app.register_blueprint(auth_bp)

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="API", description="Main routes.")


# API namespaces
api.add_namespace(auth_ns, "/api/auth")
api.add_namespace(user_ns, "/api/user")
api.add_namespace(role_ns, "/api/role")
api.add_namespace(permission_ns, "/api/permission")
