from json import JSONDecodeError


class APIException(Exception):
    ...


class TooManyRequests(APIException):
    ...


class PathNullError(APIException):
    ...


class Dead(APIException):
    ...


class RequestError(APIException):
    ...


class Failed(APIException):
    ...


class InvalidCredentials(APIException):
    ...


class UserNotFound(APIException):
    ...


class UsernameTooShort(APIException):
    ...


class UsernameTaken(APIException):
    ...


class EmailTaken(APIException):
    ...


class W2lTemplateTokenWrong(APIException):
    ...


class PasswordTooShort(APIException):
    ...


class UnAuthorized(APIException):
    ...


class TtsResultNotFound(APIException):
    ...


class EmailInvalid(APIException):
    ...


class ServerError(APIException):
    ...


class NotFount(APIException):
    ...


class UnknownError(APIException):
    ...


ERROR_TYPES = {
    401: UnAuthorized,
    429: TooManyRequests,

    "InvalidCredentials": InvalidCredentials,
    "UsernameReserved": UsernameTaken,
    "UsernameTaken": UsernameTaken,
    "EmailTaken": EmailTaken,
    "server error": ServerError,
    "not found": NotFount
}


def handle_exception(response):
    request_error_code = ERROR_TYPES.get(response.status_code)

    try:
        body = response.json()
    except JSONDecodeError:
        body = {"error": response.text}

    if request_error_code:
        raise request_error_code(body)

    if not body.get("success"):
        error_type = body.get("error_type", body.get("error_reason"))

        raise ERROR_TYPES.get(
            error_type, UnknownError
        )(
            body.get("error_message", body.get("error", error_type))
        )


def handle_response(response):
    return response if response.status_code < 300 else handle_exception(response)
