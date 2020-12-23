import datetime
import logging

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter


logger = logging.getLogger('aionasa.neows')


class NeoWs(BaseClient):
    """Client for NASA Near Earth Object Weather Service

    """

    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        super().__init__(api_key, session, rate_limiter)

    async def feed(self, start_date: datetime.date, end_date: datetime.date = None):
        """Retrieve a list of Asteroids based on their closest approach date to Earth.

        :param start_date: Starting date for asteroid search.
        :param end_date: Ending date for asteroid search.
        :return: A list of Asteroids returned by the API.
        """

        start_date = 'start_date=' + start_date.strftime('%Y-%m-%d') + '&'

        if end_date is None:  # parameter will be left out of the query.
            end_date = ''
        else:
            end_date = 'end_date=' + end_date.strftime('%Y-%m-%d') + '&'

        request = f"https://api.nasa.gov/neo/rest/v1/feed?{start_date}{end_date}api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)



