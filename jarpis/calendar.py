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

    @staticmethod
    def getCurrentYear():
        return datetime.datetime.today().year

    @staticmethod
    def getCurrentWeekday():
        return datetime.datetime.today().strftime("%A")

    @staticmethod
    def getCurrentMonth():
        return datetime.datetime.today().month

    @staticmethod
    def getCurrentDate():
        return datetime.datetime.today().replace(microsecond=0)

    @staticmethod
    def getDateByOffset(date, offset=0):
        if date is None:
            date = datetime.datetime.today()
        return date + datetime.timedelta(days=offset)

    @staticmethod
    def getCurrentDay():
        return datetime.datetime.today().day

    @staticmethod
    def getDateFor(**kwargs):
        current = Calendar.getCurrentDate()

        if "year" not in kwargs:
            kwargs["year"] = current.year
        if "month" not in kwargs:
            kwargs["month"] = current.month
        if "day" not in kwargs:
            kwargs["day"] = current.day

        return datetime.datetime(**kwargs)

    def __repr__(self):
        return "Calendar from %s to %s" % (self.from_date, self.to_date)
