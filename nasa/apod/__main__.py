from .client import APOD
import aiohttp
import asyncio
import argparse

from datetime import date, timedelta, datetime


"""
TEST SCRIPT FOR APOD API WRAPPER
"""


parser = argparse.ArgumentParser()

parser.add_argument('day')
parser.add_argument('--print', action='store_true')


def process_date(day):
    keywords = {
        'today': date.today(),
        'yesterday': date.today() - timedelta(days=1)
    }
    if day in keywords.keys():
        return keywords[day]

    dt = datetime.strptime(day, '%Y-%m-%d')
    return date(dt.year, dt.month, dt.day)


async def main(day, _print):
    day = process_date(day)

    apod = APOD()

    response = await apod.get(day, as_json=True)

    await apod.close()

    if _print:
        s = ""
        for key, value in response.items():
            s += f"{key}: {value}\n"
        print(s)

if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(main(args.day, args.print))
