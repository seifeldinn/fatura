import operator
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from app.utils import api_key_required, validation_error, err_resp, role_validation


# Auth modules
from .service import AuthService
from .dto import AuthDto
from .utils import LoginSchema, RegisterSchema

api = AuthDto.api
auth_success = AuthDto.auth_success
operator_obj = AuthDto.user_obj

login_schema = LoginSchema()
register_schema = RegisterSchema()


@api.route("/login")
class AuthLogin(Resource):
    """ User login endpoint
    User registers then receives the user's information and access_token
    """

    auth_login = AuthDto.auth_login

    @api.doc(
        "Auth login",
        responses={
            200: ("Logged in", auth_success),
            400: "Validations failed.",
            403: "Incorrect password or incomplete credentials.",
            404: "Email does not match any account.",
        },
    )
    @api.expect(auth_login, validate=True)
    def post(self):
        """ Login using email and password """
        # Grab the json data
        login_data = request.get_json()

        # Validate data
        if (errors := login_schema.validate(login_data)) :
            return validation_error(False, errors), 400
        return AuthService.login(login_data)

@api.route("/register")
class AuthRegister(Resource):
    """ User register endpoint
    User registers then receives the user's information and access_token
    """
    auth_register = AuthDto.auth_register

    @api.doc(
        "Auth registration",
        responses={
            201: ("Successfully registered user.", auth_success),
            400: "Malformed data or validations failed.",
        },
    )
    @api.expect(auth_register, validate=True)
    # @jwt_required()
    # @role_validation()
    def post(self):
        """ User registration """
        # Grab the json data
        register_data = request.get_json()

        # Validate data
        if (errors := register_schema.validate(register_data)) :
            return validation_error(False, errors), 400

        return AuthService.register(register_data)

@api.route("/operators")
class AuthRegister(Resource):
    @api.doc(
        "Auth registration",
        responses={
            201: ("Successfully registered user.", auth_success),
            400: "Malformed data or validations failed.",
        },
    )
    @jwt_required()
    # @role_validation()
    def get(self):
        operators = AuthService.return_operators()
        if not operators:
            return err_resp("No Operators Found!", "auth_204", 204)

        return api.marshal(operators, operator_obj), 200

@api.route("/edit")
class AuthRegister(Resource):
    @api.doc(
            "Retrieve Unit Relation",
            responses={
                200: ("Data successfully created"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    @role_validation()

    def post(self):
        data = request.json
        return AuthService.edit_user(data)

@api.route("/")
class AuthRegister(Resource):
    @api.doc(
            "Retrieve User data",
            responses={
                200: ("Data successfully retrieved"),
                204: "Data not found!",
                403: "Access Denied!"
            },
        )
    @jwt_required()
    # @role_validation()

    def get(self):
        user_id = request.args.get('user_id')
        operator = AuthService.retrieve_operator(user_id)
        if not operator:
            return err_resp("Data not found!", "User_204", 204)

        return api.marshal(operator, operator_obj), 200
