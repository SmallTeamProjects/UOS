import os
from types import SimpleNamespace

class UOS_User:
    # name: current login user
    # current: current login user profile
    # accounts: where all profiles are stored
    # _hex: next root profile for new user
    def __init__(self, bus):
        self.name = None
        self.current = None
        self.accounts = {}
        self._hex = '0x5a0'
        self.menu_version = "0.1.1"

        self.has_any = False
        self.has_admin = False
        self.paths = bus.uos.path
        self.drive = bus.uos.drive
        self.bus = bus

        bus.register_function('user has privilege', self.has_privilege)
        bus.register_function('user current', self.get_current)
        bus.register_function('user rootpath', self.rootpath)

    # All default menu except Main will be consider hardcoded.
    def default_menu(self):
        return {
            "MainMenu": [
                ["SubMenu", "Documents", "Documents"],
                ["SubMenu" ,"Settings", "Settings"],
                ["Selection", "Logout", "LOGOFF"],
                ["Selection", "Shutdown", "SET HALT"]
            ],
            "Documents": [
                ["Selection", "Create", "CREATE FILE"],
                ["Explorer", "> Read", "r"],
                ["Explorer", "> Edit", "e"],
                ["Explorer", "> Delete", "d"],
            ],
            "Settings": [
                ["Nested", "Terminal Color", "TerminalColor"]
            ],
            "TerminalColor": [
                ["Selection", "Green", "SET TERMINAL COLOR green"],
                ["Selection", "Amber", "SET TERMINAL COLOR amber"],
                ["Selection", "Blue", "SET TERMINAL COLOR blue"]
            ]
        }

    def get_current(self):
        return self.current

    def has_privilege(self):
        return self.current.group in ['admin', 'maintainence']

    # if accounts.f exists.
    # load all user profile and store in accounts.
    # load last hex use
    def load(self):
        if os.path.exists(self.paths.accounts):
            accounts = self.drive.deserialize_data(self.paths.accounts)
            for name, data in accounts.items():
                if name == '__hex__':
                    self._hex = data
                else:
                    self.accounts[name] = SimpleNamespace(**data)
                    if data['group'] == 'admin':
                        self.has_admin = True

            if len(self.accounts) > 0:
                self.has_any = True

        # default Maintainence account
        if not accounts.get('Maintainence', False):
            self.create('Maintainence', 'minigame', 'maintainence')

    # save all user and user profiles
    def save(self):
        data = {'__hex__': self._hex}
        for name, info in self.accounts.items():
            data[name] = info.__dict__

        self.drive.serialize_data(data, self.paths.accounts)

    def create(self, name, password, group):
        self._hex = hex(int(self._hex, 16) + 11)
        root = self._hex[2:].upper()
        self.accounts[name] = SimpleNamespace(
            password = password,
            root = root,
            group = group,
            color = 'green',
            menu = self.default_menu(),
            menu_version = self.menu_version)

        path = os.path.join(self.paths.database, root)
        os.makedirs(path)
        self.save()

    # completely remove user and profile permanently.
    def remove(self, name):
        if name in self.accounts.keys():
            del self.accounts[name]
            self.save()
            return True
        return False

    # return
    # 0 = name doesn't exists in account
    # 1 = user rename
    # 2 = newname already exists
    def rename(self, name, newname):
        if name in self.accounts.keys():
            if newname not in self.accounts.keys():
                self.accounts[newname] = self.accounts[name]
                del self.accounts[name]
                self.save()
                return 1
            else:
                return 2
        return 0

    def rootpath(self):
        return os.path.join(self.paths.database, self.current.root)

    # set user name and profile
    def set(self, name):
        self.name = name
        if name in self.accounts:
            self.current = self.accounts[name]
            self.paths.current = self.rootpath()
            if self.bus.uos.color.key != self.current.color:
                self.bus.uos.color.change_color(self.current.color)

            # will be remove later
            if vars(self.current).get('menu_version', "") != self.menu_version:
                self.current.menu_version = self.menu_version
                self.current.menu.update(self.default_menu())
                self.save()
        else:
            self.current = None
            self.paths.current = self.paths.drive
