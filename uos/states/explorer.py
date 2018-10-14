import os
import pygame
from .menu import Menu
from ..uos import UOS

class ExplorerFile:
    def __init__(self, parent, name):
        self.name = '[ {} ]'.format(name)
        self.parent = parent

    def __call__(self):
        pass

class ExplorerDir:
    def __init__(self, parent, name):
        self.name = '[ > {} ]'.format(name)
        self.parent = parent
        self.item = name

    def __call__(self):
        self.parent.dir_change(self.item)

class ExplorerDirUp:
    def __init__(self, parent):
        self.name = '[ .. ]'
        self.parent = parent

    def __call__(self):
        self.parent.dir_up()

class ExplorerBack:
    def __init__(self, parent):
        self.name = '[ < Back ]'
        self.parent = parent

    def __call__(self):
        self.parent.state.flip_back()

class ExplorerExit:
    def __init__(self, parent):
        self.name = '[ < Exit ]'
        self.parent = parent

    def __call__(self):
        self.parent.state.flip('Terminal')


class Explorer(Menu):
    def __init__(self):
        Menu.__init__(self, 'Explorer', 'Explorer')
        self.boolean_folder = False
        self.action = None
        self.strings = []

    def call_back(self):
        if self.dir in [self.start_dir, self.stop_dir]:
            self.state.flip_back()
        else:
            self.dir = os.path.split(self.dir)[0]
            self.create_menu()

    def create_menu(self):
        items = []
        if self.boolean_folder:
            pass
            #items = ['[ Select ]', None]

        if self.dir != self.stop_dir:
            items.append(ExplorerDirUp(self))

        strings = os.listdir(self.dir)
        for string in strings:
            path = os.path.join(self.dir, string)
            if os.path.isdir(path):
                items.append(ExplorerDir(self, string))
            elif not self.boolean_folder:
                items.append(ExplorerFile(self, string))

        items.append(ExplorerBack(self))
        items.append(ExplorerExit(self))
        self.strings = items
        self.select = 0
        self.writer.clear(0)
        self.writer.clear(1)
        self.display_string()

    def dir_change(self, item):
        path = os.path.join(self.dir, item)
        self.dir = path
        self.create_menu()

    def dir_up(self):
        self.dir = os.path.split(self.dir)[0]
        self.create_menu()

    def entrance(self, regain_focus, action, boolean_folder=False):
        self.action = action
        self.boolean_folder = boolean_folder

        self.header = {'r': "Explorer Read",
                       'e': "Explorer Edit",
                       'd': "Explorer Delete"}[action]

        self.dir = UOS.User.rootpath()
        self.start_dir = self.dir
        if UOS.User.has_privilege():
            self.stop_dir = UOS.Drive.Path.DRIVE
        else:
            self.stop_dir = self.start_dir

        self.create_menu()
