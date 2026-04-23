ROLE_UPDATE_HANDLERS = {}

def register_update_role(role):
    def wrapper(cls):
        ROLE_UPDATE_HANDLERS[role] = cls
        return cls
    return wrapper