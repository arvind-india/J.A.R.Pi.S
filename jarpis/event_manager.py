from jarpis.util import *
from jarpis.event import *

class EventManager(object):
    def __init__(self, event):
        self._event = event

    def rename_event(self, new_name):
        self._event._description = new_name
        self._event.update()

    def move_event(self, new_start, new_end):
        self._event._start = new_start
        self._event._end = new_end
        self._event.update()

    def move_event_by_duration(self, unit, value):
        self._event._start += DateUtil().addTime(unit, value)
        self._event._end += DateUtil().addTime(unit, value)
        self._event.update()

    @staticmethod
    def findById(id):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("SELECT * FROM EVENT WHERE ID = ?", (id,))

        result = c.fetchone()
        connection.close()

        if result is not None:
            return EventType.convert(result)

        raise EventNotFoundException("No Event found with given ID: %s" % (id))

    @staticmethod
    def findByDate(from_date, to_date):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute(
            "SELECT * FROM EVENT e LEFT JOIN SCHEDULING r ON r.id = e.FK_SERIES WHERE (e.START_DATE >= ? AND e.END_DATE <= ?) OR (r.START <= ? AND r.END >= ?)",
            (from_date, to_date, from_date, to_date,))

        eventList = []
        for result in c.fetchall():
            event = EventType.convert(result)
            if event._series is not None:
                nextEvent = Scheduling.getNextDate(event)
                while nextEvent is not None and to_date >= nextEvent._end:
                    eventList.append(nextEvent)
                    nextEvent = Scheduling.getNextDate(nextEvent)
            else:
                eventList.append(event)

        connection.close()

        return eventList

    @staticmethod
    def findAll():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("SELECT * FROM EVENT")

        eventList = []
        for result in c.fetchall():
            eventList.append(EventType.convert(result))

        connection.close()

        return eventList

    @staticmethod
    def findByUser(user, date=None):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        if date is None:
            date = datetime.datetime.now().replace(microsecond=0)

        to_date = datetime.datetime(date.year, date.month, date.day, 23, 59)

        c.execute("SELECT * FROM EVENT WHERE FK_CREATOR = ? AND START_DATE >= ? AND END_DATE <= ?",
                  (user._id, date, to_date,))
        list = c.fetchall()
        connection.close()

        eventList = []
        for result in list:
            eventList.append(EventType.convert(result))

        return eventList