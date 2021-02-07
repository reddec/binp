from binp.journals import Journals, current_journal
from tests import atest, TestWithDB


class TestJournal(TestWithDB):

    @atest
    async def test_log(self):
        journal = Journals()

        @journal(operation='sample')
        async def sample():
            """
            Some description
            """
            return current_journal.get()

        res = await sample()
        assert res > 0

        records = await self.db.fetch_all('SELECT * FROM journal WHERE id = :id', values={'id': res})
        assert len(records) == 1
        assert records[0]['operation'] == 'sample'
        assert records[0]['description'] == 'Some description'
        assert records[0]['started_at'] is not None
        assert records[0]['finished_at'] is not None
        assert records[0]['error'] is None
        assert records[0]['duration'] > 0

    @atest
    async def test_log_custom_description(self):
        journal = Journals(self.db)

        @journal(operation='sample', description='Foo bar')
        async def sample():
            """
            Some description
            """
            return current_journal.get()

        res = await sample()

        records = await self.db.fetch_one('SELECT * FROM journal WHERE id = :id', values={'id': res})
        assert records['operation'] == 'sample'
        assert records['description'] == 'Foo bar'

    @atest
    async def test_log_no_args(self):
        journal = Journals(self.db)

        @journal
        async def sample():
            """
            Some description
            """
            return current_journal.get()

        res = await sample()

        records = await self.db.fetch_one('SELECT * FROM journal WHERE id = :id', values={'id': res})
        assert records['operation'] == sample.__qualname__
        assert records['description'] == 'Some description'

    @atest
    async def test_history(self):
        journal = Journals(self.db)

        @journal
        async def sample():
            """
            Some description
            """
            return current_journal.get()

        items = await sample(), await sample(), await sample()
        ids = set(items)
        result = await journal.history()
        result_ids = set(x.id for x in result)
        assert ids == (result_ids & ids)

    @atest
    async def test_get(self):
        journal = Journals(self.db)

        @journal(operation='sample')
        async def sample():
            """
            Some description
            """
            return current_journal.get()

        res = await sample()
        assert res > 0

        saved_journal = await journal.get(res)
        assert saved_journal is not None
        assert saved_journal.operation == 'sample'
        assert saved_journal.description == 'Some description'
        assert saved_journal.started_at is not None
        assert saved_journal.finished_at is not None
        assert saved_journal.error is None
        assert saved_journal.duration > 0

    @atest
    async def test_add_records(self):
        journal = Journals(self.db)

        @journal(operation='sample')
        async def sample():
            await journal.record('some message 1', stage='init')
            await journal.record('some message 2', stage='working')
            await journal.record('some message 3', stage='complete', profit=-1)
            return current_journal.get()

        journal_id = await sample()

        saved_journal = await journal.get(journal_id)

        assert len(saved_journal.records) == 3

        record = saved_journal.records[0]
        assert record.message == 'some message 3' and record.params == {'stage': 'complete', 'profit': -1}

        record = saved_journal.records[1]
        assert record.message == 'some message 2' and record.params == {'stage': 'working'}

        record = saved_journal.records[2]
        assert record.message == 'some message 1' and record.params == {'stage': 'init'}
