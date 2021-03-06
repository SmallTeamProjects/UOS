import os
import pygame


class UOS_Text:
    def __init__(self, color):
        self.link = color
        path = os.path.join('resources', 'fixedsys.ttf')
        self.font = pygame.font.Font(path, 16)
        #self.alpha = 0.7

    def __call__(self, text, foreground=None, background=None):
        if foreground and background:
            image = self.font.render(text, 1, foreground, background)
        elif foreground:
            image = self.font.render(text, 1, foreground)
        elif background:
            image = self.font.render(text, 1, self.link.color, background)
        else:
            image = self.font.render(text, 1, self.link.color)

        # requires NumPy
        #image = image.convert_alpha()
        #array = pygame.surfarray.pixels_alpha(image)
        #w, h = array.shape
        #for y in range(w):
        #    for x in range(h):
        #        try:
        #            array[y][x] = int(array[y][x] * self.alpha)
        #        except:
        #            print(array.shape, text)

        return image

    def get_linesize(self, padding=0):
        return self.font.get_linesize() + padding

    def size(self, text):
        return self.font.size(text)

    def width(self, text):
        return self.font.size(text)[0]

    def height(self, text):
        return self.font.size(text)[1]
