import datetime
import logging
from typing import List

from ..client import BaseClient
from ..errors import *
from ..rate_limit import default_rate_limiter, demo_rate_limiter
from .data import AstronomyPicture

logger = logging.getLogger("aionasa.apod")

WP_API_URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"
legacy_api_URL = "https://api.nasa.gov/planetary/apod"

NEW_POST_TIME_UTC = datetime.time(hour=4, minute=5, second=0)


class APOD(BaseClient):
    """Client for NASA Astronomy Picture of the Day API.

    Parameters
    ----------
    api_key: :class:`str`
        NASA API key to be used by the client.
    session: :class:`Optional[aiohttp.ClientSession]`
        Optional ClientSession to be used for requests made by this client. Creates a new session by default.
    rate_limiter: :class:`Optional[RateLimiter]`
        Optional RateLimiter class to be used by this client. Uses the library's internal global rate limiting by default.
    api_url: :class:`Optional[str]`
        Optional argument for manually setting the base API URL.
    legacy_api: :class:`bool`
        Optional argument, set this to True to use the legacy ``api.nasa.gov`` API.
        As of aionasa v0.2.2, this library defaults to the new Wordpress-based ``science.nasa.gov`` API.
    """

    def __init__(
        self, api_key="DEMO_KEY", session=None, rate_limiter=default_rate_limiter, api_url=WP_API_URL, legacy_api=False
    ):
        self.legacy_api = legacy_api
        self.api_url = api_url

        # if using new API, no rate limiter
        if not legacy_api:
            rate_limiter = None
            api_key = None

        # on legacy API with demo key, use demo rate limiter
        if legacy_api and api_key == "DEMO_KEY" and rate_limiter:
            rate_limiter = demo_rate_limiter

        # when legacy_api is True, select correct URL default
        if api_url == WP_API_URL and legacy_api:
            self.api_url = legacy_api_URL

        super().__init__(api_key, session, rate_limiter)

    async def get(self, date: datetime.date = None, as_json: bool = False):
        """Retrieves a single item from NASA's APOD API.

        Parameters
        ----------
        date: :class:`datetime.Date`
            The date of the APOD image to retrieve. Defaults to ``'today'``.
        as_json: :class:`bool`
            Bool indicating whether to return the raw returned json data instead of the normal AstronomyPicture object. Defaults to ``False``.

        Returns
        -------
        :class:`AstronomyPicture`
            An AstronomyPicture containing data returned by the API.
        """

        # legacy scraper API
        if self.legacy_api:
            if date is None:  # parameter will be left out of the query.
                date_fmt = ""
            else:
                date_fmt = "date=" + date.strftime("%Y-%m-%d") + "&"
            request = f"{self.api_url}?{date_fmt}api_key={self._api_key}"
    
        # new WP API
        else:
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            # new APOD at 04:05:00 UTC
            if now.time() > NEW_POST_TIME_UTC:
                # use current date if past post time
                date = now.date()
            else:
                # use yesterday's date otherwise (between 00:00:00 and 04:05:00 UTC)
                date = now.date() - datetime.timedelta(days=1)
            date_fmt = date.strftime("%y%m%d")
            request = f"{self.api_url}/{date_fmt}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers["X-RateLimit-Remaining"])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:
            date = json.get("date")
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date() if date else None

            entry = AstronomyPicture(client=self, date=date, json=json, legacy_api=self.legacy_api)
            return entry

    async def batch_get(
        self, start_date: datetime.date, end_date: datetime.date, as_json: bool = False
    ):
        """Retrieves multiple items from NASA's APOD API. Returns a list of APOD entries.

        Parameters
        ----------
        start_date: :class:`datetime.Date`
            The first date to return when requesting a range of dates.
        end_date: :class:`datetime.Date`
            The last date to return when requesting a range of dates. Range is inclusive.
        as_json: :class:`bool`
            Bool indicating whether to return a list of dicts containing the raw returned json data instead of the normal ``List[AstronomyPicture]``. Defaults to ``False``.

        Returns
        -------
        :class:`List[AstronomyPicture]`
            A list of AstronomyPicture objects containing data returned by the API.
        """

        # legacy scraper API
        if self.legacy_api:
            start_date = "start_date=" + start_date.strftime("%Y-%m-%d")
            end_date = "end_date=" + end_date.strftime("%Y-%m-%d")
            request = f"{self.api_url}?{start_date}&{end_date}&api_key={self._api_key}"

        # new WP API
        else:
            start_date = "date_from=" + start_date.strftime("%y%m%d")
            end_date = "date_to=" + end_date.strftime("%y%m%d")
            request = f"{self.api_url}?{start_date}&{end_date}"

        if self.rate_limiter:
            await self.rate_limiter.wait()

        async with self._session.get(request) as response:
            if response.status != 200:  # not success
                raise APIException(response.status, response.reason)

            json = await response.json()

        if self.rate_limiter:
            remaining = int(response.headers["X-RateLimit-Remaining"])
            self.rate_limiter.update(remaining)

        if as_json:
            return json

        else:
            result = []

            for item in json:

                date = item.get("date")
                date = (
                    datetime.datetime.strptime(date, "%Y-%m-%d").date()
                    if date
                    else None
                )

                entry = AstronomyPicture(client=self, date=date, json=json, legacy_api=self.legacy_api)
                result.append(entry)

            return result
