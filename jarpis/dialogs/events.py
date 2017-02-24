class EventMediator:
    def __init__(self):
        self._eventHandlers = {}

    def register(self, event, handler):
        if event not in self._eventHandlers:
            self._eventHandlers[event] = []

        self._eventHandlers[event].append(handler)

    def unregister(self, event, handler):
        if event not in self._eventHandlers:
            return

        self._eventHandlers[event].remove(handler)

    def broadcast(self, event, **kwargs):
        if event not in self._eventHandlers:
            return

        for handler in self._eventHandlers[event]:
            handler(kwargs)
