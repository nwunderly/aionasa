from .errors import *


class Asset:
    """Generic class representing a file asset URL."""

    def __init__(self, client, url, filename):
        self.client = client
        self._url = url
        self.filename = filename
        self._response = None

    def __str__(self):
        return f"{self.__class__.__name__}({self.filename})"

    async def read(self, url=None):
        """Downloads the file associated with this Asset.

        Parameters
        ----------
        url: :class:`str`
            The URL to download the asset from, for subclasses with multiple options.

        Returns
        -------
        :class:`bytes`
            The file, downloaded from the URL.
        """
        if not url:
            url = self._url

        async with self.client._session.get(url) as response:
            if response.status != 200:
                raise APIException(response.status, response.reason)
            image = await response.read()

        return image

    async def save(self, path=None, url=None):
        """Downloads the file associated with this Asset and saves to the requested path.

        Parameters
        ----------
        url: :class:`str`
            The URL to download the asset from, for subclasses with multiple options.
        path:
            The file path at which to save the file.
            If ``None``, saves the image to the working directory using the filename from the asset url.
        """
        if not url:
            url = self._url

        path = path if path else f"./{url.split('/')[-1]}"

        async with self.client._session.get(url) as response:
            if response.status != 200:
                raise APIException(response.status, response.reason)
            with open(path, "wb") as f:
                bytes_written = 0
                while True:
                    chunk = await response.content.read(1000)
                    bytes_written += len(chunk)
                    if not chunk:
                        break
                    f.write(chunk)

        return bytes_written

    async def read_chunk(self, chunk_size: int, url=None):
        if not url:
            url = self._url

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
