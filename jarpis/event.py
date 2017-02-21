import sqlite3

conn = None


class Event(object):
    def __init__(self, id, description, start, end, private, creator, type, series):
        self._id = id
        self._description = description
        self._start = start
        self._end = end
        self._private = private
        self._creator = creator
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
        c.execute("CREATE TABLE EVENT(ID INTEGER,DESCRIPTION INTEGER,START_DATE TEXT,END_DATE TEXT,PRIVATE INTEGER,FK_CREATOR INTEGER,FK_TYPE INTEGER,FK_SERIES INTEGER)")
        conn.commit()

    @staticmethod
    def dropEventTable():
        c = conn.cursor()
        c.execute("DROP TABLE EVENT")
        conn.commit()

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, SUPER=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series,
            super().__repr__())


class EventNotFoundException(Exception):
    pass


class Privacy(object):
    def __init__(self):
        pass

    states = {}
    states['1'] = "public"
    states['2'] = "private"
    states['3'] = "shared"

    @staticmethod
    def createPrivacyTable():
        c = conn.cursor()
        c.execute("CREATE TABLE PRIVACY(ID INT PRIMARY KEY, TYPE TEXT);")
        conn.commit()

    @staticmethod
    def dropPrivacyTable():
        c = conn.cursor()
        c.execute("DROP TABLE PRIVACY")
        conn.commit()

    def __repr__(self):
        return "States: %s" % (self.states)


class DBUtil():
    result = None

    @staticmethod
    def exec(function, params):
        global conn
        conn = sqlite3.connect("develop.db")
        result = function(*params)
        conn.close()

        return result


class TestDBUtil():
    result = None

    @staticmethod
    def exec(function, params):
        global conn
        conn = sqlite3.connect("test.db")
        result = function(*params)
        conn.close()

        return result
