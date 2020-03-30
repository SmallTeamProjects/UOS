from .commands_admin import AdminCommands
from .commands_filesystem import FilesystemCommands
from .commands_menu import MenuCommands
from .commands_server import ServerCommands
from .commands_systems import SystemCommands
from .commands_terminal import TerminalCommands
from .commands_test import TestCommands
from .commands_user import UserCommands

from ..uos import UOS

class CommandLink:
    def __init__(self, state=None, interval=-1):
        self.state = state
        self.interval = interval

class Command:
    def __init__(self):
        self.link = CommandLink(state = None, interval = -1)

        self.cmd_admin = AdminCommands(self.link)
        self.cmd_filesystem = FilesystemCommands(self.link)
        self.cmd_menu = MenuCommands(self.link)
        self.cmd_server = ServerCommands(self.link)
        self.cmd_system = SystemCommands(self.link)
        self.cmd_terminal = TerminalCommands(self.link)
        self.cmd_test = TestCommands(self.link)
        self.cmd_user = UserCommands(self.link)

        self.command_call = {
            # Admin commands
            "CREATE USER": self.cmd_admin.command_create_user,
            "DELETE USER": self.cmd_admin.command_delete_user,
            "RUN DEBUG": self.cmd_admin.command_run_debug,
            "RUN DEBUG/ACCOUNTS.F": self.cmd_admin.command_run_debug_accounts,
            "SET DEFAULT": self.cmd_admin.command_set_default,
            "SHOW USERS": self.cmd_admin.command_show_users,

            # Filesystem commands
            "CREATE ?": self.cmd_filesystem.command_create_help,
            "CREATE DIR": self.cmd_filesystem.command_create_dir,
            "CREATE FILE": self.cmd_filesystem.command_create_file,
            "CHANGE DIR": self.cmd_filesystem.command_change_dir,
            "DELETE DIR": self.cmd_filesystem.command_delete_dir,
            "DELETE FILE": self.cmd_filesystem.command_delete_file,
            "DELETE ?": self.cmd_filesystem.command_delete_help,
            "EDIT FILE": self.cmd_filesystem.command_edit_file,
            "EDIT ?": self.cmd_filesystem.command_edit_help,
            "MOUNT": self.cmd_filesystem.command_mount,
            "MOVE DIR": self.cmd_filesystem.command_move_dir,
            "MOVE FILE": self.cmd_filesystem.command_move_file,
            "RENAME DIR": self.cmd_filesystem.command_rename_dir,
            "RENAME FILE": self.cmd_filesystem.command_rename_file,
            "RENAME ?": self.cmd_filesystem.command_rename_help,

            # Menu commands
            "MENU": self.cmd_menu.command_menu,
            "MENU ADD": self.cmd_menu.command_menu_add,
            "MENU EDIT": self.cmd_menu.command_menu_edit,
            "MENU REMOVE": self.cmd_menu.command_menu_remove,
            "MENU RESET": self.cmd_menu.command_menu_reset,

            # Server commands
            "MAIL": self.cmd_server.command_mail,
            "SET HOST": self.cmd_server.command_set_host,

            # System commands
            "EXIT": self.cmd_system.command_exit,
            "LOGON": self.cmd_system.command_logon,
            "LOGON ?": self.cmd_system.command_logon_help,
            "LOGOFF": self.cmd_system.command_logoff,
            "LOGOFF ?": self.cmd_system.command_logoff_help,
            "SETUP": self.cmd_system.command_setup,
            "HALT": self.cmd_system.command_set_halt,
            "HALT RESTART": self.cmd_system.command_set_halt_restart,

            # Terminal commands
            "CLEAR": self.cmd_terminal.command_clear,
            "SHOW TIME": self.cmd_terminal.command_show_time,

            # User commands
            "RENAME USER": self.cmd_user.command_rename_user,
            "RUN FILE": self.cmd_user.command_run_file,
            "RUN ?": self.cmd_user.command_run_help,
            "SET DIR/PROTECTION-OWNER": self.cmd_user.command_set_dir_protection_owner,
            "SET DIR/PROTECTION-PASSWORD": self.cmd_user.command_set_dir_protection_password,
            "SET FILE/PROTECTION-OWNER": self.cmd_user.command_set_file_protection_owner,
            "SET FILE/PROTECTION-OWNER.RWED ACCOUNTS.F": self.cmd_user.command_set_file_protection_owner_rwed_accounts,
            "SET FILE/PROTECTION-PASSWORD": self.cmd_user.command_set_file_protection_password,
            "SET INTERVAL":self.cmd_user.command_set_interval,
            "SET TERMINAL COLOR": self.cmd_user.command_set_terminal_color,
            "SET TERMINAL HEADER": self.cmd_user.command_set_header,
            "SET TERMINAL/INQUIRE": self.cmd_user.command_set_terminal_inquire,
            "SET TERMINAL INTERVAL":self.cmd_user.command_set_interval,
            "SET TERMINAL VOLUME":self.cmd_user.command_set_volume,
            "SET ?": self.cmd_user.command_set_help,
            "SHOW DEFAULT": self.cmd_user.command_show_default,
            "SHOW DEVICE": self.cmd_user.command_show_device,
            "SHOW DEVICE/FULL": self.cmd_user.command_show_device_full,
            "SHOW PROCESS": self.cmd_user.command_show_process,
            "SHOW PROCESS/ALL": self.cmd_user.command_show_process_all,
            "SHOW ?": self.cmd_user.command_show_help,
            "HELP": self.cmd_user.command_help,
            "?": self.cmd_user.command_help,

            # Test commands
            "MINIGAME": self.cmd_test.command_minigame
        }

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
