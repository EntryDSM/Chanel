import json, pytest

from chanel.app import create_app


@pytest.yield_fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def test_signup(test_cli):
    data = {"email": "by09115@outlook.kr", "password": "p@ssword"}
    response = await test_cli.post('/api/v1/signup/signup', data=json.dumps(data))
    assert response.status == 202
