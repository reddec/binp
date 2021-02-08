from asyncio import sleep
from datetime import date
from logging import INFO, basicConfig
from typing import Dict

import aiocron
from aiohttp import ClientSession
from pydantic.main import BaseModel

from binp import BINP

bip = BINP()


class Rates(BaseModel):
    base: str = 'USD'
    rates: Dict[str, float] = {}
    date: date


@aiocron.crontab('30 * * * *')
@bip.app.post('/currency-rate', response_model=Rates)
@bip.journal
async def currency_rate():
    """
    Fetch currency rate for USD
    """
    await bip.journal.record('fetching....', base_currency='USD')
    async with ClientSession() as session:
        res = await session.get('https://api.exchangeratesapi.io/latest?base=USD')
        assert res.ok, f"result {res.status}"
        data = await res.json()
    rates = Rates.parse_obj(data)
    await bip.journal.record('done', base_currency='USD', rates=rates)
    await bip.kv.save(rates)
    return rates


@bip.app.post('/fail')
@bip.journal
async def do_fail():
    """
    Fail always
    """

    assert 1 == 2, 'Ooops'


@bip.action
@bip.journal
async def do_something():
    """
    Do smoething
    """
    return 'hello world'


@bip.autostart
async def poll_something():
    while True:
        print("background task")
        await sleep(1)


# @journal.log(ops name)
# @events.subscribe('event name'), events.emit

basicConfig(level=INFO)
