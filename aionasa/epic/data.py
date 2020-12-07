import datetime

from ..errors import *
from ..asset import Asset


class EarthImage(Asset):
    """A NASA EPIC image asset.

    """
    def __init__(self, client, json, collection):
        self.json = json

        api_key = f'?api_key={self.client._api_key}' if self.client._api_key else ''

        yyyy, mm, dd = json['date'].split()[0].split('-')
        self.png_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/png/{json['image']}.png{api_key}"
        self.jpg_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/jpg/{json['image']}.jpg{api_key}"
        self.thumb_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/thumbs/{json['image']}.jpg{api_key}"

        # 'date': '2020-10-24 00:41:06'
        self.date = datetime.datetime.strptime(json['date'], '%Y-%m-%d %H:%M:%S')

        self.image = json['image']
        self.caption = json['caption']
        self.centroid_coordinates = json['centroid_coordinates']
        self.dscovr_j2000_position = json['dscovr_j2000_position']
        self.sun_j2000_position = json['sun_j2000_position']
        self.attitude_quaternions = json['attitude_quaternions']
        self.coords = json['coords']

        super().__init__(client, self.png_url, json['image'])

    async def read_png(self):
        await super().read(self.png_url)

    async def save_png(self, path=None):
        await super().save(path, self.png_url)

    async def read_jpg(self):
        await super().read(self.jpg_url)

    async def save_jpg(self, path=None):
        await super().save(path, self.jpg_url)

    async def read_thumb(self):
        await super().read(self.thumb_url)

    async def save_thumb(self, path=None):
        await super().save(path, self.thumb_url)


class J2000Coordinates:
    """Coordinates of an object according to the J2000_ coordinate system.

    .. _J2000: https://en.wikipedia.org/wiki/Earth-centered_inertial
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z






