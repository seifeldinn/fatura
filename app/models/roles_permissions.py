from sqlalchemy import Integer, ForeignKey, Column, DATETIME
from datetime import datetime
from app import db

Column = db.Column
Model = db.Model
relationship = db.relationship


RolesPermissions = db.Table('roles_permissions',
    Column('time_stamp', DATETIME, default=datetime.date(datetime.utcnow())),
    Column('role_id', Integer, ForeignKey("roles.id"), primary_key=True),
    Column('pemission_id', Integer, ForeignKey("permissions.id"), primary_key=True)
    )
