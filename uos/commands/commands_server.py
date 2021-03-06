from .basecommand import BaseCommand
from ..uos import UOS


class ServerCommands(BaseCommand):
    def command_mail(self):
        if not self.clearance(1):
            return

        print('invoke the mail utility')

    def command_mail_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "MAIL",
                         "MAIL ?"])

    def command_set_host(self):
        if not self.clearance(1):
            return

        print('try to connect to a network')
