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
            self._type = EventType.getTypeIdByName("default")
        else:
            self._type = type

        self._series = series

    @staticmethod
    def fromResultToObject(result):
        return Event(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])

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
        result = c.fetchone()

        if result is not None:
            return EventType.convert(result)

        raise EventNotFoundException("No Event found with given ID: %s" % (id))

    #TODO Move this to Calendar Class
    @staticmethod
    def findEventsByDate(from_date, to_date):
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT WHERE start_date > ? AND end_date < ?", (from_date, to_date,))

        eventList = []
        for result in c.fetchall():
            eventList.append(EventType.convert(result))

        return eventList

    # TODO Move this to Calendar Class
    @staticmethod
    def findAll():
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT")

        eventList = []
        for result in c.fetchall():
            eventList.append(EventType.convert(result))

        return eventList

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
    def fromResultToObject(result):
        identity = result[0]
        params = EventParameter.loadParameterById(identity)
        event = Birthday(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], params)
        return event

    def create(self):
        super(Birthday, self).create()

        c = conn.cursor()
        c.execute("SELECT last_insert_rowid()")
        result = c.fetchone()

        for paramKey in self._params:
            EventParameter.insert(result[0], paramKey, self._params[paramKey])

        conn.commit()
        return self

    def delete(self):
        super(Birthday, self).delete()
        c = conn.cursor()
        #TODO: Find out if sqlite supports delete cascade
        c.execute("DELETE FROM EVENT_PARAMETER WHERE FK_EVENT = ?", (self._id,))
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

    @staticmethod
    def convert(result):
        eventType = result[6];

        if eventType == 1:
            return Event.fromResultToObject(result)
        elif eventType == 2:
            return Birthday.fromResultToObject(result)

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
