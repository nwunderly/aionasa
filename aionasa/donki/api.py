import logging

from .data import *
from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter

logger = logging.getLogger('aionasa.donki')


# Documentation: https://ccmc.gsfc.nasa.gov/support/DONKI-webservices.php


def _from_list(cls, data):
    return [cls(i) for i in data]


class DONKI(BaseClient):
    """Client for NASA Space Weather Database of Notifications, Knowledge, Information (DONKI).

    ..note::
        The api.nasa.gov mirror is rate limited (like other api.nasa.gov APIs).
        The API at kauai.ccmc.gsfc.nasa.gov, however, is not, nor does it require an API key to use.
        These features will be ignored when using this API through kauai.ccmc.gsfc.nasa.gov.

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    """
    def __init__(self, use_nasa_mirror=False, api_key='DEMO_KEY', session=None, rate_limiter=default_rate_limiter):
        if use_nasa_mirror:
            if api_key == 'DEMO_KEY' and rate_limiter:
                rate_limiter = demo_rate_limiter
            self.base_url = 'https://api.nasa.gov/DONKI'
        else:
            api_key = None
            rate_limiter = None
            self.base_url = 'https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get'
        super().__init__(api_key, session, rate_limiter)

    async def _get_json(self, relative_url, query):
        url = self.base_url + relative_url

        def get_sep():
            return '&' if '?' in url else '?'

        if self._api_key:
            query['api_key'] = self._api_key

        for key, value in query.items():
            if value:
                url += get_sep() + f"{key}={value}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise APIException(resp.status, resp.reason)
            data = await resp.json()

        if self.rate_limiter:
            remaining = int(resp.headers['X-RateLimit-Remaining'])
            self.rate_limiter.update(remaining)

        return data

    async def _get_for_date_range(self, path, start_date, end_date):
        query = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
        }
        json = await self._get_json(path, query)
        return json

    async def coronal_mass_ejections(self, start_date=None, end_date=None):
        """Get information on coronal mass ejections for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[CME]`
        """
        json = await self._get_for_date_range('/CME', start_date, end_date)
        return _from_list(CME, json)

    async def cme_analysis(self, start_date=None, end_date=None, most_accurate_only=None, complete_entry_only=None, speed=None, half_angle=None, catalog=None, keyword=None):
        """Get coronal mass ejection analysis data.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.
        most_accurate_only: :class:`bool`
            Defaults to ``True``.
        complete_entry_only: :class:`bool`
            Defaults to ``True``.
        speed: :class:`Union[int, float]`
            Lower limit on speed of CME, in km/s. Defaults to 0.
        half_angle: :class:`Union[int, float]`
            Lower limit on half angular width, in degrees. Defaults to 0.
        catalog: :class:`str`
            Catalog to search. Defaults to ``ALL``.
            Options: ``ALL``, ``SWRC_CATALOG``, ``JANG_ET_AL_CATALOG``
        keyword: :class:`str`
            Keyword to search. Defaults to None

        Returns
        -------
        :class:`List[CMEAnalysis]`
        """
        query = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'most_accurate_only': most_accurate_only,
            'complete_entry_only': complete_entry_only,
            'speed': speed,
            'half_angle': half_angle,
            'catalog': catalog,
            'keyword': keyword,
        }

        json = await self._get_json('/CMEAnalysis', query)
        return _from_list(CMEAnalysis, json)

    async def geomagnetic_storms(self, start_date=None, end_date=None):
        """Get information on geomagnetic storms for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[GMS]`
        """
        json = await self._get_for_date_range('/GMS', start_date, end_date)
        return _from_list(GMS, json)

    async def interplanetary_shocks(self, start_date=None, end_date=None, location=None, catalog=None):
        """Get information on interplanetary shock events for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.
        location: :class:`str`
            Location to search. Defaults to ``ALL``.
            Options: ``Earth``, ``MESSENGER``, ``STEREO A``, ``STEREO B``
        catalog: :class:`str`
            Catalog to search. Defaults to ``ALL``.
            Options: ``ALL``, ``SWRC_CATALOG``, ``WINSLOW_MESSENGER_ICME_CATALOG``

        Returns
        -------
        :class:`List[IPS]`
        """
        query = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'location': location,
            'catalog': catalog,
        }

        json = await self._get_json('/IPS', query)
        return _from_list(IPS, json)

    async def solar_flares(self, start_date=None, end_date=None):
        """Get information on solar flare events for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[FLR]`
        """
        json = await self._get_for_date_range('/FLR', start_date, end_date)
        return _from_list(FLR, json)

    async def solar_energetic_particles(self, start_date=None, end_date=None):
        """Get information on solar energetic particle events for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[SEP]`
        """
        json = await self._get_for_date_range('/SEP', start_date, end_date)
        return _from_list(SEP, json)

    async def magnetopause_crossings(self, start_date=None, end_date=None):
        """Get information on magnetopause crossing events for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[MPC]`
        """
        json = await self._get_for_date_range('/MPC', start_date, end_date)
        return _from_list(MPC, json)

    async def radiation_belt_enhancements(self, start_date=None, end_date=None):
        """Get information on radiation belt enhancement events for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[RBE]`
        """
        json = await self._get_for_date_range('/RBE', start_date, end_date)
        return _from_list(RBE, json)

    async def high_speed_streams(self, start_date=None, end_date=None):
        """Get information on high speed stream events for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 30 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[HSS]`
        """
        json = await self._get_for_date_range('/HSS', start_date, end_date)
        return _from_list(HSS, json)

    async def wsa_enlil_sims(self, start_date=None, end_date=None):
        """Get information on WSA-Enlil simulations for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 7 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.

        Returns
        -------
        :class:`List[WSAEnlilSim]`
        """
        json = await self._get_for_date_range('/WSAEnlilSimulations', start_date, end_date)
        return _from_list(WSAEnlilSim, json)

    async def notifications(self, start_date=None, end_date=None, type=None):
        """Get DONKI notifications for a particular date range.

        Parameters
        ----------
        start_date: :class:`datetime.date`
            The first date to return data for. Defaults to 7 days prior to the current UTC date.
        end_date: :class:`datetime.date`
            The last date to return data for. Defaults to the current UTC date.
        type: :class:`str`
            The event type. Defaults to ``all``.
            Options: ``all``, ``FLR``, ``SEP``, ``CME``, ``IPS``, ``MPC``, ``GST``, ``RBE``, ``report``

        Returns
        -------
        :class:`List[Notification]`
        """
        query = {
            'start_date': start_date.strftime('%Y-%m-%d') if start_date else None,
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'type': type,
        }

        json = await self._get_json('/WSAEnlilSimulations', query)
        return _from_list(Notification, json)
