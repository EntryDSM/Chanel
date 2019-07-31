import pytest

from chanel.app import create_app


@pytest.yield_fixture(scope="function")
async def chanel_app(redis_proc, redis_db):
    _app = create_app()
    _app.redis_connection_info = {
            "address": f"redis://:{redis_proc.password}"
            f"@{redis_proc.host}:{redis_proc.port}",
            "minsize": 5,
            "maxsize": 10,
        }
    yield _app
