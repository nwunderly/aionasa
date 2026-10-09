import asyncio
from aionasa.apod import APOD


async def main():
    print("=====LEGACY API=====")

    async with APOD(legacy_api=True) as apod:
        print(f"{apod._api_key=}")
        print(f"{apod._session=}")
        print(f"{apod.rate_limiter=}")
        print(f"{apod.api_url=}")
        print(f"{apod.legacy_api=}")

        astropic = await apod.get()
        print(astropic.json)
        print(f"{astropic.date=}")
        print(f"{astropic.copyright=}")
        print(f"{astropic.title=}")
        print(f"{astropic.explanation=}")
        print(f"{astropic.url=}")
        print(f"{astropic.hdurl=}")
        print(f"{astropic.media_type=}")
        print(f"{astropic.service_version=}")
        print(f"{astropic.html_url=}")

        await astropic.save()

    print("\n\n\n=====NEW API=====")

    async with APOD() as apod:
        print(f"{apod._api_key=}")
        print(f"{apod._session=}")
        print(f"{apod.rate_limiter=}")
        print(f"{apod.api_url=}")
        print(f"{apod.legacy_api=}")

        astropic = await apod.get()
        print(astropic.json)
        print(f"{astropic.date=}")
        print(f"{astropic.copyright=}")
        print(f"{astropic.title=}")
        print(f"{astropic.explanation=}")
        print(f"{astropic.url=}")
        print(f"{astropic.hdurl=}")
        print(f"{astropic.media_type=}")
        print(f"{astropic.service_version=}")
        print(f"{astropic.html_url=}")

        await astropic.save()

if __name__ == "__main__":
    asyncio.run(main())
