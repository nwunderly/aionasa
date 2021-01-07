from .api import Exoplanet


async def _test_method(ref, name, *args, **kwargs):
    try:
        result = await ref(*args, **kwargs)
        try:
            iter(result)
            iterable = True
        except TypeError:
            iterable = False
        print(f"exoplanet.{name} success\n\t", type(result), len(result) if iterable else None)
        # print(result)
    except Exception as e:
        print(f"exoplanet.{name} failed\n\t", e.__class__.__name__, e)


async def _run_tests():
    async with Exoplanet() as exoplanet:

        select = 'pl_hostname,ra,dec'
        where = 'ra>45'

        await _test_method(exoplanet.query, 'query', 'exoplanets', select=select, where=where, order='dec', format='ascii')
        await _test_method(exoplanet.query_json, 'query_json', 'exoplanets', select=select, where=where, order='dec')
        await _test_method(exoplanet.query_df, 'query_df', 'exoplanets', select=select, where=where, order='dec')

        await _test_method(exoplanet.query_aliastable, 'query_aliastable', 'bet Pic')
        await _test_method(exoplanet.query_aliastable_json, 'query_aliastable_json', 'bet Pic')
        await _test_method(exoplanet.query_aliastable_df, 'query_aliastable_df', 'bet Pic')

        print("Done.")
