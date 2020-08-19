import os
import pygame


class UOS_Scanline:
    def __init__(self, timer, rect):
        self.rect = rect
        try:
            static_lines = os.path.join("resources", "images", "screen_multiply.png")
            self.static_lines = pygame.image.load(static_lines)
            self.static_lines = self.static_lines.convert_alpha()
        except:
            self.static_lines = self.create_static_lines()

        # TODO moving scan line
        self.scan_position = []

        #self.scan_timer = timer(150, self.scan_call)

    def create_static_lines(self):
        surfaces = (self.create_surface_line((186,186,186), 3),
                    self.create_surface_line((210,210,210), 3))

        surface = pygame.Surface(self.rect.size)
        surface.fill((255,255,255))

        for i in range(0, self.rect.h, 12):
            surface.blit(surfaces[0], (0, i))
            surface.blit(surfaces[1], (0, i + 6))

        return surface

    def create_surface_line(self, color, size):
        surface = pygame.Surface((1,1))
        surface.fill(color)
        return pygame.transform.scale(surface, (self.rect.w, size))

    def render(self, surface):
        surface.blit(self.static_lines, (0,0), special_flags=pygame.BLEND_MULT)

    def scan_call(self, timer):
        # TODO
        pass
