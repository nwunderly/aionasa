
import aiohttp
import datetime

from collections import namedtuple

from ..base_client import BaseClient
from ..errors import APIException
from .apod_data import AstronomyPicture



class APOD(BaseClient):
    """
    Client for NASA Astronomy Picture of the Day.

    Parameters for APOD API:
        - date: The date of the APOD image to retrieve. Defaults to 'today'.
        - start_date: The first date to return when requesting a list of dates.
        - end_date: The last date to return when requesting a list of dates. Range is inclusive.
        - hd: Bool indicating whether to retrieve the URL for the high resolution image. Defaults to 'False'.
        - concept_tags: DISABLED FOR THIS ENDPOINT.
    """

    async def get(self, date: datetime.date = None, hd: bool = None, as_json: bool = False):
        """
        Retrieves a single item from NASA's APOD API.

        :param date: The date of the APOD image to retrieve. Defaults to 'today'.
        :param hd: Retrieve the URL for the high resolution image. Defaults to 'False'.
        :param as_json: Bool indicating whether to return a dict containing the raw returned json data instead of the normal named tuple.
        :return: A named tuple containing data returned by the API.
        """
        if not (isinstance(date, datetime.date) or date is None):
            raise TypeError("Argument 'date' must be an instance of 'datetime.date'.")
        if not (isinstance(hd, bool) or hd is None):
            raise TypeError("Argument 'hd' must be an instance of 'bool'.")
        if not isinstance(as_json, bool):
            raise TypeError("Argument 'as_json' must be an instance of 'bool'.")


        if date is None:  # parameter will be left out of the query.
            date = ''
        else:
            date = 'date=' + date.strftime('%Y-%m-%d') + '&'
        if hd is None:  # parameter will be left out of the query.
            hd = ''
        else:
            hd = 'hd=' + str(hd) + '&'

        request = f"https://api.nasa.gov/planetary/apod?{date}{hd}api_key={self._api_key}"

        async with self._session.get(request) as response:

            if response.status != 200:  # not success
                raise APIException(f"{response.status} - {response.reason"})

            json = await response.json()

        if as_json:
            return json

        else:
            entry = AstronomyPicture(
                date=json.get('date'),
                copyright=json.get('copyright'),
                title=json.get('title'),
                explanation=json.get('explanation'),
                url=json.get('url'),
                hdurl=json.get('hdurl'),
                media_type=json.get('media_type'),
                service_version=json.get('service_version'),
            )
            return entry

    async def batch_get(self, start_date: datetime.date, end_date: datetime.date,
                        hd: bool = None, as_json: bool = False):
        """
        Retrieves multiple items from NASA's APOD API. Returns a list of APOD entries.

        :param start_date: The first date to return when requesting a list of dates.
        :param end_date: The last date to return when requesting a list of dates. Range is inclusive.
        :param hd: Retrieve the URL for the high resolution image. Defaults to 'False'.
        :param as_json: Bool indicating whether to return a dict containing the raw returned json data instead of the normal named tuple.
        :return: A list of named tuples containing data returned by the API.
        """
        if not isinstance(start_date, datetime.date):
            raise TypeError("Argument 'start_date' must be an instance of 'datetime.date'.")
        if not isinstance(start_date, datetime.date):
            raise TypeError("Argument 'end_date' must be an instance of 'datetime.date'.")
        if not (isinstance(hd, bool) or hd is None):
            raise TypeError("Argument 'hd' must be an instance of 'bool'.")
        if not isinstance(as_json, bool):
            raise TypeError("Argument 'as_json' must be an instance of 'bool'.")


        start_date = 'start_date=' + start_date.strftime('%Y-%m-%d') + '&'
        end_date = 'end_date=' + end_date.strftime('%Y-%m-%d') + '&'

        if hd is None:  # parameter will be left out of the query.
            hd = ''
        else:
            hd = 'hd=' + str(hd) + '&'

        request = f"https://api.nasa.gov/planetary/apod?{start_date}{end_date}{hd}api_key={self._api_key}"

        async with self._session.get(request) as response:
            
            if response.status != 200:  # not a success
                raise APIException(response.reason)

            json = await response.json()

        if as_json:
            return json

        else:
            result = []

            for item in json:

                entry = AstronomyPicture(
                    date=item.get('date'),
                    copyright=item.get('copyright'),
                    title=item.get('title'),
                    explanation=item.get('explanation'),
                    url=item.get('url'),
                    hdurl=item.get('hdurl'),
                    media_type=item.get('media_type'),
                    service_version=item.get('service_version')
                )
                result.append(entry)

            return result



