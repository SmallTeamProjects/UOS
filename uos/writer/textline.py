import pygame
from types import SimpleNamespace
from .text import WriterText
from .carrot import Carrot
from .inputline import InputLine
from ..uos import UOS


class TextLine(InputLine):
    def __init__(self, parent, writer, carrot):
        InputLine.__init__(self, parent, Carrot(carrot))
        self.writer = writer
        self.recall = SimpleNamespace(pos = -1, buffer = [])
        self.clear_buffer()

    def render(self, surface, position):
        self.carrot.topleft = position[:]
        self.text.render(surface, position)
        self.carrot.render(surface)

    def clear_buffer(self):
        self.text.buffer = self.carrot.carrot[:]
        self.carrot.pos = self.carrot.length
        self.carrot.x = self.text.get_size(self.carrot.pos)

    def keydown_backspace(self):
        UOS.sounds.play('typing')
        if len(self.text.buffer) > self.carrot.length:
            front = self.text.buffer[:self.carrot.pos - 1]
            back = self.text.buffer[self.carrot.pos:]
            self.text.buffer = front + back
            self.carrot.pos -= 1
        else:
            self.clear_buffer()

    def keydown_down(self):
        UOS.sounds.play('typing')
        if self.recall.pos > 0:
            self.recall.pos -= 1
            self.text.buffer = self.recall.buffer[self.recall.pos]
            #self.text.set_text(''.join(self.text.buffer))
            self.carrot.pos = len(self.text.buffer)
        else:
            self.recall.pos = -1
            self.clear_buffer()

    def keydown_home(self):
        self.carrot.pos = self.carrot.length
        UOS.sounds.play('typing')

    def keydown_left(self):
        if self.carrot.pos > self.carrot.length:
            self.carrot.pos -= 1
        UOS.sounds.play('typing')

    def keydown_return(self):
        UOS.sounds.play('enter')
        self.recall.pos = -1
        if WriterText.State.invisible not in self.text.state:
            if self.text.buffer not in self.recall.buffer:
                if len(self.recall.buffer) > 4:
                    self.recall.buffer = [self.text.buffer] + self.recall.buffer[:4]
                else:
                    self.recall.buffer.insert(0, self.text.buffer)
            elif self.recall.buffer[0] != self.text.buffer:
                self.recall.buffer.remove(self.text.buffer)
                self.recall.buffer.insert(0, self.text.buffer)

        text = self.text.get_text()[2:]
        self.writer.append(self.text)
        self.new_text()
        self.clear_buffer()
        UOS.command(self, text)

    def keydown_up(self):
        UOS.sounds.play('typing')
        if self.recall.pos < len(self.recall.buffer) - 1:
            self.recall.pos += 1
            self.text.buffer = self.recall.buffer[self.recall.pos]
            #self.text.set_text(''.join(self.text.buffer))
            self.carrot.pos = len(self.text.buffer)

    def new_text(self):
        self.text = WriterText(''.join(self.carrot.carrot), 0,
            None, [WriterText.State.append])
