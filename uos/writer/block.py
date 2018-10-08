import pygame
from ..uos import UOS
from .carrot import Carrot
from .text import WriterText
from .textline import TextLine
from .writerbuffer import WriterBuffer
from types import SimpleNamespace

class OutputBlock:
    def __init__(self, state, rect, padding, reverse):
        self.callback_timer = state.timer(-1, self.callback)
        self.callback_timer.stop = True
        self.writer = WriterBuffer(self.callback_timer, rect, padding, reverse)
        self.reverse = reverse
        self.state = state
        self.rect = rect

    def add(self, text,
            interval=-1,
            sound_keys=['typing multiple'],
            newline=True,
            invisible=False,
            insert_after=None,
            update_after=None):

        self.writer.add(text, interval, sound_keys, newline, invisible,
                        insert_after, update_after)

    def add_empty(self, count=1):
        for c in range(count):
            self.writer.handler.buffer.append(None)

    def clear(self):
        self.writer.bufferbox.clear();

    def callback(self, timer):
        if not self.writer.handler.is_finish():
            self.writer.handler.callback(timer)

    def color_change(self):
        for itemlist in [self.writer.bufferbox.items, self.writer.handler.buffer]:
            for item in itemlist:
                if item:
                    item.update_image()

    def is_finish(self):
        return self.writer.is_finish()

    def render(self, surface):
        if self.writer.is_finish():
            self.writer.render(surface)
        else:
            self.writer.render(surface, True)

class InputBlock(OutputBlock):
    def __init__(self, state, rect, system, padding, reverse, carrot='> '):
        OutputBlock.__init__(self, state, rect, padding, reverse)
        self.timer = state.timer(800, self.cursor_blink)
        self.system = system

        if system:
            self.writer.bufferbox.max_lines -= 1

        writer = SimpleNamespace(add=self.add, clear=self.clear,
                                 append=self.writer.append,
                                 add_empty=self.add_empty,
                                 set_system=self.set_system)

        self.text_line = TextLine(self, writer, list(carrot))

    def add(self, text,
            interval=-1,
            sound_keys=['typing multiple'],
            protect=False,
            newline=True,
            invisible=False,
            insert_after=None,
            update_after=None):

        if protect:
            self.text_line.text.state.append(WriterText.State.invisible)

        OutputBlock.add(self, text, interval, sound_keys, newline, invisible,
                        insert_after, update_after)

    def color_change(self):
        OutputBlock.color_change(self)
        self.text_line.text.update_image()

    def cursor_blink(self, timer):
        self.text_line.carrot.blink()

    def render(self, surface):
        if self.writer.is_finish():
            if not self.system:
                self.writer.render(surface)
                self.text_line.render(surface, list(self.writer.bufferbox.position))
            else:
                self.writer.render(surface, position=self.writer.bottom_line())
                h = self.rect.bottom - self.writer.linesize
                self.text_line.render(surface, [self.rect.left, h])
        else:
            if self.system:
                self.writer.render(surface, True, self.writer.bottom_line())
            else:
                self.writer.render(surface, True)

    def set_system(self, boolean):
        self.system = boolean
