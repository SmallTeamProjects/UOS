from .basecommand import BaseCommand
from ..uos import UOS


class SystemCommands(BaseCommand):
    def command_exit(self):
        if not self.clearance(1):
            return

        print('terminate a script')

    def command_logon(self, name):
        if not UOS.user.name:
            if name in UOS.user.accounts.keys():
                self.writer_add('Enter Password:', protect=True)
                self.info.name = name
                self.info.attempts = 3
                self.link.state = self.logon_password
            else:
                self.writer_add('Invalid User !')
        else:
            self.writer_add('Error: Requires Logout')

    def logon_password(self, password):
        if UOS.user.accounts[self.info.name].password == password:
            UOS.user.set(self.info.name)
            self.writer_add('Welcome {0}'.format(self.info.name))
            self.link.state = None
            self.clear_info()
        else:
            self.info.attempts -= 1
            if self.info.attempts > 0:
                self.writer_add(["Invalid Password!", "Enter Password:"], protect=True)
            else:
                self.writer_clear()
                self.writer_add(["...Checking Clearance..........",
                                 "...UNAUTHORIZED...............",
                                 "...Locking Mechanism Enable..."])
                self.link.state = None

    def command_logon_help(self):
        self.writer_clear()
        self.writer_add(["USAGE:",
                         "LOGON Username",
                         "LOGON ?"])

    def command_logoff(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["...Checking Clearance..........",
                         "...AUTHORIZED.................",
                         "...Locking Mechanism Enable..."])
        UOS.user.set(None)

    def command_logoff_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "LOGOFF Username",
                         "LOGOFF ?"])

    def command_setup(self):
        if not UOS.user.has_admin:
            self.writer_clear()
            self.link.state = self.setup_new_admin
            self.writer_add('Enter admin name.')
        else:
            self.writer_add('Invalid command')

    def setup_new_admin(self, name):
        if len(name) > 2:
            self.info.name = name
            self.link.state = self.setup_password
            self.writer_add('Enter {0} password.'.format(self.info.name), protect=True)
        else:
            self.writer_clear()
            self.writer_add('Admin name must be more than 2 characters')
            self.writer_add('Enter admin name.')

    def setup_password(self, password):
        if len(password) > 3:
            UOS.user.create(self.info.name, password, 'admin')
            self.writer_add('New admin {0} has been created.'.format(self.info.name))
            UOS.user.has_admin = True
            UOS.user.has_any = True
            self.link.state = None
            UOS.user.set(self.info.name)
            self.clear_info()
        else:
            self.writer_clear()
            self.writer_add('Password minimum of 4 characters')
            self.writer_add('Enter {0} password.'.format(self.info.name), protect=True)

    def command_set_halt(self, name):
        UOS.user.set(None)
        print('shutdown', name)

    def command_set_halt_restart(self):
        UOS.user.set(None)
        self.link.action.flip('Loading')
