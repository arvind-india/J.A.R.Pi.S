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

    #TODO Move this to Calendar Class
    @staticmethod
    def findOneById(id):
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT WHERE ID = ?", (id,))
        b = c.fetchone()

        if b is not None:
            eventType = b[6];

            if eventType == 1:
                print("Im here 1")
                return Event.fromResultToObject(b)
            elif eventType == 2:
                print("Im here 2")
                return Birthday.fromResultToObject(b)

        raise EventNotFoundException("No Event found with given ID: %s" % (id))

    #TODO Move this to Calendar Class
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
            c.execute("CREATE TABLE EVENT(ID INTEGER PRIMARY KEY autoincrement,DESCRIPTION INTEGER,START_DATE TEXT,END_DATE TEXT,PRIVATE INTEGER,FK_CREATOR INTEGER,FK_TYPE INTEGER,FK_SERIES INTEGER)")
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
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series)


class Birthday(Event):
    def __init__(self, id, description, start, end, private, creator, type, series, params = {}):
        Event.__init__(self, id, description, start, end, private, creator, type, series)
        self._params = params

    @staticmethod
    def fromResultToObject(obj):
        id = obj[0]
        params = EventParameter.loadParameterById(id)
        ev = Birthday(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], params)
        return ev

    def create(self):
        c = conn.cursor()
        c.execute(
            "INSERT INTO EVENT (ID, DESCRIPTION, START_DATE, END_DATE, PRIVATE, FK_CREATOR, FK_TYPE, FK_SERIES) VALUES(?,?,?,?,?,?,?,?)",
            (self._id, self._description, self._start, self._end, self._private, self._creator, self._type,
             self._series))

        c.execute("SELECT last_insert_rowid()")
        b = c.fetchone()

        for paramKey in self._params:
            EventParameter.insert(b[0], paramKey, self._params[paramKey])

        conn.commit()
        return self

    def delete(self):
        c = conn.cursor()
        c.execute("DELETE FROM EVENT WHERE ID = ?", (self._id,))
        #TODO: Find out if sqlite supports delete cascade
        c.execute("DELETE FROM EVENT_PARAMETER WHERE FK_EVENT = ?", (self.__id,))
        conn.commit()
        return True

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, PARAMS=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series, self._params)


class EventParameter(object):
    @staticmethod
    def loadParameterById(id):
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT_PARAMETER WHERE FK_EVENT = ?", (id,))

        params = {}
        for obj in c.fetchall():
            key = obj[2]
            val = obj[3]
            params[key] = val

        return params

    @staticmethod
    def insert(eventId, key, value):
        c = conn.cursor()
        c.execute("INSERT INTO EVENT_PARAMETER VALUES(null, ?, ?, ?)",(eventId, key, value,))
        conn.commit()

    @staticmethod
    def createEventParameterTable():
        c = conn.cursor()
        try:
            c.execute("CREATE TABLE EVENT_PARAMETER(ID INTEGER PRIMARY KEY autoincrement,FK_EVENT INTEGER, KEY TEXT,VALUE TEXT)")
        except sqlite3.OperationalError as err:
            print("CREATE TBALE WARNING: {0}".format(err))

        conn.commit()

    @staticmethod
    def dropEventParameterTable():
        c = conn.cursor()
        try:
            c.execute("DROP TABLE EVENT_PARAMETER")
        except sqlite3.OperationalError as err:
            print("DROP TBALE WARNING: {0}".format(err))
        conn.commit()

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
            c.execute("CREATE TABLE EVENT_TYPE(ID INTEGER PRIMARY KEY autoincrement, DEFINITION TEXT);")
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
            c.execute("CREATE TABLE PRIVACY(ID INTEGER PRIMARY KEY autoincrement, LEVEL TEXT);")
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
