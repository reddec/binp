from asyncio import sleep
from random import randint

from binp import BINP

binp = BINP()


@binp.app.post('/random', response_model=int)
@binp.journal
async def generate_random():
    """
    Generate random number in range 0 ... 1024
    """
    return randint(0, 1024)


@binp.action
@binp.journal
async def currency_rate():
    """
    Fetch currency rate for EUR -> USD
    """
    # go to external service
    euro = 1.3
    await sleep(3)  # emulate request
    await binp.journal.record('rates fetched', base_currency='USD', euro=euro)


@binp.action
@binp.journal
async def always_fail():
    """
    This operation should always fail
    """
    await sleep(3)  # emulate request
    raise RuntimeError("always failed")


@binp.service
async def check_rss():
    """
    Primitive service that checks rss every 3 seconds
    """
    await sleep(3)  # emulate request
    print("RSS checked")


@binp.service(restart=False)
async def one_shot():
    """
    Primitive service that runs only once
    """
    await sleep(3)  # emulate workload
