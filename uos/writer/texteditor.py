import pygame
from types import SimpleNamespace
from .texteditor_line import TextEditorLine
from .text import WriterText
from .carrot import Carrot
from ..uos import UOS

class TextEditor:
    def __init__(self, parent, rect, padding):
        self.state = parent.state
        self.timer = parent.state.timer(800, self.cursor_blink)
        self.display = SimpleNamespace(buffer=[],
                                       filename="",
                                       rect=rect,
                                       line=0,
                                       pos=0)

        self.linesize = UOS.text.font.get_linesize() + padding
        self.max_lines = int(rect.h / self.linesize) - 1
        self.editor_line = TextEditorLine(self)

    def entrance(self, filename):
        self.display.buffer = [WriterText("", sound_keys=None, state=[WriterText.State.append])]
        self.editor_line.text = self.display.buffer[0]
        self.display.filename = filename
        self.display.line = 0
        self.display.pos = 0
        self.editor_line.carrot_update()

    def load(self, filename):
        self.entrance(filename)
        keys = {'sound_keys':None, 'state':[WriterText.State.append]}
        with open(filename, 'r') as read_file:
            self.display.buffer = [WriterText(line.rstrip(), **keys) for line in read_file]
            self.editor_line.text = self.display.buffer[0]
            self.editor_line.carrot_update()

    def cursor_blink(self, timer):
        self.editor_line.carrot.blink()

    def event_keydown(self, event):
        self.editor_line.event_keydown(event)

    def render(self, surface):
        if self.display.line > self.display.pos + self.max_lines:
            self.display.pos += 1
        elif self.display.line < self.display.pos:
            self.display.pos = self.display.line

        topleft = [*self.display.rect.topleft]
        for item in self.display.buffer[self.display.pos: self.display.pos + self.max_lines]:
            item.render(surface, topleft)
            topleft[1] += self.linesize

        self.editor_line.carrot.topleft = [self.display.rect.x,
            self.display.rect.y + self.linesize * (self.display.line - self.display.pos)]
        self.editor_line.carrot.render(surface)
