class UserError(Exception):
    def __init__(self,message):
        self.message = message

class InvalidEmailError(UserError):
    pass

class UserAccountAlreadyExists(UserError):
    pass

class UserDoesNotExistError(UserError):
    pass

class IncorrectAuthCodeCode(UserError):
    pass

class PoorPasswordError(UserError):
    pass

class IncorrectPasswordError(UserError):
    pass