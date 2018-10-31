from queue import Queue

class EventBus:
    def __init__(self, uos):
        self._queue = Queue()
        self._listener = {}
        self._register = {}
        self.uos = uos

    def fetch(self, name, *args, **kwargs):
        return self._register[name](*args, **kwargs)

    def listener(self, event_type, callback):
        self._listener[event_type] = callback

    def register_event(self, event, *args, **kwargs):
        self._queue.put((event, args, kwargs))

    def register_function(self, name, function):
        self._register[name] = function

    def process(self):
        while not self._queue.empty():
            event_type, args, kwargs = self._queue.get()
            if self._listener.get(event_type, False):
                self._listener[event_type](*args, **kwargs)
            self._queue.task_done()
