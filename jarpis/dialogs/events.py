class EventMediator:

    def __init__(self):
        self._eventHandlers = {}

    def register(self, event, handler):
        # TODO try "value = value | literal" syntax
        if event not in self._eventHandlers:
            self._eventHandlers[event] = []

        self._eventHandlers[event].append(handler)

    def unregister(self, event, handler):
        if event not in self._eventHandlers:
            return

        self._eventHandlers[event].remove(handler)

    def publish(self, event, **kwargs):
        if event not in self._eventHandlers:
            return

        # this will also be the perfect point to trigger a web view update if
        # there's an appropriate 'success' event
        for handler in self._eventHandlers[event]:
            handler(kwargs)
