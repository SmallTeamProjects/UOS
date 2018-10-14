import pygame
from ..uos import UOS
from ..writer import Writer
from ..commands import Commands

class SubMenu:
    def __init__(self, parent, name, goto_menu):
        self.name = '[ {} ]'.format(name)
        self.goto_menu = goto_menu
        self.parent = parent

    def __call__(self):
        self.parent.state.flip(self.goto_menu)

class MenuCommand:
    def __init__(self, parent, name, command):
        self.name = '[ {} ]'.format(name)
        self.command = command
        self.parent = parent

    def __call__(self):
        Commands.call(self.parent, self.command, True)

class MenuExplorer:
    def __init__(self, parent, name, arg):
        self.name = '[ {} ]'.format(name)
        self.parent = parent
        self.arg = arg

    def __call__(self):
        self.parent.state.flip('Explorer', self.arg)

class MenuBack:
    def __init__(self, parent):
        self.name = '[ Back ]'
        self.parent = parent

    def __call__(self):
        self.parent.state.flip_back()

class MenuMenu(UOS.State):
    user_name = None

    # setup: Will make new states over the old ones
    @classmethod
    def setup(cls):
        cls.user_name = UOS.User.name
        menu = vars(UOS.User.current).get('menu', UOS.User.default_menu())
        for key, items in menu.items():
            menu = Menu(key, key)
            menu.strings = []
            for item in items:
                if item[0] == 'SubMenu':
                    menu.strings.append(SubMenu(menu, *item[1:]))
                elif item[0] == 'Command':
                    menu.strings.append(MenuCommand(menu, *item[1:]))
                elif item[0] == 'Explorer':
                    menu.strings.append(MenuExplorer(menu, *item[1:]))
                else:
                    print("Unknown menu command:", item)

            menu.strings.append(MenuBack(menu))
            menu.display_string()

    def __init__(self):
        UOS.State.__init__(self)
        self.regain_focus = False

    def entrance(self, regain_focus):
        self.regain_focus = regain_focus
        if self.user_name != UOS.User.name:
            MenuMenu.setup()

    def update(self, ticks, delta):
        if self.regain_focus:
            self.state.flip_back()
        else:
            self.state.flip('MainMenu')

class Menu(UOS.State):
    def __init__(self, menu_name, header, padding=0):
        UOS.State.__init__(self, menu_name)
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
                    self.state.flip_back()

                elif event.key in [pygame.K_RETURN, pygame.K_RIGHT]:
                    UOS.sounds.play('enter')
                    self.strings[self.select]()

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

        if self.writer.is_finish():
            position = self.rect.x, self.rect.y + self.linesize * self.select
            surface.blit(self.selection[self.select], position)

    def render_text(self, text):
        return UOS.text(text, (0,0,0), UOS.text.get_color())
