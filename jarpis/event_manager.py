from jarpis.util import *

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