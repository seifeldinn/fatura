def load_data(permission_db_obj):
    """ Load user's data

    Parameters:
    - User db object
    """
    from app.models.schemas import PermissionsSchema

    permission_schema = PermissionsSchema()

    data = permission_schema.dump(permission_db_obj)

    return data
