import time
from .basecommand import BaseCommand
from ..uos import UOS

class DefaultCommands(BaseCommand):
    def __init__(self, link):
        if UOS.User.has_admin:
            self.command_list = {
            'LOGON': self.command_logon,
            'LOGON ?': self.command_logon_help,
            'SHOW TIME': self.command_show_time,
            'MINIGAME': self.command_minigame,
            }
        elif UOS.User.has_any:
            self.command_list = {
            'LOGON': self.command_logon,
            'LOGON ?': self.command_logon_help,
            'SETUP': self.command_setup,
            'SHOW TIME': self.command_show_time,
            'MINIGAME': self.command_minigame,
            }
        else:
            self.command_list = {
            'SETUP': self.command_setup,
            'SHOW TIME': self.command_show_time,
            'MINIGAME': self.command_minigame,
            }

        #testing commands
        self.command_list['SYSTEM MESSAGE'] = self.command_system_message
        BaseCommand.__init__(self, link)

    def update_commands(self):
        del self.command_list['SETUP']
        self.command_list['LOGON'] = self.command_logon
        self.command_list['LOGON ?'] = self.command_logon_help
        self.keys = sorted(self.command_list.keys(), reverse=True)

    def command_logon(self, name):
        if not UOS.User.name:
            if name in UOS.User.accounts.keys():
                self.writer_add('Enter Password:', protect=True)
                self.info.name = name
                self.info.attempts = 3
                self.link.state = self.command_logon_password
            else:
                self.writer_add('Invalid User !')
        else:
            self.writer_add('Error: Requires Logout')

    def command_logon_password(self, password):
        if UOS.User.accounts[self.info.name].password == password:
            UOS.User.set(self.info.name)
            self.writer_add('Welcome {0}'.format(self.info.name))
            self.link.state = None
            self.clear_info()
        else:
            self.info.attempts -= 1
            if self.info.attempts > 0:
                self.writer_add(["Invalid Password!", "Enter Password:"], protect=True)
            else:
                self.writer_clear()
                self.writer_add( ["...Checking Clearance..........",
                             "...UNAUTHORIZED...............",
                             "...Locking Mechanism Enable..."])
                self.link.state = None

    def command_logon_help(self):
        self.writer_clear()
        self.writer_add(["USAGE:",
                     "LOGON",
                     "     USERNAME",
                     "LOGON ?"])

    def command_setup(self):
        self.writer_clear()
        self.link.state = self.command_setup_new_admin
        self.writer_add('Enter admin name.')

    def command_setup_new_admin(self, name):
        if len(name) > 2:
            self.info.name = name
            self.link.state = self.command_setup_password
            self.writer_add('Enter {0} password.'.format(self.info.name), protect=True)
        else:
            self.writer_clear()
            self.writer_add('Admin name needs to more the 2 characters')
            self.writer_add('Enter admin name.')

    def command_setup_password(self, password):
        if len(password) > 3:
            UOS.User.create(self.info.name, password, 'admin')
            self.writer_add('New admin {0} has been created.'.format(self.info.name))
            UOS.User.has_admin = True
            UOS.User.has_any = True
            self.update_commands()
            self.link.state = None
            UOS.User.set(self.info.name)
            self.clear_info()
        else:
            self.writer_clear()
            self.writer_add('Password minium of 4 characters')
            self.writer_add('Enter {0} password.'.format(self.info.name), protect=True)

    def command_show_time(self):
        self.writer_clear()
        self.writer_add(str(time.ctime()))

    def command_system_message(self):
        pass

    def command_minigame(self):
        UOS.State.next_state = 'Minigame'
