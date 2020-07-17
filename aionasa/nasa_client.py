
from .apod import APOD


class NASA:
    """
    Client that wraps all NASA APIs into a single class.
    """
    def __init__(self, api_key='DEMO_KEY', session=None):
        self._api_key = api_key
        self._apod = APOD(api_key, session)

        raise NotImplementedError("This class is not yet ready for use.")

    async def apod(self, *args, **kwargs):
        return await self._apod.get(*args, **kwargs)

