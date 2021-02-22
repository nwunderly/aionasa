import logging

from ..client import BaseClient
from ..rate_limit import default_rate_limiter, demo_rate_limiter

logger = logging.getLogger('aionasa.donki')


class DONKI(BaseClient):
    """Client for NASA Space Weather Database of Notifications, Knowledge, Information (DONKI).

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """
    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        super().__init__(api_key, session, rate_limiter)

    async def coronal_mass_ejection(self, start_date, end_date):
        pass
