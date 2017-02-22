import datetime
from jarpis.event import *


class Calendar(object):
    def __init__(self, from_date, to_date):
        if from_date is None:
            self.from_date = datetime.datetime.now()
        else:
            self.from_date = from_date

        if to_date is None:
            self.to_date = self.from_date + datetime.timedelta(days=7)
        else:
            self.to_date = to_date

    def getEvents(self):
        list = DBUtil.exec(Event.findEventsByDate, (self.from_date, self.to_date,))

        for element in list:
            print(element)

        return list

    def __repr__(self):
        return "Calendar from %s to %s" % (self.from_date, self.to_date)
