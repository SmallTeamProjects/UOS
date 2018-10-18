import pygame
from ..uos import UOS
from ..writer import Writer

class Loading(UOS.State):
    def __init__(self):
        UOS.State.__init__(self)
        self.writer = Writer(self.state)
        self.writer.add_output(self.state.machine.rect.inflate(-16, -16))
        self.time_next = 800
        for item in UOS.data.loading:
            self.writer.add(0, item.text, item.interval,
                            item.sound, item.newline,
                            insert_after=item.insert_after,
                            update_after=item.update_after)

    def entrance(self, regain_focus):
        self.writer.flush()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state.flip('Terminal')

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

    def update(self, ticks, delta):
        if self.writer.is_finish() and self.time_next > 0:
            self.time_next -= delta
        elif self.time_next < 1:
            self.state.flip('Terminal')
