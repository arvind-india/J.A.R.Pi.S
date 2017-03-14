from __future__ import absolute_import
import unittest
from jarpis.calander import *


class CalendarTest(unittest.TestCase):
    objects = None
    currentTime = datetime.datetime.now() - datetime.timedelta(hours=2)

    def setUp(self):
        self.objects = []
        DBUtil.execute(Event.createEventTable, [])
        DBUtil.execute(Repeating.createRepeatingTable, [])

        self.objects.append(
            Event(-1001, "Gute Party", self.currentTime, self.currentTime + datetime.timedelta(days=3), "public", 1, 1,
                  None))
        self.objects.append(
            Event(-1002, "Beste Party", self.currentTime, self.currentTime + datetime.timedelta(days=2), "private", 1, 1,
                  None))
        self.objects.append(
            Event(-1003, "Schlechte Party", self.currentTime, self.currentTime + datetime.timedelta(days=1), 1, 1, 1,
                  None))
        self.objects.append(
            Event(-1004, "Mega Party", self.currentTime, self.currentTime + datetime.timedelta(days=4), 2, 1, 1,
                  None))
        self.objects.append(
            Event(-1005, "Tolle Party", self.currentTime, (self.currentTime + datetime.timedelta(days=6)), 3, 1, 1,
                  None))

        for obj in self.objects:
            DBUtil.execute(obj.create, [])

    def test_get_events_by_date(self):
        cal = Calendar(self.currentTime - datetime.timedelta(seconds=1), None)
        self.assertEqual(len(DBUtil.execute(cal.getEvents, [])), 5)


    def test_find_series_events(self):
        event1 = Event(-1010, "Alte Party", datetime.datetime(2017,1,10,10,0), datetime.datetime(2017,1,10,11,0), 1, 1, 1, 1)
        event2 = Event(-1011, "Neue Party", datetime.datetime(2017,1,12,10,0), datetime.datetime(2017,1,12,11,0), 1, 1, 1, None)
        series = Repeating(1, datetime.datetime(2017,1,10,10,0), datetime.datetime(2017,1,15,11,0), "daily")
        DBUtil.execute(event1.create, [])
        DBUtil.execute(event2.create, [])
        DBUtil.execute(series.create, [])

        list = DBUtil.execute(Event.findByDate, [datetime.datetime(2017, 1, 9, 11, 0), datetime.datetime(2017, 1, 13, 10, 0)])
        self.assertEqual(len(list), 3)

    def tearDown(self):
        DBUtil.execute(Event.dropEventTable, [])
        DBUtil.execute(Repeating.dropRepeatingTable, [])
