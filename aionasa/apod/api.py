
import datetime
import logging
from typing import List

from aiohttp import ClientSession

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter
from .data import AstronomyPicture


logger = logging.getLogger('aionasa.apod')


class APOD(BaseClient):
    """Client for NASA Astronomy Picture of the Day API.

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

    async def get(self, date: datetime.date = None, hd: bool = False, as_json: bool = False):
        """Retrieves a single item from NASA's APOD API.

        Parameters
        ----------
        date: :class:`datetime.Date`
            The date of the APOD image to retrieve. Defaults to ``'today'``.
        hd: :class:`bool`
            Bool indicating whether to retrieve the URL for the high resolution image. Defaults to ``False``.
        as_json: :class:`bool`
            Bool indicating whether to return the raw returned json data instead of the normal AstronomyPicture object. Defaults to ``False``.

        Returns
        -------
        :class:`AstronomyPicture`
            An AstronomyPicture containing data returned by the API.
        """

        if date is None:  # parameter will be left out of the query.
            date = ''
        else:
            date = 'date=' + date.strftime('%Y-%m-%d') + '&'
        if hd is None:  # parameter will be left out of the query.
            hd = ''
        else:
            hd = 'hd=' + str(hd) + '&'

        request = f"https://api.nasa.gov/planetary/apod?{date}{hd}api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:
            date = json.get('date')
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None

            entry = AstronomyPicture(
                client=self,
                date=date,
                copyright=json.get('copyright'),
                title=json.get('title'),
                explanation=json.get('explanation'),
                url=json.get('url'),
                hdurl=json.get('hdurl'),
                media_type=json.get('media_type'),
                service_version=json.get('service_version'),
            )
            return entry

    async def batch_get(self, start_date: datetime.date, end_date: datetime.date,
                        hd: bool = None, as_json: bool = False):
        """Retrieves multiple items from NASA's APOD API. Returns a list of APOD entries.

        Parameters
        ----------
        start_date: :class:`datetime.Date`
            The first date to return when requesting a range of dates.
        end_date: :class:`datetime.Date`
            The last date to return when requesting a range of dates. Range is inclusive.
        hd: :class:`bool`
            Bool indicating whether to retrieve the URL for the high resolution image. Defaults to ``False``.
        as_json: :class:`bool`
            Bool indicating whether to return a list of dicts containing the raw returned json data instead of the normal ``List[AstronomyPicture]``. Defaults to ``False``.

        Returns
        -------
        List[:class:`AstronomyPicture`]
            A list of AstronomyPicture objects containing data returned by the API.
        """

        start_date = 'start_date=' + start_date.strftime('%Y-%m-%d') + '&'
        end_date = 'end_date=' + end_date.strftime('%Y-%m-%d') + '&'

        if hd is None:  # parameter will be left out of the query.
            hd = ''
        else:
            hd = 'hd=' + str(hd) + '&'

        request = f"https://api.nasa.gov/planetary/apod?{start_date}{end_date}{hd}api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:
            result = []

            for item in json:

                date = item.get('date')
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None

                entry = AstronomyPicture(
                    client=self,
                    date=date,
                    copyright=item.get('copyright'),
                    title=item.get('title'),
                    explanation=item.get('explanation'),
                    url=item.get('url'),
                    hdurl=item.get('hdurl'),
                    media_type=item.get('media_type'),
                    service_version=item.get('service_version')
                )
                result.append(entry)

            return result



