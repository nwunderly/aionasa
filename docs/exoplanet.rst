.. currentmodule:: aionasa.exoplanet


Exoplanet API Reference
=======================

This page provides a breakdown of the aionasa Exoplanet module.


Exoplanet API request structure:
--------------------------------

See the exoplanet API `documentation`_ for in-depth information about the REST API, including table schema and query syntax.

.. _documentation: https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html


- Base URL **(Required)**: ``https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI``
- Table to query **(Required)**: ``?table=exoplanets``
    - ``exoplanets``: Confirmed planets.
    - ``compositepars``: Composite planet data.
    - ``exomultpars``: Extended planet data.
    - ``aliastable``: Confirmed planet aliases.
    - ``microlensing``: Confirmed planets discovered using microlensing.
- Output format: ``&format=ascii``
- Other query information: *(see documentation)*


Client
------

.. autoclass:: Exoplanet
    :members:


Data Classes
------------

(TODO)
