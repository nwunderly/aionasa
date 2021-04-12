import io
import json
import logging

try:
    import pandas
except ImportError:
    pandas = None

from .client import BaseClient
from .errors import APIException, PandasNotFound

logger = logging.getLogger('aionasa.exoplanet')


# Documentation: https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html


BASE_URL = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"


class Exoplanet(BaseClient):
    """Client for NASA Exoplanet Archive API.

    ..note::
        Requests to this API do not seem to be subject to api.nasa.gov rate limits.
    """
    def __init__(self, api_key='DEMO_KEY', session=None):
        super().__init__(api_key, session, None)

    async def _get_raw(self, querystring):
        url = f"{BASE_URL}?{querystring}"

        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise APIException(resp.status, resp.reason)
            data = await resp.text()

        return data

    # Seems to not be supported. Throws a Mimetype error
    # async def _get_json(self, querystring):
    #     url = f"{BASE_URL}?{querystring}"
    #
    #     async with self._session.get(url) as resp:
    #         if resp.status != 200:
    #             raise APIException(resp.status, resp.reason)
    #         json = await resp.json()
    #
    #     return json

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

    async def query_json(self, table, **query):
        """Query the database.
        Format is requested as JSON and parsed to a python list before returning.

        Returns
        -------
        :class:`List[dict]`
            The parsed JSON data returned by the API.
        """
        querystring = f"table={table}"
        query['format'] = 'json'
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        text = await self._get_raw(querystring)
        return json.loads(text)

    async def query_df(self, table, **query):
        """Query the database.
        Format is requested as CSV and parsed to a pandas DataFrame before returning.

        ..note::
            ``pandas`` must be installed for this to work.

        Returns
        -------
        :class:`DataFrame`
            The parsed JSON data returned by the API.
        """
        querystring = f"table={table}"
        query['format'] = 'csv'
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        if not pandas:
            raise PandasNotFound

        text = await self._get_raw(querystring)
        file = io.StringIO(text)
        return pandas.read_csv(file)

    async def query_aliastable(self, objname, **query):
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
        querystring = f"table=aliastable&objname={objname}"
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        return await self._get_raw(querystring)

    async def query_aliastable_json(self, objname, **query):
        """Query the database's alias table.
        Format is requested as JSON and parsed to a python list before returning.

        Returns
        -------
        :class:`List[dict]`
            The alias table returned by the API.
        """
        querystring = f"table=aliastable&objname={objname}"
        query['format'] = 'json'
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        text = await self._get_raw(querystring)
        return json.loads(text)

    async def query_aliastable_df(self, objname, **query):
        """Query the database's alias table.
        Format is requested as CSV and parsed to a pandas DataFrame before returning.

        ..note::
            ``pandas`` must be installed for this to work.

        Returns
        -------
        :class:`DataFrame`
            The alias table returned by the API.
        """
        querystring = f"table=aliastable&objname={objname}"
        query['format'] = 'csv'
        queries = [f"{param}={value}" for param, value in query.items() if value]
        querystring += "&" + "&".join(queries) if query else ""

        if not pandas:
            raise PandasNotFound

        text = await self._get_raw(querystring)
        file = io.StringIO(text)
        return pandas.read_csv(file)
