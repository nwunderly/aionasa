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

    async def manifest(self, rover):
        """Retrieve a rover's mission manifest.

        Parameters
        ----------
        rover:

        Returns
        -------

        """

    async def photos(self, rover):
        """

        Parameters
        ----------
        rover

        Returns
        -------

        """

