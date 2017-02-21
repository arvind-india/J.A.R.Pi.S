import unittest
import time
from jarpis.event import *


class EventTest(unittest.TestCase):
    object = None

    def setUp(self):
        DBUtil.exec(Event.createEventTable, [])
        self.object = Event(-1000, "Party", time.time(), time.time(), True, 1, 1, None)

    def test_create_event(self):
        eventObject = DBUtil.exec(self.object.create, [])
        self.assertEqual(eventObject._id, -1000)
        self.assertEqual(eventObject._private, True)

    def test_event_find_by_id(self):
        DBUtil.exec(self.object.create, [])
        DBUtil.exec(Event.findOneById, [-1000])

    def test_event_not_found_by_id(self):
        DBUtil.exec(self.object.create, [])
        with self.assertRaises(EventNotFoundException):
            DBUtil.exec(Event.findOneById, [-1001])

    def tearDown(self):
        DBUtil.exec(Event.dropEventTable,[])
