import os
import shutil
import pickle
from .path import UOS_Path

class UOS_Drive:
    Path = UOS_Path

    @staticmethod
    def deserialize_data(filename):
        with open(filename, "rb") as serialize_in:
            deserialized_output = pickle.load(serialize_in)

        return deserialized_output

    @classmethod
    def detect(cls):
        return {
            'drive': os.path.exists(cls.Path.DRIVE),
            'systems':os.path.exists(cls.Path.SYSTEMS),
            'settings':os.path.exists(cls.Path.SETTINGS),
            'accounts':os.path.exists(cls.Path.ACCOUNTS),
            'database':os.path.exists(cls.Path.DATABASE),
            'logs':os.path.exists(cls.Path.LOGS)
        }

    @classmethod
    def mount(cls, name, path):
        if cls.Path.exists(path):
            cls.Path.mounted[name] = path
            return True
        return False

    @staticmethod
    def move_dir(source, dest):
        if isinstance(source, UOS_Path) and isinstance(dest, UOS_Path):
            shutil.move(source.path, dest.path)

    @staticmethod
    def move_file(source, dest):
        if isinstance(source, UOS_Path) and isinstance(dest, UOS_Path):
            shutil.move(source.path, dest.path)

    @staticmethod
    def rename(source, dest):
        if isinstance(source, UOS_Path) and isinstance(dest, UOS_Path):
            os.rename(source.path, dest.path)

    @staticmethod
    def serialize_data(target, filename):
        with open(filename, "wb") as serialize_out:
            pickle.dump(target, serialize_out)

    @classmethod
    def setup(cls):
        info = cls.detect()
        if not info['drive']:
            os.mkdir(cls.Path.DRIVE)

        if not info['systems']:
            os.mkdir(cls.Path.SYSTEMS)
