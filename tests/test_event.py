import unittest
import time
from jarpis.event import *


class EventTest(unittest.TestCase):
    def test_create_event(self):

        object = Event(1, "Party", time.time(), time.time(), True, 1, 1, None)
        object = object.create()

        if object._id.__eq__("1") and object._private.__eq__(True):
            assert True
        else:
            assert False

    def test_event_find_by_id(self):
        self.assertIsNotNone(Event.findOneById(1))

    def test_event_not_found_by_id(self):
        with self.assertRaises(EventNotFoundException):
            Event.findOneById(2)
