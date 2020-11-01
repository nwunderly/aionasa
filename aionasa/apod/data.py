
import datetime

from ..errors import APIException, NASAException


class AstronomyPicture:
    """A class representing a single daily APOD picture.

    Attributes
    ----------
    client: :class:`APOD`
        The APOD client that was used to retrieve this data.
    date: :class:`datetime.Date`
        The date this image was uploaded to APOD.
    copyright:
        The owner of this image, if it is not public domain.
    title:
        The APOD entry's title.
    explanation:
        The explanation for this image, written by astronomers, from this image's APOD page.
    url:
        The image url.
    hdurl:
        The HD image url, if available. Can be ``None``.
    html_url:
        The url of the APOD HTML page. This is the page a user would find this image on.
        This data is not provided by the API. This attribute has been added by the library for ease of use.
    media_type:
        The type of media. Will pretty much always be ``'image'``.
    service_version:
        The API service version. The API version is currently ``'v1'``.
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

        site_formatted_date = f"{str(date.year)[2:]}{date.month:02d}{date.day:02d}"
        self.html_url = f"https://apod.nasa.gov/apod/ap{site_formatted_date}.html"

    def json(self):
        """Convert this object to JSON format.

        Returns
        -------
        :class:`dict`
            The JSON data that was provided by the APOD API.
        """
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

    async def read(self, hdurl: bool = True):
        """Downloads the image associated with this AstronomyPicture.

        Parameters
        ----------
        hdurl: :class:`bool`
            Indicates that the HD image should be downloaded, if possible.

        Returns
        -------
        :class:`bytes`
            The image, downloaded from the URL provided by the API.
        """

        if hdurl and self.hdurl:
            url = self.hdurl
        else:
            url = self.url

        if not (url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov')):
            raise NotImplementedError("URLs from outside apod.nasa.gov are not currently supported.")

        async with self.client._session.get(url) as response:
            if response.status != 200:
                raise APIException(response.status, response.reason)
            image = await response.read()

        return image

    async def save(self, path=None, hdurl: bool = True):
        """Downloads the image associated with this AstronomyPicture and saves to a file.

        Parameters
        ----------
        path:
            The file path at which to save the image.
            If ``None``, saves the image to the working directory using the filename from the image url.
        hdurl: :class:`bool`
            Indicates that the HD image should be downloaded, if possible.
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
                raise APIException(response.status, response.reason)
            with open(path, 'wb') as f:
                bytes_written = 0
                while True:
                    chunk = await response.content.read(10)
                    bytes_written += len(chunk)
                    if not chunk:
                        break
                    f.write(chunk)

        return bytes_written





