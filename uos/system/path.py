import os

class UOS_DrivePath:
    def __init__(self):
        self.drive = "UOS_DRIVE"
        self.database = os.path.join(self.drive, 'DATABASE')
        self.systems = os.path.join(self.drive, 'systems')
        self.settings = os.path.join(self.systems, 'settings.f')
        self.accounts = os.path.join(self.systems, 'accounts.f')
        self.logs = os.path.join(self.systems, 'logs.f')

        self.current = self.drive
        self.mounted = {}

class UOS_Path:
    @classmethod
    def setup(cls, bus, drive_path):
        cls.bus = bus
        cls.drive_path = drive_path

    def __init__(self, source=None, location=None):
        if isinstance(source, (tuple, list)):
            source = '.'.join(source)

        if location:
            source = os.path.join(location, source)

        if source:
            self.path = self.uos_join(source)
        else:
            self.path = UOS_Path.drive_path.current

    def basename(self):
        return os.path.basename(self.path)

    def change_dir(self, *dirs):
        old_path = self.path
        self.path = os.path.normpath(os.path.join(self.path, *dirs))
        if self.path.startswith(UOS_Path.bus.fetch('root path')):
            return True
        elif UOS_Path.bus.fetch("user has privilege"):
            if self.path.startswith(UOS_Path.drive_path.drive):
                return True

        for holotape in UOS_Path.drive_path.mounted:
            if self.path.startswith(holotape):
                return True

        self.path = old_path
        return False

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
        privilege = UOS_Path.bus.fetch("user has privilege")
        if privilege and path_split[0] == 'uos':
            return os.path.join(UOS_Path.drive_path.drive, path[3:])

        for key in UOS_Path.drive_path.mounted.keys():
            if path_split[0] == key:
                return os.path.join(UOS_Path.drive_path.mounted[key],
                                    path[len(key):])

        return os.path.join(UOS_Path.drive_path.current, path)

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
