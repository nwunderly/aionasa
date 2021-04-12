import json

from .client import BaseClient


BASE_URL = "https://eonet.sci.gsfc.nasa.gov/api/v3"


class EONET(BaseClient):
    """Client for NASA Earth Observatory Natural Event Tracker API.

    Parameters
    ----------
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.

    .. note::
        Requests to this API do not seem to be subject to api.nasa.gov rate limits.
    """
    def __init__(self, session=None):
        super().__init__(api_key=None, session=session, rate_limiter=None)

    async def _get(self, path, **query):
        url = BASE_URL + path + '?' + '&'.join([f'{key}={value}' for key, value in query.items() if value])

        async with self._session.get(url) as resp:
            _json = json.loads(await resp.read())

        return _json

    async def magnitudes(self):
        """Get a list of all the available event magnitudes in the EONET system."""
        return await self._get('/magnitudes')

    async def sources(self):
        """Get a list of all the available event sources in the EONET system."""
        return await self._get('/sources')

    async def layers(self):
        """Get a list of web service layers in the EONET system."""
        return await self._get('/layers')

    async def categories(self):
        """Get a list of all the available event categories in the EONET system."""
        return await self._get('/categories')

    async def events(self, source=None, status=None, limit=None, days=None, start_date=None, end_date=None, mag_id=None, mag_min=None, mag_max=None, bbox=None):
        """Get information on a list of events.

        Parameters
        ----------
        source: :class:`str`
            Filter the returned events by the source.
            Pass multiple sources in a list or tuple; this operates as a boolean OR.
        status: :class:`str`
            Sort by the events' status. Defaults to ``open``.
            Options: ``open``, ``closed``, ``all``
        limit: :class:`int`
            Limits the number of events returned.
        days: :class:`int`
            Limits the number of prior days from which events will be returned.
        start_date: :class:`datetime.date`
            Select a range of dates for the events to fall between (inclusive).
        end_date: :class:`datetime.date`
            Select a range of dates for the events to fall between (inclusive).
        mag_id: :class:`str`
            Filter the returned events by the magnitude ID.
        mag_min: :class:`int`
            Select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        mag_max: :class:`int`
            Select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        bbox: :class:`tuple`
            Filter using a bounding box for the event location.
            This should be a 4-element tuple of (min_lon, max_lat, max_lon, min_lat).
            These are the coordinates of the upper left hand corner, followed by the lower right hand corner.

        Returns
        -------
        :class:`dict`
            The JSON data returned by the API.
        """
        params = {
            'source': source,
            'status': status,
            'limit': limit,
            'days': days,
            'mag_id': mag_id,
            'mag_min': mag_min,
            'mag_max': mag_max,
        }
        if start_date:
            params['start_date'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            params['enddate'] = end_date.strftime('%Y-%m-%d')
        if bbox:
            params['bbox'] = ','.join(str(coord) for coord in bbox)

        return await self._get('/events', **params)

    async def events_geojson(self, source=None, status=None, limit=None, days=None, start_date=None, end_date=None, mag_id=None, mag_min=None, mag_max=None, bbox=None):
        """Get information on a list of events, compatible with the `GeoJSON <https://geojson.org/>`_ standard.

        Parameters
        ----------
        source: :class:`str`
            Filter the returned events by the source.
            Pass multiple sources in a list or tuple; this operates as a boolean OR.
        status: :class:`str`
            Sort by the events' status. Defaults to ``open``.
            Options: ``open``, ``closed``, ``all``
        limit: :class:`int`
            Limits the number of events returned.
        days: :class:`int`
            Limits the number of prior days from which events will be returned.
        start_date: :class:`datetime.date`
            Select a range of dates for the events to fall between (inclusive).
        end_date: :class:`datetime.date`
            Select a range of dates for the events to fall between (inclusive).
        mag_id: :class:`str`
            Filter the returned events by the magnitude ID.
        mag_min: :class:`int`
            Select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        mag_max: :class:`int`
            Select a ceiling, floor, or range of magnitude values for the events to fall between (inclusive).
        bbox: :class:`tuple`
            Filter using a bounding box for the event location.
            This should be a 4-element tuple of (min_lon, max_lat, max_lon, min_lat).
            These are the coordinates of the upper left hand corner, followed by the lower right hand corner.

        Returns
        -------
        :class:`dict`
            The JSON data returned by the API.
        """
        params = {
            'source': source,
            'status': status,
            'limit': limit,
            'days': days,
            'mag_id': mag_id,
            'mag_min': mag_min,
            'mag_max': mag_max,
        }
        if start_date:
            params['start_date'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            params['enddate'] = end_date.strftime('%Y-%m-%d')
        if bbox:
            params['bbox'] = ','.join(str(coord) for coord in bbox)

        return await self._get('/events/geojson', **params)
