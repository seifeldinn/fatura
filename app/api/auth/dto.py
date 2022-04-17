from flask_restx import Namespace, fields

class AuthDto:
    api = Namespace("auth", description="Authenticate and receive tokens.")

    user_obj = api.model(
        "User object",
        {
            "email": fields.String,
            "name": fields.String,
            "phone_number": fields.String,
            "username": fields.String,
            "joined_date": fields.DateTime,
        },
    )

    auth_login = api.model(
        "Login data",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )

    auth_register = api.model(
        "Registration data",
        {
            "email": fields.String(required=True),
            "username": fields.String(required=True),
            "name": fields.String,
            "phone_number": fields.String,
            "password": fields.String(required=True),
        },
    )

    user_obj = api.model(
        "Registration data",
        {
            "id": fields.Integer,
            "name": fields.String,
            "username": fields.String,
            "email": fields.String,
            "phone_number": fields.String,
            "joined_date": fields.DateTime
        },
    )

    user_invoices = api.model(
        "Registration data",
        {
            "id": fields.Integer,
            "name": fields.String,
            "username": fields.String,
            "email": fields.String,
            "phone_number": fields.String,
            "joined_date": fields.DateTime
        },
    )

    auth_success = api.model(
        "Auth success response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "access_token": fields.String,
            "user": fields.Nested(user_obj),
        },
    )
