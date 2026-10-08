import asyncio
import logging
import time
from collections import deque

logger = logging.getLogger("aionasa.rate_limit")


class RateLimiter:
    """Class that handles rate limit across the whole library.
    This is necessary to ensure observation of rate limits even if multiple API endpoints are being used.
    """

    def __init__(self, limit, _repr=None):
        logger.debug("Initializing `RateLimiter`")
        self._requests = deque(iterable=[time.monotonic()] * limit, maxlen=limit)
        self._limit = limit
        self._remaining = limit
        self._repr = _repr or f'<{self.__qualname__}>'

    @property
    def remaining(self):
        """:class:`int`: The number of requests remaining.
        Starts at the total request count specified on initialization and updates on each API request.
        """
        return self._remaining

    async def wait(self):
        logger.debug("`RateLimiter.wait()` was called.")
        if self._remaining < 1:
            timestamp = self._requests.popleft()
            time_to_wait = 3600 - (time.monotonic() - timestamp)
            if time_to_wait > 0:
                logger.debug(f"Sleeping for {time_to_wait} seconds.")
                await asyncio.sleep(time_to_wait)
            else:
                logger.debug(
                    f"Skipping sleep due to invalid sleep duration: {time_to_wait}"
                )
        else:
            logger.debug(">0 requests remaining, sleep is not necessary.")

    def update(self, remaining):
        logger.debug(f"Updating rate limit: {remaining} requests remaining.")
        self._remaining = remaining
        self._requests.append(time.monotonic())

    def __repr__(self):
        return self._repr


default_rate_limiter = RateLimiter(1000, "<default_rate_limiter>")
insight_rate_limiter = RateLimiter(2000, "<insight_rate_limiter>")
demo_rate_limiter = RateLimiter(30)  # todo: figure out how to implement daily limit
