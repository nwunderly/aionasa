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


Python example - APOD
---------------------

This is a simple script that will return the title, explanation, and url from the most recent Astronomy Picture of the Day site,
then download and save the image.

.. code-block:: python

   import asyncio
   from aionasa import APOD

   async def main():
       async with APOD() as apod:
           apod_entry = await apod.get()
           print(f'{apod_entry.title}\n{apod_entry.explanation}\n{apod_entry.hdurl}')
           await apod_entry.save()

   asyncio.run(main())

CLI example - APOD
------------------

This command, like the above python script, will print data returned by the APOD API, then download and save the image.

.. code-block::

   python3 -m aionasa.apod --print --download .

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
