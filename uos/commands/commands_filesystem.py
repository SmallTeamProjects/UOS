from .basecommand import BaseCommand
from ..uos import UOS


class FilesystemCommands(BaseCommand):
    def command_create_dir(self, dirname, location=None):
        if not self.clearance(1):
            return

        newdir = UOS.drive.Path(dirname, location)
        if newdir.isdir():
            self.writer_add('Directory already exists')
        else:
            newdir.makedirs()
            self.writer_add("{0} directory was created".format(dirname))

    def command_create_file(self, filename, filetype, location=None):
        if not self.clearance(1):
            return

        filepath = UOS.drive.Path((filename, filetype), location)
        if filepath.exists():
            line = "{0} file already exits.".format(filename)
            self.writer_add(line)
        else:
            self.link.action.flip('Editor', filepath.path)

    def command_create_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "CREATE FILE FileName FileType Location",
                         "CREATE DIR DirectoryName Location",
                         "CREATE USER Username",
                         "     -a",
                         "CREATE ?"])

    def command_change_dir(self, *dirs):
        if not self.clearance(1):
            return

        source = UOS.drive.Path()
        if source.change_dir(*dirs):
            if source.isdir():
                UOS.drive.path.current = source.path
                self.writer_add('Directory has been change')
            else:
                self.writer_add('Is not a directory')
        else:
            self.writer_add('Does not exists')

    def command_delete_dir(self, dirname, location=None):
        if not self.clearance(1):
            return

        dirpath = UOS.drive.Path(dirname, location)
        if dirpath.isdir():
            dirpath.rmdir()
            self.writer_add('{0} directory has been deleted'.format(dirname))
        else:
            self.writer_add('{0} directory does not exist'.format(dirname))

    def command_delete_file(self, filename, filetype, location=None):
        if not self.clearance(1):
            return

        filepath = UOS.drive.Path((filename, filetype), location)
        if filepath.isfile():
            filepath.remove()
            self.writer_add('{0} has been removed'.format(filename))
        else:
            self.writer_add("File doesn't exist")

    def command_delete_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "DELETE FILE FileName FileType Location",
                         "DELETE DIR DirectoryName Location",
                         "     /FORCE",
                         "DELETE USER Username",
                         "DELETE ?"])

    def command_edit_file(self, filename, filetype, location=None):
        if not self.clearance(1):
            return

        filepath = UOS.drive.Path((filename, filetype), location)
        if filepath.isfile():
            self.link.action.flip('Editor', filepath.path, True)
        else:
            self.writer_add('Unable to find {}.{}'.format(filename, filetype))

    def command_edit_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "EDIT FILE FileName FileType Location",
                         "EDIT ?"])

    def command_mount(self):
        if not self.clearance(1):
            return

        print('look for external storage')

    def command_mount_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "MOUNT",
                         "MOUNT ?"])

    def command_move_dir(self, source):
        if not self.clearance(1):
            return

        filepath = UOS.drive.Path(source)
        if filepath.isdir():
            self.info.filepath = filepath
            self.link.state = self.move_dir_new
            self.writer_add("Enter new location")
        else:
            self.writer_add("Invalid directory")

    def move_dir_new(self, dest):
        self.link.state = None
        destpath = UOS.drive.Path(self.info.filepath.basename(), dest)
        if destpath.exists():
            self.writer_add("Directory already exists")
        else:
            UOS.drive.move_dir(self.info.filepath, destpath)
            self.writer_add('Directory has been moved')

    def command_move_file(self, filename, filetype, location=None):
        if not self.clearance(1):
            return

        filepath = UOS.drive.Path((filename, filetype), location)
        if filepath.isfile():
            self.info.filepath = filepath
            self.link.state = self.move_file_new
            self.writer_add("Enter new location")
        else:
            self.writer_add("Invalid directory")

    def move_file_new(self, dest):
        self.link.state = None
        filepath = UOS.drive.Path(self.info.filepath.basename(), dest)
        if filepath.exists():
            self.writer_add("File already exists")
        else:
            UOS.drive.move_file(self.info.filepath, dest)
            self.writer_add('File has been moved')

    def command_rename_dir(self, dirname, location=None):
        if not self.clearance(1):
            return

        dirpath = UOS.drive.Path(dirname, location)
        if dirpath.isdir():
            self.link.state = self.rename_dir_new
            self.info.filepath = dirpath
            self.writer_add('Enter new directory name')
        else:
            self.writer_add("Directory doesn't exist")

    def rename_dir_new(self, dirname, location=None):
        self.link.state = None
        dirpath = UOS.drive.Path(dirname, location)
        if not dirpath.exists():
            UOS.drive.rename(self.info.filepath, dirpath)
            self.writer_add('Directory has been renamed')
        else:
            self.writer_add("Directory already exists")

    def command_rename_file(self, filename, filetype, location=None):
        if not self.clearance(1):
            return

        self.info.data = filetype
        self.info.name = location
        filepath = UOS.drive.Path((filename, filetype), location)
        if filepath.isfile():
            self.writer_add("Enter new fileName for " + filename)
            self.info.filepath = filepath
            self.link.state = self.rename_file_new
        else:
            self.writer_add("{0} doesn't exist".format(filename))

    def rename_file_new(self, filename, force=False):
        self.link.state = None
        filepath = UOS.drive.Path((filename, self.info.data), self.info.name)
        if filepath.exists() and not force:
            self.writer_add("{0} already exists".format(filename))
        else:
            UOS.drive.rename(self.info.filepath, filepath)
            self.writer_add('{0} has been renamed to {1}'.format(self.info.name, filename))

    def command_rename_help(self):
        if not self.clearance(1):
            return

        self.writer_clear()
        self.writer_add(["USAGE:",
                         "RENAME FILE FileName FileType Location",
                         "RENAME DIR DirectoryName Location",
                         "     /FORCE",
                         "RENAME USER Username",
                         "RENAME ?"])
