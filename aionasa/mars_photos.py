import logging

from .asset import Asset
from .client import BaseClient
from .errors import APIException
from .rate_limit import default_rate_limiter, demo_rate_limiter
from .utils import date_strptime

logger = logging.getLogger('aionasa.mars_photos')


# API source code: https://github.com/chrisccerami/mars-photo-api

# ===============================
# API MIRRORS:
#   https://api.nasa.gov/mars-photos/
#   https://mars-photos.herokuapp.com/
# ===============================


class MarsPhotos(BaseClient):
    """Client for NASA Mars Rover Photos.

    Parameters
    ----------
    use_nasa_mirror: :class:`bool`
        Whether to use the api.nasa.gov mirror instead of mars-photos.herokuapp.com
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.

    .. note::
        The api.nasa.gov mirror is rate limited (like other api.nasa.gov APIs).
        The API at mars-photos.herokuapp.com, however, is not, nor does it require an API key to use.
        These features will be ignored when using this API through mars-photos.herokuapp.com.
    """
    def __init__(self, use_nasa_mirror=False, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if use_nasa_mirror:
            if api_key == 'DEMO_KEY' and rate_limiter:
                rate_limiter = demo_rate_limiter
            self.base_url = 'https://api.nasa.gov/mars-photos/api/v1'
        else:
            api_key = None
            rate_limiter = None
            self.base_url = 'https://mars-photos.herokuapp.com/api/v1'
        super().__init__(api_key, session, rate_limiter)

    async def _get_json(self, relative_url):
        url = self.base_url + relative_url

        if self._api_key:
            if '?' in url:
                url += ('&api_key=' + self._api_key)
            else:
                url += ('?api_key=' + self._api_key)

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise APIException(resp.status, resp.reason)
            data = await resp.json()

        if self.rate_limiter:
            remaining = int(resp.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        return data

    async def manifest(self, rover):
        """Retrieve a rover's mission manifest.

        Parameters
        ----------
        rover: :class:`str`

        Returns
        -------
        :class:`RoverManifest`
            The requested mission manifest.
        """
        json = await self._get_json(f'/manifests/{rover}')
        return RoverManifest(json['photo_manifest'])

    async def photos(self, rover, sol=None, date=None, camera=None, page=None):
        """Query the API by rover and Martian sol/Earth date.

        Parameters
        ----------
        rover: :class:`str`
            Rover to request images for.
        sol: :class:`int`
            Query by Martian sol.
        date: :class:`datetime.date`
            Query by Earth date.
        camera: :class:`str`
            Query by camera.
        page: :class:`int`

        .. note::
            Either a Martian sol or an Earth date must be specified.
            The API will return an empty response if no date information is given.
            These two parameters cannot both be included.

        Returns
        -------
        :class:`List[MarsPhoto]`
            A list of pictures for the requested rover/date.
        """
        url = f'/rovers/{rover}/photos'

        if (sol is not None) and (not date):
            url += f'?sol={sol}'
        elif (date is not None) and (not sol):
            date = date.strftime('%Y-%m-%d')
            url += f'?earth_date={date}'
        else:
            raise ValueError("Either 'sol' or 'date' parameter must be provided.")

        if camera:
            url += f'&camera={camera}'
        if page:
            url += f'&page={page}'

        json = await self._get_json(url)
        return MarsPhoto._from_list(self, json['photos'])


class RoverManifest:
    """A mars rover mission manifest.

    Attributes
    ----------
    name: :class:`str`
        Name of the rover.
    landing_date: :class:`datetime.date`
        The Earth date that the rover landed on Mars.
    launch_date: :class:`datetime.date`
        The Earth date that the rover was launched.
    status: :class:`str`
        The rover's status.
    max_sol: :class:`int`
        The last Martian sol with available photos.
    max_date: :class:`datetime.date`
        The last Earth date with available photos.
    total_photos: :class:`int`
        Total number of available photos for this rover.
    photos: :class:`List[MarsPhotoDate]`
        Information for each date with available photos.
    """
    def __init__(self, data):
        self.name = data['name']
        self.landing_date = date_strptime(data['landing_date'])
        self.launch_date = date_strptime(data['launch_date'])
        self.status = data['status']
        self.max_sol = data['max_sol']
        self.max_date = date_strptime(data['max_date'])
        self.total_photos = data['total_photos']
        self.photos = MarsPhotoDate._from_list(data['photos'])


class MarsPhotoDate:
    """A date from a rover's mission manifest.

    Attributes
    ----------
    sol: :class:`int`
        The Martial sol corresponding to this date.
    earth_date: :class:`datetime.date`
        The Earth date corresponding to this date.
    total_photos: :class:`int`
        The total number of photos available from this date.
    cameras: :class:`List[str]`
        List of cameras with available images from this date.
    """
    def __init__(self, data):
        self.sol = data['sol']
        self.earth_date = date_strptime(data['earth_date'])
        self.total_photos = data['total_photos']
        self.cameras = data['cameras']

    @classmethod
    def _from_list(cls, data):
        return [cls(d) for d in data]


class MarsPhoto(Asset):
    """A Mars rover photo.

    Attributes
    ----------
    id: :class:`int`
        The photo id.
    sol: :class:`int`
        The Martian sol that the photo was taken.
    earth_date: :class:`datetime.date`
        The Earth date that the photo was taken.
    camera: :class:`RoverCamera`
        The camera that took the photo.
    img_src: :class:`str`
        URL where the photo can be found.
    rover: :class:`Rover`
        The rover that took this photo.
    """
    def __init__(self, client, data):
        self.id = data['id']
        self.sol = data['sol']
        self.earth_date = date_strptime(data['earth_date'])
        self.camera = RoverCamera(data['camera'])
        self.img_src = data['img_src']
        self.rover = Rover(data['rover'])

        super().__init__(client, self.img_src, self.img_src.split('/')[-1])

    async def read(self):
        """Downloads the image associated with this MarsPhoto.

        Returns
        -------
        :class:`bytes`
            The image, downloaded from the URL provided by the API.
        """
        return await super().read(self.img_src)

    async def save(self, path=None):
        """Downloads the file associated with this MarsPhoto and saves to the requested path.

        Parameters
        ----------
        path:
            The file path at which to save the file.
            If ``None``, saves the image to the working directory using the filename from the asset url.

        Returns
        -------
        :class:`int`
            The number of bytes written.
        """
        return await super().save(path, self.img_src)

    @classmethod
    def _from_list(cls, client, data):
        return [cls(client, d) for d in data]


class RoverCamera:
    """A Mars rover camera.

    Attributes
    ----------
    id: :class:`int`
        The camera id.
    name: :class:`str`
        The camera's name, i.e. "MAST".
    rover_id: :class:`int`
        The rover id.
    full_name: :class:`str`
        The camera's full name, i.e. "Mast Camera".
    """
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.rover_id = data['rover_id']
        self.full_name = data['full_name']


class Rover:
    """A Mars rover.

    Attributes
    ----------
    id: :class:`int`
        The rover id.
    name: :class:`str`
        Name of the rover.
    landing_date: :class:`datetime.date`
        The Earth date that the rover landed on Mars.
    launch_date: :class:`datetime.date`
        The Earth date that the rover was launched.
    status: :class:`str`
        The rover's status.
    """
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.landing_date = date_strptime(data['landing_date'])
        self.launch_date = date_strptime(data['launch_date'])
        self.status = data['status']
