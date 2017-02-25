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
        first_handler = Mock()
        second_handler = Mock()
        self._mediator.register("onUnitTest", first_handler)

        # act
        self._mediator.register("onUnitTest", second_handler)

        # assert
        self.assertIn("onUnitTest", self._mediator._eventHandlers)
        self.assertEqual(2, len(self._mediator._eventHandlers["onUnitTest"]))
        self.assertIn(
            first_handler, self._mediator._eventHandlers["onUnitTest"])
        self.assertIn(
            second_handler, self._mediator._eventHandlers["onUnitTest"])

    def test_if_there_are_handlers_for_other_events_than_the_target_one(self):
        # arrange
        first_handler = Mock()
        second_handler = Mock()
        self._mediator.register("onUnitTestFirst", first_handler)

        # act
        self._mediator.register("onUnitTestSecond", second_handler)

        # assert
        self.assertIn("onUnitTestFirst", self._mediator._eventHandlers)
        self.assertIn("onUnitTestSecond", self._mediator._eventHandlers)
        self.assertEqual(
            1, len(self._mediator._eventHandlers["onUnitTestSecond"]))
        self.assertIn(
            first_handler, self._mediator._eventHandlers["onUnitTestFirst"])
        self.assertIn(
            second_handler, self._mediator._eventHandlers["onUnitTestSecond"])


class An_event_handler_fails_to_register(unittest.TestCase):

    def setUp(self):
        self._mediator = EventMediator()

    def tearDown(self):
        del self._mediator

    def test_if_the_event_argument_is_None(self):
        # arrange
        handler = Mock()

        # act and assert
        with self.assertRaises(TypeError):
            self._mediator.register(None, handler)

    def test_if_the_handler_argument_is_None(self):
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


class An_event_handler_can_be_unregistered(unittest.TestCase):

    def setUp(self):
        self._mediator = EventMediator()

    def tearDown(self):
        del self._mediator

    def test_if_the_handler_was_registered_before(self):
        # arrange
        handler = Mock()
        self._mediator.register("onUnitTest", handler)

        # act
        self._mediator.unregister("onUnitTest", handler)

        # assert
        self.assertEqual(0, len(self._mediator._eventHandlers["onUnitTest"]))

    def test_if_the_target_event_is_not_known(self):
        # arrange
        handler = Mock()

        # act
        event_not_known_before = (
            "onUnitTest" in self._mediator._eventHandlers)
        self._mediator.unregister("onUnitTest", handler)
        event_not_known_after = ("onUnitTest" in self._mediator._eventHandlers)

        # assert
        self.assertEqual(event_not_known_before, event_not_known_after)
        self.assertNotIn("onUnitTest", self._mediator._eventHandlers)

    def test_if_the_specified_handler_is_not_registered_for_the_target_event(self):
        # arrange
        first_handler = Mock()
        second_handler = Mock()
        self._mediator.register("onUnitTest", first_handler)

        # act
        handler_amount_before = len(
            self._mediator._eventHandlers["onUnitTest"])
        self._mediator.unregister("onUnitTest", second_handler)
        handler_amount_after = len(
            self._mediator._eventHandlers["onUnitTest"])

        # assert
        self.assertEqual(handler_amount_before,
                         handler_amount_after)
        self.assertIn(
            first_handler, self._mediator._eventHandlers["onUnitTest"])
        self.assertNotIn(
            second_handler, self._mediator._eventHandlers["onUnitTest"])


class An_event_handler_fails_to_unregister(unittest.TestCase):

    def setUp(self):
        self._mediator = EventMediator()

    def tearDown(self):
        del self._mediator

    def test_if_the_event_argument_is_None(self):
        self.fail()

    def test_if_the_handler_argument_is_None(self):
        self.fail()

    def test_if_the_handler_is_not_registered_for_the_target_event(self):
        self.fail()
