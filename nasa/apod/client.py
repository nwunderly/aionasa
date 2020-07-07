
import aiohttp
import datetime

from collections import namedtuple


ApodEntry = namedtuple('ApodEntry', ['date', 'copyright', 'title', 'explanation', 'url', 'hdurl', 'media_type', 'service_version'])


class APOD:
    """
    Client for NASA Astronomy Picture of the Day.
    """
    def __init__(self, api_key='DEMO_KEY', session=None):
        """
        Initializes the APOD class.

        :param api_key: api.nasa.gov key for expanded usage.
        :param session:
        """
        self._api_key = api_key
        self._session = session if session else aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def get(self, date: datetime.date = None, hd: bool = None, as_json: bool = False):
        """
        Performs a GET request to NASA's APOD API.

        :param date: The date of the APOD image to retrieve. Defaults to 'today'.
        :param hd: Retrieve the URL for the high resolution image. Defaults to 'False'.
        :param as_json: Bool indicating whether to return a dict containing the raw returned json data instead of the normal named tuple.
        :return: A named tuple containing data returned by the API.
        """
        if not (isinstance(date, datetime.date) or date is None):
            raise TypeError("Argument 'date' must be an instance of 'datetime.date'.")
        if not (isinstance(hd, bool) or hd is None):
            raise TypeError("Argument 'hd' must be an instance of 'bool'.")

        if date is None:  # parameter will be left out of the query.
            date = ''
        else:
            date = 'date=' + date.strftime('%Y-%m-%d') + '&'
        if hd is None:  # parameter will be left out of the query.
            hd = ''
        else:
            hd = 'hd=' + str(hd) + '&'

        request = f"https://api.nasa.gov/planetary/apod?{date}{hd}api_key=DEMO_KEY"

        async with self._session.get(request) as response:
            json = await response.json()

        if as_json:
            return json

        else:
            entry = ApodEntry(
                date=json.get('date'),
                copyright=json.get('copyright'),
                title=json.get('title'),
                explanation=json.get('explanation'),
                url=json.get('url'),
                hdurl=json.get('hdurl'),
                media_type=json.get('media_type'),
                service_version=json.get('service_version')
            )
            return entry

    async def close(self):
        if self._session:
            await self._session.close()



