import pygame
from .variables import UOS_Variables

class UOS_Scanline:
    screen_width = 0

    @classmethod
    def create(cls):
        size = 5
        cls.scanline = pygame.Surface((1, size))
        cls.scanline = cls.scanline.convert_alpha()
        color = pygame.Color(*UOS_Variables.color, 40)
        for i in range(size):
            color.a += 1
            cls.scanline.set_at((0, i), color)

        cls.scanline = pygame.transform.scale(cls.scanline, (cls.screen_width, size))

    def __init__(self, timer, height):
        self.height = height
        self.scan_position = []
        y = 20
        h = height / 5
        for i in range(5):
            self.scan_position.append(y)
            y += h

        self.scan_timer = timer(20, self.scan_call, self.scan_call_fast)

    def render(self, surface):
        for y in self.scan_position:
            surface.blit(UOS_Scanline.scanline, (0, y))

    def scan_call(self, timer):
        for i in range(len(self.scan_position)):
            if self.scan_position[i] < -11:
                self.scan_position[i] += self.height + 11
            else:
                self.scan_position[i] -= 1

    def scan_call_fast(self, timer):
        for i in range(len(self.scan_position)):
            self.scan_position[i] -= 1
