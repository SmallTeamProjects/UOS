from .basecommand import BaseCommand
from ..uos import UOS


class UserCommands(BaseCommand):
    def command_rename_user(self, username, newname):
        if not self.clearance(1):
            return

        if UOS.user.name == username or UOS.drive.current.group == 'admin':
            value = UOS.user.rename(username, newname)
            if value == 1:
                self.writer_add('{0} has been rename to {1}'.format(username, newname))
            elif value == 2:
                self.writer_add("{0} already taken".format(newname))
            else:
                self.writer_add("{0} doesn't exists".format(username))

    def command_run_file(self, filename, filetype, location=None):
        if not self.clearance(1):
            return

        # works on linux
        program = UOS.drive.Path((filename, filetype), location)
        if program.exists():
            FILETYPES = {'py':'python'}
            if filetype in FILETYPES.keys():
                subprocess.call([FILETYPES[filetype], program])
            else:
                self.writer_add('Unsupported type ' + filetype)

    def command_run_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "RUN FILE",
                     "     FILENAME",
                     "          FILETYPE",
                     "               LOCATION",
                     "RUN DEBUG"
                     "    /FILENAME",
                     "RUN ?"])

    def command_set_dir7protection1owner(self):
        if not self.clearance(1):
            return

        print('directory can only be opened by owner')

    def command_set_dir7protection1password(self):
        if not self.clearance(1):
            return

        print('directory can only be opened by entering a password')

    def command_set_file7protection1owner(self):
        if not self.clearance(1):
            return

        print('file can only be opened by owner')

    def command_set_file7protection1owner0rwed_accounts0f(self):
        #2nd step to running hacking minigame
        if not self.clearance(1, 1):
            if UOS.bypass == 2:
                print('step 2')
            return

    def command_set_file7protection1password(self):
        if not self.clearance(1):
            return

        print('file can only be opened by entering a password')

    def command_set_interval(self, interval):
        if not self.clearance(1):
            return

        if interval.isdigit():
            UOS.interval = int(interval)
            UOS.settings.interval = int(interval)
            UOS.save_settings()
        else:
            self.writer_add("Intervals must be a number")

    def command_set_volume(self, volume):
        if not self.clearance(1):
            return

        if volume in range(0.0, 1.0):
            UOS.volume = float(volume)
            UOS.settings.volume = float(volume)
            UOS.save_settings()
        else:
            self.writer_add("volume must be a float between 0.0 & 1.0")

    def command_set_header(self, *args):
        if not self.clearance(1):
            return

        UOS.settings.header = ' '.join(args)
        UOS.save_settings()

    def command_set_help(self):
        if not self.clearance(1):
            return

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
        if not self.clearance(1):
            return

        if color in UOS.color.COLORS:
            UOS.settings.color = color
            UOS.save_settings()
            UOS.color.change_color(color)
        else:
            self.writer_add('Invalid color')

    def command_set_terminal7inquire(self):
        # 1st step to running hacking minigame
        if not self.clearance(1, 0):
            if UOS.bypass == 1:
                print('step 1')
            return

        self.writer_clear()
        self.writer_add('RIT-V300')

    def command_show_default(self):
        if not self.clearance(1):
            return

        self.writer_add('current directory: ' + UOS.drive.path.current)

    def command_show_device(self):
        if not self.clearance(1):
            return

        print('return basic system info')

    def command_show_device_full(self):
        if not self.clearance(1):
            return

        print('return detailed system info')

    def command_show_process(self):
        if not self.clearance(1):
            return

        print('return current running process status')

    def command_show_process7all(self):
        if not self.clearance(1):
            return

        print('return status of all processes')

    def command_show_help(self):
        if not self.clearance(1):
            return

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
        if not self.clearance(1):
            return

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
