import sqlite3

conn = None

class Event(object):
    def __init__(self, id, description, start, end, private, creator, type, series):
        self._id = id
        self._description = description
        self._start = start
        self._end = end

## WTF VALIDATION STARTS: im open for smarter solutions... ##
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
## WTF VALIDATION ENDS ##

        self._creator = creator

        if type is None:
            self.type = EventType.getTypeIdByName("default")
        else:
            self._type = type

        self._series = series

    @staticmethod
    def fromResultToObject(obj):
        return Event(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7])

    def create(self):
        c = conn.cursor()
        c.execute(
            "INSERT INTO EVENT (ID, DESCRIPTION, START_DATE, END_DATE, PRIVATE, FK_CREATOR, FK_TYPE, FK_SERIES) VALUES(?,?,?,?,?,?,?,?)",
            (self._id, self._description, self._start, self._end, self._private, self._creator, self._type,
             self._series))
        conn.commit()
        return self

    def delete(self):
        c = conn.cursor()
        c.execute("DELETE FROM EVENT WHERE ID = ?", (self._id,))
        conn.commit()
        return True

    def update(self):
        return "Event updated!"

    @staticmethod
    def findOneById(id):
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT WHERE ID = ?", (id,))
        b = c.fetchone()

        if b is not None:
            return Event.fromResultToObject(b)

        raise EventNotFoundException("No Event found with given ID: %s" % (id))

    @staticmethod
    def findEventsByDate(from_date, to_date):
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT WHERE start_date > ? AND end_date < ?", (from_date, to_date,))

        resultList = []
        for obj in c.fetchall():
            resultList.append(Event.fromResultToObject(obj))

        return resultList

    @staticmethod
    def createEventTable():
        c = conn.cursor()
        try:
            c.execute("CREATE TABLE EVENT(ID INTEGER,DESCRIPTION INTEGER,START_DATE TEXT,END_DATE TEXT,PRIVATE INTEGER,FK_CREATOR INTEGER,FK_TYPE INTEGER,FK_SERIES INTEGER)")
        except sqlite3.OperationalError as err:
            print("CREATE TBALE WARNING: {0}".format(err))

        conn.commit()

    @staticmethod
    def dropEventTable():
        c = conn.cursor()
        try:
            c.execute("DROP TABLE EVENT")
        except sqlite3.OperationalError as err:
            print("DROP TBALE WARNING: {0}".format(err))
        conn.commit()

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, SUPER=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series,
            super(*args, **kwargs).__repr__())


class Birthday(Event):
    def __init__(self, id, description, start, end, private, creator, type, series, subject):
        Event.__init__(self, id, description, start, end, private, creator, type, series)
        self._subject = subject

class EventNotFoundException(Exception):
    pass

class EventType(object):
    def __init__(self):
        pass

    types = {1:'default', 2: 'birthday'}

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
        c = conn.cursor()

        try:
            c.execute("CREATE TABLE EVENT_TYPE(ID INT PRIMARY KEY, DEFINITION TEXT);")
        except sqlite3.OperationalError as err:
            print("CREATE TBALE WARNING: {0}".format(err))

        for key in EventType.types:
            c.execute("INSERT INTO EVENT_TYPE VALUES(?,?)", (key, EventType.types[key]))

        conn.commit()

    @staticmethod
    def dropEventTypeTable():
        c = conn.cursor()

        try:
            c.execute("DROP TABLE EVENT_TYPE")
        except sqlite3.OperationalError as err:
            print("DROP TBALE WARNING: {0}".format(err))

        conn.commit()

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
        c = conn.cursor()

        try:
            c.execute("CREATE TABLE PRIVACY(ID INT PRIMARY KEY, LEVEL TEXT);")
        except sqlite3.OperationalError as err:
            print("CREATE TBALE WARNING: {0}".format(err))

        for key in Privacy.levels:
            c.execute("INSERT INTO PRIVACY VALUES(?,?)", (key, Privacy.levels[key]))

        conn.commit()

    @staticmethod
    def dropPrivacyTable():
        c = conn.cursor()

        try:
            c.execute("DROP TABLE PRIVACY")
        except sqlite3.OperationalError as err:
            print("DROP TBALE WARNING: {0}".format(err))

        conn.commit()

    def __repr__(self):
        return "States: %s" % (self.levels)


class DBUtil():
    result = None

    @staticmethod
    def execute(function, params):
        global conn
        conn = sqlite3.connect("develop.db")
        result = function(*params)
        conn.close()

        return result


class TestDBUtil():
    result = None

    @staticmethod
    def execute(function, params):
        global conn
        conn = sqlite3.connect("test.db")
        result = function(*params)
        conn.close()

        return result
