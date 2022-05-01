import asyncio

from .api import InSight


async def main():
    async with InSight() as insight:
        data = await insight.get()
        print(data)
        # print(json.dumps(data, sort_keys=True, indent=4))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
