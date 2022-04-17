from app.api.permissions.service import response, save_changes
from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.user import User
from app.models.roles import Role
from app import db


class UserService:
    @staticmethod
    def get_user_data(username):
        """ Get user data by  """
        if not (user := User.query.filter_by(username=username).first()):
            return err_resp("User not found!", "user_404", 404)

        from .utils import load_data

        try:
            user_data = load_data(user)

            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    def add_user_role(data):
        if (existing_user := User.query.filter_by(username=data['username']).first()):
            for role in data['role']:
                new_role = Role(
                            name=role['name'],
                            description=role['Description']
                        )
            existing_user.roles.append(new_role)
            save_changes(new_role)
            return response()


    def save_changes():
        db.session.add()
        db.session.commit()
    

    def response():
            # generate the auth token
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
            }
            return response_object, 201
