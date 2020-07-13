
import asyncio
import json

from .insight_client import InSight


async def main():
    insight = InSight()
    data = await insight.get()
    print(json.dumps(data, sort_keys=True, indent=4))


if __name__ == '__main__':
    asyncio.run(main())

