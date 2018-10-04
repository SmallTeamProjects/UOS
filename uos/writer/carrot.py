import pygame
from ..uos import UOS

class Carrot:
    image = None

    @classmethod
    def create_image(cls):
        h = UOS.text.font.get_height()
        w = UOS.text.width(' ')
        cls.image = pygame.Surface((w, h))
        cls.image = cls.image.convert_alpha()
        cls.image.fill((*UOS.text.get_color())

    def __init__(self, carrot=None):
        if Carrot.image is None:
            Carrot.create_image()

        if carrot:
            self.carrot = carrot
            self.length = len(carrot)
            self.pos = self.length
        else:
            self.pos = 0

        self.black_letter = None
        self.topleft = 0
        self.show = True
        self.x = 0

    def render(self, surface):
        if self.show:
            x, y = self.topleft
            x += self.x
            surface.blit(Carrot.image, (x, y))
            if self.black_letter:
                surface.blit(self.black_letter, (x, y))

    def blink(self):
        self.show = not self.show

UOS.State.on_color_change.append(Carrot.create_image)
