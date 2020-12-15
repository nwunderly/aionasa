.. currentmodule:: aionasa.insight


Insight API Reference
=====================

This page provides a breakdown of the aionasa InSight (Mars Weather Data) module.

In-depth documentation for this API can be found at https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf

Parameters for InSight API:
- version: The version of this API. Locked to 1.0 currently.
- feedtype: The format of what is returned. Currently the default is JSON and only JSON works.


Client
------

.. autoclass:: InSight
    :members:


Example Code
------------

.. code-block:: python

    import asyncio
    import json
    from aionasa import InSight

    async def main():
        async with InSight() as insight:
            data = await insight.get()
        
        print(json.dumps(data, indent=2))
        
    asyncio.run(main())
