import datetime
from jarpis.event import Event


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
        list = Event.findByDate(self.from_date, self.to_date)
        return list

    def getCurrentYear(self):
        return datetime.today().year

    def getCurrentWeekday(self):
        return datetime.today().strftime("%A")

    def getCurrentMonth(self):
        return datetime.today().month

    def getCurrentDate(self):
        return self.getDateByOffset(datetime.today().replace(microsecond=0))

    def getDateByOffset(self, date=None, offset=0):
        return date + datetime.timedelta(days=offset)

    def getCurrentDay(self):
        return datetime.today().day

    def __repr__(self):
        return "Calendar from %s to %s" % (self.from_date, self.to_date)
