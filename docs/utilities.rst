.. currentmodule:: aionasa


Utilities
=========

API shared by all modules.


BaseClient
----------

The client class all aionasa API clients inherit from.

.. autoclass:: BaseClient
    :members:


Asset
-----

Base class for an image asset at a URL.

.. autoclass:: Asset
    :members:


RateLimiter
-----------

Class used internally by aionasa API clients to follow NASA API rate limits.

.. autoclass:: RateLimiter
    :members:


Miscellaneous utilities
-----------------------

.. automodule:: .utils
    :members:
