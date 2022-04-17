from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, Column, BOOLEAN
from sqlalchemy.orm import backref
from app import db, bcrypt

Column = db.Column
Model = db.Model
relationship = db.relationship

class User(Model):
    """ User model for storing user related data """

    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    name = Column(String(64))
    phone_number = Column(String(255))
    password_hash = Column(String(128))
    is_admin = Column(BOOLEAN())
    web_login = Column(BOOLEAN, default=False, index=True)
    joined_date = Column(db.DateTime, default=datetime.utcnow)
    timestamp = Column(db.DateTime, default=datetime.date(datetime.utcnow()))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_json(self):

        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name,
             "roles": [ {"id": a.id, "name": a.name} for a in self.roles] if self.roles else None
        }
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

