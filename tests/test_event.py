from __future__ import absolute_import
import unittest
import time
from jarpis.event import *


class EventTest(unittest.TestCase):
    object = None

    def setUp(self):
        TestDBUtil.execute(Event.createEventTable, [])
        TestDBUtil.execute(EventParameter.createEventParameterTable, [])
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
        self.object = Birthday(-1000, "Geburtstagsparty", time.time(), time.time(), level, 1, EventType.getTypeIdByName("birthday"), None, {"subject":subject})
        TestDBUtil.execute(self.object.create, [])
        event = TestDBUtil.execute(self.object.findOneById, [-1000])
        self.assertEqual(event._params["subject"], "Kevin")

    def test_convert_from_create_default_and_birthday_event(self):
        level = "private"
        defaultEvent = Event(-1000, "Normales Event", time.time(), time.time(), level, 1,
                             EventType.getTypeIdByName("default"), None)

        subject = "Kevin"
        birthdayEvent = Birthday(-1001, "Geburtstagsparty", time.time(), time.time(), level, 1,
                               EventType.getTypeIdByName("birthday"), None, {"subject": subject})

        TestDBUtil.execute(defaultEvent.create, [])
        TestDBUtil.execute(birthdayEvent.create, [])
        events = TestDBUtil.execute(Event.findAll, [])

        self.assertIsInstance(events[1], Event)
        self.assertIsInstance(events[0], Birthday)

    def test_delete_birthday_event(self):
        level = "private"
        subject = "Kevin"
        birthdayEvent = Birthday(-1001, "Geburtstagsparty", time.time(), time.time(), level, 1,
                                 EventType.getTypeIdByName("birthday"), None, {"subject": subject})

        TestDBUtil.execute(birthdayEvent.create, [])
        self.assertIsNotNone(birthdayEvent)
        TestDBUtil.execute(birthdayEvent.delete, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-1001])

    def test_delete_birthday_event_parameters(self):
        level = "private"
        subject = "Kevin"
        birthdayEvent = Birthday(-1001, "Geburtstagsparty", time.time(), time.time(), level, 1,
                                 EventType.getTypeIdByName("birthday"), None, {"subject": subject})

        TestDBUtil.execute(birthdayEvent.create, [])
        self.assertIsNotNone(birthdayEvent)
        params = TestDBUtil.execute(EventParameter.loadParameterById, [birthdayEvent._id])
        self.assertIsNotNone(params)
        TestDBUtil.execute(birthdayEvent.delete, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-1001])

        paramsFromDeletedEvent = TestDBUtil.execute(EventParameter.loadParameterById, [birthdayEvent._id])
        self.assertEqual(paramsFromDeletedEvent, {})

    def tearDown(self):
        # pass
        TestDBUtil.execute(Event.dropEventTable, [])
        TestDBUtil.execute(EventParameter.dropEventParameterTable, [])
