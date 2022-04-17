from datetime import datetime
from app import db, bcrypt
from sqlalchemy.orm import relationship, backref

from sqlalchemy import Integer, String, Column
from .roles_permissions import RolesPermissions
from .user_roles import User_Roles

Column = db.Column
Model = db.Model
relationship = db.relationship


class Role(Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    rolePermissions = relationship("Permissions", secondary = RolesPermissions, backref=backref("roles"), lazy="dynamic")
    users = relationship("User", secondary = User_Roles, backref=backref("roles"), lazy="dynamic")
    timestamp = Column(db.DateTime, default=datetime.date(datetime.utcnow()))

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        

    def __repr__(self):
        return f"<{self.name} - {self.id}>"

    def to_json(self):

        return {
            "id": self.id,
            "name": self.name,
            "Permissions": [ {"id": a.id, "name": a.name} for a in self.rolePermissions] if self.rolePermissions else None
        }




























# class Permission:
#     FOLLOW = 1
#     COMMENT = 2
#     WRITE = 4
#     MODERATE = 8
#     ADMIN = 16


# class Role(Model):
#     __tablename__ = "roles"
#     id = Column(db.Integer, primary_key=True)
#     name = Column(db.String(64), unique=True)
#     # default = Column(db.Boolean, default=False, index=True)
#     permissions = Column(db.Integer)
#     description = Column(db.String(50))
#     # users = db.relationship("User", backref=db.backref("role"), lazy="dynamic")

#     def __init__(self, **kwargs):
#         super(Role, self).__init__(**kwargs)
#         if self.permissions is None:
#             self.permissions = 0

#     def __repr__(self):
#         return f"<{self.name} - {self.id}>"

#     @staticmethod
#     def insert_roles():
#         roles = {
#             "User": [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
#             "Moderator": [
#                 Permission.FOLLOW,
#                 Permission.COMMENT,
#                 Permission.WRITE,
#                 Permission.MODERATE,
#             ],
#             "Admin": [
#                 Permission.FOLLOW,
#                 Permission.COMMENT,
#                 Permission.WRITE,
#                 Permission.MODERATE,
#                 Permission.ADMIN,
#             ],
#         }

#         default_role = "User"
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)

#     def has_permission(self, perm):
#         return self.permissions & perm == perm

#     def add_permission(self, perm):
#         if not self.has_permission(perm):
#             self.permissions += perm

#     def remove_permission(self, perm):
#         if self.has_permission(perm):
#             self.permissions -= perm

#     def reset_permission(self):
#         self.permissions = 0


#     # users = db.relationship("User", backref=db.backref("role"), lazy="dynamic")
