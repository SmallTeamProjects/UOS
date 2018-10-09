import pygame
from ..uos import UOS
from ..writer import TextEditor

class Editor(UOS.State):
    @staticmethod
    def setup():
        Editor()
        SavingEditor()

    def __init__(self):
        UOS.State.__init__(self)
        self.editor = TextEditor(self, self.state.machine.rect.inflate(-16, -16), 2)

    def entrance(self, regain_focus, filename, load=False):
        if filename:
            if load:
                self.editor.load(filename)
            else:
                self.editor.entrance(filename)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            self.editor.event_keydown(event)

    def render(self, surface):
        surface.fill((0,0,0))
        self.editor.render(surface)

class SavingEditor(UOS.State):
    def __init__(self):
        UOS.State.__init__(self)
        self.saving_timer = self.state.timer(300, self.call_saving)
        self.symbols = '/-\|'

    def entrance(self, filename):
        self.filename = filename
        self.saving_finish = 0
        self.pos = -1
        self.call_saving(None)

    def call_saving(self, timer):
        if timer:
            self.saving_finish += timer.interval

        if self.saving_finish > 2000:
            self.state.flip_back(None)
        else:
            self.pos = (self.pos + 1) % 4
            symbol = self.symbols[self.pos]
            self.image = UOS.text('Saving file ' + self.filename + '  ' + symbol)
            self.rect = self.image.get_rect()
            self.rect.center = self.state.machine.rect.center

    def render(self, surface):
        surface.fill((0,0,0))
        surface.blit(self.image, self.rect)
