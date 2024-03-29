import argparse
import asyncio
import json

import aiohttp
import yaml

from ..errors import ArgumentError
from ..utils import date_strptime
from .api import APOD

__doc__ = """

CLI TOOL FOR APOD API WRAPPER

"""

VALID_FILE_TYPES = ["csv", "json", "yaml"]


parser = argparse.ArgumentParser(description="CLI tool for APOD API wrapper.")

parser.add_argument("--date", "-d", help="Request APOD data for a single date.")
parser.add_argument(
    "--start-date",
    "--from",
    help="The first date to return when requesting a range of dates.",
)
parser.add_argument(
    "--end-date",
    "--to",
    help="The last date to return when requesting a range of dates. Range is inclusive.",
)
parser.add_argument(
    "--since", help="Shorthand that selects date range up to the current date"
)
parser.add_argument(
    "--print",
    "-p",
    action="store_true",
    help="Flag indicating that data should be printed in a human-readable format In addition to other actions.",
)
parser.add_argument(
    "--dump",
    help="Indicates that data should be dumped to a file. Supports json and yaml/yml extensions.",
)
parser.add_argument(
    "--download",
    help="After data is retrieved, downloads images to the given directory.",
)
parser.add_argument(
    "--key", help="Manual input option for API key. If this is left out, uses DEMO_KEY."
)
parser.add_argument(
    "--timeout",
    type=int,
    help="Configures timeout settings for the underlying aiohttp.ClientSession. Overrides the 'total' attribute.",
)


def dump_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


def dump_to_csv(data, filename):
    with open(filename, "w") as f:
        if not isinstance(data, list):  # batch_get
            data = [data]
        for _dict in data:
            items = [str(value) for value in _dict.values()]
            f.write(",".join(items) + "\n")


def dump_to_yaml(data, filename):
    with open(filename, "w") as f:
        yaml.dump(data, f, yaml.Dumper)


async def get(day, _print, dump, download, key, timeout):
    day = date_strptime(day)
    if timeout is not None:
        timeout = aiohttp.ClientTimeout(total=timeout)
    else:
        timeout = aiohttp.ClientTimeout()

    session = aiohttp.ClientSession(timeout=timeout)

    async with APOD(key or "DEMO_KEY", session=session) as apod:
        picture = await apod.get(day)
        data = picture.json()

        if _print:
            s = ""
            for key, value in data.items():
                s += f"{key}: {value}\n"
            print(s)

        if dump:
            split = dump.split(".")
            ext = split[-1]

            if ext.lower() == "json":
                dump_to_json(data, dump)
            elif ext.lower() == "csv":
                dump_to_csv(data, dump)
            elif ext.lower() == "yaml":
                dump_to_yaml(data, dump)

        if download:
            await download_image(picture, download)


async def batch_get(start_date, end_date, _print, dump, download, key, timeout):
    start_date = date_strptime(start_date)
    end_date = date_strptime(end_date)
    if timeout is not None:
        timeout = aiohttp.ClientTimeout(total=timeout)
    else:
        timeout = aiohttp.ClientTimeout()

    session = aiohttp.ClientSession(timeout=timeout)

    async with APOD(key or "DEMO_KEY", session=session) as apod:
        data = await apod.batch_get(start_date, end_date)
        json_data = [picture.json() for picture in data]

        if _print:
            s = ""
            for entry in json_data:
                for key, value in entry.items():
                    s += f"{key}: {value}\n"
                s += "\n"
            print(s)

        if dump:
            split = dump.split(".")
            ext = split[-1]

            if ext.lower() == "json":
                dump_to_json(data, dump)
            elif ext.lower() == "csv":
                dump_to_csv(data, dump)
            elif ext.lower() in {"yaml", "yml"}:
                dump_to_yaml(data, dump)

        if download:
            await asyncio.gather(
                *[download_image(picture, download, True) for picture in data]
            )


async def download_image(picture, path, ignore_not_implemented=False):
    url = picture.hdurl if picture.hdurl else picture.url

    if url.startswith("http://apod.nasa.gov") or url.startswith(
        "https://apod.nasa.gov"
    ):
        filename = url.split("/")[-1]

    else:  # todo: add support for non-apod images (youtube etc)
        if ignore_not_implemented:
            print(f"Could not download url, skipping: {url}")
            return 0
        raise NotImplementedError(
            "URL not supported by download function. File could not be downloaded."
        )

    filepath = path + "/" + filename
    try:
        print(f"Starting download: {url}")
        b = await picture.save(filepath)
        print(f"Downloaded: {url} ({b/1000} KB)")
    except asyncio.TimeoutError:
        print(f"Download failed: {url}")
        raise


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
    timeout = args.timeout

    if _date:
        if start_date or end_date or since:
            raise ArgumentError(
                "date and start-date/end-date/since are not compatible arguments."
            )
        await get(_date, _print, dump, download, key, timeout)

    elif since:
        if start_date or end_date:
            raise ArgumentError(
                "since and start-date/end-date are not compatible arguments."
            )
        await batch_get(since, "today", _print, dump, download, key, timeout)

    elif start_date or end_date:
        if not (start_date and end_date):
            raise ArgumentError(
                "start-date and end-date are both required arguments when requesting a range."
            )
        await batch_get(start_date, end_date, _print, dump, download, key, timeout)

    else:
        await get("today", _print, dump, download, key, timeout)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
