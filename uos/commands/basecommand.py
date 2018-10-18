import os
from types import SimpleNamespace

class BaseCommand:
    def __init__(self, link):
        self.link = link
        self.keys = sorted(self.command_list.keys(), reverse=True)
        self.info = SimpleNamespace(
            attempts = 0,
            data = None,
            name = None,
            group = None,
            filepath = None)

    def clear_info(self):
        self.info.attempts = 0
        self.info.data = None
        self.info.name = None
        self.info.group = None
        self.info.filepath = None

    def writer_add(self, text, *args, **kwargs):
        if args == () and 'interval' not in kwargs.keys():
            args = self.link.interval,

        self.link.writer.add(text, *args, **kwargs)

    def writer_clear(self):
        self.link.writer.clear()
