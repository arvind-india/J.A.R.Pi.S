from __future__ import absolute_import
import unittest
from jarpis.event import *
from jarpis.event_manager import *
import datetime

du = DateUtil()


class BasicTestSuite(unittest.TestCase):
    def setUp(self):
        Event.createEventTable()

    def test_rename_event(self):
        event = Event(-1000, "Tolles Event", datetime.datetime(2017, 3, 19, 6,0), datetime.datetime(2017, 3, 19, 8,0), Privacy.getLevelsIdByName("private"), None, None, None).create()

        em = EventManager(event)
        em.rename_event("Doofes Event")

        dbEvent = EventManager.findById(-1000)
        self.assertEqual(dbEvent._description, "Doofes Event")

    def test_move_date(self):
        event = Event(-1000, "Tolles Event", datetime.datetime(2017, 3, 19, 6, 0), datetime.datetime(2017, 3, 19, 8, 0),Privacy.getLevelsIdByName("private"), None, None, None).create()

        em = EventManager(event)

        new_start = du.getDate()
        new_end = du.getDate()+ du.addTime("minutes", 10)

        em.move_event(new_start, new_end)
        dbEvent = EventManager.findById(-1000)
        self.assertEqual(dbEvent._start, new_start)
        self.assertEqual(dbEvent._end, new_end)

    def test_move_date_by_duration(self):
        event = Event(-1000, "Tolles Event", datetime.datetime(2017, 3, 19, 6, 0), datetime.datetime(2017, 3, 19, 8, 0),
                      Privacy.getLevelsIdByName("private"), None, None, None).create()

        new_start = event._start + datetime.timedelta(hours=2)
        new_end = event._end + datetime.timedelta(hours=2)

        em = EventManager(event)

        em.move_event_by_duration("hours", 2)

        dbEvent = EventManager.findById(-1000)

        self.assertEqual(dbEvent._start, new_start)
        self.assertEqual(dbEvent._end, new_end)


    def tearDown(self):
        Event.dropEventTable()