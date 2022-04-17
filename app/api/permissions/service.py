from flask import current_app
from app import db

from app.utils import message, err_resp, internal_err_resp, operator_log, operator_log_initiation, faliure
from app.models.permissions import Permissions
from app.models.roles import Role

class PermissionService:
    @staticmethod
    def get_permissions():
        """ Get Permissions """
        log_initiation = operator_log_initiation()
        if not (permissions := Permissions.query.all()):
            return None
        operator_log(log_initiation)
        return permissions

    @staticmethod
    def get_permission(id):
        log_initiation = operator_log_initiation()
        """ Get user data by username """
        if not (permissions := Permissions.query.filter_by(id=id).all()):
            faliure(log_initiation)
            return None
        log_initiation['permission']= permissions[0].name
        operator_log(log_initiation)
        return permissions

    # @staticmethod
    # def get_user_data(name):
    #     log_initiation = operator_log_initiation()
    #     """ Get user data by username """
    #     if not (permission := Permissions.query.filter_by(name=name).all()):
    #         faliure(log_initiation)
    #         operator_log(log_initiation)
    #         return None

    #     from .utils import load_data

    #     try:
    #         role_data = load_data(permission)

    #         resp = message(True, "permission data sent")
    #         resp["permission"] = role_data
    #         operator_log(log_initiation)
    #         return resp, 200

    #     except Exception as error:
    #         faliure(log_initiation)
    #         current_app.logger.error(error)
    #         return internal_err_resp()

    @staticmethod
    def add_permission(data):
        log_initiation = operator_log_initiation()
        new_role = Permissions(
            name=data['name'],
            edit=data['edit'],
            view=data['view'],
            add=data['add'],
            delete=data['delete'],
            path=data['path'],
        )
        save_changes(new_role)
        log_initiation['name']= data['name']
        log_initiation['edit']= data['edit']
        log_initiation['view']= data['view']
        log_initiation['add']= data['add']
        log_initiation['delete']= data['delete']
        log_initiation['path']= data['path']
        operator_log(log_initiation)
        return response()

    @staticmethod
    def get_alt_permissions(id):
        log_initiation = operator_log_initiation()
        if not (role := Role.query.filter_by(id=id).first()):
            faliure(log_initiation)
            return err_resp("Role not found!", "role_204", 204)

        if not (permissions := Permissions.query.all()):
            faliure(log_initiation)
            return err_resp("Role not found!", "role_204", 204)
        
        log_initiation['role']= role.name

        permissions = [permission for permission in permissions if permission not in role.rolePermissions]
        
        operator_log(log_initiation)
        return permissions

def response():
        # generate the auth token
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return response_object, 201


def save_changes(data):
        db.session.add(data)
        db.session.commit()

    