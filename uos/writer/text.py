import pygame
from enum import Enum
from ..uos import UOS


# This class will handle rendering text. Flags will give more
# options. Append allows for typewriter. Invisible hide text in
# star format. Interval are for typewriter effect speed. Interval
# zero equals no typewriter effect.
# insert and update_after = tuple(interval, start, string). interval = 0 just
# prints everything. insert happens after line is printed. update happens
# after the whole block is printed

class WriterText:
    State = Enum('State', 'invisible, append', module=__name__)

    def __init__(self, text,
                 interval=0,
                 sound_keys=['typing multiple'],
                 state=[],
                 insert_after = None,
                 update_after = None):

        if isinstance(text, (tuple, list)):
            self.interval_change = [len(t) - 1 for t in text][:-1]
            text = ''.join(text)
        else:
            self.interval_change = None

        self.pos = 0
        self.offset = 0
        self.image = None
        self.state = state
        self.updated = False
        self.buffer = list(text)
        self.interval = interval
        self.interval_pos = 0
        self.sound_keys = sound_keys
        self.insert_after = insert_after
        self.insert_pos = -1
        self.insert_finish = insert_after is None
        self.update_after = update_after
        self.update_pos = -1
        self.update_finish = self.update_after is None

        # Track how many spaces. Helps typewriter effect from typing
        # spaces.
        for letter in self.buffer:
            if letter == ' ':
                self.offset += 1
            else:
                break

    def callback_after(self, timer):
        interval, start, text = self.update_after
        if interval == 0:
            self.buffer[start:start + len(text)] = list(text)
            self.update_finish = True
        else:
            if self.update_pos == -1:
                timer.interval = interval
                self.update_pos = 0

            if self.update_pos < len(text):
                self.buffer[start + self.update_pos] = text[self.update_pos]
                self.update_pos += 1
            else:
                self.update_finish = True

    def callback(self, timer):
        if not self.is_finish(True):
            self.pos += timer.count
            if isinstance(self.interval, tuple):
                if self.interval_change:
                    if self.interval_pos < len(self.interval_change):
                        if self.pos > self.interval_change[self.interval_pos]:
                            self.pos = self.interval_change[self.interval_pos]

                        if self.interval_change[self.interval_pos] <= self.pos:
                            self.interval_pos += 1
                            if len(self.interval_change) >= self.interval_pos:
                                timer.interval = self.interval[self.interval_pos]
        elif not self.is_finish():
            if self.insert_after and not self.insert_finish:
                interval, start, text = self.insert_after
                if interval == 0:
                    self.buffer[start:start + len(text)] = list(text)
                    self.insert_finish = True
                else:
                    if self.insert_pos == -1:
                        timer.interval = interval

                    for i in range(timer.count):
                        if self.insert_pos < len(text):
                            self.buffer[start + self.insert_pos] = text[self.insert_pos]
                            self.insert_pos += 1
                        else:
                            self.insert_finish = True
                            break

    def extend(self, text):
        self.buffer.extend(text.buffer)
        self.updated = False

    def get_rect(self):
        if self.image:
            return self.image.get_rect()
        return pygame.Rect(0,0,0,UOS.text.get_linesize())

    def get_height(self):
        return UOS.text.get_linesize()

    def get_text(self):
        return ''.join(self.buffer)

    def get_settings(self):
        return {'interval': self.interval,
                'sound_keys': self.sound_keys,
                'state': self.state}

    def get_size(self, slice=-1):
        if slice == -1:
            return UOS.text.width(self.get_text())
        if slice == 0:
            return 0

        text = ''.join(self.buffer[:slice])
        return UOS.text.width(text)

    def get_width(self):
        return UOS.text.width(self.get_text())

    def is_finish(self, text_finish=False):
        if text_finish:
            return self.interval == 0 or self.pos > len(self.buffer)
        return self.is_finish(True) and self.insert_finish

    def render(self, surface, position):
        if not self.updated or self.image is None:
            if self.sound_keys:
                for sound in self.sound_keys:
                    UOS.sounds.play(sound)

            self.update_image()

        surface.blit(self.image, position)

    def reset(self):
        self.pos = 0
        self.insert_pos = -1
        self.insert_finish = self.insert_after is None
        self.interval_pos = 0
        self.update_pos = -1
        self.update_finish = self.update_after is None

    def update_image(self):
        if self.interval == 0 or WriterText.State.append in self.state:
            length = len(self.buffer)
        else:
            length = self.pos

        if WriterText.State.invisible in self.state:
            star = '> ' + '*' * (length - 2)
            self.image = UOS.text(star)
        else:
            text = ''.join(self.buffer[:length])
            self.image = UOS.text(text)

        self.updated = True

    def set_text(self, text):
        self.buffer = list(text)
        self.updated = False

    def __repr__(self):
        if self.interval == 0:
            return "WriterText(text:{0})".format(self.get_text())
        return "WriterText(text:{0}, interval:{1})".format(self.get_text(), self.interval)
