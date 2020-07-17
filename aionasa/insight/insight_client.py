
import aiohttp
import asyncio
import datetime

from collections import namedtuple

from ..base_client import BaseClient


MarsWeatherData = namedtuple('MarsWeatherData', ['sols', 'sol_keys', 'validity_checks'])



class InSight(BaseClient):
    """
    Client for NASA Insight Mars weather data.

    In-depth documentation for this API can be found at https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf

    Parameters for InSight API:
        - version: The version of this API. Locked to 1.0 currently.
        - feedtype: The format of what is returned. Currently the default is JSON and only JSON works.
    """

    async def get(self, feedtype='json', as_json=False):
        """
        Retrieves Mars weather data from the last seven available days.

        :param feedtype: The format of what is returned. Currently the default is JSON and only JSON works.
        :param as_json: Bool indicating whether to return a dict containing the raw returned json data instead of the normal named tuple.
        :return: A named tuple containing data returned by the API.
        """

        request = f"https://api.nasa.gov/insight_weather/?ver=1.0&feedtype={feedtype}&api_key={self._api_key}"

        async with self._session.get(request) as response:
            json = await response.json()

        if as_json:
            return json

        else:
            sol_keys = json.pop('sol_keys')
            validity_checks = json.pop('validity_checks')
            data = MarsWeatherData(
                sols=json,
                sol_keys=sol_keys,
                validity_checks=validity_checks
            )
            return data



