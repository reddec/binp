from contextvars import ContextVar
from datetime import datetime
from functools import wraps
from json import dumps, loads
from logging import getLogger
from time import monotonic
from typing import List, Optional, Union, Any, Dict

from databases import Database
from pydantic.main import BaseModel

from binp.db import ensure

"""
Current journal record ID. Can be used only from functions under @journal.log decorators.
Useful to link some other entities to the journal record.
It's not recommended modify the variable outside core module.
"""
current_journal: ContextVar[Optional[int]] = ContextVar('current_journal', default=None)


class Event(BaseModel):
    journal_id: int
    id: int
    name: str
    value: Any
    created: datetime


class Record(BaseModel):
    message: str
    created_at: datetime
    params: Dict[str, Any]


class Headline(BaseModel):
    id: int
    operation: str
    description: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
    duration: Optional[float] = None


class Journal(Headline):
    records: List[Record]


class Journals:
    """
    Journal of logged invokes
    """

    def __init__(self, database: Optional[Database] = None):
        self.__db = ensure(database)

    def __call__(self, func=None, *, operation: Optional[str] = None, description: Optional[str] = None):
        """
        Decorator that tracks operation and put it to journal.
        """

        def trace_operation(fn):
            nonlocal operation
            nonlocal description

            if operation is None:
                operation = fn.__qualname__
            if description is None:
                description = "\n".join(line.strip() for line in (fn.__doc__ or '').splitlines()).strip()

            @wraps(fn)
            async def wrapper(*args, **kwargs):

                a = monotonic()
                ex: Optional[Exception] = None
                rec = await self.__begin(operation, description)
                token = current_journal.set(rec)
                try:
                    return await fn(*args, **kwargs)
                except Exception as f_ex:
                    ex = f_ex
                    raise
                finally:
                    current_journal.reset(token)
                    await self.__end(rec, monotonic() - a, ex)

            return wrapper

        if func is None:
            return trace_operation
        return trace_operation(func)

    async def history(self, offset: int = 0, limit: int = 20) -> List[Headline]:
        """
        Get journal headlines in reverse order (newest - first).
        """
        db = await self.__db()
        rows = await db.fetch_all('''
            SELECT * FROM journal ORDER BY id DESC LIMIT :limit OFFSET :offset
        ''', values={
            'offset': offset,
            'limit': limit
        })
        return [
            Headline(
                id=info['id'],
                operation=info['operation'],
                description=info['description'],
                started_at=info['started_at'],
                finished_at=info['finished_at'],
                error=info['error'],
                duration=info['duration'],
            )
            for info in rows
        ]

    async def get(self, journal_id: int) -> Optional[Journal]:
        """
        Get single journal by ID
        """
        db = await self.__db()

        info = await db.fetch_one('SELECT * FROM journal WHERE id = :journal_id', values={
            'journal_id': journal_id
        })
        if info is None:
            return None
        records = await self.__fetch_records(journal_id)

        return Journal(
            id=info['id'],
            operation=info['operation'],
            description=info['description'],
            started_at=info['started_at'],
            finished_at=info['finished_at'],
            error=info['error'],
            duration=info['duration'],
            records=records,
        )

    async def record(self, message: str, **events: Union[BaseModel, str, int, float, bool]):
        """
        Add record to journal. Will work only if there is
        @journal function in call chain.

        :param message: short message, describes record
        :param events: key->value of events, where key is event name, and value is basic type or pydantic model.
        Value will be serialized as JSON
        """
        logger = getLogger(self.__class__.__qualname__)
        journal_id = current_journal.get()
        if journal_id is None:
            logger.warning('function no marked as @journal - event will not be published')
            return

        db = await self.__db()

        async with db.transaction():
            await db.execute('''INSERT INTO record (journal_id, message) VALUES (:journal_id, :message)''', values={
                'journal_id': journal_id,
                'message': message or '',
            })
            record_id = (await db.fetch_one('SELECT last_insert_rowid()'))[0]
            logger.info(message)
            await db.execute_many('''INSERT INTO record_field (record_id, name, value) 
                                   VALUES (:record_id, :name, :value)
                                   ''', values=[{
                'name': name,
                'value': value.json() if isinstance(value, BaseModel) else dumps(value, ensure_ascii=False),
                'record_id': record_id
            } for name, value in events.items()])

    async def remove_dead(self):
        """
        Remove all records without finish_at timestamp. Should be called only once BEFORE any writes.
        """
        db = await self.__db()
        await db.execute('''
                   DELETE FROM journal
                   WHERE finished_at IS NULL
               ''')

    async def __fetch_records(self, journal_id: int) -> List[Record]:
        db = await self.__db()
        rows = await db.fetch_all('SELECT * FROM record WHERE journal_id = :journal_id ORDER BY id DESC', values={
            'journal_id': journal_id
        })
        if rows is None or len(rows) == 0:
            return []
        result = []
        for row in rows:
            fields = await self.__fetch_fields(row['id'])
            result.append(Record(
                message=row['message'],
                created_at=row['created_at'],
                params=fields
            ))
        return result

    async def __fetch_fields(self, record_id: int) -> Dict[str, Any]:
        db = await self.__db()
        rows = await db.fetch_all('SELECT name, value FROM record_field WHERE record_id = :record_id', values={
            'record_id': record_id
        })
        if rows is None or len(rows) == 0:
            return {}
        return dict((row['name'], loads(row['value'])) for row in rows)

    async def __begin(self, name, description) -> int:
        db = await self.__db()

        async with db.transaction():
            await db.execute('''INSERT INTO journal (operation, description) 
                        VALUES (:operation, :description)
                        ''', values={
                'operation': name,
                'description': description,
            })
            res = await db.fetch_one('SELECT last_insert_rowid()')

        return res[0]

    async def __end(self, rec_id: int, delta: float, exc=None):
        db = await self.__db()
        await db.execute('''
        UPDATE journal
        SET finished_at = current_timestamp,
            duration = :duration,
            error = :error
        WHERE id = :id                
                            ''', values={
            'duration': delta,
            'id': rec_id,
            'error': str(exc) if exc is not None else None
        })
