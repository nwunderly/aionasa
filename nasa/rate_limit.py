
import asyncio
import time


class RateLimiter:
    """
    Class that handles rate limit across the whole library.
    This is necessary to ensure observation of rate limits even if multiple API endpoints are being used.
    """

    def __init__(self):
        self._available_requests = 1000

    async def _restore(self):
        await asyncio.sleep(3600)
        self._available_requests += 1

    async def _wait(self):
        while self._available_requests < 1:
            await asyncio.sleep(10**-6)

    async def update(self):
        if self._available_requests < 1:
            await self._wait()
        else:
            self._available_requests -= 1
            asyncio.create_task(self._restore())


class RateLimiter2:
    def __init__(self):
        self._requests = []
        self._count = 0

    async def update(self):
        if self._count > 999:
            timestamp = self._requests.pop(0)
            await asyncio.sleep(time.monotonic() - timestamp)
            self._count -= 1
        else:
            self._requests.append(time.monotonic())
            self._count += 1




