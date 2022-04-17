from flask import current_app
from sqlalchemy.sql.elements import and_
from app import db
from flask_jwt_extended import get_jwt, get_jwt_identity

from app.utils import message, err_resp, internal_err_resp, operator_log, operator_log_initiation, faliure
from app.models.roles import Role
from app.models.user import User
from app.models.user import User
from app.models.permissions import Permissions
from app.models.schemas import RoleSchema, VillageSchema

class RoleService:
    # @staticmethod
    # def get_role_data(name):
    #     """ Get role data by username """
    #     if not (role := Role.query.filter_by(name=name).all()):
    #         return None

    #     from .utils import load_data

    #     try:
    #         role_data = load_data(role)

    #         resp = message(True, "User data sent")
    #         resp["role"] = role_data
    #         return resp, 200

    #     except Exception as error:
    #         current_app.logger.error(error)
    #         return internal_err_resp()

    @staticmethod
    def add_role(data):
        log_initiation = operator_log_initiation()
        if not (role := Role.query.filter_by(name=data['name']).first()):
            role = Role(
                name=data['name'],
            )
            log_initiation['role']= role.name
            operator_log(log_initiation)
            return data_response(True, 'Data Added', 200)
        return err_resp("Role Exists!", "role_204", 200)

    @staticmethod
    def get_role(id):
        log_initiation = operator_log_initiation()
        if not (role := Role.query.filter_by(id=id).first()):
            faliure(log_initiation)
            return None

        log_initiation['role']= role.name
        operator_log(log_initiation)
        return role

    @staticmethod
    def get_roles():
        log_initiation = operator_log_initiation()

        user_id = get_jwt_identity()
        if not (user := User.query.filter_by(id=user_id).first()):
            faliure(log_initiation)
            return err_resp("User not found!", "user_204", 200)
        
        if not (roles := Role.query.all()):
            faliure(log_initiation)
            return err_resp("Role not found!", "role_204", 200)
        operator_log(log_initiation)
        return roles

    @staticmethod
    def add_role_permission(data):
        log_initiation = operator_log_initiation()
        if not (role := Role.query.filter_by(id=data['role_id']).first()):
            faliure(log_initiation)
            return err_resp("Role not found!", "role_204", 204)
        numbered = 1
        for permission in data['permissions']:
            koko = Permissions.query.filter_by(id=permission).first()
        
            name = 'permission_' + str(numbered) + 'name'
            log_initiation[name]= koko.name
            numbered+=1

        permissions = [Permissions.query.filter_by(id=permission).first() for permission in data['permissions']  if permission ]
        [role.rolePermissions.append(permission) for permission in permissions if permission not in role.rolePermissions]
        db.session.commit()
        log_initiation['role']= role.name
        operator_log(log_initiation)
        return response()

    @staticmethod
    def add_user_role(data):
        log_initiation = operator_log_initiation()
        
        
        if not (user := User.query.filter_by(id=data['user_id']).first()):
            faliure(log_initiation)
            return err_resp("User not found!", "user_204", 204)

        if not (role := Role.query.filter_by(id=data['role_id']).first()):
            faliure(log_initiation)
            return err_resp("User not found!", "user_204", 204)
        user.roles.append(role)
        db.session.commit()
        log_initiation['user_name']= user.name
        log_initiation['role']= role.name
        operator_log(log_initiation)
        return data_response(True, 'Data Added', 200)

    @staticmethod
    def delete_user_role(data):
        log_initiation = operator_log_initiation()
        
        if not (user := User.query.filter_by(id=data['user_id']).first()):
            faliure(log_initiation)
            return err_resp("User not found!", "user_204", 204)

        if not (role := Role.query.filter_by(id=data['role_id']).first()):
            faliure(log_initiation)
            return err_resp("Role not found!", "role_204", 204)
        user.roles.remove(role)
        db.session.commit()

        log_initiation['user_name']= user.name
        log_initiation['role']= role.name
        operator_log(log_initiation)
        return data_response(True, 'Update Success', 200)

    @staticmethod
    def remove_permission(data):
        log_initiation = operator_log_initiation()
        if not (role := Role.query.filter_by(id=data['role_id']).first()):
            faliure(log_initiation)
            return None

        numbered = 1
        for permission in data['permissions']:
            koko = Permissions.query.filter_by(id=permission).first()
        
            name = 'permission_' + str(numbered) + 'name'
            log_initiation[name]= koko.name
            numbered+=1

        permissions = [Permissions.query.filter_by(id=permission).first() for permission in data['permissions']  if permission ]
        
        [role.rolePermissions.remove(permission) for permission in role.rolePermissions if permission in permissions]
        db.session.commit()
        log_initiation['role']= role.name
        operator_log(log_initiation)
        return data_response(True, 'Update Success', 200)
                
def save_role_changes(obj, permissions):
    db.session.add(obj)

    for permission in permissions:
        db.session.add(permission)

    obj.rolePermissions.extend(permissions)

    if(db.session.commit()):
        return response()

def response():
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return response_object, 201

def save_roles(assocs):

        [db.session.add(assoc) for assoc in assocs]
        db.session.commit()
        return response()

def save_changes(data):
        db.session.add(data)
        db.session.commit()
        
def delete_changes(data):
        db.session.delete(data)
        db.session.commit()
        
def data_response(value, responseMessage, res):

    resp = message(value, responseMessage)
    return resp, res