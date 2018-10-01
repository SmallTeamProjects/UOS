from types import SimpleNamespace
from .text import WriterText
from ..uos import UOS


# WriterHandler handles the typewriting effect. It store all the
# lines. Display first one then send it to display when finish.
class WriterHandler:
    def __init__(self, link):
        self.link = link
        self.buffer = []
        self.update_after = []
        self.current = None
        self.update = False

    def add(self, *args):
        self.buffer.extend(args)
        self.update = False
        if self.current is None:
            self.next_line()

    def callback(self, timer):
        if self.current:
            self.current.updated = False

    def callback_fast(self, timer):
        if self.update:
            self.current.callback_after(timer)
        elif self.current:
            self.current.callback_fast(timer)

    def is_finish(self):
        return self.current is None

    def next_line(self):
        self.current = False
        while self.current is False:
            if len(self.buffer) > 0:
                self.current = self.buffer.pop(0)
                if self.current:
                    if isinstance(self.current.interval, (tuple, list)):
                        self.link.timer.interval = self.current.interval[0]
                    else:
                        self.link.timer.interval = self.current.interval
                    self.link.timer.reset()
                else:
                    self.link.append(None)
                    self.current = False
            else:
                if len(self.update_after) > 0:
                    self.update = True
                    self.current = self.update_after.pop(0)
                else:
                    self.update = False
                    self.current = None

    def newline(self):
        if self.current and self.current != 'update':
            return self.current.newline
        return True

    def render(self, surface, position, linesize, left):
        if self.current:
            if not self.update:
                self.current.render(surface, position)
                
            if self.current.newline:
                position[0] = left
                position[1] += linesize
            else:
                position[0] += self.current.image.get_rect().w

            if self.update:
                if self.current.update_finish:
                    self.next_line()
            elif self.current.is_finish():
                if self.current.update_after:
                    self.update_after.append(self.current)

                self.link.append(self.current)
                self.next_line()
