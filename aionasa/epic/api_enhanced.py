
import datetime
import logging
from typing import List
from aiohttp import ClientSession

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter, RateLimiter
from .data_enhanced import EarthImage


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
    use_nasa_mirror: :class:`bool`
        Whether to use the api.nasa.gov mirror instead of epic.gsfc.nasa.gov
    API_KEY: :class:`str`
        NASA API key to be used by the client.
    session: Optional[:class:`aiohttp.ClientSession`]
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: Optional[:class:`RateLimiter`]
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """

    def __init__(self, use_nasa_mirror=False, API_KEY='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if use_nasa_mirror:
            if API_KEY == 'DEMO_KEY' and rate_limiter:
                rate_limiter = demo_rate_limiter
            self.base_url = 'https://api.nasa.gov/EPIC'
        else:
            API_KEY = None
            rate_limiter = None
            self.base_url = 'https://epic.gsfc.nasa.gov'
        super().__init__(API_KEY, session, rate_limiter)

    async def enhanced(self, date: datetime.date = None):
        """Retrieves metadata for enhanced color imagery for a given date.
        Defaults to most recent date.

        Parameters
        ----------
        date: :class:`datetime.date`
            The date to request data for.

        Returns
        -------
        List[:class:`EarthImage`]
            Data returned by the API.
        """

        if date is None:
            date = ''
        else:
            date = date.strftime('/date/%Y-%m-%d')

        API_KEY = f'?API_KEY={self._API_KEY}' if self._API_KEY else ''
        request = f'{self.base_url}/api/enhanced{date}{API_KEY}'

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            data = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        images = []

        for item in data:
            image = EarthImage(client=self, json=item, collection='enhanced')
            images.append(image)

        return images

    async def enhanced_all(self):
        """Retrieve a listing of all dates with available enhanced color imagery.

        Returns
        -------
        List[:class:`datetime.date`]
            The dates returned by the API.
        """
        API_KEY = f'?API_KEY={self._API_KEY}' if self._API_KEY else ''
        request = f'{self.base_url}/api/enhanced/all{API_KEY}'

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            data = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        dates = []

        for item in data:
            date = datetime.datetime.strptime(item['date'], '%Y-%m-%d').date()
            dates.append(date)

        return dates

    async def enhanced_available(self):
        """Retrieve a listing of all dates with available enhanced color imagery.

        Returns
        -------
        List[:class:`datetime.date`]
            The dates returned by the API.
        """
        API_KEY = f'?API_KEY={self._API_KEY}' if self._API_KEY else ''
        request = f'{self.base_url}/api/enhanced/available{API_KEY}'

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            data = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        dates = []

        for item in data:
            date = datetime.datetime.strptime(item, '%Y-%m-%d').date()
            dates.append(date)

        return dates



