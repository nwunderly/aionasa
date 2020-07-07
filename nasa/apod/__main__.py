from .client import APOD
import aiohttp
import asyncio


"""
TEST SCRIPT FOR APOD API WRAPPER
"""


async def main():
    apod = APOD()
    response = await apod.get()
    await apod.close()
    return response

if __name__ == "__main__":
    print(asyncio.run(main()))
