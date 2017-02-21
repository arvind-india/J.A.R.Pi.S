import unittest
import datetime
from jarpis.event import *
from jarpis.calander import *


class CalendarTest(unittest.TestCase):
    objects = []
    currentTime = datetime.datetime.now() - datetime.timedelta(hours=2)

    def setUp(self):
        TestDBUtil.exec(Event.createEventTable, [])
        self.objects.append(
            Event(-1001, "Gute Party", self.currentTime, self.currentTime + datetime.timedelta(days=3), True, 1, 1,
                  None))
        self.objects.append(
            Event(-1002, "Beste Party", self.currentTime, self.currentTime + datetime.timedelta(days=2), True, 1, 1,
                  None))
        self.objects.append(
            Event(-1003, "Schlechte Party", self.currentTime, self.currentTime + datetime.timedelta(days=1), True, 1, 1,
                  None))
        self.objects.append(
            Event(-1004, "Mega Party", self.currentTime, self.currentTime + datetime.timedelta(days=4), True, 1, 1,
                  None))
        self.objects.append(
            Event(-1005, "Tolle Party", self.currentTime, (self.currentTime + datetime.timedelta(days=6)), True, 1, 1,
                  None))

        for obj in self.objects:
            TestDBUtil.exec(obj.create, [])

    def test_get_events_by_date(self):
        cal = Calendar(self.currentTime - datetime.timedelta(seconds=1), None)
        self.assertEqual(len(TestDBUtil.exec(cal.getEvents, [])), 5)

    def tearDown(self):
        # for obj in self.objects:
        #     TestDBUtil.exec(obj.delete, [])

        TestDBUtil.exec(Event.dropEventTable, [])
