from flask_restx import Namespace, fields


class PermissionsDto:

    api = Namespace("Permissions", description="Permissions defind for roles.")
    permission = api.model(
        "Permissions",
        {
            "name": fields.String,
            "edit": fields.Boolean,
            "add": fields.Boolean,
            "view": fields.Boolean,
            "delete": fields.Boolean,
            "path": fields.String,
        },
    )
    permission_ret = api.inherit(
        "Permissions", permission,
        {
            "id": fields.Integer
        },
    )

    data_resp = api.model(
        "Permission Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "role": fields.Nested(permission),
        },
    )
