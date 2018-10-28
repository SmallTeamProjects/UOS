import os
from types import SimpleNamespace
from ..uos import UOS

class BaseCommand:
    def __init__(self, link):
        self.link = link
        self.info = SimpleNamespace(
            attempts = 0,
            data = None,
            name = None,
            group = None,
            filepath = None)

    def clearance(self, level, bypass=None):
        if level == 1:
            boolean = UOS.user.name is not None
        elif level == 2:
            boolean = UOS.user.has_privilege()
        elif level == 3:
            boolean = UOS.user.is_admin()

        if not boolean:
            if bypass == UOS.bypass:
                UOS.bypass += 1
            else:
                self.writer_add("Clearance Denied")
                UOS.bypass = 0
        elif UOS.bypass != 0:
            UOS.bypass = 0

        return boolean

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
