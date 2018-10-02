import pygame
from ..uos import UOS
from ..writer import Writer

class Terminal(UOS.State):
    def __init__(self):
        UOS.State.__init__(self)
        self.writer = Writer(self.timer)
        if UOS.User.has_admin:
            x = 10
            y = 10
            w = UOS.Screen.rect.w - x * 2
            rect = pygame.Rect(x, y, w, UOS.text.get_linesize())
            self.writer.add_output(rect)
            y += UOS.text.get_linesize()
            rect = pygame.Rect(x, y, w, UOS.Screen.rect.bottom - y)
            self.writer.add_input(rect)
            self.writer.add(0, 'Welcome to ROBCO Industries (TM) Termlink')
        else:
            for item in UOS.Data.intro:
                self.writer.add_input(UOS.Screen.rect.inflate(-20, -20))
                self.writer.add(0, item.text, item.interval,
                                item.sound, newline=item.newline,
                                insert_after=item.insert_after,
                                update_after=item.update_after)

    def entrance(self, args):
        self.writer.flush()

    def color_change(self):
        self.writer.color_change()

    def event(self, event):
        if self.writer.is_finish():
            if event.type == pygame.KEYDOWN:
                self.writer.event_keydown(event)

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)
