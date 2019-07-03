from typing import List

def get_error_response(exception):
    error = {
        "status": "error",
        "error": {
            "error": exception.type,
            "errorDescription": exception.description
        }
    }
    return error

class InternalServerError(Exception):
    def __init__(self):
        self.type = 'internalServerError'
        self.description = 'Internal error occurred, please try again. If error persists contact support.'

class InvalidSyntaxError(Exception):
    def __init__(self, error):
        self.type = 'syntaxError'
        self.description = f'Invalid syntax in request. {error}'

class ValidationError(Exception):
    def __init__(self, errors: List):
        self.type = 'validationError'
        self.description = 'Validation error(s) have occurred'
        self.errors = []
        for error in errors:
            error_dict = dict()
            error_dict["errorDescription"] = error
            self.errors.append(error_dict)

class generalException(Exception):
    def __init__(self, typeerror, message):
        self.type = typeerror
        self.description = message


class notAuthorised(Exception):
    def __init__(self, scope: str):
        self.type = 'notAuthorised'
        self.description = f'Error in Authentication!!!'
