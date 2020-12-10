import argparse
import asyncio

from .api import EPIC
from ..utils import date_strptime


def argument_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--date', '-d', type=date_strptime)
    parser.add_argument('img_folder')

    return parser


async def setup(date, path):
    async with EPIC() as epic:
        images = await epic.natural_images(date)
        for image in images:
            await image.save(path + image.image)


async def main():
    args = argument_parser().parse_args()
    await setup(args.date, args.img_folder)
    # open_window(img_folder)



if __name__ == '__main__':
    asyncio.run(main())
