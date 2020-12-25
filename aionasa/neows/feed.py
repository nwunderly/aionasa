from .data import Asteroid


class NeoWsFeedPage:
    """Class representing the paginated NEO API feed.
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
            self.near_earth_objects[date] = []
            for asteroid in asteroids:
                self.near_earth_objects[date].append(Asteroid(asteroid))

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
