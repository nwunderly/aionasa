import datetime
import logging

from .asset import Asset
from .client import BaseClient
from .errors import APIException
from .rate_limit import default_rate_limiter, demo_rate_limiter

logger = logging.getLogger('aionasa.apod')


class APOD(BaseClient):
    """Client for NASA Astronomy Picture of the Day API.

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """
    def __init__(self, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if api_key == 'DEMO_KEY' and rate_limiter:
            rate_limiter = demo_rate_limiter
        super().__init__(api_key, session, rate_limiter)

    async def get(self, date: datetime.date = None, as_json: bool = False):
        """Retrieves a single item from NASA's APOD API.

        Parameters
        ----------
        date: :class:`datetime.Date`
            The date of the APOD image to retrieve. Defaults to ``'today'``.
        as_json: :class:`bool`
            Bool indicating whether to return the raw returned json data instead of the normal AstronomyPicture object. Defaults to ``False``.

        Returns
        -------
        :class:`AstronomyPicture`
            An AstronomyPicture containing data returned by the API.
        """

        if date is None:  # parameter will be left out of the query.
            date = ''
        else:
            date = 'date=' + date.strftime('%Y-%m-%d') + '&'

        request = f"https://api.nasa.gov/planetary/apod?{date}api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:
            date = json.get('date')
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None

            entry = AstronomyPicture(
                client=self,
                date=date,
                json=json
            )
            return entry

    async def batch_get(self, start_date: datetime.date, end_date: datetime.date,
                        as_json: bool = False):
        """Retrieves multiple items from NASA's APOD API. Returns a list of APOD entries.

        Parameters
        ----------
        start_date: :class:`datetime.Date`
            The first date to return when requesting a range of dates.
        end_date: :class:`datetime.Date`
            The last date to return when requesting a range of dates. Range is inclusive.
        as_json: :class:`bool`
            Bool indicating whether to return a list of dicts containing the raw returned json data instead of the normal ``List[AstronomyPicture]``. Defaults to ``False``.

        Returns
        -------
        :class:`List[AstronomyPicture]`
            A list of AstronomyPicture objects containing data returned by the API.
        """

        start_date = 'start_date=' + start_date.strftime('%Y-%m-%d') + '&'
        end_date = 'end_date=' + end_date.strftime('%Y-%m-%d') + '&'

        request = f"https://api.nasa.gov/planetary/apod?{start_date}{end_date}api_key={self._api_key}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:
            result = []

            for item in json:

                date = item.get('date')
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date() if date else None

                entry = AstronomyPicture(
                    client=self,
                    date=date,
                    json=json
                )
                result.append(entry)

            return result


class AstronomyPicture(Asset):
    """A class representing a single daily APOD picture.
    Attributes
    ----------
    client: :class:`APOD`
        The APOD client that was used to retrieve this data.
    date: :class:`datetime.Date`
        The date this image was uploaded to APOD.
    copyright:
        The owner of this image, if it is not public domain.
    title:
        The APOD entry's title.
    explanation:
        The explanation for this image, written by astronomers, from this image's APOD page.
    url:
        The image url.
    hdurl:
        The HD image url, if available. Can be ``None``.
    html_url:
        The url of the APOD HTML page. This is the page a user would find this image on.
        This data is not provided by the API. This attribute has been added by the library for ease of use.
    media_type:
        The type of media. Will pretty much always be ``'image'``.
    service_version:
        The API service version. The API version is currently ``'v1'``.
    """
    def __init__(self, client, date: datetime.date, json):
        self.client = client
        self.date = date
        self.json = json
        self.copyright = json.get('copyright')
        self.title = json.get('title')
        self.explanation = json.get('explanation')
        self.url = json.get('url')
        self.hdurl = json.get('hdurl')
        self.media_type = json.get('media_type')
        self.service_version = json.get('service_version')

        site_formatted_date = f"{str(date.year)[2:]}{date.month:02d}{date.day:02d}"
        self.html_url = f"https://apod.nasa.gov/apod/ap{site_formatted_date}.html"

        super().__init__(client, self.url, self.url.split('/')[-1])

    async def read(self, hdurl: bool = True):
        """Downloads the image associated with this AstronomyPicture.

        Parameters
        ----------
        hdurl: :class:`bool`
            Indicates that the HD image should be downloaded, if possible.

        Returns
        -------
        :class:`bytes`
            The image, downloaded from the URL provided by the API.
        """
        if hdurl:
            url = self.hdurl or self.url
        else:
            url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        return await super().read(url)

    async def save(self, path=None, hdurl: bool = True):
        """Downloads the image associated with this AstronomyPicture and saves to a file.

        Parameters
        ----------
        path:
            The file path at which to save the image.
            If ``None``, saves the image to the working directory using the filename from the image url.
        hdurl: :class:`bool`
            Indicates that the HD image should be downloaded, if possible.

        Returns
        -------
        :class:`int`
            The number of bytes written.
        """
        if hdurl:
            url = self.hdurl or self.url
        else:
            url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        return await super().save(path=path, url=url)

    async def read_chunk(self, chunk_size: int, hdurl: bool = True):
        """Reads a chunk of the image associated with this AstronomyPicture.

        Parameters
        ----------
        chunk_size: :class:`int`
            Number of bytes to read.
        hdurl: :class:`bool`
            Indicates that the HD image should be downloaded, if possible.

        Returns
        -------
        :class:`bytes`
            The chunked data. Will be None if the image has been completely read.
        """
        if hdurl:
            url = self.hdurl or self.url
        else:
            url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        await super().read_chunk(chunk_size, self.url)
