from pydantic.main import BaseModel

from binp.kv import KV
from tests import TestWithDB, atest


class TestKV(TestWithDB):
    @atest
    async def test_set(self):
        kv = KV(db=self.db)
        await kv.set(a=1, b=True, c=0.3, d='hello world')

        res = await self.db.fetch_all("SELECT value FROM kv WHERE key IN ('a','b','c','d') ORDER BY key")
        assert len(res) == 4

        values = [k['value'] for k in res]
        assert ['1', 'true', '0.3', '"hello world"'] == values

    @atest
    async def test_set_replace(self):
        kv = KV(db=self.db)
        await kv.set(foo='bar')

        res = await self.db.fetch_one("SELECT value FROM kv WHERE key = :key", values={'key': 'foo'})
        assert res['value'] == '"bar"'

        await kv.set(foo='zee')

        res = await self.db.fetch_one("SELECT value FROM kv WHERE key = :key", values={'key': 'foo'})
        assert res['value'] == '"zee"'

    @atest
    async def test_set_ns(self):
        kv_a = KV(db=self.db, namespace='a')
        kv_b = kv_a.select('b')
        await kv_a.set(spam='bar')
        await kv_b.set(spam='zee')

        res = await self.db.fetch_all("SELECT value, namespace FROM kv WHERE key = :key ORDER BY namespace",
                                      values={'key': 'spam'})
        assert len(res) == 2

        values = [x['value'] for x in res]
        ns = [x['namespace'] for x in res]

        assert values == ['"bar"', '"zee"']
        assert ns == ['a', 'b']

    @atest
    async def test_get(self):
        kv = KV(db=self.db)
        await kv.set(foo='bar')

        value = await kv.get('foo')

        assert value == 'bar'

    @atest
    async def test_remove(self):
        kv = KV(db=self.db)
        await kv.set(foo='bar')

        value = await kv.get('foo')
        assert value == 'bar'

        await kv.remove('foo')
        value = await kv.get('foo')
        assert value is None

    @atest
    async def test_save_load(self):
        class User(BaseModel):
            name: str
            uid: int

        user = User(name='Foo Bar', uid=123)

        kv = KV(db=self.db)

        await kv.save(user)

        parsed_user = await kv.load(User)

        assert user == parsed_user

    @atest
    async def test_namespaces(self):
        kv = KV('alfa', db=self.db)
        await kv.set(foo='bar')

        kv = KV('beta', db=self.db)
        await kv.set(foo='bar')

        names = set(await kv.namespaces())
        assert names == (names & {'alfa', 'beta'})
