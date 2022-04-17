def load_data(role_db_obj):
    """ Load user's data

    Parameters:
    - User db object
    """
    from app.models.schemas import RoleSchema

    role_schema = RoleSchema()

    data = role_schema.dump(role_db_obj)

    return data
