import datetime
from collections import namedtuple

from ..asset import Asset
from ..errors import *


class EarthImage(Asset):
    """A NASA EPIC image asset.

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
        self.sun_j2000_position = J2000Coordinates(**json['sun_j2000_position'])
        self.attitude_quaternions = Attitude(**json['attitude_quaternions'])
        # self.coords = json['coords']

        super().__init__(client, self.png_url, json['image'] + '.png')

    async def read(self, filetype='png'):
        url = {'png': self.png_url,
               'jpg': self.jpg_url,
               'thumb': self.thumb_url}.get(filetype)

        if not url:
            raise ArgumentError("Invalid file type. Expected 'png', 'jpg', or 'thumb'.")

        await super().read(url)

    async def save(self, path=None, filetype='png'):
        url = {'png': self.png_url,
               'jpg': self.jpg_url,
               'thumb': self.thumb_url}.get(filetype)

        if not url:
            raise ArgumentError("Invalid file type. Expected 'png', 'jpg', or 'thumb'.")

        await super().save(path, url)

    async def read_png(self):
        await self.read('png')

    async def save_png(self, path=None):
        await self.save(path, 'png')

    async def read_jpg(self):
        await self.read('jpg')

    async def save_jpg(self, path=None):
        await self.save(path, 'jpg')

    async def read_thumb(self):
        await self.read('thumb')

    async def save_thumb(self, path=None):
        await self.save(path, 'thumb')


# class J2000Coordinates:
#     """Coordinates of an object according to the J2000_ coordinate system.
#
#     .. _J2000: https://en.wikipedia.org/wiki/Earth-centered_inertial
#     """
#     def __init__(self, x, y, z):
#         self.x = x
#         self.y = y
#         self.z = z


J2000Coordinates = namedtuple('J2000Coordinates', ['x', 'y', 'z'])
Attitude = namedtuple('Attitude', ['q0', 'q1', 'q2', 'q3'])
EarthCoordinates = namedtuple('EarthCoordinates', ['lat', 'lon'])
