from types import SimpleNamespace
from .default import DefaultCommands
from .admin import AdminCommands
from .user import UserCommands
from ..uos import UOS

class Commands:
    link = SimpleNamespace(state = None, interval = -1)
    group_user = ['admin', 'user', 'maintainence']
    group_admin = ['admin', 'maintainence']
    is_init = False

    @classmethod
    def init(cls):
        if not cls.is_init:
            cls.is_init = True
            cls.default = DefaultCommands(cls.link)
            cls.admin = AdminCommands(cls.link)
            cls.user = UserCommands(cls.link)

    @classmethod
    def cat_command(cls, text, group, cat):
        if UOS.User.name:
            if UOS.User.current.group in group:
                key, command = cls.find_key(text, cat)
                if key:
                    cls.call_command(command, cls.call_args(key, text))
                    return True
        return False

    @classmethod
    def default_command(cls, text):
        key, command = cls.find_key(text, cls.default)
        if key:
            cls.call_command(command, cls.call_args(key, text))
            return True
        return False

    @classmethod
    def call(cls, parent, text):
        cls.link.action = parent.parent.state
        cls.link.parent = parent
        cls.link.writer = parent.writer
        if cls.link.state:
            cls.call_command(cls.link.state, cls.call_args(None, text))
        else:
            if not cls.cat_command(text, cls.group_admin, cls.admin):
                if not cls.cat_command(text, cls.group_user, cls.user):
                    if not cls.default_command(text):
                        writer.add('ERROR_INVALID_FUNCTION', 30)

    @staticmethod
    def call_args(key, text):
        if key:
            text = text.lstrip(key).strip()

        if ' ' in text:
            return text.split(' ')
        elif len(text) > 0:
            return text

    @classmethod
    def call_command(cls, command, args):
        if args:
            if isinstance(args, (tuple, list)) and len(args) > 1:
                try:
                    command(*args)
                except TypeError as error:
                    cls.error_guard(error, cls.link.writer)
            else:
                try:
                    command(args)
                except TypeError as error:
                    cls.error_guard(error, cls.link.writer)
        else:
            try:
                command()
            except TypeError as error:
                cls.error_guard(error, cls.link.writer)

    @staticmethod
    def error_guard(error, writer):
        print(error)
        error = ''.join(error.args).split(' ')
        print(error)
        c = error[0].lstrip('command_').rstrip('()').upper()
        if 'missing' in error:
            writer.add("{0} is missing {1} arguments".format(c, error[2]), 40)
        elif 'takes' in error:
            writer.add("{0} takes {1} arguments".format(c, int(error[2]) - 2), 40)
        else:
            writer.add("Error: " + error, 40)

    @staticmethod
    def find_key(line, commands):
        line = line.split(' ')
        for key in commands.keys:
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
                return key, commands.command_list[key]

        return None, None
