import logging

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter

logger = logging.getLogger('aionasa.donki')


# Documentation: https://ccmc.gsfc.nasa.gov/support/DONKI-webservices.php


class DONKI(BaseClient):
    """Client for NASA Space Weather Database of Notifications, Knowledge, Information (DONKI).

    ..note::
        The api.nasa.gov mirror is rate limited (like other api.nasa.gov APIs).
        The API at kauai.ccmc.gsfc.nasa.gov, however, is not, nor does it require an API key to use.
        These features will be ignored when using this API through kauai.ccmc.gsfc.nasa.gov.

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """
    def __init__(self, use_nasa_mirror=False, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if use_nasa_mirror:
            if api_key == 'DEMO_KEY' and rate_limiter:
                rate_limiter = demo_rate_limiter
            self.base_url = 'https://api.nasa.gov/DONKI'
        else:
            api_key = None
            rate_limiter = None
            self.base_url = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get'
        super().__init__(api_key, session, rate_limiter)

    async def _get_json(self, relative_url):
        url = self.base_url + relative_url

        if self._api_key:
            if '?' in url:
                url += ('&api_key=' + self._api_key)
            else:
                url += ('?api_key=' + self._api_key)

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise APIException(resp.status, resp.reason)
            data = await resp.json()

        if self.rate_limiter:
            remaining = int(resp.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        return data

    async def coronal_mass_ejection(self, start_date=None, end_date=None):
        """Get information on coronal mass ejections for a particular date.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[...]`
        """

        url = '/CME'

        def get_sep():
            return '&' if '?' in url else '?'

        if start_date:
            url += get_sep()
            url += 'startDate=' + start_date.strftime('%Y-%m-%d')
        if end_date:
            url += get_sep()
            url += 'endDate=' + end_date.strftime('%Y-%m-%d')

        json = await self._get_json(url)

        return json




