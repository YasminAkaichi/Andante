class SubstitutionError(Exception):
    def __init__(self, key, item):
        message = 'Substitution {%s/%s} is not valid' % (str(key), str(item))
        super().__init__(message)
