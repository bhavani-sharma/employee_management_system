class EmployeeNotFoundError(Exception):
    pass

class EmployeeAlreadyExistsError(Exception):
    pass

class EmployeeNotEligibleError(Exception):
    pass

class EmployeeAlreadyHasUserError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class CannotDeleteOwnProfileError(Exception):
    pass