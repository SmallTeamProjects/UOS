import pygame
import random
import os

pygame.init()
class UOS_Sounds:
    PATH = os.path.join('resources', 'sound')

    def __init__(self):
        self.sounds = {}
        self.channels = {}
        self.typing_sound = [None, None, None]

        self.sound_loader('enter', 3, 'UI_Hacking_CharEnter_0{0}.wav')
        self.sound_loader('typing', 5, 'UI_Hacking_CharSingle_0{0}.wav')
        self.sound_loader('hard drive', 15, 'UI_Terminal_HardDrive_A_{0:02}.wav')
        self.sound_loader('typing multiple', 4, 'UI_Hacking_CharMultiple_0{0}.wav')
        self.sounds['scroll'] = pygame.mixer.Sound(os.path.join(UOS_Sounds.PATH,
            'UI_Terminal_CharScroll_LP.wav'))
        self.sounds['password'] = {}
        self.sounds['password']['bad'] = pygame.mixer.Sound(os.path.join(UOS_Sounds.PATH,
            'UI_Hacking_PassBad.wav'))
        self.sounds['password']['good'] = pygame.mixer.Sound(os.path.join(UOS_Sounds.PATH,
            'UI_Hacking_PassGood.wav'))
        self.sounds['password']['dud'] = pygame.mixer.Sound(os.path.join(UOS_Sounds.PATH,
            'UI_Hacking_PasswordHelpDud.wav'))
        self.sounds['password']['attempt'] = pygame.mixer.Sound(os.path.join(UOS_Sounds.PATH,
         'UI_Hacking_PasswordHelpAttempts.wav'))

        self.channels['enter'] = pygame.mixer.Channel(0)
        self.channels['hard drive'] = pygame.mixer.Channel(1)
        self.channels['typing multiple'] = pygame.mixer.Channel(2)
        self.sound_channel_keys = self.channels.keys()
        self.channels['misc'] = pygame.mixer.Channel(6)
        for i in range(3, 6):
            key = 'typing{0}'.format(i)
            self.channels[key] = pygame.mixer.Channel(i)

    def sound_loader(self, key, count, line):
        self.sounds[key] = []
        for i in range(1,count + 1):
            self.sounds[key].append(
                pygame.mixer.Sound(os.path.join(UOS_Sounds.PATH, line.format(i))))

    def play(self, sound_key, sound_key2=None):
        if sound_key in self.sound_channel_keys:
            if not self.channels[sound_key].get_busy():
                self.channels[sound_key].play(random.choice(self.sounds[sound_key]))
        elif sound_key == 'typing':
            typing_choice = random.choice(list(set(
                self.sounds['typing']) - set(self.typing_sound)))
            self.typing_sound = self.typing_sound[:1] + [typing_choice]
            for i in range(3,6):
                key = 'typing{0}'.format(i)
                if not self.channels[key].get_busy():
                    self.channels[key].play(typing_choice)
                    break
        else:
            if sound_key2:
                self.channels['misc'].play(self.sounds[sound_key][sound_key2])
            else:
                self.channels['misc'].play(self.sounds[sound_key])

    def stop(self, sound_key):
        if sound_key == 'all':
            for key in self.channels.keys():
                if self.channels[key].get_busy():
                    self.channels[key].stop()
        elif sound_key in self.channels.keys():
            if self.channels[sound_key].get_busy():
                self.channels[sound_key].stop()
        else:
            if self.channels['misc'].get_busy():
                self.channels['misc'].stop()
