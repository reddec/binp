Basic Integration Platform - BINP
=================================

.. image:: https://user-images.githubusercontent.com/6597086/107153224-4dc2d080-69a7-11eb-96d1-31c304fb821f.png

Provides a platform for automation with code-first approach,
with embedded batteries:

* Tracing (journals)
* Internal and user-defined API
* Ultra-light but rich mobile-first UI
* Embedded key-value storage

It is heavily inspired by node-red and aims to provide same
enjoyment during development but without mess of nodes and connections
for tasks a little bit more complicated than just hello world.

The platform also tries to be easy in deployment and maintaining.
Code could be stored in a SCM (ex: git) and persistent storage is just a single file that
could be backed up and restored trivially.

Because memory and CPU consumption relatively low a solution based on the platform
could be launched even on Raspberry Pi Zero with 512MB RAM.

Requires:

* python 3.8+


Installation
------------

``pip install binp uvicorn``


Sample usage
------------

Put your code to sample.py and run

``uvicorn --reload sample:binp.app``

- UI: http://localhost:8000
- Internal API: http://localhost:8000/internal/redoc

Hello world
^^^^^^^^^^^


.. code-block:: python

   from binp import BINP

   binp = BINP()


   @binp.action
   @binp.journal
   async def hello():
       """
       Print hello world in console
       """
       print("hello world")


Hello world with API
^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

   from binp import BINP

   binp = BINP()


   @binp.app.get("/hello")
   @binp.journal
   async def hello():
       """
       Return hello world
       """
       return {"message": "hello world"}


- Exposed API: http://localhost:8000/redoc

Try by Curl: ``curl http://127.0.0.1:8000/hello``

Real-world example: fetch currencies every day or manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Requires additional dependencies: ``pip install aiohttp aiocron``


.. code-block:: python

    from datetime import date
    from typing import Dict

    from aiocron import crontab
    from aiohttp import ClientSession
    from binp import BINP
    from pydantic import BaseModel

    binp = BINP()


    class Rates(BaseModel):
        base: str = 'USD'
        rates: Dict[str, float] = {}
        date: date


    @crontab('0 12 * * *')
    @binp.action
    @binp.journal
    async def currency_rates():
        """
        Fetch currency rates
        """
        # make basic HTTP API request
        async with ClientSession() as session:
            res = await session.get('https://api.exchangeratesapi.io/latest?base=USD')
            assert res.ok, f"result {res.status}"
            data = await res.json()
        # parse response data
        rates = Rates.parse_obj(data)
        # add record to journal about result
        await binp.journal.record('current exchange rates', base_currency='USD', rates=rates)
         # save rates to default namespace
        await binp.kv.save(rates)


.. toctree::
    :maxdepth: 2
    :caption: Contents:

    binp.rst
    journal.rst
    action.rst
    kv.rst
    utils.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

