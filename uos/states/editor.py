import pygame
from ..uos import UOS
from ..writer import TextEditor

class Editor(UOS.State):
    @staticmethod
    def setup():
        Editor()
        SavingEditor()

    def __init__(self):
        UOS.State.__init__(self, track=True)
        self.editor = TextEditor(self.timer,
                                 UOS.Screen.rect.inflate(-20, -20),
                                 2, self.last_state)

    def entrance(self, filename, load=False):
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
    def __init__(self, track=True):
        UOS.State.__init__(self, None, True)
        self.saving_timer = self.timer(300, self.call_saving)
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
            self.last_state()
        else:
            self.pos = (self.pos + 1) % 4
            symbol = self.symbols[self.pos]
            self.image = UOS.text('Saving file ' + self.filename + '  ' + symbol)
            self.rect = self.image.get_rect()
            self.rect.center = UOS.Screen.rect.center

    def render(self, surface):
        surface.fill((0,0,0))
        surface.blit(self.image, self.rect)
