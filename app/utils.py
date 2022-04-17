from sqlalchemy import and_
import os
from flask_jwt_extended import get_jwt, get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request
from flask import request
from functools import wraps
from datetime import datetime
from flask_socketio import emit, namespace
from operator import and_, or_

import logging
from app.models.user import User
from app import db
from config import get_api_key
from config import Config, basedir
import base64   
from app.models.permissions import Permissions
from flask.helpers import send_from_directory

from random import choice
from string import ascii_uppercase


image_destination = basedir + '/' + 'uploads'

def message(status, message):
    response_object = {"status": status, "message": message}
    return response_object

def validation_error(status, errors):
    response_object = {"status": status, "errors": errors}

    return response_object

def err_resp(msg, reason, code):
    err = message(False, msg)
    err["error_reason"] = reason
    return err, code

def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return err_resp("Access Denied!", "user_403", 403)

        return decorator

    return wrapper

def role_validation():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            if not (user := User.query.filter_by(id=user_id).first()):
                return err_resp("User not found!", "user_204", 204)
            logger.info('Request Made by ( ' + user.name + ' ) With Id: ' + str(user.id))
            if not user.is_admin:            
                has_permission = [permission.path==request.path 
                for role in user.roles 
                for permission in role.rolePermissions 
                if (permission.path==request.path) and (permission.edit and request.method=='PUT') or (permission.view and request.method=='GET') or (permission.add and request.method == 'POST') or (permission.delete and request.method == 'DELETE')]

                if True in has_permission:
                    return fn(*args, **kwargs)
                else:
                    return err_resp("Access Denied!", "Auth_403", 403)
            return fn(*args, **kwargs)
        return decorator

    return wrapper
    
class SearchService:
    @staticmethod
    def search(Model, searchString):
        """ Get data by search string """
        search = "%{}%".format(searchString)
        if not (searchResult := Model.query.filter(Model.name.like(search)).all()):
            return None
        return searchResult

class Utilities:

    @staticmethod 
    def response(value, responseMessage, res):

        resp = message(value, responseMessage)
        return resp, res

    @staticmethod
    def delete_changes(data):
        db.session.delete(data)
        db.session.commit()
        return Utilities.response(True, 'Update Success', 200)
        
    @staticmethod
    def save_changes(data):
        db.session.add(data)
        db.session.commit()
        return Utilities.response(True, 'Update Success', 200)

    @staticmethod
    def commit_changes():
        db.session.commit()


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if api_key:
            if api_key == get_api_key():
                return f(*args, **kwargs)
        
        response_object = {
            'status': False,
            'message': 'Provide a valid auth token.'
        }
        return response_object, 200
    return decorated


class __RequestFormatter(logging.Formatter):

    def format(self, record):
        # you can set here everything what you need
        # I just added url and id from GET parameter
        record.url = request.url
        return super().format(record)

# format of our log record.
# print url and id of record which was set in format()
__stream_handler = logging.StreamHandler()
__stream_handler.setFormatter(__RequestFormatter(
    '[%(asctime)s %(levelname)s] requested: %(url)s %(message)s'
))

logger = logging.getLogger('my_loger')
logger.setLevel(logging.INFO)
logger.addHandler(__stream_handler)

def save_changes(data):
        db.session.add(data)
        db.session.commit()
        return response(True, 'Update Success', 200)

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()

def response(value, responseMessage, res):

    resp = message(value, responseMessage)
    return resp, res


def operator_log(data):
    if 'request_status' not in data:
        data['request_status'] = 'success'
    data['time_stamp_log'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # operator_log= mongo.db.operator_log
    room_name = 'operatorlogs'
    emit("welcome", data, room=room_name, namespace="/")
    # operator_log.insert_one(data)
    print(data)
   
# def search(Model, id, exported, path):

#         if exported:    
#             searchResult = Model.query.filter_by(ext_id=id).first()
                
                    
#         searchResult = Model.query.filter_by(id=id).first()
            
        
#         permission = Permissions.query.filter_by(path=path).first()
            
#         return searchResult

def operator_log_initiation():

        operator_log = {}
        
        user_id = get_jwt_identity()   
        user = User.query.filter_by(id=user_id).first()   
        
        match request.method:
            case 'POST':
                    permission = Permissions.query.filter(and_(Permissions.path==request.path, Permissions.add==True)).first()
                    operator_log['method'] = 'Add'
            case 'GET':
                    permission = Permissions.query.filter(and_(Permissions.path==request.path, Permissions.view==True)).first()
                    operator_log['method'] = 'View'
            case 'PUT':
                    permission = Permissions.query.filter(and_(Permissions.path==request.path, Permissions.edit==True)).first()
                    operator_log['method'] = 'Update'
            case 'DELETE':
                    permission = Permissions.query.filter(and_(Permissions.path==request.path, Permissions.delete==True)).first()
                    operator_log['method'] = 'Delete'
        operator_log['device_IP'] = request.remote_addr


        # permission = Permissions.query.filter_by(path=request.path).first()
        
        operator_log['operator_id'] = user.id
        operator_log['operator_name'] = user.name
        operator_log['API'] = request.path
        
        return operator_log

def faliure(data):
    data['request_status']= 'faliure'
    operator_log(data)