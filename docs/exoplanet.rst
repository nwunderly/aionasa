.. currentmodule:: aionasa.exoplanet


Exoplanet API Reference
=======================

This page provides a breakdown of the aionasa Exoplanet module.


Exoplanet API request structure:
--------------------------------

See the exoplanet API `documentation`_ for in-depth information about the REST API, including table schema and query syntax.

.. _documentation: https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html


A basic query will generally be made up of a few common parts:

- Base URL **(Required)**: ``https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI``
- Table to query **(Required)**: ``?table=exoplanets``
    - ``exoplanets``: Confirmed planets.
    - ``compositepars``: Composite planet data.
    - ``exomultpars``: Extended planet data.
    - ``aliastable``: Confirmed planet aliases.
    - ``microlensing``: Confirmed planets discovered using microlensing.
    - Other tables: *(see documentation)*
- Output format: ``&format=ascii``
- Other query params: *(see documentation)*


:superscript:`TODO: write up documentation for full set of query params and tables.</sup>`


.. note::
    Optionally install the `pandas`_ package to be able to output API data as a pandas DataFrame.

.. _pandas: https://pandas.pydata.org/


Client
------

.. autoclass:: Exoplanet
    :members:


Example Code
------------

This is a sample query from the Exoplanet API documentation:

``https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=pl_hostname,ra,dec&order=dec&format=ascii``


With *curl*, this could be done using the command:

.. code-block:: sh

    curl "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=pl_hostname,ra,dec&order=dec&format=ascii"


With aionasa, it could be done using a python script:

.. code-block:: python

    import asyncio
    from aionasa import Exoplanet

    async def main():
        async with Exoplanet() as exoplanet:
            text = await exoplanet.query('exoplanets', select='pl_hostname,ra,dec', order='dec', format='ascii')
            print(text)

    if __name__ == "__main__":
        asyncio.run(main())
