
import datetime

from ..errors import *


class EarthImage:
    """A NASA EPIC image asset.

    """
    def __init__(self, client, **kwargs):
        self.client = client

        yyyy, mm, dd = kwargs['date'].split()[0].split('-')
        self.url = f"https://api.nasa.gov/EPIC/archive/natural/{yyyy}/{mm}/{dd}/png/{kwargs['image']}.png"

        # 'date': '2020-10-24 00:41:06'
        self.date = datetime.datetime.strptime(kwargs['date'], '%Y-%m-%d %H:%M:%S')

        self.image = kwargs['image']
        self.caption = kwargs['caption']
        self.centroid_coordinates = kwargs['centroid_coordinates']
        self.dscovr_j2000_position = kwargs['dscovr_j2000_position']
        self.sun_j2000_position = kwargs['sun_j2000_position']
        self.attitude_quaternions = kwargs['attitude_quaternions']
        self.coords = kwargs['coords']




