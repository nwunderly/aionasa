import os
import argparse
import asyncio

from .api import EPIC
from ..utils import date_strptime
from .img_viewer import open_gui


def argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--date', '-d', type=date_strptime, default=None)
    parser.add_argument('--collection', '-c', default='natural')
    parser.add_argument('img_folder')

    return parser


async def setup(date, path, collection):
    if not os.path.exists(path):
        os.mkdir(path)
    async with EPIC() as epic:
        images = []
        if 'natural' in collection:
            images += await epic.natural_images(date)
        if 'enhanced' in collection:
            images += await epic.enhanced_images(date)
        print('downloading', len(images), 'images.')
        for image in images:
            await image.save(path + '/' + image.filename)


async def main():
    args = argument_parser().parse_args()
    await setup(args.date, args.img_folder, args.collection.split(','))
    open_gui(args.img_folder)



if __name__ == '__main__':
    asyncio.run(main())
