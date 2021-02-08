from asyncio import sleep
from datetime import date
from logging import INFO, basicConfig
from typing import Dict

import aiocron
from aiohttp import ClientSession
from pydantic.main import BaseModel

from binp import BINP

binp = BINP()


class Rates(BaseModel):
    base: str = 'USD'
    rates: Dict[str, float] = {}
    date: date


@aiocron.crontab('30 * * * *')
@binp.app.post('/currency-rate', response_model=Rates)
@binp.journal
async def currency_rate():
    """
    Fetch currency rate for USD
    """
    await binp.journal.record('fetching....', base_currency='USD')
    async with ClientSession() as session:
        res = await session.get('https://api.exchangeratesapi.io/latest?base=USD')
        assert res.ok, f"result {res.status}"
        data = await res.json()
    rates = Rates.parse_obj(data)
    await binp.journal.record('done', base_currency='USD', rates=rates)
    await binp.kv.save(rates)
    return rates


@binp.app.post('/fail')
@binp.journal
async def do_fail():
    """
    Fail always
    """

    assert 1 == 2, 'Ooops'


@binp.action
@binp.journal
async def do_something():
    """
    Do smoething
    """
    return 'hello world'


@binp.autostart
async def poll_something():
    while True:
        print("background task")
        await sleep(1)


basicConfig(level=INFO)
