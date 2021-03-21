import asyncio
import datetime
from aionasa.donki.api import DONKI


async def main():

    async with DONKI() as client:
        cme = await client.coronal_mass_ejection()
        print(cme)

    async with DONKI(use_nasa_mirror=True) as client:
        cme = await client.coronal_mass_ejection(start_date=datetime.date.today() - datetime.timedelta(days=6), end_date=datetime.date.today() - datetime.timedelta(days=3))
        print(cme)


asyncio.run(main())
