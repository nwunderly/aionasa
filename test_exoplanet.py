import asyncio

from aionasa.exoplanet import Exoplanet
from aionasa.exoplanet.query import *


async def main():
    async with Exoplanet() as exoplanet:
        try:
            a = await exoplanet.query('exoplanets', select='pl_hostname,ra,dec', where='ra > 45', order='dec', format=csv)
            try:
                iter(a)
                iterable = True
            except TypeError:
                iterable = False
            print("exoplanet.query success\n\t", type(a), len(a) if iterable else None)
        except Exception as e:
            print("exoplanet.query failed\n\t", e.__class__.__name__, e)
        try:
            b = await exoplanet.query_json('exoplanets', select='pl_hostname,ra,dec', where='ra > 45', order='dec')
            try:
                iter(b)
                iterable = True
            except TypeError:
                iterable = False
            print("exoplanet.query_json success\n\t", type(b), len(b) if iterable else None)
        except Exception as e:
            print("exoplanet.query_json failed\n\t", e.__class__.__name__, e)
        try:
            c = await exoplanet.query_alias_table('bet Pic')
            try:
                iter(c)
                iterable = True
            except TypeError:
                iterable = False
            print("exoplanet.query_alias_table success\n\t", type(c), len(c) if iterable else None)
        except Exception as e:
            print("exoplanet.query_alias_table failed\n\t", e.__class__.__name__, e)

        print("Done.")


asyncio.run(main())
