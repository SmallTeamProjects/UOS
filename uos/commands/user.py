import subprocess
from .basecommand import BaseCommand
from ..uos import UOS


class UserCommands(BaseCommand):
    def __init__(self, link):

        self.command_list = {
            "CREATE ?": self.command_create_help,
            'CREATE DIR': self.command_create_dir,
            'CREATE FILE': self.command_create_file,
            'CHANGE DIR': self.command_change_dir,
            'DELETE DIR': self.command_delete_dir,
            'DELETE FILE': self.command_delete_file,
            'DELETE ?': self.command_delete_help,
            'EDIT FILE': self.command_edit_file,
            'EDIT ?': self.command_edit_help,
            'EXIT': self.command_exit,
            'LOGOFF': self.command_logoff,
            'LOGOFF ?': self.command_logoff_help,
            'MAIL': self.command_mail,
            'MENU': self.command_menu,
            'MOUNT': self.command_mount,
            'MOVE DIR': self.command_move_dir,
            'MOVE FILE': self.command_move_file,
            'RENAME DIR': self.command_rename_dir,
            'RENAME FILE': self.command_rename_file,
            'RENAME USER': self.command_rename_user,
            'RENAME ?': self.command_rename_help,
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
            'SET TERMINAL COLOR': self.command_set_color,
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

        BaseCommand.__init__(self, link)

    def command_create_dir(self, dirname, location=None):
        newdir = UOS.Drive.Path(dirname, location)
        if newdir.isdir():
            self.writer_add('Directory already exists')
        else:
            newdir.makedirs()
            self.writer_add("{0} directory was created".format(dirname))

    def command_create_file(self, filename, filetype, location=None):
        filepath = UOS.Drive.Path((filename, filetype), location)
        if filepath.exists():
            line = "{0} file already exits.".format(filename)
            self.writer_add(line)
        else:
            self.link.action.flip('Editor', filepath.path)

    def command_create_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "CREATE FILE",
                     "     FILENAME",
                     "          FILETYPE",
                     "               LOCATION",
                     "CREATE DIR",
                     "     NAME",
                     "          LOCATION",
                     "CREATE USER",
                     "     USERNAME",
                     "          -a",
               "CREATE ?"])

    def command_change_dir(self, *dirs):
        source = UOS.Drive.Path()
        if source.change_dir(*dirs):
            if source.isdir():
                UOS.Drive.Path.current = source.path
                self.writer_add('Dir has been change')
            else:
                self.writer_add('Is not a directory')
        else:
            self.writer_add('Does not exists')

    def command_delete_dir(self, dirname, location=None):
        dirpath = UOS.Drive.Path(dirname, location)
        if dirpath.isdir():
            dirpath.rmdir()
            self.writer_add('{0} directory has been delete'.format(dirname))
        else:
            self.writer_add('{0} directory does not exists'.format(dirname))

    def command_delete_file(self, filename, filetype, location=None):
        filepath = UOS.Drive.Path((filename, filetype), location)
        if filepath.isfile():
            filepath.remove()
            self.writer_add('{0} has been removed'.format(filename))
        else:
            self.writer_add("File does't exists")

    def command_delete_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "DELETE FILE",
                     "     FILENAME",
                     "          FILETYPE",
                     "               LOCATION",
                     "DELETE DIR",
                     "     NAME",
                     "          LOCATION",
                     "               /FORCE",
                     "DELETE USER",
                     "     USERNAME",
                     "DELETE ?"] )

    def command_edit_file(self, filename, filetype, location=None):
        filepath = UOS.Drive.Path((filename, filetype), location)
        if filepath.isfile():
            self.link.action.flip('Editor', filepath.path, True)
        else:
            self.writer_add('Unable to find {}.{}'.format(filename, filetype))

    def command_edit_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                          "EDIT FILE",
                          "     FILENAME",
                          "          FILETYPE",
                          "               LOCATION",
                          "EDIT ?"])

    def command_exit(self):
        print('terminate a script')

    def command_logoff(self):
        self.writer_clear()
        self.writer_add( ["...Checking Clearance..........",
                          "...AUTHORIZED.................",
                          "...Locking Mechanism Enable..."] )
        UOS.User.set(None)

    def command_logoff_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                          "LOGOFF",
                          "     USERNAME",
                          "LOGOFF ?"] )

    def command_mail(self):
        print('invoke the mail utility')

    def command_mount(self):
        print('look for external storage')

    def command_move_dir(self, source):
        filepath = UOS.Drive.Path(source)
        if filepath.isdir():
            self.info.filepath = filepath
            self.link.state = self.command_move_dir_new
            self.writer_add("Enter new location")
        else:
            self.writer_add("Invalid directory")

    def command_move_dir_new(self, dest):
        self.link.state = None
        destpath = UOS.Drive.Path(self.info.filepath.basename(), dest)
        if destpath.exists():
            self.writer_add("Directory already exists")
        else:
            UOS.Drive.move_dir(self.info.filepath, destpath)
            self.writer_add('Directory has been moved')

    def command_move_file(self, filename, filetype, location=None):
        filepath = UOS.Drive.Path((filename, filetype), location)
        if filepath.isfile():
            self.info.filepath = filepath
            self.link.state = self.command_move_file_new
            self.writer_add("Enter new location")
        else:
            self.writer_add("Invalid directory")

    def command_move_file_new(self, dest):
        self.link.state = None
        filepath = UOS.Drive.Path(self.info.filepath.basename(), dest)
        if filepath.exists():
            self.writer_add("File already exists")
        else:
            UOS.Drive.move_file(self.info.filepath, dest)
            self.writer_add('File has been moved')

    def command_rename_dir(self, dirname, location=None):
        dirpath = UOS.Drive.Path(dirname, location)
        if dirpath.isdir():
            self.link.state = self.command_rename_dir_new
            self.info.filepath = dirpath
            self.writer_add('Enter new directory name')
        else:
            self.writer_add("Directory doesn't exists")

    def command_rename_dir_new(self, dirname, location=None):
        self.link.state = None
        dirpath = UOS.Drive.Path(dirname, location)
        if not dirpath.exists():
            UOS.Drive.rename(self.info.filepath, dirpath)
            self.writer_add('Directory has been rename')
        else:
            self.writer_add("Directory already exists")

    def command_rename_file(self, filename, filetype, location=None):
        self.info.data = filetype
        self.info.name = location
        filepath = UOS.Drive.Path((filename, filetype), location)
        if filepath.isfile():
            self.writer_add("Enter new filename for " + filename)
            self.info.filepath = filepath
            self.link.state = self.command_rename_file_new
        else:
            self.writer_add("{0} doesn't exists".format(filename))

    def command_rename_file_new(self, filename, force=False):
        self.link.state = None
        filepath = UOS.Drive.Path((filename, self.info.data), self.info.name)
        if filepath.exists() and not force:
            self.writer_add("{0} already exists".format(filename))
        else:
            UOS.Drive.rename(self.info.filepath, filepath)
            self.writer_add('{0} has been rename to {1}'.format(self.info.name, filename))

    def command_rename_user(self, username, newname):
        if UOS.User.name == username or UOS.Drive.current.group == 'admin':
            value = UOS.User.rename(username, newname)
            if value == 1:
                self.writer_add('{0} has been rename to {1}'.format(username, newname))
            elif value == 2:
                self.writer_add("{0} already taken".format(newname))
            else:
                self.writer_add("{0} doesn't exists".format(username))

    def command_rename_help(self):
        self.writer_clear()
        self.writer_add( ["USAGE:",
                     "RENAME FILE",
                     "     FILENAME",
                     "          FILETYPE",
                     "               LOCATION",
                     "RENAME DIR",
                     "     NAME",
                     "          LOCATION",
                     "               /FORCE",
                     "RENAME USER",
                     "     USERNAME",
                     "RENAME ?"])

    def command_run_file(self, filename, filetype, location=None):
        program = UOS.Drive.Path((filename, filetype), location)
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
        UOS.User.set(None)
        print('shutdown', name)

    def command_set_halt_restart(self):
        UOS.User.set(None)
        self.link.action.flip('Loading')

    def command_set_halt_restart_maintainence(self):
        print('reset into maintainence mode')
        # 3rd step to running hacking minigame

    def command_set_host(self):
        print('try to connect to a network')

    def command_set_interval(self, interval):
        if interval.isdigit():
            UOS.Variables.interval = int(interval)
        else:
            self.writer_add("Intervals must be a number")

    def command_set_color(self, color):
        if color in UOS.text.get_colors():
            UOS.User.current.color = color
            UOS.User.save()
            UOS.State.set_color(color)
        else:
            self.writer_add("Invalid color")

    def command_set_header(self):
        print('set header text')

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

    def command_show_default(self):
        self.writer_add('current directory: ' + UOS.Drive.Path.current)

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

    def command_menu(self):
        self.link.action.flip('MenuMenu')
