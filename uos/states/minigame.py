import pygame
import math
import string
from types import SimpleNamespace
from random import randint, random, choice
from ..uos import UOS
from ..writer import Writer
from ..writer.carrot import Carrot
from ..system.words import get_random_word, get_words


class MinigameBase(UOS.State):
    def __init__(self, attempts=4):
        UOS.State.__init__(self)
        self.writer = Writer(self.state)
        h = UOS.text.get_linesize()
        w = self.state.machine.rect.w
        self.top_height = h * 4 - 4
        bottom_height = h * 16
        b1, b2 = self.block_position = 8, 188
        # header
        self.writer.add_output(pygame.Rect(8, 8, w, h * 3))
        # body1
        self.writer.add_output(pygame.Rect(b1, self.top_height, 186, bottom_height))
        # body2
        self.writer.add_output(pygame.Rect(b2, self.top_height, 186, bottom_height))
        # body3
        self.writer.add_input(pygame.Rect(364, self.top_height, 140, bottom_height), True, 0, True)
        # configuration variables
        self.text_width = UOS.text.width(' ')
        self.carrot = Carrot()

        self.hex_seed = 0
        self.attempts = attempts
        self.difficulty = 5
        self.line_length = 12
        self.lines = 32
        self.characters = self.line_length * self.lines
        self.secret_word = None
        self.select = 0
        self.create_tab_exit()

    def attempts_remaining(self, count):
        debug_text = 'Attempts Remaining:'
        for x in range(count):
            debug_text += ' \x7f'
        return debug_text

    def call_selection(self):
        pass

    def carrot_highlight_words(self):
        self.carrot.type = ''
        position = None
        boolean_good = False
        line = self.carrot.line + (self.carrot.block - 1) * 16
        for pos in self.highlight_position:
            for pline, p in zip(pos['line'], pos['pos']):
                if pline == line:
                    if pos['type'] == 'words':
                        self.carrot.type = 'words'
                        if p[0] <= self.carrot.pos < p[1]:
                            position = pos
                            boolean_good = True
                            break
                    elif pos['type'] == 'brackets':
                        self.carrot.type = 'brackets'
                        if p[0] == self.carrot.pos or p[1] - 1 == self.carrot.pos:
                            position = pos
                            boolean_good = True
                            break

            if boolean_good:
                break

        self.carrot.text = ''
        self.carrot.hposition = position
        if position:
            self.highlight_images = []
            y = self.top_height
            for pline, p in zip(position['line'], position['pos']):
                text = self.display_buffer[pline][p[0]:p[1]]
                self.carrot.text += text
                if pline < 16:
                    x = self.block_position[0] - 8
                    pos = self.text_width * (p[0] + 8) + x, UOS.text.get_linesize() * pline + y
                else:
                    x = self.block_position[1] - 8
                    pos = self.text_width * (p[0] + 8) + x, UOS.text.get_linesize() * (pline - 16) + y

                self.highlight_images.append((UOS.text(text, (0,0,0), UOS.color.color), pos))
        else:
            self.highlight_images = None

    def color_change(self):
        self.create_tab_exit()
        self.writer.color_change()

    def create_tab_exit(self):
        self.brackets = UOS.text('[        ]')
        self.brackets_rect = self.brackets.get_rect()
        h = UOS.text.get_linesize()
        bracket_height = int(h * 1.5)
        self.brackets = pygame.transform.scale(self.brackets, (self.brackets_rect.w, bracket_height))
        self.brackets_rect.y = self.state.machine.rect.bottom - bracket_height - 2
        self.brackets_rect.centerx = self.state.machine.rect.centerx

        self.tab_exit = UOS.text('Tab)EXIT')
        self.tab_rect = self.tab_exit.get_rect()
        self.tab_rect.y = self.state.machine.rect.bottom - h - 4
        self.tab_rect.centerx = self.state.machine.rect.centerx

    def display_string(self):
        self.writer.add(0, UOS.settings.header)
        self.writer.add(0, "Password Required")
        self.writer.add(0, self.attempts_remaining(self.attempts))
        self.generate_outline(1, self.hex_seed, 16)
        self.generate_outline(2, self.hex_seed + 192, 16)
        # temporary section
        self.writer.add(3, '> ' + self.secret_word)
        self.writer.add(3, '> Entry denied.')
        self.writer.add(3, '> Likeness=0')

    def entrance(self, regain_focus):
        if not regain_focus:
            for i in range(4):
                self.writer.clear(i)

            self.generate_display()
            self.display_string()
            self.carrot_hposition = None
            self.carrot.init = False
            self.carrot.block = 1
            self.carrot.line = 0
            self.carrot.pos = 0
            self.carrot.width = self.text_width * 8
            self.carrot.topleft = [self.carrot.width, self.top_height]
            self.highlight_images = None

        self.carrot.show = False
        self.writer.flush()
        self.select = 0

    def event(self, event):
        if self.writer.is_finish():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.event_update_line(1)

                elif event.key == pygame.K_UP:
                    self.event_update_line(-1)

                elif event.key == pygame.K_LEFT:
                    self.event_update_pos(-1)

                elif event.key == pygame.K_RIGHT:
                    self.event_update_pos(1)

                elif event.key == pygame.K_RETURN:
                    UOS.sounds.play('password', 'attempt')
                    self.get_likeness(self.carrot.text)
                    # print(self.carrot.type)

                    # todo get selected word

                elif event.key == pygame.K_TAB:
                    self.state.flip_back()

    def event_update_block(self):
        self.carrot.block = self.carrot.block % 2 + 1
        self.carrot.topleft[0] = self.writer.blocks[self.carrot.block].rect.left
        self.carrot.topleft[0] += self.carrot.width - 8

    def event_update_line(self, inc):
        UOS.sounds.play('scroll')
        self.carrot.line += inc
        if self.carrot.line > 15 or self.carrot.line < 0:
            self.event_update_block()
        self.carrot.line %= 16
        height = self.writer.blocks[self.carrot.block].rect.top
        self.carrot.topleft[1] = height + UOS.text.get_linesize() * self.carrot.line
        self.update_carrot_data()

    def event_update_pos(self, inc):
        UOS.sounds.play('scroll')
        # if words then skip to front or back
        if self.carrot.hposition and self.carrot.hposition['type'] == 'words':
            for line, pos in zip(self.carrot.hposition['line'], self.carrot.hposition['pos']):
                i = (self.carrot.block - 1) * 16
                if self.carrot.line + i == line:
                    if inc > 0:
                        self.carrot.pos = pos[1] - 1
                    else:
                        self.carrot.pos = pos[0]
                    break

        self.carrot.pos += inc
        if self.carrot.pos > 11 or self.carrot.pos < 0:
            self.event_update_block()
        self.carrot.pos %= 12
        self.update_carrot_data()

    # creates the full grid by filling remaining space with junk
    def generate_display(self):
        # remove . from punctuation
        punctuation = string.punctuation
        punctuation = punctuation[:13] + punctuation[14:]
        # fill display buffer with junk
        self.display_buffer = [choice(punctuation) for i in range(self.characters)]
        self.hex_seed = randint(4096, 65535)
        word_count = randint(self.difficulty // 2 + 3, self.difficulty + self.difficulty // 2)
        self.secret_word = get_random_word(self.difficulty)
        random_words = get_words(self.difficulty, self.secret_word, word_count)

        junk = SimpleNamespace(
            low = 0.0,
            high = self.characters / (word_count + 1),
            value = self.characters / (word_count + 1)
        )

        hposition = []
        # insert words and store highlight position
        for word in random_words:
            # don't let words touch
            x = randint(int(junk.low) + 1, int(junk.high) - self.difficulty)
            self.display_buffer[x: x + self.difficulty] = list(word)
            hposition.append((x, x + self.difficulty))
            junk.low += junk.value
            junk.high += junk.value

        # covert display buffer to string
        self.display_buffer = ''.join(self.display_buffer)
        # split into lines
        self.display_buffer = [self.display_buffer[i:i + 12] for i in range(0, self.characters, 12)]
        self.highlight_position = self.generate_highlight_positions(hposition, 'words')
        self.highlight_position.extend(self.get_bracket_sets())

    def generate_highlight_positions(self, hposition, type):
        # print(hposition)
        highlight_position = []
        self.highlight_images = None
        for position in hposition:
            # line numbers
            dx = position[0] // 12
            dy = position[1] // 12
            # position on line
            p = position[0] % 12, position[1] % 12
            if dx == dy or p[1] == 0:
                if p[1] == 0:
                    p = p[0], 12

                # line number, position
                highlight_position.append({'line':(dx,), 'pos':(p,), 'type':type})
            else:
                p1 = p[0], 12
                p2 = 0, p[1]
                highlight_position.append({'line':(dx,dy), 'pos':(p1,p2), 'type':type})

        return highlight_position

    def generate_outline(self, index, hex_seed, count):
        hex_num = hex_seed
        i = (index - 1) * 16
        for x in range(count):
            self.writer.add(index, hex(hex_num).upper() + ' ............', -1,
                update_after = (-1, 7, self.display_buffer[x + i]))
            hex_num += 12

    # highlight bracket sets
    def get_bracket_sets(self):
        openers = '([{<'
        closers = ')]}>'
        sets = []
        index = 0
        # iterates over each line to find sets
        for enum, line in enumerate(self.display_buffer):
            j = 0
            n = enum * self.line_length
            # find every possible match
            for j in range(self.line_length):
                letter = line[j]
                if letter in openers:
                    br_index = openers.index(letter)
                    start_index = j
                    closer = closers[br_index]
                    if closer in line[start_index:]:
                        end_index = line.find(closer, start_index)
                        sets.append((start_index + n, end_index + n + 1))
        return self.generate_highlight_positions(sets, 'brackets')

    # gets character likeness
    def get_likeness(self, word):
        likeness = 0
        if self.carrot.type is 'words' and word is not '':
            for enum, letter in enumerate(self.secret_word):
                if word[enum] == letter:
                    likeness += 1

        if self.carrot.type is 'words' and likeness == len(self.secret_word):
            UOS.sounds.play('password', 'good')
            # todo pass valid logon
        elif self.carrot.type is 'words' and word is not '':
            UOS.sounds.play('password', 'bad')
            self.writer.add(3, '> ' + word)
            self.writer.add(3, '> Entry denied.')
            self.writer.add(3, '> Likeness=' + str(likeness))
            if self.attempts > 0:
                self.attempts -= 1
                attempt_line = self.writer.get_line(0, 2)
                attempt_line.set_text(attempt_line.get_text()[:-2])
            # todo if 0 attempts lock
        elif self.carrot.type is 'brackets':
            self.hack()
        else:
            UOS.sounds.play('password', 'bad')
            self.writer.add(3, '> Error.')

    # returns word from highlight_position

    # runs bracket functions
    def hack(self):
        roll = randint(0,4)
        if roll == 4:
            self.reset_tries()
        else:
            self.remove_dud()


    # removes dud
    def remove_dud(self):
        UOS.sounds.play('password', 'dud')
        self.writer.add(3, '> Dud Removed.')
        # todo replace letters of a random word that isn't the secret word with "."

    def render(self, surface):
        if self.writer.is_finish() and not self.carrot.init:
            self.carrot.init = True
            self.carrot.show = True
            self.update_carrot_data()

        surface.fill((0,0,0))
        self.writer.render(surface)
        self.carrot.render(surface)

        if self.writer.is_finish():
            surface.blit(self.tab_exit, self.tab_rect)
            surface.blit(self.brackets, self.brackets_rect)

            if self.highlight_images:
                for image, pos in self.highlight_images:
                    surface.blit(image, pos)

    def render_text(self, text):
        return UOS.text(text, (0,0,0), UOS.color.color)

    # sets attempts back to 4
    def reset_tries(self):
        UOS.sounds.play('password', 'attempt')
        self.writer.add(3, '> Tries Reset.')
        self.attempts = 4
        attempt_line = self.writer.get_line(0, 2)
        attempt_line.set_text(self.attempts_remaining(self.attempts))

    def update_carrot_data(self):
        self.carrot_highlight_words()
        i = (self.carrot.block - 1) * 16
        letter = self.display_buffer[self.carrot.line + i][self.carrot.pos]
        self.carrot.black_letter = UOS.text(letter, (0,0,0))
        self.carrot.x = self.text_width * self.carrot.pos


class Minigame(MinigameBase):
    @staticmethod
    def setup():
        Minigame()

    def __init__(self):
        MinigameBase.__init__(self, 4)  # initialize class
        self.strings = ('')

    def call_selection(self):
        self.state.flip_back()  # placeholder
