import pygame

class UOS_Scanline:
    def __init__(self, timer, rect):
        surfaces = [pygame.Surface((1,1)), pygame.Surface((1,1))]
        surfaces[0].fill((190,190,190))
        surfaces[1].fill((210,210,210))
        self.scanline = (pygame.transform.scale(surfaces[0], (rect.w, 2)),
                         pygame.transform.scale(surfaces[1], (rect.w, 2)))

        self.scan_position = [[],[]]
        self.rect = rect
        for i in range(0, rect.h, 12):
            self.scan_position[0].append([0, i])
            self.scan_position[1].append([0, i + 6])

        self.scan_timer = timer(150, self.scan_call)

    def render(self, surface):
        for i in range(len(self.scan_position)):
            for pos in self.scan_position[i]:
                surface.blit(self.scanline[i], pos,
                    special_flags=pygame.BLEND_MULT)

    def scan_call(self, timer):
        for i in range(len(self.scan_position)):
            for pos in self.scan_position[i]:
                pos[1] -= 1
                if pos[1] < 0:
                    pos[1] = self.rect.h - 1
