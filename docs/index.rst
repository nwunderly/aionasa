.. aionasa documentation master file, created by
   sphinx-quickstart on Mon Sep 28 00:36:36 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aionasa's documentation!
===================================

aionasa is an async python wrapper for the NASA Open APIs.


Contents
--------

.. toctree::
   :maxdepth: 2

   apod
   insight


Installing
----------

aionasa can be installed from pypi with the command:

.. code-block:: sh

   # Linux
   python3 -m pip install -U aionasa

   # Windows
   python -m pip install -U aionasa


To install the development version of the library directly from source:

.. code-block:: sh

   $ git clone https://github.com/nwunderly/aionasa
   $ cd aionasa
   $ python3 -m pip install -U .


Quickstart
-----------

We'll be using IPython because it supports `await` expressions directly from the console.

.. code-block:: sh

   $ pip install aionasa ipython
   $ ipython

.. code-block:: python

   from aionasa import APOD, InSight

   async with APOD() as apod:
       picture = await apod.get()

   picture.url # this will be the most recent APOD image URL.

   async with InSight() as insight:
       data = await insight.get()

   data # this will be a dict containing the JSON data returned by the API.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
