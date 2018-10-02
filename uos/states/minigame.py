import pygame
from random import randint
from ..uos import UOS
from ..writer import Writer


class MinigameBase(UOS.State):
    def __init__(self, attempts=4):
        UOS.State.__init__(self, None, True)
        self.writer = Writer(self.timer)
        h = UOS.text.get_linesize()
        w = UOS.Screen.rect.w
        # header
        self.writer.add_output(pygame.Rect(8, 8, w, h * 3))
        # body1
        self.writer.add_output(pygame.Rect(8, h * 4, 186, 308))
        # body2
        self.writer.add_output(pygame.Rect(188, h * 4, 186, 308))
        # body3
        self.writer.add_input(pygame.Rect(364, h, 140, 342), True, 0, True)
        self.header = 'temp header'
        self.attempts = attempts
        self.select = 0
        self.hex_seed = randint(4096,65535)
        self.password = 'APPLE'

    def call_back(self):
        UOS.State.flip_state = self._state.track

    def call_selection(self):
        pass

    def create_highlighter(self):
        self.selection = []
        for string in self.strings:
            if string:
                self.selection.append(self.render_text(string))
            else:
                self.selection.append(None)

    def attempts_remaining(self, count):
        debug_text = 'Attempts Remaining:'
        for x in range(count):
            debug_text += ' \x7f'
            x += 1
        return debug_text

    def generate_outline(self, index, hex_seed, count):
        hex_num = hex_seed
        for x in range(count):
            self.writer.add(index, hex(hex_num).upper() + ' ...........')
            hex_num += 12
            x += 1

    def remove_dud(self):
        UOS.sounds.play('dud')

    def test_likeness(self, password, attempt):
        length = len(password)
        matches = 0
        for x in range(length):
            if password[x] == attempt[x]:
                matches += 1
        if matches == length:
            UOS.sounds.play('good')
            # do stuff here
        else:
            UOS.sounds.play('bad')
            self.writer.add(3, '> Entry denied.')
            self.writer.add(3, '> Likeness=' + matches)
            # remove attempt


    def display_string(self):
        self.create_highlighter()
        self.writer.add(0, self.header)
        self.writer.add(0, "Password Required")
        self.writer.add(0, self.attempts_remaining(self.attempts))
        self.generate_outline(1, self.hex_seed, 16)
        self.generate_outline(2, self.hex_seed + 192, 16)
        # temporary section
        self.writer.add(3, '> CABINET')
        self.writer.add(3, '> Entry denied.')
        self.writer.add(3, '> Likeness=0')

    def entrance(self, args):
        self.writer.flush()
        self.select = 0


    def event(self, event):
        if self.writer.is_finish():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    UOS.sounds.play('scroll')
                    self.select += 11
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select += 11
                        self.select %= len(self.selection)

                elif event.key == pygame.K_UP:
                    UOS.sounds.play('scroll')
                    self.select -= 11
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select -= 11
                        self.select %= len(self.selection)

                elif event.key == pygame.K_LEFT:
                    self.select -= 1
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select -= 1
                        self.select %= len(self.selection)

                elif event.key == pygame.K_RIGHT:
                    UOS.sounds.play('scroll')
                    self.select += 1
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select += 1
                        self.select %= len(self.selection)

                elif event.key == pygame.K_RETURN:
                    UOS.sounds.play('attempt')
                    self.test_likeness(self.password,self.selection[self.select])  # todo get selected word

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

    def render_text(self, text):
        return UOS.text(text, (0,0,0), UOS.text.get_color())


class Minigame(MinigameBase):
    @staticmethod
    def setup():
        Minigame()

    def __init__(self):
        MinigameBase.__init__(self, 4)  # initialize class
        self.strings = ('')

        self.display_string()

    def call_selection(self):
        self.call_back()  # placeholder
