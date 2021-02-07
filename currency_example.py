from random import randint

from binp import BINP

bip = BINP()


@bip.app.post('/random', response_model=int)
@bip.journal
async def generate_random():
    """
    Generate random number in range 0 ... 1024
    """
    return randint(0, 1024)


@bip.action
@bip.journal
async def currency_rate():
    """
    Fetch currency rate for EUR -> USD
    """
    # go to external service
    euro = 1.3
    await bip.journal.record('rates fetched', base_currency='USD', euro=euro)
