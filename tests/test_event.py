from __future__ import absolute_import
import unittest
import time
from jarpis.event import *


class EventTest(unittest.TestCase):
    object = None

    def setUp(self):
        TestDBUtil.execute(Event.createEventTable, [])
        self.object = Event(-1000, "Party", time.time(), time.time(), 1, 1, 1, None)

    def test_create_event(self):
        eventObject = TestDBUtil.execute(self.object.create, [])
        self.assertEqual(eventObject._id, -1000)
        self.assertEqual(eventObject._private, TestDBUtil.execute(Privacy.getLevelsIdByName,["public"]))

    def test_event_find_by_id(self):
        TestDBUtil.execute(self.object.create, [])
        event = TestDBUtil.execute(Event.findOneById, [-1000])
        self.assertIsNotNone(event)

    def test_event_not_found_by_id(self):
        TestDBUtil.execute(self.object.create, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-999])

    def test_create_private_event(self):
        level = "private"
        self.object = Event(-1000, "Party", time.time(), time.time(), level, 1, 1, None)
        TestDBUtil.execute(self.object.create,[])
        event = TestDBUtil.execute(self.object.findOneById,[-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName(level))


    def test_create_public_event(self):
        level = "public"
        self.object = Event(-1000, "Party", time.time(), time.time(), level, 1, 1, None)
        TestDBUtil.execute(self.object.create, [])
        event = TestDBUtil.execute(self.object.findOneById, [-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName(level))

    def test_create_event_without_privacy(self):
        self.object = Event(-1000, "Party", time.time(), time.time(), None, 1, 1, None)
        TestDBUtil.execute(self.object.create, [])
        event = TestDBUtil.execute(self.object.findOneById, [-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName("public"))

    def test_create_birthday_event(self):
        subject = "Kevin"
        level = "private"
        self.object = Birthday(-1000, "Party", time.time(), time.time(), level, 1, 1, None, subject)
        TestDBUtil.execute(self.object.create, [])
        event = TestDBUtil.execute(self.object.findOneById, [-1000])
        self.assertTrue(event._private, Privacy.getLevelsIdByName(level))

    def tearDown(self):
        TestDBUtil.execute(Event.dropEventTable, [])
