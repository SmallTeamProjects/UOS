import pygame
from ..uos import UOS
from ..writer import Writer

class Idle(UOS.State):
    def __init__(self):
        UOS.State.__init__(self, None, True)
        self.writer = Writer(self.timer)
        self.writer.add_input(UOS.Screen.rect.inflate(-20, -20))

    def color_change(self):
        self.writer.color_change()

    def entrance(self, args):
        UOS.Screen.idle_timer.stop = True
        UOS.Variables.idle = True

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            UOS.Variables.idle = False
            UOS.Screen.idle_timer.reset()
            self.last_state()

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)
