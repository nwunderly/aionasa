import argparse
import asyncio

from .api import EPIC
from ..utils import date_strptime


async def listing_subcommand(args):
    raise NotImplementedError


async def metadata_subcommand(args):
    raise NotImplementedError


async def gui_subcommand(args):
    raise NotImplementedError


def argument_parser():
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers()

    listing = subcommands.add_parser('listing')
    listing.add_argument('--print', action='store_true')
    listing.add_argument('--dump')
    listing.set_defaults(subcommand='listing', func=listing_subcommand)

    metadata = subcommands.add_parser('metadata')
    metadata.add_argument('date', type=date_strptime)
    metadata.set_defaults(subcommand='metadata', func=metadata_subcommand)

    gui = subcommands.add_parser('gui')
    gui.set_defaults(subcommand='gui', gui=gui_subcommand)

    return parser


async def main():
    args = argument_parser().parse_args()
    await args.func(args)


if __name__ == '__main__':
    asyncio.run(main())
