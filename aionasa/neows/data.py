from datetime import datetime
from ..utils import date_strptime


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
    """
    def __init__(self, json):
        self.json = json
        close_approach_date = json['close_approach_date']
        close_approach_time = json['close_approach_date_full'].split()[1]
        self.date = date_strptime(close_approach_date)
        self.time = datetime.strptime(f'{close_approach_date} {close_approach_time}', '%Y-%m-%d %H:%M')
        self.epoch_date = json['epoch_date']
        self.orbiting_body = json['orbiting_body']

        # TODO: make these nicer
        self.relative_velocity = json['relative_velocity']
        self.miss_distance = json['miss_distance']

    @classmethod
    def _from_list(cls, json):
        return [cls(obj) for obj in json]


class OrbitalData:
    """NEO orbital data.
    """
    def __init__(self, json):
        self.json = json


# TODO: maybe make this an enum
class OrbitClass:
    pass
