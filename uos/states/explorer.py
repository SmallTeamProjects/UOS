import os
import pygame
from .menu import MenuBase
from ..uos import UOS


class ExplorerBase:
    def __init__(self, menu, header, boolean_folder):
        self.menu = menu
        self.menu.header = header
        self.boolean_folder = boolean_folder
        self.dir = UOS.User.rootpath()
        self.start_dir = self.dir
        if UOS.User.current.group in ['admin', 'maintainence']:
            self.stop_dir =  UOS.Drive.Path.DRIVE
        else:
            self.stop_dir =  self.start_dir

        self.create_menu()

    def call_back(self):
        if self.dir in [self.start_dir, self.stop_dir]:
            self.menu.last_state()
        else:
            self.dir = os.path.split(self.dir)[0]
            self.create_menu()

    def create_menu(self):
        items = []
        if self.boolean_folder:
            items = ['[ Select ]', None]

        if self.dir != self.stop_dir:
            items.append('[ .. ]')

        strings = os.listdir(self.dir)
        for string in strings:
            path = os.path.join(self.dir, string)
            if os.path.isdir(path):
                items.append('[ > {0} ]'.format(string))
            elif not self.boolean_folder:
                items.append('[ {0} ]'.format(string))

        items.append('[ ^Back ]')
        items.append('[ ^Exit ]')
        self.menu.strings = items
        self.menu.select = 0
        self.menu.writer.clear(0)
        self.menu.display_string()

    def get_exit_state(self):
        state = self.menu
        while state.get_last_state():
            state = state.get_last_state()

        return state

    def exit_state(self):
        UOS.State.flip_state = self.get_exit_state()

class ExplorerCreate(ExplorerBase):
    def __init__(self, menu, boolean_folder):
        ExplorerBase.__init__(self, menu, 'Explorer Create', boolean_folder)

    def call_selection(self):
        pass

class ExplorerDelete(ExplorerBase):
    def __init__(self, menu, boolean_folder):
        ExplorerBase.__init__(self, menu, 'Explorer Delete', boolean_folder)

    def call_selection(self):
        pass

class ExplorerEdit(ExplorerBase):
    def __init__(self, menu, boolean_folder):
        ExplorerBase.__init__(self, menu, 'Explorer Edit', boolean_folder)

    def call_selection(self):
        pass

class ExplorerRead(ExplorerBase):
    def __init__(self, menu, boolean_folder):
        ExplorerBase.__init__(self, menu, 'Explorer Read', boolean_folder)

    def call_selection(self):
        item = self.menu.strings[self.menu.select].lstrip('[ > ').rstrip(' ]')
        path = os.path.join(self.dir, item)
        if item == '^Back':
            UOS.State.flip_state = self.menu._state.track
        elif item == '^Exit':
            self.exit_state()
        elif item == '..':
            self.dir = os.path.split(self.dir)[0]
            self.create_menu()
        elif os.path.isdir(path):
            self.dir = path
            self.create_menu()
        elif os.path.isfile(path):
            print(path)

class Explorer(MenuBase):
    def __init__(self):
        MenuBase.__init__(self, 'Explorer')
        self.strings = []
        self.last_args = None

    def entrance(self, action, boolean_folder=False):
        if action:
            self.last_args = [action, boolean_folder]
        elif self.last_args:
            action, boolean_folder = self.last_args

        self.explorer = {'c':ExplorerCreate,
                         'd':ExplorerDelete,
                         'e':ExplorerEdit,
                         'r':ExplorerRead}[action](self, boolean_folder)

    def call_back(self):
        self.explorer.call_back()

    def call_selection(self):
        self.explorer.call_selection()
