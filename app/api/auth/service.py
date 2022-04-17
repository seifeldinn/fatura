from datetime import datetime
from flask import current_app
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy import and_

from app import db
from app.utils import message, err_resp, internal_err_resp, operator_log, operator_log_initiation, faliure
from app.models.user import User
from app.models.schemas import UserSchema, PermissionsSchema

user_schema = UserSchema()
permission_schema = PermissionsSchema()


class AuthService:
    @staticmethod
    def login(data):
        # log_initiation = operator_log_initiation()
        # Assign vars
        email = data["email"]
        password = data["password"]

        try:
            # Fetch user data
            if not (user := User.query.filter_by(email=email).first()):
                # faliure(log_initiation)
                return err_resp(
                    "The email you have entered does not match any account.",
                    "email_404",
                    404,
                )

            elif user and user.verify_password(password):
                user_info = user_schema.dump(user)

                access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})

                resp = message(True, "Successfully logged in.")
                resp["access_token"] = access_token
                resp["user"] = user_info
                # resp['roles'] = user.roles
                
                # operator_log(log_initiation)       
                return resp, 200
            
            # faliure(log_initiation)
            return err_resp(
                "Failed to log in, password may be incorrect. or maybe not allowed for web login", "password_invalid", 401
            )

        except Exception as error:
            # faliure(log_initiation)
            current_app.logger.error(error)
            return internal_err_resp()
    
    # @staticmethod
    # def forgot(data):
    #     # Assign vars
    #     log_initiation = operator_log_initiation()
    #     old_password = data["old_password"]
    #     new_password = data["new_password"]
    #     user_id = get_jwt_identity()

    #     try:
    #         # Fetch user data
    #         if not (user := User.query.filter_by(id=user_id).first()):
    #             faliure(log_initiation)
    #             return err_resp(
    #                 "User Not Found.", "email_204", 204,
    #             )

    #         elif user and user.verify_password(old_password):
    #             user.password = new_password
    #             db.session.commit()
    #             resp = message(True, "Password Successfully changed.")
                
    #             operator_log(log_initiation)
    #             return resp, 200
            

    #         log_initiation['user_name']= user.name
    #         faliure(log_initiation)
    #         return err_resp(
    #             "Failed Chnage password.", "password_invalid", 401
    #         )

    #     except Exception as error:
    #         faliure(log_initiation)
    #         current_app.logger.error(error)
    #         return internal_err_resp()

    @staticmethod
    def edit_user(data):
        # Assign vars
        log_initiation = operator_log_initiation()
        if not (user := User.query.filter_by(id=data['user_id']).first()):
                faliure(log_initiation)
                return err_resp(
                    "User Not Found.", "User_204", 204,
                )

        if (existing_user := User.query.filter(and_(User.username==data['username'], User.id != data['user_id'] )).all()):
            faliure(log_initiation)
            return err_resp("Username is already taken.", "User_204", 204)
        if (existing_user := User.query.filter(and_(User.email==data['email'], User.id != data['user_id'] )).all()):
            faliure(log_initiation)
            return err_resp("Email is already taken.", "User_204", 204)
        

        user.name = user.name if 'name' not in data else data['name']
        user.email = user.email if 'email' not in data else data['email']
        user.phone_number = user.phone_number if 'phone_number' not in data else data['phone_number']

        user.username = user.username if 'username' not in data else data['username']
        db.session.commit()
        resp = message(True, "User has been updated.")
        log_initiation['user_name']= user.name
        log_initiation['email']= user.email
        log_initiation['phone_number']= user.phone_number
        operator_log(log_initiation)       
        return resp, 201
        
    @staticmethod
    def register(data):
        # Assign vars
        # log_initiation = operator_log_initiation()

        ## Required values
        email = data["email"]
        username = data["username"]
        password = data["password"]
        phone_number = data["phone_number"]

        ## Optional
        data_name = data.get("name")
        # log_initiation['email']= email
        # log_initiation['user_name']= username
        # log_initiation['phone_number']= phone_number
        # log_initiation['name']= data_name
        # Check if the email is taken
        if User.query.filter_by(email=email).first() is not None:
            # faliure(log_initiation)
            return err_resp("Email is already being used.", "email_taken", 403)

        # Check if the username is taken
        if User.query.filter_by(username=username).first() is not None:
            # faliure(log_initiation)
            return err_resp("Username is already taken.", "username_taken", 403)

        try:
            
            new_user = User(
                email=email,
                username=username,
                name=data_name,
                password=password,
                phone_number=phone_number,
                joined_date=datetime.utcnow(),
            )

            db.session.add(new_user)
            db.session.flush()
            # user_id = get_jwt_identity()

            # if logged := User.query.filter_by(id=id).first() is not None:
            #     # faliure(log_initiation)
            #     return err_resp("Email is already being used.", "email_taken", 403)

            # Load the new user's info
            user_info = user_schema.dump(new_user)

            # Commit changes to DB
            db.session.commit()

            # Create an access token
            access_token = create_access_token(identity=new_user.id)

            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["user"] = user_info
            # operator_log(log_initiation)       

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            # faliure(log_initiation)
            return internal_err_resp()

    @staticmethod
    def return_operators():
        log_initiation = operator_log_initiation()
        
        operators = User.query.all()
        operator_log(log_initiation)       
        return operators

    @staticmethod
    def retrieve_operator(id):
        log_initiation = operator_log_initiation()
        if not (operator := User.query.filter_by(id=id).first()):
                faliure(log_initiation)
                return err_resp(
                    "no operators found.",
                    "email_404",
                    404,
                )
        log_initiation['email']= operator.email

        operator_log(log_initiation)       
        return operator
