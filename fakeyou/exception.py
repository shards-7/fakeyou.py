# class InvalidCredentials(Exception):
#    def __init__(*args, **kwargs):
#        Exception.__init__(*args, **kwargs)

class TooManyRequests(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "Too many requests, try again later.")


class PathNullError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "FakeYou.com returned a null path", **kwargs)

class Dead(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "TTS job is dead, Server discarded it", **kwargs)


class RequestError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class Failed(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "check token and text/file, or try again")


class InvalidCredentials(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "check username or password")


class UserNotFound(Exception):
    def __init__(self, username):
        Exception.__init__(*args, f"The user {username} not found")


class UsernameTooShort(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "Username too short")


class UsernameTaken(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "Username taken")


class EmailTaken(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "Email taken")


class W2lTemplateTokenWrong(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "Wrong w2l template token")


class PasswordTooShort(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "Password too short")


class UnAuthorized(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class TtsResultNotFound(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class EmailInvalid(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, "invalid email format")
