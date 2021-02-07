from _asyncio import get_event_loop
from asyncio import get_event_loop
from logging import basicConfig, INFO
from pathlib import Path
from unittest import TestCase

from databases import Database

from binp.db import migrate


def atest(fn):
    def wrapper(*args, **kwargs):
        return get_event_loop().run_until_complete(fn(*args, *kwargs))

    return wrapper


class TestWithDB(TestCase):
    db_file = Path() / 'data.db'

    def setUp(self) -> None:
        super().setUp()
        basicConfig(level=INFO)

        self.db_file.unlink(missing_ok=True)
        self.db = Database(f'sqlite:///{self.db_file}')

        async def init():
            await self.db.connect()
            await migrate(self.db)

        get_event_loop().run_until_complete(init())

    def tearDown(self) -> None:
        super().tearDown()
        get_event_loop().run_until_complete(self.db.disconnect())
        self.db_file.unlink(missing_ok=True)
