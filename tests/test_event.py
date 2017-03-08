from __future__ import absolute_import
import unittest
import time
from jarpis.event import *


class EventTest(unittest.TestCase):

    def setUp(self):
        TestDBUtil.execute(Event.createEventTable, [])
        TestDBUtil.execute(EventParameter.createEventParameterTable, [])

    def test_create_event(self):
        event = Event(-1000, "Party", time.time(), time.time(), 1, 1, 1, None)
        TestDBUtil.execute(event.create, [])
        self.assertEqual(event._id, -1000)
        self.assertEqual(event._private, TestDBUtil.execute(Privacy.getLevelsIdByName,["public"]))

    def test_event_find_by_id(self):
        event = Event(-1000, "Party", time.time(), time.time(), 1, 1, 1, None)
        TestDBUtil.execute(event.create, [])
        result_event = TestDBUtil.execute(Event.findOneById, [-1000])
        self.assertIsNotNone(result_event)

    def test_event_not_found_by_id(self):
        event = Event(-1000, "Party", time.time(), time.time(), 1, 1, 1, None)
        TestDBUtil.execute(event.create, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-999])

    def test_create_private_event(self):
        level = "private"
        event = Event(-1000, "Party", time.time(), time.time(), level, 1, 1, None)
        TestDBUtil.execute(event.create,[])
        result_event = TestDBUtil.execute(Event.findOneById,[-1000])
        self.assertTrue(result_event._private, Privacy.getLevelsIdByName(level))

    def test_create_public_event(self):
        level = "public"
        event = Event(-1000, "Party", time.time(), time.time(), level, 1, 1, None)
        TestDBUtil.execute(event.create, [])
        result_event = TestDBUtil.execute(Event.findOneById, [-1000])
        self.assertTrue(result_event._private, Privacy.getLevelsIdByName(level))

    def test_create_event_without_privacy(self):
        event = Event(-1000, "Party", time.time(), time.time(), None, 1, 1, None)
        TestDBUtil.execute(event.create, [])
        result_event = TestDBUtil.execute(Event.findOneById, [-1000])
        self.assertTrue(result_event._private, Privacy.getLevelsIdByName("public"))

    def test_create_birthday_event(self):
        subject = "Kevin"
        level = "private"
        event = Birthday(-1000, "Geburtstagsparty", time.time(), time.time(), level, 1, None, {"subject":subject})
        TestDBUtil.execute(event.create, [])
        result_event = TestDBUtil.execute(Event.findOneById, [-1000])
        self.assertEqual(result_event._params["subject"], "Kevin")

    def test_convert_from_create_default_and_birthday_event(self):
        level = "private"
        default_event = Event(-1001, "Normales Event", time.time(), time.time(), level, 1,
                             EventType.getTypeIdByName("default"), None)

        subject = "Kevin"
        birthday_event = Birthday(-1000, "Geburtstagsparty", time.time(), time.time(), level, 1, None, {"subject": subject})

        TestDBUtil.execute(default_event.create, [])
        TestDBUtil.execute(birthday_event.create, [])
        birthday = TestDBUtil.execute(Event.findOneById, [-1000])
        event = TestDBUtil.execute(Event.findOneById, [-1001])

        self.assertIsInstance(event, Event)
        self.assertIsInstance(birthday, Birthday)

    def test_delete_birthday_event(self):
        level = "private"
        subject = "Kevin"
        birthday_event = Birthday(-1001, "Geburtstagsparty", time.time(), time.time(), level, 1,None, {"subject": subject})

        TestDBUtil.execute(birthday_event.create, [])
        self.assertIsNotNone(TestDBUtil.execute(Birthday.findOneById, [-1001]))
        TestDBUtil.execute(birthday_event.delete, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-1001])

    def test_delete_birthday_event_parameters(self):
        level = "private"
        subject = "Kevin"
        birthday_event = Birthday(-1001, "Geburtstagsparty", time.time(), time.time(), level, 1, None, {"subject": subject})

        TestDBUtil.execute(birthday_event.create, [])
        self.assertIsNotNone(TestDBUtil.execute(Event.findOneById, [-1001]))
        params = TestDBUtil.execute(EventParameter.loadParameterById, [birthday_event._id])
        self.assertIsNotNone(params)
        TestDBUtil.execute(birthday_event.delete, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-1001])

        params_from_deleted_event = TestDBUtil.execute(EventParameter.loadParameterById, [birthday_event._id])
        self.assertEqual(params_from_deleted_event, {})

    def test_create_shopping_event(self):
        shopping_items = ['waffeln','kekse','schoggi']
        level = "private"
        event = Shopping(-1000, "Wocheneinkauf", time.time(), time.time(), level, 1, None, shopping_items)
        TestDBUtil.execute(event.create, [])
        result_event = TestDBUtil.execute(Event.findOneById, [-1000])
        params = TestDBUtil.execute(EventParameter.loadParameterById, [result_event._id])
        self.assertEqual(len(params), 3)

    def test_delete_shopping_event(self):
        shopping_items = ['waffeln', 'kekse', 'schoggi']
        level = "private"
        event = Shopping(-1001, "Wocheneinkauf", time.time(), time.time(), level, 1, None, shopping_items)

        TestDBUtil.execute(event.create, [])
        self.assertIsNotNone(TestDBUtil.execute(Event.findOneById, [-1001]))
        TestDBUtil.execute(event.delete, [])
        with self.assertRaises(EventNotFoundException):
            TestDBUtil.execute(Event.findOneById, [-1001])

    def tearDown(self):
        TestDBUtil.execute(Event.dropEventTable, [])
        TestDBUtil.execute(EventParameter.dropEventParameterTable, [])
