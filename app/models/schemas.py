# Model Schemas
from multiprocessing.connection import Client
from pip import List
from app import ma

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name", "is_admin")

class RoleSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name")

class TypeSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name")


class CardSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "card_id", "type")
    type = ma.Nested(TypeSchema)

class PermissionsSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name", "path", "edit", "view", "add", 'delete')

class PojectSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name", "description")

class VillageSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name", "description")


class ImageSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "path", "image_type")

class ClientSchema(ma.Schema):
    class Meta:
        
        # Fields to expose, add more if needed.
        fields =("id", 
                "name",
                "birth_date",
                "gender",
                "phone_number",
                "relation",
                "email",
                "cancelled",
                "activated",
                "valid_from",
                "valid_to",
                "national_id",
                "cards",
                "images"
                )
    cards = ma.List(ma.Nested(CardSchema))

    images = ma.List(ma.Nested(ImageSchema))

class UnitSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id", "name", "ext_id")
    clients = ma.List(ma.Nested(ClientSchema))
    # type = ma.Nested(TypeSchema)

class DeveloperSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id","name")

class CardSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("id","card_id", "license_plate")
 