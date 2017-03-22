from datetime import datetime


class DateUtil(object):
    def __init__(self):
        pass

    def getYear(self):
        return datetime.today().year

    def getWeekday(self):
        return datetime.today().weekday()

    def getMonth(self):
        return datetime.today().month

    def getDate(self):
        return datetime.today().replace(microsecond=0)

    #TODO Maybe we can add a check if the time from the system equals the time from web...
