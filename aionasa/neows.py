import datetime
import logging

from .client import BaseClient
from .errors import APIException
from .rate_limit import default_rate_limiter, demo_rate_limiter
from .utils import date_strptime, datetime_strptime

logger = logging.getLogger('aionasa.neows')


class NeoWs(BaseClient):
    """Client for NASA Near Earth Object Weather Service.

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

    async def _get(self, url):
        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(url) as response:
            if response.status != 200:
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        return json

    async def feed(self, start_date: datetime.date, end_date: datetime.date = None):
        """Retrieve a list of Asteroids based on their closest approach date to Earth.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            Starting date for asteroid search.
        end_date: :class:`datetime.date`
            Ending date for asteroid search.

        Returns
        -------
        :class:`List[Asteroid]`
            A list of Asteroids returned by the API.
        """
        start_date = 'start_date=' + start_date.strftime('%Y-%m-%d') + '&'

        if end_date is None:  # parameter will be left out of the query.
            end_date = ''
        else:
            end_date = 'end_date=' + end_date.strftime('%Y-%m-%d') + '&'

        request = f"https://api.nasa.gov/neo/rest/v1/feed?{start_date}{end_date}api_key={self._api_key}"
        json = await self._get(request)
        return NeoWsFeedPage(self, json)

    async def lookup(self, asteroid_id: int):
        """Retrieve a list of Asteroids based on their closest approach date to Earth.

        Parameters
        ----------
        asteroid_id: :class:`int`
            Asteroid SPK-ID correlates to the NASA JPL small body.

        Returns
        -------
        :class:`Asteroid`
            Data for the requested NEO.
        """
        request = f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={self._api_key}"
        json = await self._get(request)
        return json


    async def browse(self, page: int = 0):
        """Browse the overall asteroid dataset.

        Parameters
        ----------
        page: :class:`int`
            The page to request. Defaults to 'page 0'.

        Returns
        -------
        :class:`List[...]`
            The paginated NeoWs asteroid data.
        """
        raise NotImplementedError
        # TODO: this
        #   maybe use async iterator for this.


##########################################################################
# NOTE: "epoch" should generally refer to the J2000 epoch (January 2000) #
##########################################################################


class Asteroid:
    """NASA data on a single NEO.

    Attributes
    ----------
    json: :class:`dict`
        Raw JSON data from the API that was used to build this object.
    id: :class:`int`
        JPL NEO ID. In the JSON data, ``'neo_reference_id'`` is an alias for this.
    name: :class:`str`
        Name of the NEO. In the JSON data, ``'designation'`` is an alias for this.
    nasa_jpl_url: :class:`str`
        NASA Jet Propulsion Laboratory website URL containing information regarding this NEO.
    absolute_magnitude_h: :class:`float`
        Absolute magnitude of the NEO (magnitude at 1 au from Sun and observer).
    is_potentially_hazardous_asteroid: :class:`bool`
        :strike:`Self-explanatory, I hope.`
    is_sentry_object: :class:`bool`
        `Sentry: Earth Impact Monitoring https://cneos.jpl.nasa.gov/sentry/`_
    estimated_diameter: :class:`dict`
        Estimated diameter of the NEO. A dict containing minimum and maximum diameters in four units:
        ``kilometers``, ``meters``, ``miles``, ``feet``.
    close_approach_data: :class:`List[CloseApproach]`
        A list of close approach events between this NEO and Earth.
    orbital_data: :class:`OrbitalData`
        Information regarding this NEO's orbit.
    """
    def __init__(self, json):
        self.json = json
        self.id = int(json['id'])
        # self.neo_reference_id = int(json['neo_reference_id'])
        self.name = json['designation']
        # self.designation = json['designation']
        self.nasa_jpl_url = json['nasa_jpl_url']
        self.absolute_magnitude_h = float(json['absolute_magnitude_h'])
        self.is_potentially_hazardous_asteroid = json['is_potentially_hazardous_asteroid']
        self.is_sentry_object = json['is_sentry_object']
        self.estimated_diameter = json['estimated_diameter']  # TODO: make this not terrible
        self.close_approach_data = CloseApproach._from_list(json['close_approach_data'])
        self.orbital_data = OrbitalData(json['orbital_data'])

    @classmethod
    def _from_list(cls, json):
        return [cls(obj) for obj in json]

    def min_diameter(self, unit):
        return self.estimated_diameter[unit]['estimated_diameter_min']

    def max_diameter(self, unit):
        return self.estimated_diameter[unit]['estimated_diameter_max']


class CloseApproach:
    """A single NEO close-approach date.

    Attributes
    ----------
    json: :class:`dict`
        Raw JSON data from the API that was used to build this object.
    date: :class:`datetime.date`
        The date of this close approach.
    date_full: :class:`datetime.datetime`
        The full timestamp of this close approach.
    epoch_date: :class:`int`
        The timestamp of this close approach, in seconds from the epoch.
    orbiting_body: :class:`str`
        The name of the body this NEO is orbiting.
    relative_velocity: :class:`dict`
        Relative velocity of this NEO with respect to Earth during this close approach.
        TODO: uncertain about this one.
    miss_distance: :class:`dict`
        The distance by which this NEO missed the Earth during this close approach.
    """
    def __init__(self, json):
        self.json = json
        close_approach_date = json['close_approach_date']
        close_approach_time = json['close_approach_date_full'].split()[1]
        self.date = date_strptime(close_approach_date)
        self.date_full = datetime_strptime(f'{close_approach_date} {close_approach_time}')
        self.epoch_date = int(json['epoch_date'])
        self.orbiting_body = json['orbiting_body']

        # TODO: make these nicer
        self.relative_velocity = json['relative_velocity']
        self.miss_distance = json['miss_distance']

    @classmethod
    def _from_list(cls, json):
        return [cls(obj) for obj in json]


class OrbitalData:
    """NEO orbital data.

    Attributes
    ----------
    orbit_id: :class:`int`
        JPL orbit ID (JPL 13, JPL 24, etc).
        TODO: figure out what this actually means
    orbit_determination_date: :class:`datetime.datetime`
        When orbit solution was computed.
    first_observation_date: :class:`datetime.date`
        Date of the first recorded observation of this orbit.
    last_observation_date: :class:`datetime.date`
        Date of the last recorded observation of this orbit.
    data_arc_in_days: :class:`int`
        Number of days spanned by the data-arc.
    observations_used: :class:`int`
        Number of recorded observations of this orbit.
    orbit_uncertainty: :class:`int`
        MPC "U" parameter: orbit uncertainty estimate 0-9, with 0 being good, and 9 being highly uncertain.
    minimum_orbit_intersection: :class:`float`
        Earth MOID (Minimum Orbit Intersection Distance), in au.
    jupiter_tisserand_invariant: :class:`float`
        Jupiter Tisserand invariant.
    epoch_osculation: :class:`float`
        When these orbital elements were determined, in seconds from the epoch.
    eccentricity: :class:`float`
        Eccentricity of the orbit.
    semi_major_axis: :class:`float`
        Semi-major axis of the orbit, in au.
    inclination: :class:`float`
        Inclination of the NEO's orbit, in degrees.
    ascending_node_longitude: :class:`float`
        Longitude of the ascending node, in degrees.
    orbital_period: :class:`float`
        Orbital period, in days.
    perihelion_distance: :class:`float`
        Perihelion distance, in au.
    perihelion_argument: :class:`float`
        Argument of perihelion, in degrees.
    aphelion_distance: :class:`float`
        Aphelion distance, in au.
    perihelion_time: :class:`float`
        Time of perihelion passage, in `TDB`_ (Barycentric Dynamical Time).
    mean_anomaly: :class:`float`
        Mean anomaly, in degrees.
    mean_motion: :class:`float`
        Mean motion, in degrees per day.
    equinox: :class:`str`
        Will most likely be J2000 (January 1, 2000)
    orbit_class: :class:`dict`
        Orbital classification information.

    .. _TDB: https://www.timeanddate.com/time/terrestrial-dynamic-time.html
    """
    def __init__(self, json):
        self.json = json
        self.orbit_id = int(json['orbit_id'])
        self.orbit_determination_date = datetime_strptime(json['orbit_determination_date'], seconds=True)
        self.first_observation_date = date_strptime(json['first_observation_date'])
        self.last_observation_date = date_strptime(json['last_observation_date'])
        self.data_arc_in_days = int(json['data_arc_in_days'])
        self.observations_used = int(json['observations_used'])
        self.orbit_uncertainty = int(json['orbit_uncertainty'])  # TODO: INT OR FLOAT??
        self.minimum_orbit_intersection = float(json['minimum_orbit_intersection'])
        self.jupiter_tisserand_invariant = float(json['jupiter_tisserand_invariant'])
        self.epoch_osculation = float(json['epoch_osculation'])
        self.eccentricity = float(json['eccentricity'])
        self.semi_major_axis = float(json['semi_major_axis'])
        self.inclination = float(json['inclination'])
        self.ascending_node_longitude = float(json['ascending_node_longitude'])
        self.orbital_period = float(json['orbital_period'])
        self.perihelion_distance = float(json['perihelion_distance'])
        self.perihelion_argument = float(json['perihelion_argument'])
        self.aphelion_distance = float(json['aphelion_distance'])
        self.perihelion_time = float(json['perihelion_time'])
        self.mean_anomaly = float(json['mean_anomaly'])
        self.mean_motion = float(json['mean_motion'])
        self.equinox = json['equinox']
        self.orbit_class = json['orbit_class']  # TODO: clean this up


# # TODO: maybe make this an enum
# class OrbitClass:
#     pass


class NeoWsFeedPage:
    """Class representing the paginated NEO API feed endpoint.
    Asteroids are sorted into a dict by date.

    Attributes
    ----------
    json: :class:`dict`
        JSON data returned by the API.
    element_count: :class:`int`
        Number of Asteroids on this page.
    """
    def __init__(self, client, json):
        self.json = json
        self._client = client
        self._session = client._session
        self._url_self = json['links']['self']
        self._url_prev = json['links']['prev']
        self._url_next = json['links']['next']
        self.element_count = json['element_count']

        self.near_earth_objects = {}
        for date, asteroids in json['near_earth_objects'].items():
            self.near_earth_objects[date] = Asteroid._from_list(asteroids)

    async def next(self):
        """Returns the next page in the feed.

        Returns
        -------
        :class:`NeoWsFeedPage`
            The next page in the feed.
        """
        json = await self._client._get(self._url_next)
        return NeoWsFeedPage(self._client, json)

    async def prev(self):
        """Returns the previous page in the feed.

        Returns
        -------
        :class:`NeoWsFeedPage`
            The previous page in the feed.
        """
        json = await self._client._get(self._url_prev)
        return NeoWsFeedPage(self._client, json)


class NeoWsBrowsePage:
    """Class representing the paginated NEO API browse endpoint.
    Asteroids are all in a single list, ``'near_earth_objects'``.

    Attributes
    ----------
    json: :class:`dict`
        JSON data returned by the API.
    page_number
        The page number of this page.
    page_size
        TODO
    page_count
        Total number of pages available through the API.
    element_count
        Number of Asteroids on this page.
    """
    def __init__(self, client, json):
        self.json = json
        self._client = client
        self._session = client._session
        self._url_self = json['links']['self']

        # one of these might be None (if it's the first or last page)
        self._url_prev = json['links'].get('prev')
        self._url_next = json['links'].get('next')

        self.page_number = json['page']['number']
        self.page_size = json['page']['size']
        self.page_count = json['page']['total_pages']
        self.element_count = json['page']['total_elements']
        self.near_earth_objects = Asteroid._from_list(json['near_earth_objects'])

    async def next(self):
        """Returns the next page in the browse feed.

        Returns
        -------
        :class:`NeoWsBrowsePage`
            The next page in the feed.
        """
        if not self._url_next:
            raise ValueError(f"Last page has no next page available. (Page {self.page_number})")
        json = await self._client._get(self._url_next)
        return NeoWsBrowsePage(self._client, json)

    async def prev(self):
        """Returns the previous page in the browse feed.

        Returns
        -------
        :class:`NeoWsBrowsePage`
            The previous page in the feed.
        """
        if not self._url_prev:
            raise ValueError(f"First page has no previous page available. (Page {self.page_number})")
        json = await self._client._get(self._url_prev)
        return NeoWsBrowsePage(self._client, json)
