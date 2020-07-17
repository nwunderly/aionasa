from .apod_client import APOD
import aiohttp
import asyncio
import argparse

import json
import yaml

from datetime import date, timedelta, datetime


__doc__ = """

CLI TOOL FOR APOD API WRAPPER

"""

VALID_FILE_TYPES = ['csv', 'json', 'yaml']



parser = argparse.ArgumentParser(description="CLI tool for APOD API wrapper.")

parser.add_argument('--date', '-d', help="Request APOD data for a single date.")
parser.add_argument('--start-date', '--from', help="The first date to return when requesting a range of dates.")
parser.add_argument('--end-date', '--to', help="The last date to return when requesting a range of dates. Range is inclusive.")
parser.add_argument('--since', help="Shorthand that selects date range up to the current date")
parser.add_argument('--print', '-p', action='store_true', help="Flag indicating that data should be printed in a human-readable format In addition to other actions.")
parser.add_argument('--dump', help="Indicates that data should be dumped to a file. Supports json and yaml/yml extensions.")
parser.add_argument('--download', help="After data is retrieved, downloads images to the given directory.")
parser.add_argument('--key', help="Manual input option for API key. If this is left out, uses DEMO_KEY.")


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


async def get(day, _print, dump, download, key):
    day = process_date(day)

    async with APOD(key if key else 'DEMO_KEY') as apod:
        response = await apod.get(day, as_json=True)

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

    if download:
        async with aiohttp.ClientSession() as session:
            url = response.get('hdurl')
            url = url if url else response['url']

            if url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov'):
                filename = url.split('/')[-1]

            else:  # todo: add support for non-apod images (youtube etc)
                raise Exception("URL not supported by download function. File could not be downloaded.")

            async with session.get(url) as image_response:
                image = await image_response.read()

            filepath = download + '/' + filename
            with open(filepath, 'wb') as f:
                f.write(image)


async def batch_get(start_date, end_date, _print, dump, download, key):
    start_date = process_date(start_date)
    end_date = process_date(end_date)

    apod = APOD(key if key else 'DEMO_KEY')

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

    if download:  # todo: fucking clean this up
        async with aiohttp.ClientSession() as session:
            for entry in response:
                url = entry.get('hdurl')
                url = url if url else entry['url']

                # do this with regex later
                if url.startswith('http://apod.nasa.gov') or url.startswith('https://apod.nasa.gov'):
                    filename = url.split('/')[-1]

                else:  # todo: add support for non-apod images (youtube etc)
                    continue

                async with session.get(url) as image_response:
                    image = await image_response.read()

                filepath = download + '/' + filename
                with open(filepath, 'wb') as f:
                    f.write(image)



async def main():
    args = parser.parse_args()
    _date = args.date
    start_date = args.start_date
    end_date = args.end_date
    since = args.since
    _print = args.print
    dump = args.dump
    download = args.download
    key = args.key

    if _date:
        if start_date or end_date or since:
            raise argparse.ArgumentError("date and start-date/end-date/since are not compatible arguments.")
        await get(_date, _print, dump, download, key)

    elif since:
        if start_date or end_date:
            raise argparse.ArgumentError("since and start-date/end-date are not compatible arguments.")
        await batch_get(since, 'today', _print, dump, download, key)

    elif start_date or end_date:
        if not (start_date and end_date):
            raise argparse.ArgumentError("start-date and end-date are both required arguments when requesting a range.")
        await batch_get(start_date, end_date, _print, dump, download, key)

    else:
        await get('today', _print, dump, download, key)



if __name__ == "__main__":
    asyncio.run(main())
