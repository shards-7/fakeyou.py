#class InvalidCredentials(Exception):
#    def __init__(*args, **kwargs):
#        Exception.__init__(*args, **kwargs)

class TooManyRequests(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("Too many requests, try again later.")

class PathNullError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("FakeYou.com returned a null path")


class RequestError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)
class Failed(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("check token and text/file, or try again")

class InvalidCredentials(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("check username or password")

class UserNotFound(Exception):
    def __init__(self,username):
        Exception.__init__(f"The user {username} not found")


class UsernameTooShort(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("Username too short")

class UsernameTaken(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("Username taken")
class EmailTaken(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("Email taken")
class W2lTemplateTokenWrong(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("Wrong w2l template token")

class PasswordTooShort(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("Password too short")

class UnAuthorized(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class TtsResultNotFound(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class EmailInvalid(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__("invalid email format")
