.. currentmodule:: aionasa.neows


Asteroids-NeoWs API Reference
=============================

This page provides a breakdown of the aionasa Asteroids-NeoWs (Near Earth Object Web Service) module.

The NeoWs REST API has three endpoints:
- Feed: Retrieve a list of Asteroids based on their closest approach date to Earth.
    - ``GET https://api.nasa.gov/neo/rest/v1/feed``
- Lookup: Lookup a specific Asteroid based on its NASA JPL small body ID (`SPK-ID`_).
    - ``GET https://api.nasa.gov/neo/rest/v1/neo/``
- Browse: Browse the overall Asteroid data-set.
    - ``GET https://api.nasa.gov/neo/rest/v1/neo/browse``

.. _SPK-ID: https://ssd.jpl.nasa.gov/sbdb_query.cgi


.. note::
    In this context, "epoch" should generally refer to the J2000 epoch (January 2000).
    This is also the basis of the coordinate systems used by most of the NASA APIs (i.e. EPIC's coordinate data).


Client
------

.. autoclass:: NeoWs
    :members:


Data Classes
------------

.. autoclass:: Asteroid
    :members:

.. autoclass:: CloseApproach
    :members:

.. autoclass:: OrbitalData
    :members:


Data Paginators
---------------

.. autoclass:: NeoWsFeedPage
    :members:

.. autoclass:: NeoWsBrowsePage
    :members:
