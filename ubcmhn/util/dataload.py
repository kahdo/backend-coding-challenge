# Return a Module as a List of Objects to be analyzed dynamically
def module2list(_m):
    return [getattr(_m, _name) for _name in dir(_m)]
