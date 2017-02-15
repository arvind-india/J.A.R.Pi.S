from jarpis import conn

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
        c.execute("INSERT INTO EVENT (ID, DESCRIPTION, START_DATE, END_DATE, PRIVATE, FK_CREATOR, FK_TYPE, FK_SERIES) VALUES(?,?,?,?,?,?,?,?)", (self._id,self._description,self._start,self._end,self._private,self._creator,self._type,self._series))
        conn.commit()
        conn.close()
        return self

    def delete(self):
        return "Event deleted!"

    def update(self):
        return "Event updated!"

    @staticmethod
    def findOneById(id):
        c = conn.cursor()
        a = c.execute("SELECT * FROM EVENT WHERE ID = ?", (id,))
        b = c.fetchone()
        c.close()

        if b != None:
            return Event(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7])

        raise EventNotFoundException("No Event found with given ID: %s" % (id))

    def __repr__(self, *args, **kwargs):
        return "ID=%s, Description=%s, START=%s, END=%s, PRIVATE=%s, CREATOR=%s, TYPE=%s, SERIES=%s, SUPER=%s" % (self._id, self._description, self._start, self._end, self._private, self._creator, self._type, self._series, super().__repr__())

class EventNotFoundException(Exception):
    pass