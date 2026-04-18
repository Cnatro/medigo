ROLE_HANDLES = {}

def register_role(role):
    def wrapper(cls):
        ROLE_HANDLES[role] = cls
        return cls

    return wrapper