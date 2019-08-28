from functools import wraps
from typing import List

from common.exception import BadRequest


def json_verify(scheme: dict):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not request.json:
                raise BadRequest("please check json parameters")

            for k, v in scheme.items():
                if k not in request.json or type(request.json[k]) is not v:
                    raise BadRequest("invalid json syntax detected")

            response = await f(request, *args, **kwargs)

            return response
        return decorated_function
    return decorator


def header_verify(headers: List[str]):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not request.headers:
                raise BadRequest("please check headers")

            for header in headers:
                if header not in request.headers:
                    raise BadRequest("missing header detected")

            response = await f(request, *args, **kwargs)

            return response
        return decorated_function
    return decorator
