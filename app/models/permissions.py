from datetime import datetime
from app import db, bcrypt
from sqlalchemy import Integer, ForeignKey, String, Column, BOOLEAN, DateTime, DATETIME


# Alias common DB names
Column = db.Column
Model = db.Model
from sqlalchemy.orm import relationship


class Permissions(Model):
    """ Permissions model for adding new permissions """

    id = Column(Integer, primary_key=True)
    edit = Column(BOOLEAN, default=False, index=True)
    view = Column(BOOLEAN, default=False, index=True)
    add = Column(BOOLEAN, default=False, index=True)
    delete = Column(BOOLEAN, default=False, index=True)
    name = Column(String(255))
    path = Column(String(255))

    def __init__(self, **kwargs):
        super(Permissions, self).__init__(**kwargs)

