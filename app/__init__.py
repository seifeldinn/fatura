""" Top level module

This module:

- Contains create_app()
- Registers extensions
"""

from flask import Flask

# Import extensions
from .extensions import bcrypt, cors, db, jwt, ma, rbac, socketio
import flask_monitoringdashboard as dashboard

from flask_socketio import SocketIO
from .api import api_bp


# Import config
from config import config_by_name



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    dashboard.bind(app)

    register_extensions(app)

    # socketio.init_app(app, cors_allowed_origins="*")
    # socketio.on_event('init', handle_init)

    # Register blueprints

    app.register_blueprint(api_bp, url_prefix="/")

    return app


def register_extensions(app):
    # Registers flask extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    rbac.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")


    # mongo.init_app(app)
