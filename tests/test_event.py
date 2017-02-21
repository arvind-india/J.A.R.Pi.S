import unittest
import time
from jarpis.event import *


class EventTest(unittest.TestCase):
    object = None

    def setUp(self):
        TestDBUtil.exec(Event.createEventTable, [])
        self.object = Event(-1000, "Party", time.time(), time.time(), 1, 1, 1, None)

    def test_create_event(self):
        eventObject = TestDBUtil.exec(self.object.create, [])
        self.assertEqual(eventObject._id, -1000)
        self.assertEqual(eventObject._private, TestDBUtil.exec(Privacy.getLevelsIdByName,["public"]))

    def test_event_find_by_id(self):
        TestDBUtil.exec(self.object.create, [])
        TestDBUtil.exec(Event.findOneById, [-1000])

    def test_event_not_found_by_id(self):
        TestDBUtil.exec(self.object.create, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.exec(Event.findOneById, [-1001])

    def test_create_private_event(self):
        level = "private"
        self.object = Event(-1000, "Party", time.time(), time.time(), level, 1, 1, None)
        TestDBUtil.exec(self.object.create,[])
        event = TestDBUtil.exec(self.object.findOneById,[-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName(level))


    def test_create_public_event(self):
        level = "public"
        self.object = Event(-1000, "Party", time.time(), time.time(), level, 1, 1, None)
        TestDBUtil.exec(self.object.create, [])
        event = TestDBUtil.exec(self.object.findOneById, [-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName(level))

    def test_create_event_without_privacy(self):
        self.object = Event(-1000, "Party", time.time(), time.time(), None, 1, 1, None)
        TestDBUtil.exec(self.object.create, [])
        event = TestDBUtil.exec(self.object.findOneById, [-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName("public"))

    def tearDown(self):
        TestDBUtil.exec(Event.dropEventTable,[])
