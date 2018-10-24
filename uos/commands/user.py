from .basecommand import BaseCommand
from ..uos import UOS
from .user_menu import UserMenu
from .user_filesystem import UserFilesystem


class UserCommands(BaseCommand, UserFilesystem, UserMenu):
    def __init__(self, link):

        self.command_list = {
            'EXIT': self.command_exit,
            'LOGOFF': self.command_logoff,
            'LOGOFF ?': self.command_logoff_help,
            'MAIL': self.command_mail,
            'RENAME USER': self.command_rename_user,
            'RUN FILE': self.command_run_file,
            'RUN ?': self.command_run_help,
            'SET COLOR': self.command_set_color,
            'SET DIR/PROTECTION-OWNER': self.command_set_dir_protection_owner,
            'SET DIR/PROTECTION-PASSWORD': self.command_set_dir_protection_password,
            'SET FILE/PROTECTION-OWNER': self.command_set_file_protection_owner,
            'SET FILE/PROTECTION-OWNER.RWED ACCOUNTS.F': self.command_set_file_protection_owner_rwed,
            'SET FILE/PROTECTION-PASSWORD': self.command_set_file_protection_password,
            'SET HALT': self.command_set_halt,
            'SET HALT/RESTART': self.command_set_halt_restart,
            'SET HALT/RESTART MAINT' : self.command_set_halt_restart_maintainence,
            'SET HOST': self.command_set_host,
            'SET INTERVAL':self.command_set_interval,
            'SET TERMINAL COLOR': self.command_set_terminal_color,
            'SET TERMINAL HEADER': self.command_set_header,
            'SET TERMINAL/INQUIRE': self.command_set_inquire,
            'SET TERMINAL INTERVAL':self.command_set_interval,
            'SET ?': self.command_set_help,
            'SHOW DEFAULT': self.command_show_default,
            'SHOW DEVICE': self.command_show_device,
            'SHOW DEVICE/FULL': self.command_show_device_full,
            'SHOW PROCESS': self.command_show_process,
            'SHOW PROCESS/ALL': self.command_show_process_all,
            'SHOW ?': self.command_show_help,
            'HELP': self.command_help,
            '?': self.command_help,
        }

        self.command_list.update(self.user_filesystem_commands())
        self.command_list.update(self.user_menu_commands())
        BaseCommand.__init__(self, link)

    def command_exit(self):
        print('terminate a script')

    def command_logoff(self):
        self.writer_clear()
        self.writer_add( ["...Checking Clearance..........",
                          "...AUTHORIZED.................",
                          "...Locking Mechanism Enable..."] )
        UOS.user.set(None)

    def command_logoff_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                          "LOGOFF",
                          "     USERNAME",
                          "LOGOFF ?"] )

    def command_mail(self):
        print('invoke the mail utility')

    def command_rename_user(self, username, newname):
        if UOS.user.name == username or UOS.drive.current.group == 'admin':
            value = UOS.user.rename(username, newname)
            if value == 1:
                self.writer_add('{0} has been rename to {1}'.format(username, newname))
            elif value == 2:
                self.writer_add("{0} already taken".format(newname))
            else:
                self.writer_add("{0} doesn't exists".format(username))

    def command_run_file(self, filename, filetype, location=None):
        # work on linux
        program = UOS.drive.Path((filename, filetype), location)
        if program.exists():
            FILETYPES = {'py':'python'}
            if filetype in FILETYPES.keys():
                subprocess.call([FILETYPES[filetype], program])
            else:
                self.writer_add('Unsupported type ' + filetype)

    def command_run_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "RUN FILE",
                     "     FILENAME",
                     "          FILETYPE",
                     "               LOCATION",
                     "RUN DEBUG"
                     "    /FILENAME",
                     "RUN ?"])

    def command_set_dir_protection_owner(self):
        print('directory can only be opened by owner')

    def command_set_dir_protection_password(self):
        print('directory can only be opened by entering a password')

    def command_set_file_protection_owner(self):
        print('file can only be opened by owner')

    def command_set_file_protection_owner_rwed(self):
        print('generate list of words that are similar to the password of the last logged user')
        #2nd step to running hacking minigame

    def command_set_file_protection_password(self):
        print('file can only be opened by entering a password')

    def command_set_halt(self, name):
        UOS.user.set(None)
        print('shutdown', name)

    def command_set_halt_restart(self):
        UOS.user.set(None)
        self.link.action.flip('Loading')

    def command_set_halt_restart_maintainence(self):
        print('reset into maintainence mode')
        # 3rd step to running hacking minigame

    def command_set_host(self):
        print('try to connect to a network')

    def command_set_interval(self, interval):
        if interval.isdigit():
            UOS.interval = int(interval)
            UOS.settings.interval = int(interval)
            UOS.save_settings()
        else:
            self.writer_add("Intervals must be a number")

    def command_set_color(self, color):
        if color in UOS.color.COLORS:
            UOS.user.current.color = color
            UOS.user.save()
            UOS.color.change_color(color)
        else:
            self.writer_add("Invalid color")

    def command_set_header(self, *args):
        UOS.settings.header = ' '.join(args)
        UOS.save_settings()

    def command_set_inquire(self):
        self.writer_clear()
        self.writer_add('RIT-V300')
        # 1st step to running hacking minigame

    def command_set_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "SET HALT",
                     "    /RESTART",
                     "    /RESTART MAINT",
                     "SET HOST",
                     "    HOSTNAME",
                     "SET TERMINAL",
                     "    /INQUIRE",
                     "     HEADER",
                     "     COLOR",
                     "SET DEFAULT",
                     "SET FILE",
                     "    /PROTECTION-OWNER",
                     "    /PROTECTION-PASSWORD",
                     "SET DIR",
                     "    /PROTECTION-OWNER",
                     "    /PROTECTION-PASSWORD",
                     "SET ?"])

    def command_set_terminal_color(self, color):
        if color in UOS.color.COLORS:
            UOS.settings.color = color
            UOS.save_settings()
            UOS.user.current.color = color
            UOS.user.save()
            UOS.color.change_color(color)
        else:
            self.writer_add("Invalid color")

    def command_show_default(self):
        self.writer_add('current directory: ' + UOS.drive.path.current)

    def command_show_device(self):
        print('return basic system info')

    def command_show_device_full(self):
        print('return detailed system info')

    def command_show_process(self):
        print('return current running process status')

    def command_show_process_all(self):
        print('return status of all processes')

    def command_show_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "SHOW DEFAULT",
                     "SHOW DEVICE",
                     "    /FULL",
                     "SHOW PROCESS",
                     "    /ALL",
                     "SHOW TIME",
                     "SHOW ?"])

    def command_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                          "SET ?",
                          "SHOW ?",
                          "RUN ?",
                          "CREATE ?",
                          "EDIT ?",
                          "DELETE ?",
                          "RENAME ?",
                          "LOGON ?",
                          "LOGOFF ?",
                          "MOUNT ?",
                          "MAIL ?",
                          "EXIT ?",
                          "HELP or ?"])
