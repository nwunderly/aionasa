
import datetime

from ..errors import APIException, NASAException


class AstronomyPicture:
    """
    A class representing a single daily APOD picture.
    """
    def __init__(self, client, date: datetime.date, **kwargs):
        self.client = client
        self.date = date
        self.copyright = kwargs.get('copyright')
        self.title = kwargs.get('title')
        self.explanation = kwargs.get('explanation')
        self.url = kwargs.get('url')
        self.hdurl = kwargs.get('hdurl')
        self.media_type = kwargs.get('media_type')
        self.service_version = kwargs.get('service_version')

    def json(self):
        return {
            'date': self.date.strftime('%Y-%m-%d'),
            'copyright': self.copyright,
            'title': self.title,
            'explanation': self.explanation,
            'url': self.url,
            'hdurl': self.hdurl,
            'media_type': self.media_type,
            'service_version': self.service_version,
        }

    async def read(self, hdurl: bool = True) -> bytes:
        """
        Downloads the image associated with this AstronomyPicture.

        :param hdurl: Indicates that the HD image should be downloaded, if possible.
        :return: bytes object containing the image.
        """

        if hdurl and self.hdurl:
            url = self.hdurl
        else:
            url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        async with self.client._session.get(url) as response:
            if response.status != 200:
                raise APIException(f"{response.status} - {response.reason}")
            image = await response.read()

        return image

    async def save(self, path=None, hdurl: bool = True):
        """
        Downloads the image associated with this AstronomyPicture and saves to a file.

        :param path: The file path at which to save the image.
        :param hdurl: Indicates that the HD image should be downloaded, if possible.
        """

        if hdurl and self.hdurl:
            url = self.hdurl
        else:
            url = self.url

        path = path if path else f"./{url.split('/')[-1]}"

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        async with self.client._session.get(url) as response:
            if response.status != 200:
                raise APIException(f"{response.status} - {response.reason}")
            image = await response.read()

        with open(path, 'wb') as f:
            f.write(image)



