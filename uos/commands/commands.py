from types import SimpleNamespace
from .commands_admin import AdminCommands
from .commands_filesystem import FilesystemCommands
from .commands_menu import MenuCommands
from .commands_server import ServerCommands
from .commands_systems import SystemCommands
from .commands_terminal import TerminalCommands
from .commands_test import TestCommands
from .commands_user import UserCommands

from ..uos import UOS

class Command:
    def __init__(self):
        self.link = SimpleNamespace(state = None, interval = -1)

        self.cmd_admin = AdminCommands(self.link)
        self.cmd_filesystem = FilesystemCommands(self.link)
        self.cmd_menu = MenuCommands(self.link)
        self.cmd_server = ServerCommands(self.link)
        self.cmd_system = SystemCommands(self.link)
        self.cmd_terminal = TerminalCommands(self.link)
        self.cmd_test = TestCommands(self.link)
        self.cmd_user = UserCommands(self.link)

        self.command_call = {}
        replace = [('_', ' '), ('7','/'), ('1', '-'), ('0', '.')]
        for commands in [getattr(self, cmd) for cmd in vars(self) if cmd.startswith('cmd_')]:
            for command in [cmd for cmd in dir(commands) if cmd.startswith('command_')]:
                # build the commands
                c = command[8:]
                for a, b in replace:
                    c = c.replace(a, b)

                self.command_call[c.upper()] = getattr(commands, command)

        self.command_keys = sorted(self.command_call.keys(), reverse=True)

    def __call__(self, parent, text, single=False):
        if single:
            self.link.action = parent.state
        else:
            self.link.action = parent.parent.state

        self.link.parent = parent
        self.link.writer = parent.writer
        if self.link.state:
            self.call_command(self.link.state, self.call_args(None, text))
        else:
            key, command = self.find_key(text)
            if key:
                self.call_command(command, self.call_args(key, text))
            else:
                self.link.writer.add('ERROR INVALID FUNCTION')

    def call_args(self, key, text):
        if key:
            text = text[len(key):].strip()

        if ' ' in text:
            return text.split(' ')
        elif len(text) > 0:
            return text

    def call_command(self, command, args):
        if args:
            if isinstance(args, (tuple, list)) and len(args) > 1:
                try:
                    command(*args)
                except TypeError as error:
                    self.error_guard(error)
            else:
                try:
                    command(args)
                except TypeError as error:
                    self.error_guard(error)
        else:
            try:
                command()
            except TypeError as error:
                self.error_guard(error)

    def error_guard(self, error):
        #print(error)
        error = ''.join(error.args).split(' ')
        #print(error)
        if error[0].startswith('command_'):
            error[0] = error[0][8:]

        c = error[0].rstrip('()').upper()
        if '_' in c:
            c = ' '.join(c.split('_'))

        if 'missing' in error:
            self.link.writer.add("{0} is missing {1} arguments".format(c, error[2]), 40)
        elif 'takes' in error:
            self.link.writer.add("{0} takes {1} arguments".format(c, int(error[2]) - 2), 40)
        else:
            self.link.writer.add("Error: " + ' '.join(error))

    def find_key(self, line):
        line = line.split(' ')
        for key in self.command_keys:
            skey = key.split(' ')
            boolean = True
            for i, k in enumerate(skey):
                if len(line) > i:
                    if line[i] != k:
                        boolean = False
                        break
                else:
                    boolean = False
                    break

            if boolean:
                return key, self.command_call[key]

        return None, None
