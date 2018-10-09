import pygame
from ..uos import UOS
from ..writer import Writer


class MenuBase(UOS.State):
    def __init__(self, header, padding=0):
        UOS.State.__init__(self)
        self.rect = self.state.machine.rect.inflate(-16, -16)
        self.writer = Writer(self.state)
        self.writer.add_output(self.rect, padding)
        self.linesize = UOS.text.get_linesize(padding)
        self.header = header
        self.select = 0

    def call_selection(self):
        pass

    def create_highlighter(self):
        self.selection = []
        for string in self.strings:
            if string:
                self.selection.append(self.render_text(string))
            else:
                self.selection.append(None)

    def color_change(self):
        self.writer.color_change()
        self.create_highlighter()

    def display_string(self):
        self.create_highlighter()
        self.writer.add(0, self.header)
        self.writer.add_empty(0, 2)
        self.writer.add(0, self.strings)

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
                    self.call_selection()

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

        if self.writer.is_finish():
            position = self.rect.x, self.rect.y + self.linesize * (self.select + 3)
            surface.blit(self.selection[self.select], position)

    def render_text(self, text):
        return UOS.text(text, (0,0,0), UOS.text.get_color())


class Menu(MenuBase):
    @staticmethod
    def setup():
        Menu()
        MenuColor()
        MenuSetting()
        MenuDocuments()

    def __init__(self):
        MenuBase.__init__(self, 'UOS Main Menu')
        self.strings = ('[ Documents ]',
                        '[ Settings ]',
                        '[ Logout ]',
                        '[ Shutdown ]',
                        '[ Back ]')

        self.display_string()

    def call_selection(self):
        if self.select == 0:
            self.state.flip('MenuDocuments')
        elif self.select == 1:
            self.state.flip('MenuSetting')
        elif self.select == 4:
            self.state.flip_back()

class MenuSetting(MenuBase):
    def __init__(self):
        MenuBase.__init__(self, 'UOS Setting Menu')
        self.strings = ('[ > Terminal Color ]', '[ Back ]')
        self.display_string()

    def call_selection(self):
        if self.select == 0:
            self.state.flip('MenuColor')
        elif self.select == 1:
            self.state.flip_back()

class MenuColor(MenuBase):
    def __init__(self):
        MenuBase.__init__(self, 'UOS Colors')
        colors = ['[ {0} ]'.format(color.capitalize()) for color in UOS.text.get_colors()]
        self.strings = (*colors, '[ Back ]')
        self.display_string()

    def call_selection(self):
        if self.select < 3:
            UOS.State.set_color(UOS.text.get_colors()[self.select])
        elif self.select == 3:
            self.state.flip_back()

class MenuDocuments(MenuBase):
    def __init__(self):
        MenuBase.__init__(self, 'Documents Menu')
        self.strings = ('[ Create ]',
                        '[ > Read ]',
                        '[ > Edit ]',
                        '[ > Delete ]',
                        '[ Back]')

        self.display_string()

    def call_selection(self):
        if self.select == 1:
            self.state.flip('Explorer', 'r')
        elif self.select == 4:
            self.state.flip_back()
