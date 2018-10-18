import os
import shutil
import pickle
from .path import UOS_Path, UOS_DrivePath

class UOS_Drive:
    def __init__(self, bus):
        self.Path = UOS_Path
        self.path = UOS_DrivePath()
        UOS_Path.setup(bus, self.path)

    def deserialize_data(self, filename):
        with open(filename, "rb") as serialize_in:
            deserialized_output = pickle.load(serialize_in)

        return deserialized_output

    def detect(self):
        return {
            'drive': os.path.exists(self.path.drive),
            'systems':os.path.exists(self.path.systems),
            'settings':os.path.exists(self.path.settings),
            'accounts':os.path.exists(self.path.accounts),
            'database':os.path.exists(self.path.database),
            'logs':os.path.exists(self.path.logs)
        }

    def mount(self, name, path):
        if self.Path(path).exists():
            self.path.mounted[name] = path
            return True
        return False

    def move_dir(self, source, dest):
        if isinstance(source, UOS_Path) and isinstance(dest, UOS_Path):
            shutil.move(source.path, dest.path)

    def move_file(self, source, dest):
        if isinstance(source, UOS_Path) and isinstance(dest, UOS_Path):
            shutil.move(source.path, dest.path)

    def rename(self, source, dest):
        if isinstance(source, UOS_Path) and isinstance(dest, UOS_Path):
            os.rename(source.path, dest.path)

    def serialize_data(self, target, filename):
        with open(filename, "wb") as serialize_out:
            pickle.dump(target, serialize_out)

    def setup(self):
        info = self.detect()
        if not info['drive']:
            os.mkdir(self.path.drive)

        if not info['systems']:
            os.mkdir(self.path.systems)
