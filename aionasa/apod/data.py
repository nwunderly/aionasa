
import datetime

from ..asset import Asset
from ..errors import APIException, NASAException


class AstronomyPicture(Asset):
    """A class representing a single daily APOD picture.

    Attributes
    ----------
    client: :class:`APOD`
        The APOD client that was used to retrieve this data.
    date: :class:`datetime.Date`
        The date this image was uploaded to APOD.
    json: :class:`dict`
        The JSON data that was provided by the API.
    copyright:
        The owner of this image, if it is not public domain.
    title:
        The APOD entry's title.
    explanation:
        The explanation for this image, written by astronomers, from this image's APOD page.
    html_url:
        The url of the APOD HTML page. This is the page a user would find this image on.
        This data is not provided by the API. This attribute has been added by the library for ease of use.
    media_type:
        The type of media. Will pretty much always be ``'image'``.
    service_version:
        The API service version. The API version is currently ``'v1'``.
    """
    def __init__(self, client, date: datetime.date, json):
        self.client = client
        self.date = date
        self.json = json
        self.copyright = json.get('copyright')
        self.title = json.get('title')
        self.explanation = json.get('explanation')
        self._url = json.get('url')
        self._hdurl = json.get('hdurl')
        self.media_type = json.get('media_type')
        self.service_version = json.get('service_version')

        site_formatted_date = f"{str(date.year)[2:]}{date.month:02d}{date.day:02d}"
        self.html_url = f"https://apod.nasa.gov/apod/ap{site_formatted_date}.html"

        self._response = None

    @property
    def url(self):
        """The image url.
        """
        return self._hdurl or self._url

    async def read(self):
        """Downloads the image associated with this AstronomyPicture.
        Will download the HD URL, if possible.

        Returns
        -------
        :class:`bytes`
            The image, downloaded from the URL provided by the API.
        """
        url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        return await super().read(url)

    async def save(self, path=None):
        """Downloads the image associated with this AstronomyPicture and saves to a file.
        Will download the HD URL, if possible.

        Parameters
        ----------
        path:
            The file path at which to save the image.
            If ``None``, saves the image to the working directory using the filename from the image url.
        """
        url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        return await super().save(path=path, url=url)

    # def stream(self, hdurl: bool = True):
    #     if hdurl and self.hdurl:
    #         url = self.hdurl
    #     else:
    #         url = self.url
    #
    #     if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
    #         raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")
    #
    #     return _StreamReader(self, self.client._session.get(url))


    async def read_chunk(self, chunk_size: int, hdurl: bool = True):
        """Reads a chunk of the image associated with this AstronomyPicture.

        Parameters
        ----------
        chunk_size: :class:`int`
            Number of bytes to read.
        hdurl: :class:`bool`
            Indicates that the HD image should be downloaded, if possible.

        Returns
        -------
        :class:`bytes`
            The chunked data. Will be None if the image has been completely read.
        """
        url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        if not self._response:
            response = await self.client._session.get(url)
            if response.status != 200:
                await response.close()
                raise APIException(response.status, response.reason)
            self._response = response

        chunk = await self._response.content.read(chunk_size)
        if not chunk:
            await self._response.close()
            self._response = None
        return chunk


# class _StreamReader:
#     def __init__(self, picture, response):
#         self.picture = picture
#         self.response = response
#
#     async def __aenter__(self):
#         await self.response.__aenter__()
#         if self.response.status != 200:
#             raise APIException(self.response.status, self.response.reason)
#         return self
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         return await self.response.__aexit__(exc_type, exc_val, exc_tb)
#
#     async def read(self, num):
