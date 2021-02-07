from unittest import TestCase

from binp.action import Action, ActionInfo
from tests import atest


class TestAction(TestCase):

    @atest
    async def test_invoke(self):
        action = Action()
        triggered = False

        @action(name='hello')
        async def hello():
            nonlocal triggered
            triggered = True

        await action.invoke('wrong')
        assert not triggered

        await action.invoke('hello')
        assert triggered

    def test_actions(self):
        action = Action()

        @action
        async def handler(): pass

        @action(name='handler-2')
        async def handler2():
            """
            Some help
            """
            pass

        @action(name='handler-3', description='some operation')
        async def handler3(): pass

        assert action.actions == [
            ActionInfo(name=handler.__qualname__, description=''),
            ActionInfo(name='handler-2', description='Some help'),
            ActionInfo(name='handler-3', description='some operation')
        ]
