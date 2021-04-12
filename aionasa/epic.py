import datetime
import logging
from collections import namedtuple

from .asset import Asset
from .client import BaseClient
from .errors import APIException, ArgumentError
from .rate_limit import default_rate_limiter, demo_rate_limiter

logger = logging.getLogger('aionasa.epic')


# ===============================
# API MIRRORS:
#   https://epic.gsfc.nasa.gov/api/
#   https://api.nasa.gov/EPIC/api/
# ===============================


class EPIC(BaseClient):
    """Client for NASA Earth Polychromatic Imaging Camera.

    Parameters
    ----------
    use_nasa_mirror: :class:`bool`
        Whether to use the api.nasa.gov mirror instead of epic.gsfc.nasa.gov
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.

    ..note::
        The api.nasa.gov mirror is rate limited (like other api.nasa.gov APIs).
        The API at epic.nasa.gov, however, is not, nor does it require an API key to use.
        These features will be ignored when using this API through epic.nasa.gov.
    """
    def __init__(self, use_nasa_mirror=False, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if use_nasa_mirror:
            if api_key == 'DEMO_KEY' and rate_limiter:
                rate_limiter = demo_rate_limiter
            self.base_url = 'https://api.nasa.gov/EPIC'
        else:
            api_key = None
            rate_limiter = None
            self.base_url = 'https://epic.gsfc.nasa.gov'
        super().__init__(api_key, session, rate_limiter)

    async def _get_metadata(self, collection, date):
        """Retrieves metadata for imagery for a given collection and date.

        Parameters
        ----------
        collection: :class:`str`
            The collection to search. Should be 'natural' or 'enhanced'.
        date: :class:`datetime.date`
            The date to retrieve data for.

        Returns
        -------
        :class:`List[EarthImage]`
            Data returned by the API.
        """
        if collection not in ('natural', 'enhanced'):
            raise ArgumentError(f"collection expected be 'natural' or 'enhanced' got {collection}")

        if date is None:
            date = ''
        else:
            date = date.strftime('/date/%Y-%m-%d')

        api_key = f'?api_key={self._api_key}' if self._api_key else ''
        request = f'{self.base_url}/api/{collection}{date}{api_key}'

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        images = []

        for item in json:
            image = EarthImage(client=self, json=item, collection=collection)
            images.append(image)

        return images

    async def _get_listing(self, collection):
        """Retrieves a listing of dates with available images in the requested collection.

        Parameters
        ----------
        collection: :class:`str`
            The collection to get a listing for. Should be 'natural' or 'enhanced'.

        Returns
        -------
        :class:`List[datetime.date`
            List of dates with available imagery.
        """
        if collection not in ('natural', 'enhanced'):
            raise ArgumentError(f"collection expected be 'natural' or 'enhanced' got {collection}")

        api_key = f'?api_key={self._api_key}' if self._api_key else ''
        request = f'{self.base_url}/api/{collection}/available{api_key}'

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        dates = []

        for item in json:
            date = datetime.datetime.strptime(item, '%Y-%m-%d').date()
            dates.append(date)

        return dates

    async def natural_images(self, date: datetime.date = None):
        """Retrieves metadata for natural color imagery for a given date.
        Defaults to most recent date.

        Parameters
        ----------
        date: :class:`datetime.date`
            The date to request data for.

        Returns
        -------
        :class:`List[EarthImage]`
            Data returned by the API.
        """
        return await self._get_metadata('natural', date)

    async def natural_listing(self):
        """Retrieve a listing of all dates with available natural color imagery.

        Returns
        -------
        :class:`List[datetime.date]`
            The dates returned by the API.
        """
        return await self._get_listing('natural')

    async def enhanced_images(self, date: datetime.date = None):
        """Retrieves metadata for enhanced color imagery for a given date.
        Defaults to most recent date.

        Parameters
        ----------
        date: :class:`datetime.date`
            The date to request data for.

        Returns
        -------
        :class:`List[EarthImage]`
            Data returned by the API.
        """
        return await self._get_metadata('enhanced', date)

    async def enhanced_listing(self):
        """Retrieve a listing of all dates with available enhanced color imagery.

        Returns
        -------
        :class:`List[datetime.date]`
            The dates returned by the API.
        """
        return await self._get_listing('enhanced')


class EarthImage(Asset):
    """A NASA EPIC image asset. Accessible as a full-resolution PNG, half-resolution JPG,
    or a thumbnail JPG image.

    Attributes
    ----------
    client: :class:`EPIC`
        The EPIC client that was used to retrieve this data.
    json: :class:`dict`
        The JSON data returned by the API.
    png_url:
        The URL of the full-resolution PNG image.
    jpg_url:
        The URL of the half-resolution JPEG image.
    thumb_url:
        The URL of the thumbnail-size JPEG image.
    date: :class:`datetime.Date`
        The date this image was taken.
    caption:
        The caption for this image.
    image:
        The image name.
    centroid_coordinates: :class:`EarthCoordinates`
        Geographical coordinates that the satellite is looking at as a named tuple.
    dscovr_j2000_position: :class:`J2000Coordinates`
        Position of the satellite in space as a named tuple.
    lunar_j2000_position: :class:`J2000Coordinates`
        Position of the moon in space as a named tuple.
    sun_j2000_position: :class:`J2000Coordinates`
        Position of the sun in space as a named tuple.
    attitude_quaternions: :class:`Attitude`
        Satellite attitude as a named tuple.
    """
    def __init__(self, client, json, collection):
        self.json = json
        self.client = client

        api_key = f'?api_key={self.client._api_key}' if self.client._api_key else ''

        yyyy, mm, dd = json['date'].split()[0].split('-')
        self.png_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/png/{json['image']}.png{api_key}"
        self.jpg_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/jpg/{json['image']}.jpg{api_key}"
        self.thumb_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/thumbs/{json['image']}.jpg{api_key}"

        # 'date': '2020-10-24 00:41:06'
        self.date = datetime.datetime.strptime(json['date'], '%Y-%m-%d %H:%M:%S')

        self.identifier = json['identifier']
        self.image = json['image']
        self.caption = json['caption']
        self.centroid_coordinates = EarthCoordinates(**json['centroid_coordinates'])
        self.dscovr_j2000_position = J2000Coordinates(**json['dscovr_j2000_position'])
        self.lunar_j2000_position = J2000Coordinates(**json['lunar_j2000_position'])
        self.sun_j2000_position = J2000Coordinates(**json['sun_j2000_position'])
        self.attitude_quaternions = Attitude(**json['attitude_quaternions'])
        # self.coords = json['coords']

        super().__init__(client, self.png_url, json['image'] + '.png')

    async def read(self, filetype='png'):
        """Downloads the file associated with this EarthImage.

        Parameters
        ----------
        filetype: :class:`str`
            The file type to download. Can be ``'png'``, ``'jpg'``, or ``'thumb'``. Defaults to ``'png'``.

        Returns
        -------
        :class:`bytes`
            The file, downloaded from the URL.
        """
        url = {'png': self.png_url,
               'jpg': self.jpg_url,
               'thumb': self.thumb_url}.get(filetype)

        if not url:
            raise ArgumentError("Invalid file type. Expected 'png', 'jpg', or 'thumb'.")

        return await super().read(url)

    async def save(self, path=None, filetype='png'):
        """Downloads the file associated with this EarthImage and saves to the requested path.

        Parameters
        ----------
        path:
            The file path at which to save the file.
            If ``None``, saves the image to the working directory using the filename from the asset url.
        filetype: :class:`str`
            The file type to download. Can be ``'png'``, ``'jpg'``, or ``'thumb'``. Defaults to ``'png'``.

        Returns
        -------
        :class:`int`
            The number of bytes written.
        """
        url = {'png': self.png_url,
               'jpg': self.jpg_url,
               'thumb': self.thumb_url}.get(filetype)

        if not url:
            raise ArgumentError("Invalid file type. Expected 'png', 'jpg', or 'thumb'.")

        return await super().save(path, url)

    async def read_png(self):
        return await self.read('png')

    async def save_png(self, path=None):
        return await self.save(path, 'png')

    async def read_jpg(self):
        return await self.read('jpg')

    async def save_jpg(self, path=None):
        return await self.save(path, 'jpg')

    async def read_thumb(self):
        return await self.read('thumb')

    async def save_thumb(self, path=None):
        return await self.save(path, 'thumb')


J2000Coordinates = namedtuple('J2000Coordinates', ['x', 'y', 'z'])
Attitude = namedtuple('Attitude', ['q0', 'q1', 'q2', 'q3'])
EarthCoordinates = namedtuple('EarthCoordinates', ['lat', 'lon'])
