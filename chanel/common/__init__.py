from functools import wraps
from typing import List

from chanel.common.exception import BadRequest


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


def query_parameter_verify(query_strings: List[str]):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not request.args:
                raise BadRequest("please check query strings")

            print(request.query_args)

            for query_string in query_strings:
                for query_args in request.query_args:
                    if query_string not in query_args:
                        raise BadRequest("invalid query string syntax detected")

            response = await f(request, *args, **kwargs)

            return response

        return decorated_function

    return decorator
