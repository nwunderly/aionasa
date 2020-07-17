
import aiohttp
import asyncio
import datetime

from collections import namedtuple

from ..base_client import BaseClient



class InSight(BaseClient):
    """
    Client for NASA Insight Mars weather data.

    In-depth documentation for this API can be found at https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf

    Parameters for InSight API:
        - version: The version of this API
        - feedtype: The format of what is returned. Currently the default is JSON and only JSON works.
        -
    """

    async def get(self, feedtype='json'):


        request = f"https://api.nasa.gov/insight_weather/?ver=1.0&feedtype={feedtype}&api_key={self._api_key}"

        async with self._session.get(request) as response:
            json = await response.json()

        return json



