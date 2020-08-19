import pygame
from ..uos import UOS
from ..writer import Writer


class Terminal(UOS.State):
    def __init__(self):
        UOS.State.__init__(self)
        self.writer = Writer(self.state)
        if UOS.user.has_admin:
            x = 10
            y = 10
            w = self.state.machine.rect.w - x * 2
            rect = pygame.Rect(x, y, w, UOS.text.get_linesize())
            self.writer.add_output(rect)
            y += UOS.text.get_linesize()
            rect = pygame.Rect(x, y, w, self.state.machine.rect.bottom - y)
            self.writer.add_input(rect)
            self.writer.add(0, UOS.settings.header)
        else:
            for item in UOS.data.intro:
                self.writer.add_input(self.state.machine.rect.inflate(-20, -20))
                self.writer.add(0, item.text, item.interval, item.sound,
                                insert_after=item.insert_after,
                                update_after=item.update_after)

    def entrance(self, regain_focus):
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
