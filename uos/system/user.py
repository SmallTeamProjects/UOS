import os
from types import SimpleNamespace
from .variables import UOS_Variables
from .drive import UOS_Drive
from .state import UOS_State
from .path import UOS_Path

class UOS_User:
    # name: current login user
    # current: current login user profile
    # accounts: where all profiles are stored
    # _hex: next root profile for new user
    name = None
    current = None
    accounts = {}
    _hex = '0x5a0'

    has_any = False
    has_admin = False

    # if accounts.f exists.
    # load all user profile and store in accounts.
    # load last hex use
    @classmethod
    def load(cls):
        if os.path.exists(UOS_Path.ACCOUNTS) :
            accounts = UOS_Drive.deserialize_data(UOS_Path.ACCOUNTS)
            for name, data in accounts.items():
                if name == '__hex__':
                    cls._hex = data
                else:
                    cls.accounts[name] = SimpleNamespace(**data)
                    if data['group'] == 'admin':
                        cls.has_admin = True

            if len(cls.accounts) > 0:
                cls.has_any = True

    # save all user and user profiles
    @classmethod
    def save(cls):
        data = {'__hex__': cls._hex}
        for name, info in cls.accounts.items():
            data[name] = info.__dict__

        UOS_Drive.serialize_data(data, UOS_Path.ACCOUNTS)

    @classmethod
    def create(cls, name, password, group):
        cls._hex = hex(int(cls._hex, 16) + 11)
        root = cls._hex[2:].upper()
        cls.accounts[name] = SimpleNamespace(
            password = password,
            root = root,
            group = group,
            color = 'green')
        path = os.path.join(UOS_Path.DATABASE, root)
        os.makedirs(path)
        cls.save()

    # completely remove user and profile permanently.
    @classmethod
    def remove(cls, name):
        if name in cls.accounts.keys():
            del cls.accounts[name]
            cls.save()
            return True
        return False

    # return
    # 0 = name doesn't exists in account
    # 1 = user rename
    # 2 = newname already exists
    @classmethod
    def rename(cls, name, newname):
        if name in cls.accounts.keys():
            if newname not in cls.accounts.keys():
                cls.accounts[newname] = cls.accounts[name]
                del cls.accounts[name]
                cls.save()
                return 1
            else:
                return 2
        return 0

    @classmethod
    def rootpath(cls):
        return os.path.join(UOS_Path.DATABASE, cls.current.root)

    # set user name and profile
    @classmethod
    def set(cls, name):
        cls.name = name
        if name in cls.accounts:
            cls.current = cls.accounts[name]
            UOS_Variables.group = cls.current.group
            UOS_Path.current = cls.rootpath()
            if UOS_Variables.color_key != cls.current.color:
                UOS_State.set_color(cls.current.color)
        else:
            cls.current = None
            UOS_Path.current = UOS_Path.DRIVE
