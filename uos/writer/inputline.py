import pygame
from ..uos import UOS
from .text import WriterText


class InputLine:
    def __init__(self, link, carrot):
        self.link = link
        self.carrot = carrot
        self.new_text()

        self.key_event = {
            pygame.KMOD_NONE: {
                pygame.K_BACKSPACE: self.keydown_backspace,
                pygame.K_DELETE: self.keydown_delete,
                pygame.K_DOWN: self.keydown_down,
                pygame.K_END: self.keydown_end,
                pygame.K_HOME: self.keydown_home,
                pygame.K_LEFT: self.keydown_left,
                pygame.K_RETURN: self.keydown_return,
                pygame.K_RIGHT: self.keydown_right,
                pygame.K_UP: self.keydown_up
            }
        }

    def carrot_update(self):
        self.carrot.x = self.text.get_size(self.carrot.pos)
        if self.carrot.pos < len(self.text.buffer):
            self.carrot.black_letter = UOS.text(self.text.buffer[self.carrot.pos], (0,0,0))
        else:
            self.carrot.black_letter = None

    def clear_buffer(self):
        self.text.buffer = []
        self.carrot.pos = 0
        self.carrot.x = 0

    def event_keydown(self, event):
        self.carrot.show = True
        self.link.timer.reset()

        ctrl = event.mod & pygame.KMOD_CTRL
        if ctrl == 0 and 31 < event.key < 127:
            self.text.buffer.insert(self.carrot.pos, event.unicode)
            self.carrot.pos += 1
            UOS.sounds.play('typing')
            self.update_line()
        elif ctrl == 0:
            if self.key_event[pygame.KMOD_NONE].get(event.key, False):
                self.key_event[pygame.KMOD_NONE][event.key]()
        elif ctrl > 0:
            if self.key_event.get(pygame.KMOD_CTRL, False):
                if self.key_event[pygame.KMOD_CTRL].get(event.key, False):
                    self.key_event[pygame.KMOD_CTRL][event.key]()

        self.text.updated = False
        self.carrot_update()

    def keydown_backspace(self):
        UOS.sounds.play('typing')
        if self.carrot.pos > 1:
            front = self.text.buffer[:self.carrot.pos - 1]
            back = self.text.buffer[self.carrot.pos:]
            self.text.buffer = front + back
            self.carrot.pos -= 1
        else:
            self.clear_buffer()

    def keydown_delete(self):
        UOS.sounds.play('typing')
        self.clear_buffer()

    def keydown_down(self):
        pass

    def keydown_end(self):
        self.carrot.pos = len(self.text.buffer)
        UOS.sounds.play('typing')

    def keydown_home(self):
        self.carrot.pos = 0
        UOS.sounds.play('typing')

    def keydown_left(self):
        if self.carrot.pos > 0:
            self.carrot.pos -= 1
        UOS.sounds.play('typing')

    def keydown_return(self):
        pass

    def keydown_right(self):
        if self.carrot.pos < len(self.text.buffer):
            self.carrot.pos += 1
        UOS.sounds.play('typing')

    def keydown_up(self):
        pass

    def new_text(self):
        self.text = WriterText('', 0, None, True, [WriterText.State.append])

    def update_line(self):
        pass
