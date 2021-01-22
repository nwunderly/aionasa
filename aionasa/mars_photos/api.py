import logging

from ..client import BaseClient
from ..errors import APIException
from ..rate_limit import default_rate_limiter, demo_rate_limiter

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

    ..note::
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

        print(url)

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
        return await self._get_json(f'/manifests/{rover}')

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

        return await self._get_json(url)

