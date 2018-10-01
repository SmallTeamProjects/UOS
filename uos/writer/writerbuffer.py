from .writerhandler import WriterHandler
from .bufferbox import BufferBox
from .text import WriterText
from ..uos import UOS

class WriterBuffer:
    def __init__(self, timer, rect, padding, reverse=False):
        self.bufferbox = BufferBox(rect, UOS.text.get_linesize(padding), reverse)
        self.linesize = UOS.text.get_linesize(padding)
        self.handler = WriterHandler(self)
        self.timer = timer
        self.rect = rect

    def add(self, text, interval, sound_keys, newline, invisible,
            insert_after, update_after):
        states = []
        if invisible:
            states.append(WriterText.State.invisible)

        if isinstance(text, (tuple, list)):
            texts = []
            for t in text:
                texts.extend(self.wordwrap(t))
            text = texts
        else:
            text = self.wordwrap(text)

        if isinstance(text, (tuple, list)):
            self.handler.add(*[WriterText(t, interval, sound_keys, newline,
                             states, insert_after, update_after) for t in text])
        else:
            self.handler.add(WriterText(text, interval, sound_keys, newline,
                             states, insert_after, update_after))

    def append(self, item):
        self.bufferbox.add(item)

    def bottom_line(self):
        return [self.bufferbox.rect.left, self.bufferbox.rect.bottom - self.linesize]

    def flush(self):
        if len(self.bufferbox.items) > 0:
            for item in self.bufferbox.items:
                if item:
                    item.pos = 0
                    item.updated = False
                    if item.interval == 0:
                        item.interval = -1

                    if item.sound_keys is None:
                        item.sound_keys = ['typing multiple']

                    if WriterText.State.invisible in item.state:
                        item.state = [WriterText.State.invisible]
                    else:
                        item.state = []

            self.handler.add(*self.bufferbox.items)
            self.bufferbox.items = []
            self.bufferbox.position = self.bufferbox.rect.topleft

    def is_finish(self):
        return self.handler.is_finish()

    def render(self, surface, render_handler=False, position=None):
        if position:
            position = list(position)
        else:
            position = list(self.bufferbox.position)

        if self.bufferbox.reverse:
            if render_handler:
                self.handler.render(surface, position, -self.linesize, self.rect.x)

            self.bufferbox.render(surface)
        else:
            self.bufferbox.render(surface)
            if render_handler:
                self.handler.render(surface, position, self.linesize, self.rect.x)

    def set_rect(self, rect):
        self.rect = rect
        self.bufferbox.set_rect(rect)

    def wordwrap(self, text):
        if isinstance(text, (tuple, list)):
            return [text]

        if UOS.text.size(text)[0] > self.rect.w:
            words = text.split()
            line = []
            texts = []
            for word in words:
                if UOS.text.size(' '.join(line + [word]))[0] < self.rect.w:
                    line.append(word)
                else:
                    texts.append(' '.join(line))
                    line = [word]

            if len(line) > 0:
                texts.append(' '.join(line))

            return texts
        else:
            return [text]
