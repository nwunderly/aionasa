import asyncio
from aionasa.donki import DONKI


async def test_method(func):
    print(await func())


async def main():
    async with DONKI() as client:
        await test_method(client.coronal_mass_ejections)
        await test_method(client.cme_analysis)
        await test_method(client.geomagnetic_storms)
        await test_method(client.interplanetary_shocks)
        await test_method(client.solar_flares)
        await test_method(client.solar_energetic_particles)
        await test_method(client.magnetopause_crossings)
        await test_method(client.radiation_belt_enhancements)
        await test_method(client.high_speed_streams)
        await test_method(client.wsa_enlil_sims)
        await test_method(client.notifications)


asyncio.run(main())
