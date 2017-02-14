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
        return "Event created!"

    def delete(self):
        return "Event deleted!"

    def update(self):
        return "Event updated!"