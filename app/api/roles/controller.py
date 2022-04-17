from flask_jwt_extended.view_decorators import jwt_required
from flask_restx import Resource
from flask import request

from app.utils import role_validation, err_resp

from .service import RoleService
from .dto import RoleDto

api = RoleDto.api
data_resp = RoleDto.data_resp
_role = RoleDto.role
_just_role = RoleDto.just_role


@api.route("/")
class RoleServices(Resource):
#this does that
    @api.expect(_role, validate=True)
    @api.doc(
            "Create new Role",
            responses={
                200: ("Role data successfully Created"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()

    def post(self):
        data = request.json
        return RoleService.add_role(data=data)

    @jwt_required()
    @role_validation()

    def get(self):
        """ Get a specific Role's data by it's name """
        role_id = request.args.get('role_id')        
        roles = RoleService.get_role(role_id)
        if not roles:
            return err_resp("Data not found!", "operators_204", 204)
        
        return api.marshal(roles, _role), 200
 
@api.route("/removePermission")
class PermissionRemovalService(Resource):
#this does that
    @api.doc(
            "Role's Search",
            responses={
                200: ("Data successfully updated"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()

    def delete(self):
        """remove permission from specific role """
        data = request.json
        return RoleService.remove_permission(data=data)

@api.route("/all")
class RoleRetreivalService(Resource):
#this does that
    @api.doc(
            "Role's List",
            responses={
                200: ("Data successfully updated"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()

    def get(self):
        """ Role's List """
        
        detailed = request.args.get('detailed')        
        roles = RoleService.get_roles()
        if not roles:
            return err_resp("Data not found!", "operators_204", 204)
        if not detailed:
                    return api.marshal(roles, _just_role), 200
        return api.marshal(roles, _role), 200

@api.route("/urole")
class PermissionRegestirationService(Resource):
#this does that
    @api.doc(
            "Add new role for user",
            responses={
                200: ("Data successfully created"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()

    def post(self):
        """add permission from specific role """
        data = request.json
        return RoleService.add_user_role(data=data)
    def delete(self):
        """add permission from specific role """
        data = request.json
        return RoleService.delete_user_role(data=data)