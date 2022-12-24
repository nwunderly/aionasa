import datetime
from collections import namedtuple

from ..asset import Asset
from ..errors import ArgumentError


class EarthImage(Asset):
    """A NASA EPIC image asset. Accessible as a full-resolution PNG, half-resolution JPG,
    or a thumbnail JPG image.

    Attributes
    ----------
    client: :class:`EPIC`
        The EPIC client that was used to retrieve this data.
    json: :class:`dict`
        The JSON data returned by the API.
    png_url:
        The URL of the full-resolution PNG image.
    jpg_url:
        The URL of the half-resolution JPEG image.
    thumb_url:
        The URL of the thumbnail-size JPEG image.
    date: :class:`datetime.Date`
        The date this image was taken.
    caption:
        The caption for this image.
    image:
        The image name.
    centroid_coordinates: :class:`EarthCoordinates`
        Geographical coordinates that the satellite is looking at as a named tuple.
    dscovr_j2000_position: :class:`J2000Coordinates`
        Position of the satellite in space as a named tuple.
    lunar_j2000_position: :class:`J2000Coordinates`
        Position of the moon in space as a named tuple.
    sun_j2000_position: :class:`J2000Coordinates`
        Position of the sun in space as a named tuple.
    attitude_quaternions: :class:`Attitude`
        Satellite attitude as a named tuple.
    """

    def __init__(self, client, json, collection):
        self.json = json
        self.client = client

        api_key = f"?api_key={self.client._api_key}" if self.client._api_key else ""

        yyyy, mm, dd = json["date"].split()[0].split("-")
        self.png_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/png/{json['image']}.png{api_key}"
        self.jpg_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/jpg/{json['image']}.jpg{api_key}"
        self.thumb_url = f"{self.client.base_url}/archive/{collection}/{yyyy}/{mm}/{dd}/thumbs/{json['image']}.jpg{api_key}"

        # 'date': '2020-10-24 00:41:06'
        self.date = datetime.datetime.strptime(json["date"], "%Y-%m-%d %H:%M:%S")

        self.identifier = json["identifier"]
        self.image = json["image"]
        self.caption = json["caption"]
        self.centroid_coordinates = EarthCoordinates(**json["centroid_coordinates"])
        self.dscovr_j2000_position = J2000Coordinates(**json["dscovr_j2000_position"])
        self.lunar_j2000_position = J2000Coordinates(**json["lunar_j2000_position"])
        self.sun_j2000_position = J2000Coordinates(**json["sun_j2000_position"])
        self.attitude_quaternions = Attitude(**json["attitude_quaternions"])
        # self.coords = json['coords']

        super().__init__(client, self.png_url, json["image"] + ".png")

    async def read(self, filetype="png"):
        url = {"png": self.png_url, "jpg": self.jpg_url, "thumb": self.thumb_url}.get(
            filetype
        )

        if not url:
            raise ArgumentError("Invalid file type. Expected 'png', 'jpg', or 'thumb'.")

        await super().read(url)

    async def save(self, path=None, filetype="png"):
        url = {"png": self.png_url, "jpg": self.jpg_url, "thumb": self.thumb_url}.get(
            filetype
        )

        if not url:
            raise ArgumentError("Invalid file type. Expected 'png', 'jpg', or 'thumb'.")

        await super().save(path, url)

    async def read_png(self):
        await self.read("png")

    async def save_png(self, path=None):
        await self.save(path, "png")

    async def read_jpg(self):
        await self.read("jpg")

    async def save_jpg(self, path=None):
        await self.save(path, "jpg")

    async def read_thumb(self):
        await self.read("thumb")

    async def save_thumb(self, path=None):
        await self.save(path, "thumb")


J2000Coordinates = namedtuple("J2000Coordinates", ["x", "y", "z"])

Attitude = namedtuple("Attitude", ["q0", "q1", "q2", "q3"])

EarthCoordinates = namedtuple("EarthCoordinates", ["lat", "lon"])
