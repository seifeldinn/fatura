from app.models import roles_permissions
from app.models.roles import Role
from flask_restx import Namespace, fields
from app.models.roles_permissions import RolesPermissions

class RoleDto:

    api = Namespace("Roles", description="User Roles.")
    
    rolesPermissions = api.model(
        "role's permissions Data Response",
        {
            "id": fields.Integer,
            "add": fields.Boolean,
            "view": fields.Boolean,
            "edit": fields.Boolean,
            "path": fields.String,
            "name": fields.String
        },
    )
    role = api.model(
        "Role object",
        {
            "id": fields.Integer,
            "name": fields.String,
            "rolePermissions": fields.List(fields.Nested(rolesPermissions, as_list=True))
        },
    )
    
    just_role = api.model(
        "Role object",
        {
            "id": fields.Integer,
            "name": fields.String,
        },
    )
    
    village_role = api.model(
        "Role object",
        {
            "id": fields.Integer,
            "user_id": fields.Integer,
            "village_id": fields.Integer,
            "role_id": fields.Integer
        },
    )

    data_resp = api.model(
        "User Data Response",
        {
            # "status": fields.Boolean,
            # "message": fields.String,
            "role": fields.Nested(RolesPermissions)
        },
    )
    
    
    


