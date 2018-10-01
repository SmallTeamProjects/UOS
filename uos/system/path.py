import os
from .variables import UOS_Variables

class UOS_Path:
    DRIVE = 'UOS_DRIVE'
    DATABASE = os.path.join(DRIVE, 'DATABASE')
    SYSTEMS = os.path.join(DRIVE, 'systems')
    SETTINGS = os.path.join(SYSTEMS, 'settings.f')
    ACCOUNTS = os.path.join(SYSTEMS, 'accounts.f')
    LOGS = os.path.join(SYSTEMS, 'logs.f')

    current = DRIVE
    mounted = {}

    def __init__(self, source, location=None):
        if isinstance(source, (tuple, list)):
            source = '.'.join(source)

        if location:
            source = os.path.join(location, source)

        self.path = self.uos_join(source)

    def basename(self):
        return os.path.basename(self.path)

    def exists(self):
        return os.path.exists(self.path)

    def isdir(self):
        return os.path.isdir(self.path)

    def isfile(self):
        return os.path.isfile(self.path)

    def mkdir(self):
        os.mkdir(self.path)

    def makedirs(self):
        os.makedirs(self.path)

    def remove(self):
        os.remove(self.path)

    def rmdir(self):
        os.rmdir(self.path)

    def split(self):
        return os.path.split(self.path)

    def uos_join(self, path):
        path_split = self.uos_split(path)
        admin = UOS_Variables.group in ['admin', 'maintainence']
        if admin and path_split[0] == 'uos':
            return os.path.join(UOS_Path.DRIVE, path[3:])

        for key in UOS_Path.mounted.keys():
            if path_split[0] == key:
                return os.path.join(UOS_Path.mounted[key], path[len(key):])

        return os.path.join(UOS_Path.current, path)

    def uos_split(self, path):
        allparts = []
        while True:
            parts = os.path.split(path)
            if parts[0] == path:
                allparts.insert(0, path)
                break
            elif parts[1] == path:
                allparts.insert(0, path)
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])

        return allparts
