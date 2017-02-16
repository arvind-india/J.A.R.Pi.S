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
        print("i was called...")
        c = conn.cursor()
        c.execute("SELECT * FROM EVENT WHERE ID = ?", (id,))
        b = c.fetchone()

        if b != None:
            return Event(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7])

        raise EventNotFoundException("No Event found with given ID: %s" % (id))

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, SUPER=%s" % (
            self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series,
            super().__repr__())


class EventNotFoundException(Exception):
    pass


class DBUtil():
    result = None

    @staticmethod
    def exec(callback, *args):
        global conn
        conn = sqlite3.connect("develop.db")
        result = callback(*args)
        conn.close()

        return result
