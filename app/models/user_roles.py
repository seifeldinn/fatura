from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, Column, BOOLEAN, DateTime, DATETIME, UniqueConstraint

from sqlalchemy.orm import backref
from app import db, bcrypt

Column = db.Column
Model = db.Model
relationship = db.relationship

User_Roles = db.Table('user_roles',
    Column('time_stamp', DATETIME, default=datetime.date(datetime.utcnow())),
    Column('user_id', Integer, ForeignKey("user.id"), primary_key=True),
    Column('role_id', Integer, ForeignKey("roles.id"), primary_key=True)
    )
