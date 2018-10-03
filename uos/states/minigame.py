import pygame
import math
import string
from random import randint,random, choice
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
        # configuration variables
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
        self.display = ''
        self.select = 0

    def call_back(self):
        UOS.State.flip_state = self._state.track

    def call_selection(self):
        pass


    def attempts_remaining(self, count):
        debug_text = 'Attempts Remaining:'
        for x in range(count):
            debug_text += ' \x7f'
        return debug_text

    def generate_outline(self, index, hex_seed, count):
        hex_num = hex_seed
        for x in range(count):
            self.writer.add(index, hex(hex_num).upper() + ' ...........')
            hex_num += 12

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
    def generate_display(self,places,difficulty,characters):
        places = places[:]
        display = ''
        x = 0
        while x < len(characters):
            if len(places) > 0 and x == places[0][0]:
                display += places[0][1]
                x += difficulty
            else:
                display += choice(string.punctuation)
                x += 1
        return display

    # takes the entire code string and breaks it into lines
    def split_into_lines(self,display,lines,line_length):
        screen = []
        for x in range(len(lines)):
            screen.append(display[0:line_length])
            display = display[line_length]
        return screen

    # highlight words UNFINISHED
    def highlight_word(self,places,difficulty):
        for x in range(len(places)):
            position = int(places[x][0])
            j = position
            while j < position + difficulty:
                # todo make index of words
                j += 1

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

    # handle selection highlighting
    def change_selection(self):
        select = self.select
        # todo
        # if a letter in a word is selected, highlights and selects the whole word
        # print current selection to the input line without committing it to writer queue
        # if at the edge of a column move to next column

    # runs bracket functions
    def hack(self):
        roll = randint(0,4)
        if roll == 4:
            self.reset_tries()
        else:
            self.remove_dud()

    # sets attempts back to 4
    def reset_tries(self):
        self.attempts = 4

    # removes dud
    def remove_dud(self):
        UOS.sounds.play('dud')

    # gets character likeness
    def get_likeness(self, word, secret_word, visible=True):
        likeness = 0
        for x in range(len(secret_word)):
            if word[x] == secret_word[x]:
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
                likeliness = self.get_likeness(word,secret_word,False)
                if word not in words and likeliness < randint(1,3) or count > 100:  # important to avoid infinite loop
                    words.append(word)
                    found = True
        return words


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

    def entrance(self, args):
        self.writer.flush()
        self.select = 0


    def event(self, event):
        if self.writer.is_finish():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    UOS.sounds.play('scroll')
                    self.select += 12
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select += 12
                        self.select %= len(self.selection)

                elif event.key == pygame.K_UP:
                    UOS.sounds.play('scroll')
                    self.select -= 12
                    self.select %= len(self.selection)
                    while self.selection[self.select] is None:
                        self.select -= 12
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
                    # todo get selected word

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
