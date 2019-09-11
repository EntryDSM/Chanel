import ujson

from aiohttp import ClientSession, TCPConnector, ClientTimeout


class HTTPClient:
    _session: ClientSession = None

    @classmethod
    async def init(cls):
        await cls.get_session()

    @classmethod
    async def get_session(cls) -> ClientSession:
        if not cls._session:
            conn = TCPConnector(limit=100)
            timeout = ClientTimeout(total=10)
            cls._session = ClientSession(connector=conn, timeout=timeout)

        return cls._session

    @classmethod
    async def destroy(cls) -> None:
        if cls._session:
            await cls._session.close()

        cls._session = None

    @classmethod
    async def get(cls, url: str) -> dict:
        session = await cls.get_session()

        async with session.get(
                url, raise_for_status=True
        ) as response:
            data = await response.read()
            return dict(data=ujson.loads(data), status=response.status)

    @classmethod
    async def post(cls, url: str, json) -> dict:
        session = await cls.get_session()

        async with session.post(
                url, json=json, raise_for_status=True
        ) as response:
            data = await response.read()
            return dict(data=ujson.loads(data), status=response.status)

    @classmethod
    async def patch(cls, url: str) -> dict:
        session = await cls.get_session()

        async with session.patch(
                url, raise_for_status=True
        ) as response:
            data = await response.read()
            return dict(data=ujson.loads(data), status=response.status)
