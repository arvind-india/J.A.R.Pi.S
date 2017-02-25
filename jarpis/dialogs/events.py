class EventMediator:

    def __init__(self):
        self._eventHandlers = {}

    def register(self, event, handler):
        if event is None or handler is None:
            raise TypeError()

        # TODO try "value = value | literal" syntax
        if event not in self._eventHandlers:
            self._eventHandlers[event] = []

        if handler in self._eventHandlers[event]:
            raise DuplicateEventHandler()

        self._eventHandlers[event].append(handler)

    def unregister(self, event, handler):
        if event is None or handler is None:
            raise TypeError()

        if event not in self._eventHandlers:
            return

        if handler not in self._eventHandlers[event]:
            return

        self._eventHandlers[event].remove(handler)

    def publish(self, event, **with_kwargs):
        if event is None:
            raise TypeError()

        if event not in self._eventHandlers:
            return

        # this will also be the perfect point to trigger a web view update if
        # there's an appropriate 'success' event
        for callHandler in self._eventHandlers[event]:
            callHandler(**with_kwargs)


class DuplicateEventHandler(Exception):
    pass
