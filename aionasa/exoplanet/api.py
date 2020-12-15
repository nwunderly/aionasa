import aiohttp
import asyncio
import datetime

try:
    import pandas
except ImportError:
    pandas = None

from ..client import BaseClient


class Exoplanet(BaseClient):
    """
    Client for NASA Exoplanet Archive API.

    In-depth documentation for this API can be found at https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html

    Parameters for Exoplanet API:
        -
    """

    async def raw_get(self, query):
        pass

    async def get(self, table: str, select=None, count=None, colset=None, where=None, order=None, ra=None, dec=None, format=None):
        pass

