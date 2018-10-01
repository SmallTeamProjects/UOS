import os
import pygame
from .variables import UOS_Variables

class UOS_Text:
    def __init__(self):
        path = os.path.join('resources', 'fixedsys.ttf')
        self.font = pygame.font.Font(path, 16)

    def __call__(self, text, foreground=None, background=None):
        if foreground and background:
            return self.font.render(text, 1, foreground, background)
        elif foreground:
            return self.font.render(text, 1, foreground)
        elif background:
            return self.font.render(text, 1, self.color, background)

        return self.font.render(text, 1, UOS_Variables.color)

    def get_color(self):
        return UOS_Variables.color

    def get_colors(self):
        return list(UOS_Variables.COLORS.keys())

    def get_linesize(self, padding=0):
        return self.font.get_linesize() + padding

    def size(self, text):
        return self.font.size(text)

    def width(self, text):
        return self.font.size(text)[0]

    def height(self, text):
        return self.font.size(text)[1]
