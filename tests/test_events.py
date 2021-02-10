from asyncio import get_event_loop, Event
from unittest import TestCase

from binp.events import Emitter
from tests import atest


class TestEmitter(TestCase):
    @atest
    async def test_subscribe(self):
        event: Emitter[int] = Emitter()

        get_event_loop().call_soon(lambda: event.emit(2))

        with event.subscribe() as queue:
            value = await queue.get()

        assert value == 2

    @atest
    async def test_decorator(self):
        event: Emitter[str] = Emitter()
        done = Event()

        @event
        async def greeter(value: str):
            assert value == 'hello'
            done.set()

        get_event_loop().call_soon(lambda: event.emit('hello'))

        await done.wait()

    def test_decorator_without_loop(self):
        event: Emitter[str] = Emitter()
        done = Event()

        @event
        async def greeter(value: str):
            assert value == 'hello'
            done.set()

        async def main():
            event.emit('hello')
            await done.wait()

        get_event_loop().run_until_complete(main())
