import pygame
import math
import string
from random import randint, random, choice, shuffle
from ..uos import UOS
from ..writer import Writer
from ..writer.carrot import Carrot


class MinigameBase(UOS.State):
    def __init__(self, attempts=4):
        UOS.State.__init__(self)
        self.writer = Writer(self.state)
        h = UOS.text.get_linesize()
        w = self.state.machine.rect.w
        self.top_height = h * 4 - 4
        bottom_height = h * 16
        # header
        self.writer.add_output(pygame.Rect(8, 8, w, h * 3))
        # body1
        self.writer.add_output(pygame.Rect(8, self.top_height, 186, bottom_height))
        # body2
        self.writer.add_output(pygame.Rect(188, self.top_height, 186, bottom_height))
        # body3
        self.writer.add_input(pygame.Rect(364, self.top_height, 140, bottom_height), True, 0, True)
        # configuration variables
        self.text_width = UOS.text.width(' ')
        self.carrot = Carrot()

        self.header = 'temp header'
        self.hex_seed = randint(4096, 65535)
        self.attempts = attempts
        self.difficulty = 5
        self.line_length = 12
        self.lines = 32
        self.characters = self.line_length * self.lines
        self.secret_word = 'APPLE'
        self.words = []
        self.places = []
        self.select = 0
        self.generate_display()

        self.brackets = UOS.text('[        ]')
        self.brackets_rect = self.brackets.get_rect()
        bracket_height = int(h * 1.5)
        self.brackets = pygame.transform.scale(self.brackets, (self.brackets_rect.w, bracket_height))
        self.brackets_rect.y = self.state.machine.rect.bottom - bracket_height - 2
        self.brackets_rect.centerx = self.state.machine.rect.centerx

        self.tab_exit = UOS.text('Tab)EXIT')
        self.tab_rect = self.tab_exit.get_rect()
        self.tab_rect.y = self.state.machine.rect.bottom - h - 4
        self.tab_rect.centerx = self.state.machine.rect.centerx

    def attempts_remaining(self, count):
        debug_text = 'Attempts Remaining:'
        for x in range(count):
            debug_text += ' \x7f'
        return debug_text

    def call_selection(self):
        pass

    def carrot_highlight_words(self):
        position = None
        boolean_good = False
        line = self.carrot.line + (self.carrot.block - 1) * 16
        for pos in self.highlight_position:
            for pline, p in zip(pos['line'], pos['pos']):
                if pline == line:
                    if p[0] <= self.carrot.pos < p[1]:
                        position = pos
                        boolean_good = True
                        break

                        if boolean_good:
                            break

                            if position:
                                self.highlight_images = []
                                x = self.writer.blocks[self.carrot.block].rect.left - 8
                                y = self.writer.blocks[self.carrot.block].rect.top
                                for pline, p in zip(position['line'], position['pos']):
                                    text = self.display_buffer[pline][p[0]:p[1]]
                                    pos = self.text_width * (p[0] + 8) + x, UOS.text.get_linesize() * (pline % 16) + y
                                    self.highlight_images.append((UOS.text(text, (0,0,0), UOS.text.get_color()), pos))
                                else:
                                    self.highlight_images = None

    def display_string(self):
        self.writer.add(0, self.header)
        self.writer.add(0, "Password Required")
        self.writer.add(0, self.attempts_remaining(self.attempts))
        self.generate_outline(1, self.hex_seed, 16)
        self.generate_outline(2, self.hex_seed + 192, 16)
        # temporary section
        self.writer.add(3, '> CABINET')
        self.writer.add(3, '> Entry denied.')
        self.writer.add(3, '> Likeness=0')

    def entrance(self, regain_focus):
        if not regain_focus:
            for i in range(4):
                self.writer.clear(i)

            self.generate_display()
            self.display_string()
            self.carrot.show = False
            self.carrot.init = False
            self.carrot.block = 1
            self.carrot.line = 0
            self.carrot.pos = 0
            self.carrot.width = self.text_width * 8
            self.carrot.topleft = [self.carrot.width, self.top_height]
            self.highlight_images = None

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
        self.carrot.pos += inc
        if self.carrot.pos > 11 or self.carrot.pos < 0:
            self.event_update_block()
        self.carrot.pos %= 12
        self.update_carrot_data()

    # randomizes world locations, returns 2d array with paired index and word
    def find_places(self,words,difficulty,characters):
        places = []
        placed = False
        blacklist = []
        for x in range(len(words)):
            placed = False
            while not placed and len(blacklist) < characters * 0.8:
                place = math.floor(random.random() * (characters - difficulty))
                # check blacklist array to make sure there isn't a word conflict
                if place in blacklist < 0:
                    places.append([place,words[x]])
                    places = True
                    # add used spaces to blacklist array
                    j = place - difficulty
                    while j <= place + difficulty:
                        blacklist.append(j)
                        j += 1
        return places.sort()  # this might need tweaking

    # creates the full grid by filling remaining space with junk
    def generate_display(self):
        self.display_buffer = ''
        # temp words
        random_words = ['APPLE', 'READY', 'WORLD', 'HELLO', 'FILED', 'JAMMED',
                        'WALLS', 'BOXES', 'JUNK', 'MIRCO', 'CHIPS', 'COMS',
                        'LISTS', 'FOLLOW', 'PRINT', 'WHILE', 'CLASS']

        shuffle(random_words)
        max_junk = 34
        min_junk = 24
        word_count = 0
        junk_count = min_junk + 1
        x = 0

        # remove . from punctuation
        hposition = []
        punctuation = string.punctuation
        punctuation = punctuation[:13] + punctuation[14:]
        while x < self.characters:
            if ((randint(0, 5) == 0 and junk_count > min_junk) or
                 junk_count > max_junk) and word_count < 10:
                self.display_buffer += random_words[word_count]
                l = len(random_words[word_count])
                hposition.append((x, x + l))
                x += l
                word_count += 1
                junk_count = 0
            else:
                self.display_buffer += choice(punctuation)
                junk_count += 1
                x += 1

        # split into lines
        self.display_buffer = [self.display_buffer[i:i + 12] for i in range(0, self.characters, 12)]
        self.generate_highlight_positions(hposition)

    def generate_highlight_positions(self, hposition):
        self.highlight_position = []
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
                self.highlight_position.append({'line':(dx,), 'pos':(p,)})
            else:
                p1 = p[0], 12
                p2 = 0, p[1]
                # (line number, position), (line number, position)
                self.highlight_position.append({'line':(dx,dy), 'pos':(p1,p2)})

    def generate_outline(self, index, hex_seed, count):
        hex_num = hex_seed
        i = (index - 1) * 16
        for x in range(count):
            self.writer.add(index, hex(hex_num).upper() + ' ............', 20,
                update_after = (20, 7, self.display_buffer[x + i]))
            hex_num += 12

    # gets character likeness
    def get_likeness(self, word, visible=True):
        likeness = 0
        for enum, letter in enumerate(self.secret_word):
            if word[enum] == letter:
                likeness += 1

        if visible:
            if likeness == len(secret_word):
                UOS.sounds.play('good')
                # todo pass valid logon
            else:
                UOS.sounds.play('bad')
                self.writer.add(3, '> Entry denied.')
                self.writer.add(3, '> Likeness=' + likeness)
                self.attempts -= 1
                # todo if 0 attempts lock
        else:
            return likeness

    # make sure words are random, but at least similar to secret word
    def get_words(self,secret_word):
        word = ''
        likeliness = 0
        wordset = []  # todo access to word list based on length
        words = [secret_word]
        for x in range(15):
            found = False
            count = 0
            while not found:
                # get random word from wordset
                word = wordset[randint(0,len(wordset))]
                # test likeness of word to secret word
                likeliness = self.get_likeness(word,False)
                if word not in words and likeliness < randint(1,3) or count > 100:  # important to avoid infinite loop
                    words.append(word)
                    found = True
        return words

    # runs bracket functions
    def hack(self):
        roll = randint(0,4)
        if roll == 4:
            self.reset_tries()
        else:
            self.remove_dud()

    # highlight bracket sets
    def highlight_bracket_set(self,lines):
        openers = ['(','[','{','<']
        closers = [')',']','}','>']
        sets = []
        index = 0
        # iterates over each line to find sets
        for x in range(len(lines)):
            for j in range(len(lines[x])):
                letter = lines[x][j]
                if letter in openers >=0:
                    br_index = letter in openers
                    queue = lines[x:j]  # not sure if this is right
                    if closers[br_index] in queue > 0:
                        end_index = closers[br_index] in queue
                        snippet = queue[0:end_index + 1]
                        # supposed to check for letters
                        if any((c in string.ascii_uppercase) for c in snippet):
                            index +=1
                        else:
                            sets.append([index, index + end_index, snippet])

    # removes dud
    def remove_dud(self):
        UOS.sounds.play('dud')

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
        return UOS.text(text, (0,0,0), UOS.text.get_color())

    # sets attempts back to 4
    def reset_tries(self):
        self.attempts = 4

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
