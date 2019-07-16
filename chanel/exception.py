from sanic.exceptions import add_status_code, SanicException


@add_status_code(400)
class BadRequest(SanicException):
    ...


@add_status_code(401)
class Unauthorized(SanicException):
    ...


@add_status_code(403)
class Forbidden(SanicException):
    ...


@add_status_code(404)
class NotFound(SanicException):
    ...


@add_status_code(409)
class Conflict(SanicException):
    ...


@add_status_code(500)
class InternalServerError(SanicException):
    ...