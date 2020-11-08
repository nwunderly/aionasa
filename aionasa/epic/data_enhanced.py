
import datetime

from ..errors import *


class EarthImage:
    """A NASA EPIC image asset.

    """
    def __init__(self, client, json, collection):
        self.client = client
        self.json = json

        API_KEY = f'?API_KEY={self.client._API_KEY}' if self.client._API_KEY else ''

        yyyy, mm, dd = json['date'].split()[0].split('-')
        self.png_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/png/{json['image']}.png{API_KEY}"
        self.jpg_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/jpg/{json['image']}.jpg{API_KEY}"
        self.thumb_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/thumbs/{json['image']}.jpg{API_KEY}"

        # 'date': '2020-10-24 00:41:06'
        self.date = datetime.datetime.strptime(json['date'], '%Y-%m-%d %H:%M:%S')

        self.image = json['image']
        self.caption = json['caption']
        self.centroid_coordinates = json['centroid_coordinates']
        self.dscovr_j2000_position = json['dscovr_j2000_position']
        self.sun_j2000_position = json['sun_j2000_position']
        self.attitude_quaternions = json['attitude_quaternions']
        self.coords = json['coords']




