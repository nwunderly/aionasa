import argparse
import asyncio
import os

from .api import EPIC
from .gui import open_gui
from ..utils import date_strptime


__doc__ = "Download some images from NASA's EPIC archive and open them in a gui browser."
usage = "python -m aionasa.epic [-h] [--date DATE] [--collection COLLECTION] img_folder"


def argument_parser():
    """Generates the parser used by the aionasa.epic.__main__ script."""
    parser = argparse.ArgumentParser(description=__doc__, usage=usage)

    parser.add_argument(
        '--date', '-d', type=date_strptime, default=None,
        help="Format: YYYY-MM-DD"
    )
    parser.add_argument(
        '--collection', '-c', default='natural',
        help="Collection to get images from. Should be 'natural', 'enhanced', or 'natural,enhanced'"
    )
    parser.add_argument(
        'img_folder',
        help='Directory to download the images to.'
    )

    return parser


async def _task(coro, arg):
    """Safely execute an async function"""
    try:
        await coro(arg)
    except:
        pass


async def setup(date, path, collection):
    """Downloads all EPIC images in a collection to a directory given by the 'path' parameter."""
    # make image directory if necessary
    if not os.path.exists(path):
        os.mkdir(path)

    async with EPIC() as epic:
        # API request, gets images (urls etc)
        images = []
        if 'natural' in collection:
            images += await epic.natural_images(date)
        if 'enhanced' in collection:
            images += await epic.enhanced_images(date)

        # download the images asynchronously
        print('downloading', len(images), 'images.')
        tasks = [_task(image.save, path + '/' + image.filename) for image in images]
        await asyncio.gather(*tasks)


async def main():
    await setup(args.date, args.img_folder, args.collection.split(','))
    open_gui(args.img_folder)


if __name__ == '__main__':
    args = argument_parser().parse_args()
    asyncio.run(main())
