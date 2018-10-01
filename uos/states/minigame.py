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

    def attempts_remaining(self, attempts):
        debug_text = 'Attempts Remaining:'
        x = 0
        while x != attempts:
            debug_text += ' \x7f'
            x += 1
        return debug_text

    def generate_outline(self, index, hex_seed, count):
        hex_num = hex_seed
        x = 0
        while x != count:
            self.writer.add(index, hex(hex_num).upper() + ' ...........')
            hex_num += 12
            x += 1

    def display_string(self):
        self.create_highlighter()
        self.writer.add(0, self.header)
        self.writer.add(0, "Password Required")
        self.writer.add(0, self.attempts_remaining(self.attempts))
        self.generate_outline(1, self.hex_seed, 16)
        self.generate_outline(2, self.hex_seed + 192, 16)
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
                    self.select += 1
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select += 1
                        self.select %= len(self.selection)

                elif event.key == pygame.K_UP:
                    UOS.sounds.play('scroll')
                    self.select -= 1
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select -= 1
                        self.select %= len(self.selection)

                elif event.key == pygame.K_LEFT:
                    UOS.sounds.play('enter')
                    UOS.State.flip_state = self._state.track

                elif event.key in [pygame.K_RETURN, pygame.K_RIGHT]:
                    UOS.sounds.play('enter')
                    self.call_selection()

    def render(self, surface):
        surface.fill((0,0,0))
        self.writer.render(surface)

        #if self.writer.is_finish():
         #   position = self.rect.x, self.rect.y + self.linesize * (self.select + 3)
          #  surface.blit(self.selection[self.select], position)

    def render_text(self, text):
        return UOS.text(text, (0,0,0), UOS.text.get_color())


class Minigame(MinigameBase):
    @staticmethod
    def setup():
        Minigame()

    def __init__(self):
        MinigameBase.__init__(self, 3)  # initialize class
        self.strings = ('')

        self.display_string()

    def call_selection(self):
        self.call_back() #placeholder