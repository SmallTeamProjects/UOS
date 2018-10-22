import pygame
from types import SimpleNamespace
from ..uos import UOS
from ..writer import Writer
from ..commands import Command

class MenuBase:
    def __init__(self, parent, position=0, name=None):
        self.parent = parent
        self.position = position
        if name:
            self.name = '[ {} ]'.format(name)

    def call_right(self):
        pass

    def call_left(self):
        pass

class MenuBack(MenuBase):
    def __init__(self, parent, position):
        MenuBase.__init__(self, parent, position, "Back")

    def call_right(self):
        self.parent.state.flip_back()

class MenuExplorer(MenuBase):
    def __init__(self, parent, position, name, arg):
        MenuBase.__init__(self, parent, position, name)
        self.arg = arg

    def call_right(self):
        self.parent.state.flip('Explorer', self.arg)

class MenuNested:
    def __init__(self, parent, position, name, nested_menu):
        self.nested_menu = nested_menu
        self.position = position
        self.basename = name
        self.parent = parent
        self.menu_pos = {'green': 0, 'amber': 1, 'blue': 2}[UOS.color.key]
        self.name = self.get_name()

    def get_item(self):
        return self.parent.menu[self.nested_menu][self.menu_pos]

    def get_name(self):
        return "{:<20} < {} > ".format(self.basename, self.get_item()[1])

    def call_right(self):
        self.menu_pos += 1
        self.menu_pos %= len(self.parent.menu[self.nested_menu])
        self.call_command()

    def call_left(self):
        self.menu_pos -= 1
        self.menu_pos %= len(self.parent.menu[self.nested_menu])
        self.call_command()

    def call_command(self):
        self.name = self.get_name()
        self.parent.writer.get_line(1, self.position).set_text(self.name)
        Command.call(self.parent, self.get_item()[2], True)

class MenuSelection(MenuBase):
    def __init__(self, parent, position, name, command):
        MenuBase.__init__(self, parent, position, name)
        self.command = command

    def call_right(self):
        pass
        #Command.call(self.parent, self.command, True)

class MenuText(MenuBase):
    def __init__(self, parent, position, name, info):
        MenuBase.__init__(self, parent, position, None)
        # Give command a fake writer
        self.writer = SimpleNamespace(add=self.add, clear=self.clear)
        self.name = name
        for item in info:
            if item[0] == '-t':
                self.name += "  " + item[1]
            elif item[0] == '-c':
                Command.call(self, item[1])
                self.name += " " + self.text

    def add(self, text, *args, **kwargs):
        self.text = text

    def clear(self):
        pass

class SubMenu(MenuBase):
    def __init__(self, parent, position, name, goto_menu):
        MenuBase.__init__(self, parent, position, name)
        self.goto_menu = goto_menu

    def call_right(self):
        self.parent.state.flip(self.goto_menu)

class MenuMenu(UOS.State):
    user_name = None

    # setup: Will make new states over the old ones
    @classmethod
    def setup(cls):
        cls.user_name = UOS.user.name
        menu = UOS.user.current.menu
        for key, items in menu.items():
            new_menu = Menu(menu, key, key)
            new_menu.strings = []
            for enum, item in enumerate(items):
                if item[0] == 'SubMenu':
                    new_menu.strings.append(SubMenu(new_menu, enum, *item[1:]))
                elif item[0] == 'Nested':
                    new_menu.strings.append(MenuNested(new_menu, enum, *item[1:]))
                elif item[0] == 'Selection':
                    new_menu.strings.append(MenuSelection(new_menu, enum, *item[1:]))
                elif item[0] == 'Text':
                    new_menu.strings.append(MenuText(new_menu, enum, *item[1:]))
                elif item[0] == 'Explorer':
                    new_menu.strings.append(MenuExplorer(new_menu, enum, *item[1:]))
                else:
                    print("Unknown menu command:", item)

            new_menu.strings.append(MenuBack(new_menu, enum))
            new_menu.display_string()

    def __init__(self):
        UOS.State.__init__(self)
        self.regain_focus = False

    def entrance(self, regain_focus):
        self.regain_focus = regain_focus
        #if self.user_name != UOS.user.name:
        MenuMenu.setup()

    def update(self, ticks, delta):
        if self.regain_focus:
            self.state.flip_back()
        else:
            self.state.flip('MainMenu')

class Menu(UOS.State):
    def __init__(self, menu, menu_name, header, padding=0):
        UOS.State.__init__(self, menu_name)
        self.menu = menu
        self.linesize = UOS.text.get_linesize(padding)
        size = self.state.machine.rect.size
        y = 8 + self.linesize * 2
        self.rect = pygame.Rect(8, y, size[0] - 16,  size[1] - y)
        self.writer = Writer(self.state)
        # header
        self.writer.add_output(pygame.Rect(8, 8, self.rect.w, self.linesize), padding)
        # body
        self.writer.add_output(self.rect, padding)
        self.header = header
        self.select = 0

    def create_highlighter(self):
        self.selection = []
        for string in self.strings:
            if string:
                self.selection.append(self.render_text(string.name))
            else:
                self.selection.append(None)

    def color_change(self):
        self.writer.color_change()
        self.create_highlighter()

    def display_string(self):
        self.create_highlighter()
        self.writer.add(0, self.header)
        self.writer.add(1, [s.name for s in self.strings])

    def entrance(self, regain_focus):
        self.writer.flush()
        self.select = 0

    def event(self, event):
        if self.writer.is_finish():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    UOS.sounds.play('scroll')
                    self.select += 1
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select += 1
                        self.select %= len(self.selection)

                elif event.key == pygame.K_UP:
                    UOS.sounds.play('scroll')
                    self.select -= 1
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select -= 1
                        self.select %= len(self.selection)

                elif event.key == pygame.K_LEFT:
                    UOS.sounds.play('enter')
                    self.strings[self.select].call_left()

                elif event.key in [pygame.K_RETURN, pygame.K_RIGHT]:
                    UOS.sounds.play('enter')
                    self.strings[self.select].call_right()

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

        if self.writer.is_finish():
            position = self.rect.x, self.rect.y + self.linesize * self.select
            surface.blit(self.selection[self.select], position)

    def render_text(self, text):
        return UOS.text(text, (0,0,0), UOS.color.color)
