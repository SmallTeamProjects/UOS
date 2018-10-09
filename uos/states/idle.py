import pygame
from ..uos import UOS
from ..writer import Writer

class Idle(UOS.State):
    def __init__(self):
        UOS.State.__init__(self)
        self.writer = Writer(self.state)
        self.writer.add_input(self.state.machine.rect.inflate(-20, -20))

    def color_change(self):
        self.writer.color_change()

    def entrance(self, regain_focus):
        self.state.machine.idle_timer.stop = True
        UOS.Variables.idle = True

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            UOS.Variables.idle = False
            self.state.machine.idle_timer.reset()
            self.state.flip_back()

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)
