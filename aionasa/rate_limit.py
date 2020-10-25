
import asyncio
import time
import logging

from collections import deque

logger = logging.getLogger('aionasa.rate_limit')



class RateLimiter:
    """
    Class that handles rate limit across the whole library.
    This is necessary to ensure observation of rate limits even if multiple API endpoints are being used.
    """

    def __init__(self, limit, _repr=None):
        logger.debug("Initializing `RateLimiter`")
        self._requests = deque(iterable=[time.monotonic()]*limit, maxlen=limit)
        self._limit = limit
        self._remaining = limit
        self._repr = _repr or f'<{self.__class__}>'

    @property
    def remaining(self):
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
                logger.debug(f"Skipping sleep due to invalid sleep duration: {time_to_wait}")
        else:
            logger.debug(">0 requests remaining, sleep is not necessary.")

    def update(self, remaining):
        logger.debug(f"Updating rate limit: {remaining} requests remaining.")
        self._remaining = remaining
        self._requests.append(time.monotonic())

    def __repr__(self):
        return self._repr


default_rate_limiter = RateLimiter(1000, '<default_rate_limiter>')
# default_rate_limiter.__repr__ = lambda: '<default_rate_limiter>'
insight_rate_limiter = RateLimiter(2000)
# insight_rate_limiter.__repr__ = lambda: '<insight_rate_limiter>'
demo_rate_limiter = RateLimiter(30)  # todo: figure out how to implement daily limit
# demo_rate_limiter.__repr__ = lambda: '<demo_rate_limiter>'


# class RateLimiter:
#     def __init__(self):
#         self._available_requests = 1000
#
#     async def _restore(self):
#         await asyncio.sleep(3600)
#         self._available_requests += 1
#
#     async def _wait(self):
#         while self._available_requests < 1:
#             await asyncio.sleep(10**-6)
#
#     async def update(self):
#         if self._available_requests < 1:
#             await self._wait()
#         else:
#             self._available_requests -= 1
#             asyncio.create_task(self._restore())


# class RateLimiter2:
#     def __init__(self):
#         self._requests = []
#         self._count = 0
#
#     async def update(self):
#         if self._count > 999:
#             timestamp = self._requests.pop(0)
#             await asyncio.sleep(time.monotonic() - timestamp)
#             self._count -= 1
#         else:
#             self._requests.append(time.monotonic())
#             self._count += 1
