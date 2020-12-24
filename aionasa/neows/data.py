from datetime import datetime
from typing import List

from ..utils import date_strptime, datetime_strptime


class Asteroid:
    """NASA data on a single NEO.

    Attributes
    ----------
    json: :class:`dict`
        Raw JSON data from the API that was used to build this object.
    id: :class:`int`
        JPL NEO ID.
    name: :class:`str`
        Name of the NEO.
    designation: :class:`str`
        TODO
    nasa_jpl_url: :class:`str`
        TODO
    absolute_magnitude_h: :class:`int`
        TODO
    is_potentially_hazardous_asteroid: :class:`bool`
        TODO
    is_sentry_object: :class:`bool`
        TODO
    estimated_diameter: :class:`dict`
        TODO
    close_approach_data: :class:`List[CloseApproach]`
        TODO
    orbital_data: :class:`OrbitalData`
        TODO
    """
    def __init__(self, json):
        self.json = json
        self.id = int(json['id'])
        # self.neo_reference_id = int(json['neo_reference_id'])
        self.name = json['name']
        self.designation = json['designation']
        self.nasa_jpl_url = json['nasa_jpl_url']
        self.absolute_magnitude_h = json['absolute_magnitude_h']
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
        TODO
    date: :class:`datetime.date`
        TODO
    date_full: :class:`datetime.datetime`
        TODO
    epoch_date: :class:`int`
        TODO
    orbiting_body: :class:`str`
        TODO
    relative_velocity: :class:``
        TODO
    miss_distance: :class:``
        TODO
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
        TODO
    orbit_determination_date: :class:`datetime.datetime`
        TODO
    first_observation_date: :class:`datetime.date`
        TODO
    last_observation_date: :class:`datetime.date`
        TODO
    data_arc_in_days: :class:`int`
        TODO
    observations_used: :class:`int`
        TODO
    orbit_uncertainty: :class:`float`
        TODO
    minimum_orbit_intersection: :class:`float`
        TODO
    jupiter_tisserand_invariant: :class:`float`
        TODO
    epoch_osculation: :class:`float`
        TODO
    eccentricity: :class:`float`
        TODO
    semi_major_axis: :class:`float`
        TODO
    inclination: :class:`float`
        TODO
    ascending_node_longitude: :class:`float`
        TODO
    orbital_period: :class:`float`
        TODO
    perihelion_distance: :class:`float`
        TODO
    perihelion_argument: :class:`float`
        TODO
    aphelion_distance: :class:`float`
        TODO
    perihelion_time: :class:`float`
        TODO
    mean_anomaly: :class:`float`
        TODO
    mean_motion: :class:`float`
        TODO
    equinox: :class:`str`
        TODO
    orbit_class: :class:`dict`
        TODO
    """
    def __init__(self, json):
        self.json = json
        self.orbit_id = int(json["orbit_id"])
        self.orbit_determination_date = datetime_strptime(json["orbit_determination_date"], seconds=True)
        self.first_observation_date = date_strptime(json["first_observation_date"])
        self.last_observation_date = date_strptime(json["last_observation_date"])
        self.data_arc_in_days = int(json["data_arc_in_days"])
        self.observations_used = int(json["observations_used"])
        self.orbit_uncertainty = float(json["orbit_uncertainty"])  # TODO: INT OR FLOAT??
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
