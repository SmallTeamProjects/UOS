import os
import pygame
from .state import UOS_State
from .timer import UOS_Timer
from .scanline import UOS_Scanline

class UOS_Screen:
    @classmethod
    def create(cls, caption, size):
        pygame.display.set_caption(caption)
        cls.surface = pygame.display.set_mode(size)
        cls.rect = pygame.Rect(0, 0, *size)
        cls.clock = pygame.time.Clock()
        cls.timer = UOS_Timer()
        cls.idle_timer = cls.timer(20000, cls.call_idle)
        cls.running = False
        cls.scanline = UOS_Scanline(cls.timer, cls.rect)
        pygame.key.set_repeat(80,80)

    @staticmethod
    def call_idle(timer):
        UOS_State.next_state = 'Idle'

    @staticmethod
    def center():
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    @classmethod
    def loop(cls, fps):
        cls.running = True
        while cls.running:
            if UOS_State.next_state:
                current = UOS_State.current
                UOS_State.current = UOS_State.states[UOS_State.next_state]
                UOS_State.current.screen_entrance(current)
                UOS_State.next_state = None
            elif UOS_State.flip_state:
                UOS_State.current = UOS_State.flip_state
                UOS_State.current.screen_flip()
                UOS_State.flip_state = None

            for event in pygame.event.get():
                cls.idle_timer.reset()
                if event.type == pygame.QUIT:
                    cls.running = False

                UOS_State.current.event(event)

            UOS_Timer.tick()
            cls.timer.update(True)
            UOS_State.current.screen_render(cls.surface)
            cls.scanline.render(cls.surface)
            pygame.display.flip()
            cls.clock.tick(fps)

        pygame.quit()

    @classmethod
    def scan_call(self, timer):
        for i in range(len(self.scan_position)):
            if self.scan_position[i] < -11:
                self.scan_position[i] += UOS.Screen.rect.h + 11
            else:
                self.scan_position[i] -= 1

    @classmethod
    def scan_call_fast(self, timer):
        for i in range(len(self.scan_position)):
            self.scan_position[i] -= 1
