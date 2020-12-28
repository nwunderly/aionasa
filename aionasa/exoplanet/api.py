import aiohttp
import asyncio
import datetime

try:
    import pandas
except ImportError:
    pandas = None

from ..client import BaseClient
from ..rate_limit import default_rate_limiter, demo_rate_limiter


####################################################################################################################################
# Note: in-depth documentation for this API can be found at https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html #
####################################################################################################################################


BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"


class Exoplanet(BaseClient):
    """Client for NASA Exoplanet Archive API.
    """
    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        super().__init__(api_key, session, rate_limiter)

    async def _get(self, table, **query):
        """Query the database.

        Parameters
        ----------
        table:
            The table to query. This is required.
        query:
            Other query parameters to be included in the request.

        Returns
        -------
        A dict containing the JSON data returned by the API.
        """
        query = "&" + "&".join([f"{param}={value}" for param, value in query.items()]) if query else ""
        url = f"{BASE_URL}?table={table}{query}"

        async with self._session.get(url) as resp:
            json = await resp.json()

        return json
