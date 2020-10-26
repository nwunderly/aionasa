import asyncio

from aionasa.epic import EPIC



async def main():

    async with EPIC() as epic:

        data = await epic.natural()
        print(data)



if __name__ == '__main__':
    asyncio.run(main())
