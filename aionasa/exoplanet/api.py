import aiohttp
import asyncio
import datetime

# try:
#     import pandas
# except ImportError:
#     pandas = None

from ..client import BaseClient
from ..rate_limit import default_rate_limiter, demo_rate_limiter
from ..errors import APIException


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

    async def _get_raw(self, querystring):
        url = f"{BASE_URL}?{querystring}"

        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise APIException(resp.status, resp.reason)
            data = await resp.text()

        return data

    async def _get_json(self, querystring):
        url = f"{BASE_URL}?{querystring}"

        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise APIException(resp.status, resp.reason)
            json = await resp.json()

        return json

    async def query(self, table, **query):
        """Query the database.

        Parameters
        ----------
        table:
            The table to query. This is required.
        query:
            Other query parameters to be included in the request.

        Returns
        -------
        :class:`str`
            The data returned by the API.
        """
        querystring = f"table={table}"
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        return await self._get_raw(querystring)

    # async def query_json(self, table, **query):
    #     """Query the database. Format is requested as JSON and parsed before returning.
    #
    #     Parameters
    #     ----------
    #     table:
    #         The table to query. This is required.
    #     query:
    #         Other query parameters to be included in the request.
    #
    #     Returns
    #     -------
    #     The parsed JSON data returned by the API.
    #     """
    #     querystring = f"table={table}"
    #     query['format'] = 'json'
    #     queries = [f"{param}={value}" for param, value in query.items() if value]
    #     querystring += "&" + "&".join(queries) if query else ""
    #
    #     return await self._get_json(querystring)

    async def query_alias_table(self, objname, **query):
        """Query the database's alias table.

        Shorthand for `?table=aliastable&objname=OBJNAME&...`

        Parameters
        ----------
        objname:
            The name of the object to list aliases for.
        query:
            Other query parameters to be included in the request.

        Returns
        -------
        :class:`str`
            The alias table returned by the API.
        """
        querystring = f"?table=aliastable&objname={objname}"
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        return await self._get_raw(querystring)


