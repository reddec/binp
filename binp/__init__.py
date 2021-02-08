from asyncio import get_event_loop
from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Callable, Awaitable, List

from fastapi import FastAPI

from .action import Action
from .api import create_app
from .journals import Journals
from .kv import KV


@dataclass(frozen=True)
class BINP:
    #: Key-Value default storage
    kv: KV = field(default_factory=KV)
    #: Journal for operation tracing
    journal: Journals = field(default_factory=Journals)
    #: UI exposed actions (buttons)
    action: Action = field(default_factory=Action)

    __autostart: List[Callable[[], Awaitable]] = field(default_factory=list)

    @cached_property
    def app(self) -> FastAPI:
        """
        Creates FastAPI applications and caches result.
        """
        app = create_app(self.journal, self.kv, self.action)

        @app.on_event('startup')
        async def run_autostart():
            for fn in self.__autostart:
                get_event_loop().create_task(fn())

        return app

    def autostart(self, func: Optional[Callable[[], Awaitable]] = None):
        """
        Launches annotated async function in 'background' (added to event queue).

        It uses `fastapi` `@on_event` approach but doesn't wait for result.

        Useful to interact with environment in unpredictable schedule (ex: listen for low-level network requests)

        Better do not use it for scheduling. Use `aiocron` instead:

        .. code-block::

            pip install aiocron

        .. highlight:: python
        .. code-block:: python

            from binp import BINP
            from aiocron import crontab

            binp = BINP()

            @crontab("*/5 * * * *")
            @binp.journal
            async def poll_something():
                print("do something every 5 minutes....")

        `aicron` supports up to seconds precision (6 arguments instead of classical 5).
        """

        def register_function(fn: Callable[[], Awaitable]):
            self.__autostart.append(fn)
            return fn

        if func is None:
            return register_function
        return register_function(func)
