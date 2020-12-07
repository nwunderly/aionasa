
import datetime
import logging
from typing import List

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter
from .data import EarthImage


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
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: Optional[:class:`aiohttp.ClientSession`]
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: Optional[:class:`RateLimiter`]
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """

    def __init__(self, use_nasa_mirror=False, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if use_nasa_mirror:
            if api_key == 'DEMO_KEY' and rate_limiter:
                rate_limiter = demo_rate_limiter
            self.base_url = 'https://api.nasa.gov/EPIC'
        else:
            api_key = None
            rate_limiter = None
            self.base_url = 'https://epic.gsfc.nasa.gov'
        super().__init__(api_key, session, rate_limiter)

    async def _get_metadata(self, collection, date):
        """Retrieves metadata for imagery for a given collection and date.

        Parameters
        ----------
        collection: :class:`str`
            The collection to search. Should be 'natural' or 'enhanced'.
        date: :class:`datetime.date`
            The date to retrieve data for.

        Returns
        -------
        :class:`List[EarthImage]`
            Data returned by the API.
        """
        if collection not in ('natural', 'enhanced'):
            raise ArgumentError(f"collection expected be 'natural' or 'enhanced' got {collection}")

        if date is None:
            date = ''
        else:
            date = date.strftime('/date/%Y-%m-%d')

        api_key = f'?api_key={self._api_key}' if self._api_key else ''
        request = f'{self.base_url}/api/{collection}{date}{api_key}'

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            data = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        images = []

        for item in data:
            image = EarthImage(client=self, json=item, collection=collection)
            images.append(image)

        return images

    async def _get_listing(self, collection):
        """Retrieves a listing of dates with available images in the requested collection.

        Parameters
        ----------
        collection: :class:`str`
            The collection to get a listing for. Should be 'natural' or 'enhanced'.

        Returns
        -------
        :class:`List[datetime.date`
            List of dates with available imagery.
        """
        if collection not in ('natural', 'enhanced'):
            raise ArgumentError(f"collection expected be 'natural' or 'enhanced' got {collection}")

        api_key = f'?api_key={self._api_key}' if self._api_key else ''
        request = f'{self.base_url}/api/{collection}/available{api_key}'

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

    async def natural_images(self, date: datetime.date = None):
        """Retrieves metadata for natural color imagery for a given date.
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
        return await self._get_metadata('natural', date)

    async def natural_listing(self):
        """Retrieve a listing of all dates with available natural color imagery.

        Returns
        -------
        List[:class:`datetime.date`]
            The dates returned by the API.
        """
        return await self._get_listing('natural')

    async def enhanced_images(self, date: datetime.date = None):
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
        return await self._get_metadata('enhanced', date)

    async def enhanced_listing(self):
        """Retrieve a listing of all dates with available enhanced color imagery.

        Returns
        -------
        List[:class:`datetime.date`]
            The dates returned by the API.
        """
        return await self._get_listing('enhanced')


