from aiohttp import ClientSession, TCPConnector, ClientTimeout, ClientResponse


class HTTPClient:
    _session: ClientSession = None

    @classmethod
    def __init__(cls):
        conn = TCPConnector(limit=100)
        timeout = ClientTimeout(total=10)
        cls._session = ClientSession(connector=conn, timeout=timeout)

    @classmethod
    async def get_session(cls) -> ClientSession:
        return cls._session if cls._session else None

    @classmethod
    async def destroy(cls) -> None:
        if cls._session:
            await cls._session.close()

        cls._session = None

    @classmethod
    async def get(cls, url: str, headers: dict = None, **kwargs) -> ClientResponse:
        async with cls._session.get(
                url=url,
                headers=headers,
                param=kwargs,
                raise_for_status=True,
        ) as response:
            return response

    @classmethod
    async def post(cls, url: str, headers: dict = None, **kwargs) -> ClientResponse:
        async with cls._session.post(
                url=url,
                headers=headers,
                param=kwargs,
                raise_for_status=True,
        ) as response:
            return response

    @classmethod
    async def patch(cls, url:str, headers: dict = None, **kwargs) -> ClientResponse:
        async with cls._session.patch(
            url=url,
            headers=headers,
            param=kwargs,
            raise_for_status=True,
        ) as response:
            return response
