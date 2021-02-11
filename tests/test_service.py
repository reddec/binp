from asyncio import Event, sleep, get_event_loop
from unittest import TestCase

from binp.service import Service, Status, Info
from tests import atest


class TestService(TestCase):
    @atest
    async def test_start(self):
        service = Service()
        run = Event()

        @service(name="good", autostart=False)
        async def good():
            run.set()

        assert service.services[0].status == Status.stopped
        service.start("good")
        await run.wait()

    @atest
    async def test_stop(self):
        service = Service()
        run = Event()

        @service
        async def good():
            run.set()
            await sleep(10)

        assert service.services[0].status == Status.starting
        await run.wait()

        assert service.services[0].status == Status.running

        service.stop(good.__qualname__)
        await sleep(0.0001)  # just next tick
        assert service.services[0].status == Status.stopped, service.services[0].status

    @atest
    async def test_services(self):
        service = Service()
        good_run = Event()

        @service(restart_delay=0.1)
        async def good():
            """
            Hello world
            """
            good_run.set()

        assert service.services[0].status == Status.starting
        await good_run.wait()
        good_run.clear()

        assert service.services[0].status == Status.restarting
        # should be restarted
        await good_run.wait()

        assert Info(
            name=good.__qualname__,
            description='Hello world',
            restart=True,
            restart_delay=0.1,
            autostart=True,
            status=Status.restarting
        ) == service.services[0]

    @atest
    async def test_replace(self):
        service = Service()
        good_run = Event()
        bad_run = Event()

        @service(name='good', restart=False, autostart=True)
        async def good():
            good_run.set()
            await sleep(100)

        await good_run.wait()

        @service(name='good', restart=False, autostart=True)
        async def bad():
            bad_run.set()

        await bad_run.wait()
        assert len(service.services) == 1
