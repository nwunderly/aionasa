
import datetime
import logging
from typing import List
from aiohttp import ClientSession

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter, RateLimiter
from .data_natural import EarthImage


logger = logging.getLogger('aionasa.epic')


# ===============================
# API MIRRORS:
#   https://epic.gsfc.nasa.gov/api/
#   https://api.nasa.gov/EPIC/api/
# ===============================


# TODO:
#   - plan methods for this class
#   - data class for EPIC images


class EPIC(BaseClient):
    """Client for NASA Earth Polychromatic Imaging Camera.

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: Optional[:class:`aiohttp.ClientSession`]
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: Optional[:class:`RateLimiter`]
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """

    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        super().__init__(api_key, session, rate_limiter)

    async def natural(self, date: datetime.date = None):
        """Retrieves metadata for natural color imagery for a given date.
        Defaults to most recent date.

        Parameters
        ----------
        date: :class:`datetime.date`
            The date to request data for.

        Returns
        -------
        List[:class:`dict`]
            JSON data returned by the API.
        """

        if date is None:
            date = ''
        else:
            date = date.strftime('/date/%Y-%m-%d')

        request = f'https://api.nasa.gov/EPIC/api/natural{date}?api_key={self._api_key}'

        async with self._session.get(request) as response:
            data = await response.json()

        return data





