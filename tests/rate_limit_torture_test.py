import asyncio
import datetime

from aionasa import APOD
from aionasa.rate_limit import RateLimiter
from API_KEY import API_KEY


async def main():

    async with APOD(API_KEY, rate_limiter=RateLimiter(2000)) as apod:

        while True:

            await apod.get(date=datetime.date.today()-datetime.timedelta(days=1))

            print("remaining:", apod.rate_limiter.remaining)
            print("requests:", len(apod.rate_limiter._requests))

            await asyncio.sleep(.25)


asyncio.run(main())
