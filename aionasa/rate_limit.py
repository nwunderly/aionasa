
import asyncio
import time
import logging

logger = logging.getLogger('aionasa.rate_limit')



class RateLimiter:
    """
    Class that handles rate limit across the whole library.
    This is necessary to ensure observation of rate limits even if multiple API endpoints are being used.
    """

    def __init__(self, limit):
        logger.debug("Initializing `RateLimiter`")
        self._requests = []
        self._limit = limit
        self._remaining = limit

    @property
    def remaining(self):
        logger.debug(f"`RateLimiter.remaining` property was accessed. Value: {self._remaining}")
        return self._remaining

    async def wait(self):
        logger.debug("`RateLimiter.wait()` was called.")
        if self._remaining < 1:
            timestamp = self._requests.pop(0)
            time_to_wait = 3600 - (time.monotonic() - timestamp)
            if time_to_wait > 0:
                logger.debug(f"Sleeping for {time_to_wait} seconds.")
                await asyncio.sleep(time_to_wait)
            else:
                logger.debug(f"Skipping sleep due to invalid sleep duration: {time_to_wait}")
        else:
            logger.debug(">0 requests remaining, sleep is not necessary.")

    async def update(self, remaining):
        logger.debug(f"Updating rate limit: {remaining} requests remaining.")
        self._remaining = remaining
        self._requests.append(time.monotonic())


default_rate_limiter = RateLimiter(1000)
insight_rate_limiter = RateLimiter(2000)
demo_rate_limiter = RateLimiter(30)  # todo: figure out how to implement daily limit


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
