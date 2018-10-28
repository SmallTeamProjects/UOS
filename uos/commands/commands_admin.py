from .basecommand import BaseCommand
from ..uos import UOS

class AdminCommands(BaseCommand):
    def command_create_user(self, name, group):
        if not self.clearance(2):
            return

        if group in ['-a', '-u', '-m']:
            group = {'-a':'admin', '-u':'user', '-m':'maintainence'}[group]

        self.link.state = self.command_create_user_password
        self.info.name = name
        self.info.group = group
        self.writer_add('Enter {0} password.'.format(self.info.name), protect=True)

    def command_create_user_password(self, password):
        if not self.clearance(2):
            return

        if len(password) > 3:
            UOS.user.create(self.info.name, password, self.info.group)
            self.writer_add('User {0} has been added'.format(self.info.name))
            self.info.name = None
            self.info.group = None
            self.link.state = None
        else:
            self.writer_clear()
            self.writer_add('Password minimum of 4 characters')
            self.writer_add('Enter {0} password.'.format(self.info.name), protect=True)

    def command_delete_user(self, username):
        if not self.clearance(2):
            return

        if UOS.user.current.group == 'admin':
            if UOS.user.remove(username):
                self.writer_add('{0} has been removed'.format(username))
            else:
                self.writer_add("{0} doesn't exists".format(username))
        else:
            self.writer_add('Only admin can delete users')

    def command_run_debug(self):
        if not self.clearance(2):
            return

        print('run diagnostic test')

    def command_run_debug_accounts(self):
        if not self.clearance(2):
            return

        print('run hacking minigame if previous steps completed')
        #Last step to running hacking minigame
        if UOS.bypass is 3:
            self.link.action.flip('Minigame')
            UOS.bypass = 0
            UOS.settings.bypass = 0
            UOS.save_settings()

    def command_set_default(self):
        if not self.clearance(2):
            return

        print('set default directory')

    def command_show_users(self):
        if not self.clearance(2):
            return

        if len(UOS.user.accounts) > 0:
            self.writer_clear()
            keys = list(UOS.user.accounts.keys())
            keys.sort()
            for key in keys:
                item = UOS.user.accounts[key]
                self.writer_add('{0} : {1}, {2}'.format(key, item.group, item.root))
        else:
            self.writer_add("System has no users".format(filename))
