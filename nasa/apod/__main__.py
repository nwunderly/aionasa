from .apod_client import APOD
import aiohttp
import asyncio
import argparse

import json
import yaml

from datetime import date, timedelta, datetime


"""
TEST SCRIPT FOR APOD API WRAPPER
"""

VALID_FILE_TYPES = ['csv', 'json', 'yaml']



parser = argparse.ArgumentParser()

parser.add_argument('--date', '-d')
parser.add_argument('--start-date', '-start')
parser.add_argument('--end-date', '-end')
parser.add_argument('--print', '-p', action='store_true')
parser.add_argument('--dump', '-D')


def process_date(day):
    keywords = {
        'today': date.today(),
        'yesterday': date.today() - timedelta(days=1)
    }
    if day in keywords.keys():
        return keywords[day]

    dt = datetime.strptime(day, '%Y-%m-%d')
    return date(dt.year, dt.month, dt.day)


def dump_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


def dump_to_csv(data, filename):
    with open(filename, 'w') as f:
        if not isinstance(data, list):  # batch_get
            data = [data]
        for _dict in data:
            items = [str(value) for value in _dict.values()]
            f.write(','.join(items) + '\n')


def dump_to_yaml(data, filename):
    with open(filename, 'w') as f:
        yaml.dump(data, f, yaml.Dumper)


async def get(day, _print, dump):
    day = process_date(day)

    apod = APOD()

    response = await apod.get(day, as_json=True)

    await apod.close()

    if _print:
        s = ""
        for key, value in response.items():
            s += f"{key}: {value}\n"
        print(s)

    if dump:
        split = dump.split('.')
        ext = split[-1]

        if ext.lower() == 'json':
            dump_to_json(response, dump)
        elif ext.lower() == 'csv':
            dump_to_csv(response, dump)
        elif ext.lower() == 'yaml':
            dump_to_yaml(response, dump)


async def batch_get(start_date, end_date, _print, dump):
    start_date = process_date(start_date)
    end_date = process_date(end_date)

    apod = APOD()

    response = await apod.batch_get(start_date, end_date, as_json=True)

    await apod.close()

    if _print:
        s = ""
        for entry in response:
            for key, value in entry.items():
                s += f"{key}: {value}\n"
            s += "\n"
        print(s)

    if dump:
        split = dump.split('.')
        ext = split[-1]

        if ext.lower() == 'json':
            dump_to_json(response, dump)
        elif ext.lower() == 'csv':
            dump_to_csv(response, dump)
        elif ext.lower() in {'yaml', 'yml'}:
            dump_to_yaml(response, dump)



async def main():
    args = parser.parse_args()
    _date = args.date
    start_date = args.start_date
    end_date = args.end_date
    _print = args.print
    dump = args.dump

    if _date:
        if start_date or end_date:
            raise argparse.ArgumentError("date and start-date/end-date are not compatible arguments.")
        await get(_date, _print, dump)

    elif start_date or end_date:
        if not (start_date and end_date):
            raise argparse.ArgumentError("start-date and end-date are both required arguments when requesting a range.")
        await batch_get(start_date, end_date, _print, dump)

    else:
        await get('today', _print, dump)



if __name__ == "__main__":
    asyncio.run(main())
