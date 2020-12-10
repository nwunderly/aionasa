import argparse
import asyncio
import os

from .api import EPIC
from .img_viewer import open_gui
from ..utils import date_strptime

"""
USAGE:
    [arg] - optional
    (arg) - required

python -m aionasa.epic [--date DATE] [--collection COLLECTION] (IMG_FOLDER)
    DATE:           YYYY-MM-DD
    COLLECTION:     natural | enhanced | natural,enhanced
    IMG_FOLDER:     (directory to download images to)
"""


def argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--date', '-d', type=date_strptime, default=None)
    parser.add_argument('--collection', '-c', default='natural')
    parser.add_argument('img_folder')

    return parser


async def _task(coro, arg):
    """Safely execute an async function"""
    try:
        await coro(arg)
    except:
        pass


async def setup(date, path, collection):
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
        await asyncio.gather([_task(image.save, path + '/' + image.filename) for image in images])


async def main():
    args = argument_parser().parse_args()
    await setup(args.date, args.img_folder, args.collection.split(','))
    open_gui(args.img_folder)


if __name__ == '__main__':
    asyncio.run(main())
