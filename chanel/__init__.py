from sanic import Sanic

from chanel.config import SERVICE_NAME, LOGO


def create_app() -> Sanic:
    _app = Sanic(SERVICE_NAME)
    _app.config.LOGO = LOGO

    return _app
