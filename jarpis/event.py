import sqlite3
import datetime
from dateutil.relativedelta import relativedelta
import copy
import jarpis


class Event(object):
    def __init__(self, id, description, start, end, private, creator, type, series):
        self._id = id
        self._description = description
        self._start = start.replace(microsecond=0)
        self._end = end.replace(microsecond=0)

        if private is None:
            self._private = Privacy.getLevelsIdByName("public")
        elif isinstance(private, int):
            name = Privacy.getLevelsNameById(private)
            if name is not None:
                self._private = private
            else:
                raise TypeError("Give privacy level is not valid: %s" % (private))
        elif isinstance(private, str):
            id = Privacy.getLevelsIdByName(private)
            if id is not None:
                self._private = id
            else:
                raise TypeError("Give privacy level is not valid: %s" % (private))

        self._creator = creator

        if type is None:
            self._type = EventType.getTypeIdByName("default")
        else:
            self._type = type

        self._series = series

    @staticmethod
    def fromResultToObject(result):
        start = None
        end = None

        if result[2] is not None:
            start = datetime.datetime.strptime(result[2], "%Y-%m-%d %H:%M:%S")

        if result[3] is not None:
            end = datetime.datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S")

        return Event(result[0], result[1], start, end, result[4], result[5], result[6], result[7])

    def create(self):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute(
                "INSERT INTO EVENT (ID, DESCRIPTION, START_DATE, END_DATE, PRIVATE, FK_CREATOR, FK_TYPE, FK_SERIES) VALUES(?,?,?,?,?,?,?,?)",
                (self._id, self._description, self._start, self._end, self._private, self._creator, self._type,
                 self._series))

            self._id = c.lastrowid

        except sqlite3.IntegrityError as err:
            print("Error while inserting Event with ID {1}: {0}".format(err, self._id))

        connection.commit()
        connection.close()

        return self

    def delete(self):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()
        c.execute("DELETE FROM EVENT WHERE ID = ?", (self._id,))
        connection.commit()
        connection.close()
        return True

    def update(self):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()
        c.execute("UPDATE EVENT SET DESCRIPTION=?, START_DATE=?, END_DATE=?, PRIVATE=?, FK_CREATOR=?, FK_TYPE=?, FK_SERIES=? WHERE ID = ?", (self._description, self._start, self._end, self._private, self._creator, self._type,
             self._series,self._id))
        connection.commit()
        connection.close()
        return self

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

        c.execute("SELECT * FROM EVENT e LEFT JOIN SCHEDULING r ON r.id = e.FK_SERIES WHERE (e.START_DATE >= ? AND e.END_DATE <= ?) OR (r.START <= ? AND r.END >= ?)", (from_date, to_date, from_date, to_date,))

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
    def findByUser(user, date = None):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        if date is None:
            date = datetime.datetime.now().replace(microsecond=0)

        to_date = datetime.datetime(date.year, date.month, date.day, 23, 59)

        c.execute("SELECT * FROM EVENT WHERE FK_CREATOR = ? AND START_DATE >= ? AND END_DATE <= ?", (user._id, date, to_date,))
        list = c.fetchall()
        connection.close()

        eventList = []
        for result in list:
            eventList.append(EventType.convert(result))

        return eventList

    @staticmethod
    def createEventTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("CREATE TABLE `EVENT` (`ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,`DESCRIPTION`	TEXT,`START_DATE`	TEXT,`END_DATE`	TEXT,`PRIVATE`	INTEGER,`FK_CREATOR`	INTEGER,`FK_TYPE`	INTEGER,`FK_SERIES`	INTEGER,FOREIGN KEY(`PRIVATE`) REFERENCES PRIVACY(ID),FOREIGN KEY(`FK_TYPE`) REFERENCES TYPES(ID),FOREIGN KEY(`FK_SERIES`) REFERENCES SCHEDULING(ID))")
        except sqlite3.OperationalError as err:
            print("CREATE TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    @staticmethod
    def dropEventTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("DROP TABLE EVENT")
        except sqlite3.OperationalError as err:
            print("DROP TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series)


class Birthday(Event):
    def __init__(self, id, description, start, end, private, creator, series, params):
        Event.__init__(self, id, description, start, end, private, creator, EventType.getTypeIdByName("birthday"), series)

        self._params = params

    @staticmethod
    def fromResultToObject(result):
        identity = result[0]
        params = EventParameter.loadParameterById(identity)

        start = None
        end = None

        if result[2] is not None:
            start = datetime.datetime.strptime(result[2], "%Y-%m-%d %H:%M:%S")

        if result[3] is not None:
            end = datetime.datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S")

        event = Birthday(result[0], result[1], start, end, result[4], result[5], result[7], params)
        return event

    def create(self):
        event = super(Birthday, self).create()

        for paramKey in self._params:
            EventParameter.insert(event._id, paramKey, self._params[paramKey])

        return self

    def update(self):
        super(Birthday, self).update()

    def delete(self):
        super(Birthday, self).delete()
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("DELETE FROM EVENT_PARAMETER WHERE FK_EVENT = ?", (self._id,))

        connection.commit()
        connection.close()
        return True

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, PARAMS=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series, self._params)


class Shopping(Event):
    def __init__(self, id, description, start, end, private, creator, series, params):
        Event.__init__(self, id, description, start, end, private, creator, EventType.getTypeIdByName("shopping"), series)
        self._params = params

    @staticmethod
    def fromResultToObject(result):
        identity = result[0]

        params = EventParameter.loadParameterById(identity)

        start = None
        end = None

        if result[2] is not None:
            start = datetime.datetime.strptime(result[2], "%Y-%m-%d %H:%M:%S")

        if result[3] is not None:
            end = datetime.datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S")

        event = Shopping(result[0], result[1], start, end, result[4], result[5], result[7], params)
        return event

    def create(self):
        event = super(Shopping, self).create()

        for idx, item in enumerate(self._params):
            EventParameter.insert(event._id, "shopping_item"+str(idx), item)

        return self

    def update(self):
        super(Shopping, self).update()

    def delete(self):
        super(Shopping, self).delete()
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("DELETE FROM EVENT_PARAMETER WHERE FK_EVENT = ?", (self._id,))
        connection.commit()
        connection.close()

        return True

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, PARAMS=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series, self._params)


class EventParameter(object):

    @staticmethod
    def loadParameterById(id):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("SELECT * FROM EVENT_PARAMETER WHERE FK_EVENT = ?", (id,))
        results = c.fetchall()

        params = {}
        for obj in results:

            key = obj[2]
            val = obj[3]
            params[key] = val

        connection.close()

        return params

    @staticmethod
    def insert(eventId, key, value):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("INSERT INTO EVENT_PARAMETER VALUES(null, ?, ?, ?)",(eventId, key, value,))

        connection.commit()
        connection.close()

    @staticmethod
    def createEventParameterTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()
        try:
            c.execute("CREATE TABLE `EVENT_PARAMETER` (`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,`FK_EVENT`	INTEGER,`KEY`	TEXT,`VALUE`	TEXT,FOREIGN KEY(`FK_EVENT`) REFERENCES EVENT(ID));")
        except sqlite3.OperationalError as err:
            print("CREATE TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    @staticmethod
    def dropEventParameterTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("DROP TABLE EVENT_PARAMETER")
        except sqlite3.OperationalError as err:
            print("DROP TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()


class EventNotFoundException(Exception):
    pass


class EventType(object):
    def __init__(self):
        pass

    @staticmethod
    def convert(result):
        eventType = result[6];

        if eventType == 1:
            return Event.fromResultToObject(result)
        elif eventType == 2:
            return Birthday.fromResultToObject(result)
        elif eventType == 3:
            return Shopping.fromResultToObject(result)

    types = {1:'default', 2: 'birthday', 3: 'shopping'}

    @staticmethod
    def getTypeIdByName(name):
        for type in EventType.types:
            if EventType.types[type] == name:
                return type

        return None

    @staticmethod
    def getTypeNameById(id):
        try:
            return EventType.types[id]
        except KeyError:
            return None

    @staticmethod
    def createEventTypeTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("CREATE TABLE EVENT_TYPE(ID INTEGER PRIMARY KEY autoincrement, DEFINITION TEXT);")
        except sqlite3.OperationalError as err:
            print("CREATE TABLE WARNING: {0}".format(err))

        for key in EventType.types:
            c.execute("INSERT INTO EVENT_TYPE VALUES(?,?)", (key, EventType.types[key]))

        connection.commit()
        connection.close()

    @staticmethod
    def dropEventTypeTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("DROP TABLE EVENT_TYPE")
        except sqlite3.OperationalError as err:
            print("DROP TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    def __repr__(self):
        return "Event Types: %s" % (self.types)


class Privacy(object):
    def __init__(self):
        pass

    levels = {1:'public', 2:'private',3:'shared'}

    @staticmethod
    def getLevelsIdByName(name):
        for level in Privacy.levels:
            if Privacy.levels[level] == name:
                return level

        return None

    @staticmethod
    def getLevelsNameById(id):
        try:
            return Privacy.levels[id]
        except KeyError:
            return None

    @staticmethod
    def createPrivacyTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("CREATE TABLE PRIVACY(ID INTEGER PRIMARY KEY autoincrement, LEVEL TEXT);")
        except sqlite3.OperationalError as err:
            print("CREATE TABLE WARNING: {0}".format(err))

        for key in Privacy.levels:
            c.execute("INSERT INTO PRIVACY VALUES(?,?)", (key, Privacy.levels[key]))

        connection.commit()
        connection.close()

    @staticmethod
    def dropPrivacyTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("DROP TABLE PRIVACY")
        except sqlite3.OperationalError as err:
            print("DROP TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    def __repr__(self):
        return "States: %s" % (self.levels)


class Scheduling(object):

    def __init__(self, id, start, end, interval):
        self._id = id
        self._start = start
        self._end = end
        self._interval = interval

    @staticmethod
    def findById(id):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("SELECT * FROM SCHEDULING WHERE ID = ?", (id,))
        result = c.fetchone()

        connection.close()

        return Scheduling.fromResultToObject(result)

    @staticmethod
    def createSchedulingTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("CREATE TABLE SCHEDULING(ID INTEGER PRIMARY KEY autoincrement, START DATE, END DATE, INTERVAL TEXT);")
        except sqlite3.OperationalError as err:
            print("CREATE TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    def create(self):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("INSERT INTO SCHEDULING VALUES(?, ?, ?, ?)", (self._id, self._start, self._end, self._interval,))

        connection.commit()
        connection.close()

    def update(self, ):
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()
        c.execute("UPDATE SCHEDULING SET START = ?, END = ?, INTERVAL = ? WHERE ID = ?", (self._start,self._end, self._interval, self._id))
        connection.commit()
        connection.close()

    @staticmethod
    def dropSchedulingTable():
        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        try:
            c.execute("DROP TABLE SCHEDULING")
        except sqlite3.OperationalError as err:
            print("DROP TABLE WARNING: {0}".format(err))

        connection.commit()
        connection.close()

    @staticmethod
    def getNextDate(event):
        newEvent = copy.deepcopy(event)

        connection = sqlite3.connect(jarpis.database)
        c = connection.cursor()

        c.execute("SELECT * FROM SCHEDULING WHERE ID = ?", (newEvent._series,))

        result = c.fetchone()

        if result is None:
            return None

        schedule = Scheduling.fromResultToObject(result)

        newStart = Scheduling.addIntervalToDate(newEvent._start, schedule._interval)
        newEnd = Scheduling.addIntervalToDate(newEvent._end, schedule._interval)

        if newStart >= schedule._start and newEnd <= schedule._end:
            newEvent._start = newStart
            newEvent._end = newEnd
        else:
            return None

        connection.close()

        return newEvent

    @staticmethod
    def addIntervalToDate(date, interval):
        if interval == "daily":
            return date + relativedelta(days=1)
        elif interval == "weekly":
            return date + relativedelta(weeks=1)
        elif interval == "monthly":
            return date + relativedelta(months=1)
        elif interval == "yearly":
            return date + relativedelta(years=1)

    @staticmethod
    def getNextDates(event, count):
        dates = []

        for x in range(0, count):
            dates.append(Scheduling.getNextDate(event))

        return dates

    @staticmethod
    def fromResultToObject(result):

        start = None
        end = None

        if result[1] is not None:
            start = datetime.datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S")

        if result[2] is not None:
            end = datetime.datetime.strptime(result[2], "%Y-%m-%d %H:%M:%S")

        return Scheduling(result[0], start, end, result[3])
