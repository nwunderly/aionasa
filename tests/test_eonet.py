import asyncio
from aionasa.eonet import EONET


async def test_method(func):
    print(await func())


async def main():
    async with EONET() as client:
        await test_method(client.magnitudes)
        await test_method(client.sources)
        await test_method(client.layers)
        await test_method(client.categories)
        await test_method(client.events)
        await test_method(client.events_geojson)


asyncio.run(main())
