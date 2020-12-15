import aiohttp


class BaseClient:
    """
    Base class for NASA API clients.
    """
    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=None, timeout=None):
        """
        Initializes the client class.

        :param api_key: api.nasa.gov key for expanded usage.
        :param session:
        """
        self._api_key = api_key
        timeout = timeout or aiohttp.ClientTimeout()
        self._session = session or aiohttp.ClientSession(timeout=timeout)
        self.rate_limiter = rate_limiter

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def close(self):
        if self._session:
            await self._session.close()
