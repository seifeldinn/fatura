from flask_restx import Resource
from flask import request
from flask_jwt_extended.view_decorators import jwt_required
from app.utils import err_resp, role_validation

from .service import PermissionService
from .dto import PermissionsDto

from app.models.permissions import Permissions
from app.utils import SearchService
api = PermissionsDto.api
data_resp = PermissionsDto.data_resp
_permission = PermissionsDto.permission
_permission_ret = PermissionsDto.permission_ret

@api.route("/")
class AddRole(Resource):
#this does that
    @api.expect(_permission, validate=True)
    @api.doc(
            "Get a specific Client's Notes",
            responses={
                200: ("Data successfully created"),
                404: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()

    def post(self):
        """Creates a new permission """
        data = request.json
        return PermissionService.add_permission(data=data)
    
    @jwt_required()
    @role_validation()

    def get(self):
        """ Get all permission's data """
        permissions = PermissionService.get_permissions()
        if not permissions:
            return err_resp("Data not found!", "Permission_204", 204)

        return api.marshal(permissions, _permission_ret), 200

@api.route("/retrieve/")
class PermissionRetrieval(Resource):
    @api.doc(
            "Retrieve Permissions",
            responses={
                200: ("Data successfully retrieved"),
                404: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()
    def get(self):
        """ Get a specific permission's data by it's id """
        id = request.args.get('id')        
        permissions = SearchService.search(Permissions, id)
        if not permissions:
            return err_resp("Data not found!", "Permission_204", 204)

        return api.marshal(permissions, _permission_ret), 200

@api.route("/reverse")
class RoleServices(Resource):
#this does that
    @api.doc(
            "retrieve alternate permissions",
            responses={
                200: ("Data successfully Retrieved"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()
    
    def get(self):
        """ Get a specific Role's data by it's name """
        role_id = request.args.get('role_id')        
        permissions = PermissionService.get_alt_permissions(role_id)
        if not permissions:
            return err_resp("Data not found!", "operators_204", 204)

        return api.marshal(permissions, _permission_ret), 200
