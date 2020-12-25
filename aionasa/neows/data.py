from typing import List

from ..utils import date_strptime, datetime_strptime


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
        self.orbit_id = int(json["orbit_id"])
        self.orbit_determination_date = datetime_strptime(json["orbit_determination_date"], seconds=True)
        self.first_observation_date = date_strptime(json["first_observation_date"])
        self.last_observation_date = date_strptime(json["last_observation_date"])
        self.data_arc_in_days = int(json["data_arc_in_days"])
        self.observations_used = int(json["observations_used"])
        self.orbit_uncertainty = int(json["orbit_uncertainty"])  # TODO: INT OR FLOAT??
        self.minimum_orbit_intersection = float(json["minimum_orbit_intersection"])
        self.jupiter_tisserand_invariant = float(json["jupiter_tisserand_invariant"])
        self.epoch_osculation = float(json["epoch_osculation"])
        self.eccentricity = float(json["eccentricity"])
        self.semi_major_axis = float(json["semi_major_axis"])
        self.inclination = float(json["inclination"])
        self.ascending_node_longitude = float(json["ascending_node_longitude"])
        self.orbital_period = float(json["orbital_period"])
        self.perihelion_distance = float(json["perihelion_distance"])
        self.perihelion_argument = float(json["perihelion_argument"])
        self.aphelion_distance = float(json["aphelion_distance"])
        self.perihelion_time = float(json["perihelion_time"])
        self.mean_anomaly = float(json["mean_anomaly"])
        self.mean_motion = float(json["mean_motion"])
        self.equinox = json["equinox"]
        self.orbit_class = json["orbit_class"]


# TODO: maybe make this an enum
class OrbitClass:
    pass
