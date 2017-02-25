from __future__ import absolute_import

import unittest

from mock import Mock

from jarpis.dialogs.events import EventMediator, DuplicateEventHandler


class An_event_handler_can_be_registered(unittest.TestCase):

    def setUp(self):
        self._mediator = EventMediator()

    def tearDown(self):
        del self._mediator

    def test_if_there_is_no_handler_for_the_target_event_yet(self):
        # arrange
        handler = Mock()

        # act
        self._mediator.register("onUnitTest", handler)

        # assert
        self.assertIn("onUnitTest", self._mediator._eventHandlers)
        self.assertIn(handler, self._mediator._eventHandlers["onUnitTest"])

    def test_if_there_is_a_handler_other_than_the_target_handler_for_the_target_event(self):
        # arrange
        firstHandler = Mock()
        secondHandler = Mock()
        self._mediator.register("onUnitTest", firstHandler)

        # act
        self._mediator.register("onUnitTest", secondHandler)

        # assert
        self.assertIn("onUnitTest", self._mediator._eventHandlers)
        self.assertEqual(2, len(self._mediator._eventHandlers["onUnitTest"]))
        self.assertIn(
            firstHandler, self._mediator._eventHandlers["onUnitTest"])
        self.assertIn(
            secondHandler, self._mediator._eventHandlers["onUnitTest"])

    def test_if_there_are_handlers_for_other_events_than_the_target_one(self):
        # arrange
        firstHandler = Mock()
        secondHandler = Mock()
        self._mediator.register("onUnitTestFirst", firstHandler)

        # act
        self._mediator.register("onUnitTestSecond", secondHandler)

        # assert
        self.assertIn("onUnitTestFirst", self._mediator._eventHandlers)
        self.assertIn("onUnitTestSecond", self._mediator._eventHandlers)
        self.assertEqual(
            1, len(self._mediator._eventHandlers["onUnitTestSecond"]))
        self.assertIn(
            firstHandler, self._mediator._eventHandlers["onUnitTestFirst"])
        self.assertIn(
            secondHandler, self._mediator._eventHandlers["onUnitTestSecond"])


class An_event_handler_fails_to_register(unittest.TestCase):

    def setUp(self):
        self._mediator = EventMediator()

    def tearDown(self):
        del self._mediator

    def test_if_it_is_None(self):
        # arrange
        handler = None

        # act and assert
        with self.assertRaises(TypeError):
            self._mediator.register("onUnitTest", handler)

    def test_if_the_same_handler_is_already_registered(self):
        # arrange
        handler = Mock()
        self._mediator.register("onUnitTest", handler)

        # act and assert
        with self.assertRaises(DuplicateEventHandler):
            self._mediator.register("onUnitTest", handler)
