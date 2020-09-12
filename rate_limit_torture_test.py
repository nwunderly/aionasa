
import aiohttp
import asyncio
import logging
import datetime
import sys

from aionasa import APOD
from API_KEY import API_KEY


async def main():

    async with APOD(API_KEY) as apod:

        while True:

            await apod.get()

            print(apod.rate_limiter.remaining)

            await asyncio.sleep(.25)


asyncio.run(main())
