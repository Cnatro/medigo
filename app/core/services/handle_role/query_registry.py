ROLE_QUERY_HANDLERS = {}

def register_query_role(role):
    def wrapper(cls):
        ROLE_QUERY_HANDLERS[role] = cls
        return cls
    return wrapper