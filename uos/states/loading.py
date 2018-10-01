import pygame
from ..uos import UOS
from ..writer import Writer

class Loading(UOS.State):
    def __init__(self):
        UOS.State.__init__(self)
        self.writer = Writer(self.timer)
        self.writer.add_output(UOS.Screen.rect.inflate(-20, -20))
        self.time_next = 800
        for item in UOS.Data.loading:
            self.writer.add(0, item.text, item.interval,
                            item.sound, item.newline,
                            insert_after=item.insert_after,
                            update_after=item.update_after)

    def entrance(self, args):
        self.writer.flush()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                UOS.State.next_state = 'Terminal'
            else:
                self.writer.event_keydown(event)

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

        if self.writer.is_finish() and self.time_next > 0:
            self.time_next -= UOS.Timer.delta
        elif self.time_next < 1:
            UOS.State.next_state = 'Terminal'
