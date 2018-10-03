import pygame

class UOS_Scanline:
    def __init__(self, timer, rect):
        self.scan_position = []
        self.rect = rect
        self.count = 5
        self.size = 3
        y = 0
        h = rect.h / self.count
        for i in range(self.count):
            self.scan_position.append(pygame.Rect(0, y, rect.right, self.size))
            y += h

        self.scan_timer = timer(100, self.scan_call, self.scan_call_fast)

    def render(self, surface):
        scan = surface.copy()
        for rect in self.scan_position:
            if self.rect.contains(rect):
                item = scan.subsurface(rect)
                surface.blit(item, rect, special_flags=pygame.BLEND_RGBA_ADD)

    def scan_call(self, timer):
        for i in range(len(self.scan_position)):
            if self.scan_position[i].bottom < 0:
                self.scan_position[i].top = self.rect.h
            else:
                self.scan_position[i].top -= 1

    def scan_call_fast(self, timer):
        for i in range(len(self.scan_position)):
            self.scan_position[i].top -= 1
