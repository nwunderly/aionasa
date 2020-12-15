import logging

from ..client import BaseClient
from ..errors import APIException
from ..rate_limit import insight_rate_limiter, demo_rate_limiter


logger = logging.getLogger('aionasa.insight')


class _InSightRateLimiterRepr:
    def __repr__(self):
        return '<insight_rate_limiter>'


_default = _InSightRateLimiterRepr()


class InSight(BaseClient):
    """Client for NASA Insight Mars weather data.

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: Optional[:class:`aiohttp.ClientSession`]
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: Optional[:class:`RateLimiter`]
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.

    """

    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=_default, **kwargs):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        elif rate_limiter is _default:
            rate_limiter = insight_rate_limiter
        super().__init__(api_key, session, rate_limiter, **kwargs)

    async def get(self, feedtype='json'):
        """Retrieves Mars weather data from the last seven available days.

        Parameters
        ----------
        feedtype: :class:`str`
            The format of what is returned. Currently the default is JSON and only JSON works.
        
        Returns
        -------
        :class:`dict`
            A dict containing JSON data returned by the API.
        """

        request = f"https://api.nasa.gov/insight_weather/?ver=1.0&feedtype={feedtype}&api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not a success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        return json

