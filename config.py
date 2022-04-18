import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Change the secret key in production run.
    SECRET_KEY = os.environ.get("SECRET_KEY", "AEDF0099534528EA")
    DEBUG = False

    # JWT Extended config
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "AEDF76359724EA")
    ## Set the token to expire every week
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)


class DevelopmentConfig(Config):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_monitoringdashboard.db'
    # MONGO_URI = ""  
  
    API_KEY = 'c8f06001-bf5a-46b3-afd75f-f5677769fc6c'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add logger


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # In-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:////flask_monitoringdashboard.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = 'c8f06001-bf5a-46b3-afd75f-f5677769fc6c'


class ProductionConfig(Config):
    DEBUG = False
    # MONGO_URI = ""
    # MONGO_URI = "mongodb://root:admin@mongo/accessLog?authSource=admin"  
    SQLALCHEMY_DATABASE_URI = 'sqlite:////flask_monitoringdashboard.db'
    # MONGO_URI = ""    

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@db/new_giza_club'
    # MONGO_URI = ""    
    API_KEY = 'c8f06001-bf5a-46b3-afd75f-f5677769fc6c'


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)


def get_api_key():
    config_name = os.getenv('BOILERPLATE_ENV') or 'development'
    configs = config_by_name[config_name]
    return configs.API_KEY
