import pygame
from types import SimpleNamespace
from .inputline import InputLine
from .text import WriterText
from .carrot import Carrot
from ..uos import UOS


class TextEditorLine(InputLine):
    @staticmethod
    def create_link(timer, display, max_lines, last_state):
        return SimpleNamespace(
            timer = timer,
            display = display,
            max_lines = max_lines,
            last_state = last_state)

    def __init__(self, link):
        InputLine.__init__(self, link, Carrot())

        self.key_event.update(
            {pygame.KMOD_CTRL: {
                pygame.K_END: self.keydown_ctrl_end,
                pygame.K_HOME: self.keydown_ctrl_home,
                pygame.K_s: self.keydown_ctrl_s,
                pygame.K_x: self.keydown_ctrl_x
            }})

    def get_display_line(self, offset=0):
        return self.link.display.buffer[self.link.display.line + offset]

    def keydown_backspace(self):
        if self.carrot.pos > 0:
            InputLine.keydown_backspace(self)
        elif self.link.display.line > 0:
            text = self.link.display.buffer.pop(self.link.display.line)
            self.link.display.line -= 1
            self.carrot.pos = self.get_display_line().get_length()
            self.get_display_line().extend(text)
            self.update_line_length()
            self.text = self.get_display_line()

    def keydown_down(self):
        UOS.sounds.play('typing')
        if len(self.link.display.buffer) - 1 > self.link.display.line:
            self.link.display.line += 1
            self.text = self.get_display_line()
            if self.carrot.pos > len(self.text.buffer):
                self.carrot.pos = len(self.text.buffer)

    def keydown_return(self):
        UOS.sounds.play('enter')
        self.new_text()
        self.carrot.pos = 0
        self.link.display.line += 1
        self.link.display.buffer.insert(self.link.display.line, self.text)

    def keydown_up(self):
        UOS.sounds.play('typing')
        if self.link.display.line > 0:
            self.link.display.line -= 1
            self.text = self.get_display_line()
            if self.carrot.pos > len(self.text.buffer):
                self.carrot.pos = len(self.text.buffer)

    def keydown_ctrl_end(self):
        self.link.display.line = len(self.link.display.buffer) - 1
        self.link.display.pos = max(0, self.link.display.line - self.link.max_lines)
        self.text = self.get_display_line()
        self.carrot.pos = len(self.text.buffer)

    def keydown_ctrl_home(self):
        self.link.display.line = 0
        self.link.display.pos = 0
        self.carrot.pos = 0
        self.text = self.get_display_line()

    def keydown_ctrl_s(self):
        if len(self.link.display.buffer) > 0:
            with open(self.link.display.filename, 'w') as write_file:
                for item in self.link.display.buffer:
                    write_file.write(item.get_text() + '\n')

            UOS.State.args = self.link.display.filename
            UOS.State.next_state = 'SavingEditor'

    def keydown_ctrl_x(self):
        self.link.last_state()

    def update_line(self):
        if self.update_line_length():
            self.link.display.line += 1
            self.text = self.get_display_line()
            self.carrot.pos = self.text.get_length()

    def update_line_length(self):
        lines = self.wordwrap(self.get_display_line())
        if lines:
            for enum, line in enumerate(lines):
                if enum != 0:
                    self.link.display.buffer.insert(self.link.display.line + enum, line)
                else:
                    self.link.display.buffer[self.link.display.line] = line

            return True
        return False

    def wordwrap(self, textline):
        text = textline.get_text()
        if UOS.text.width(text) > self.link.display.rect.w:
            words = text.split()
            line = []
            texts = []
            for word in words:
                if UOS.text.width(' '.join(line + [word])) < self.link.display.rect.w:
                    line.append(word)
                else:
                    tex = ' '.join(line)
                    texts.append(WriterText(tex, **textline.get_settings()))
                    line = [word]

            if len(line) > 0:
                tex = ' '.join(line)
                texts.append(WriterText(tex, **textline.get_settings()))

            return texts
        else:
            return None
