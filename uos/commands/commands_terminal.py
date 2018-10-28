import time
from .basecommand import BaseCommand
from ..uos import UOS


class TerminalCommands(BaseCommand):
    def command_clear(self):
        self.writer_clear()

    def command_show_time(self):
        self.writer_clear()
        self.writer_add(str(time.ctime()))
