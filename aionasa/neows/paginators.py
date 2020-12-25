from .data import Asteroid


class NeoWsFeedPage:
    """Class representing the paginated NEO API feed endpoint.
    Asteroids are sorted into a dict by date.

    Attributes
    ----------
    json: :class:`dict`
        JSON data returned by the API.
    element_count: :class:`int`
        Number of Asteroids on this page.
    """
    def __init__(self, client, json):
        self.json = json
        self._client = client
        self._session = client.session
        self._url_self = json['links']['self']
        self._url_prev = json['links']['prev']
        self._url_next = json['links']['next']
        self.element_count = json['element_count']

        self.near_earth_objects = {}
        for date, asteroids in json['near_earth_objects'].items():
            self.near_earth_objects[date] = Asteroid._from_list(asteroids)

    async def next(self):
        """Returns the next page in the feed.

        Returns
        -------
        :class:`NeoWsFeedPage`
            The next page in the feed.
        """
        json = await self._client._get(self._url_next)
        return NeoWsFeedPage(self._client, json)

    async def prev(self):
        """Returns the previous page in the feed.

        Returns
        -------
        :class:`NeoWsFeedPage`
            The previous page in the feed.
        """
        json = await self._client._get(self._url_prev)
        return NeoWsFeedPage(self._client, json)


class NeoWsBrowsePage:
    """Class representing the paginated NEO API browse endpoint.
    Asteroids are all in a single list, ``'near_earth_objects'``.

    Attributes
    ----------
    json: :class:`dict`
        JSON data returned by the API.
    page_number
        The page number of this page.
    page_size
        TODO
    page_count
        Total number of pages available through the API.
    element_count
        Number of Asteroids on this page.
    """
    def __init__(self, client, json):
        self.json = json
        self._client = client
        self._session = client.session
        self._url_self = json['links']['self']

        # one of these might be None (if it's the first or last page)
        self._url_prev = json['links'].get('prev')
        self._url_next = json['links'].get('next')

        self.page_number = json['page']['number']
        self.page_size = json['page']['size']
        self.page_count = json['page']['total_pages']
        self.element_count = json['page']['total_elements']
        self.near_earth_objects = Asteroid._from_list(json['near_earth_objects'])

    async def next(self):
        """Returns the next page in the browse feed.

        Returns
        -------
        :class:`NeoWsBrowsePage`
            The next page in the feed.
        """
        if not self._url_next:
            raise ValueError(f"Last page has no next page available. (Page {self.page_number})")
        json = await self._client._get(self._url_next)
        return NeoWsBrowsePage(self._client, json)

    async def prev(self):
        """Returns the previous page in the browse feed.

        Returns
        -------
        :class:`NeoWsBrowsePage`
            The previous page in the feed.
        """
        if not self._url_prev:
            raise ValueError(f"First page has no previous page available. (Page {self.page_number})")
        json = await self._client._get(self._url_prev)
        return NeoWsBrowsePage(self._client, json)
