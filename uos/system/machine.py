import os
import pygame
from .timer import UOS_TickTimer
from .scanline import UOS_Scanline
from .state import UOS_StateMethods, UOS_State

class UOS_StateMachine:
    @classmethod
    def create(cls, title, width, height, flags=0):
        self = cls()
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.current_state = None
        self.instances = {}
        self.delta = 0

        self.timer = UOS_TickTimer()
        self.idle_timer = self.timer(30000, self.call_idle)
        self.scanline = UOS_Scanline(self.timer, self.rect)

        # changable variables
        self.next_state = None
        self.running = False
        self.fps = 30

        UOS_StateMethods.machine = self

    def call_idle(self, timer):
        self.next_state = 'Idle', (), {}

    def loop(self, state):
        # set the initial state
        self.current_state = state
        self.running = True
        while self.running:
            if self.next_state:
                # clean up
                self.current_state.drop()
                if isinstance(self.next_state[0], UOS_State):
                    self.current_state, args, kwargs = self.next_state
                    previous_state = None
                    regain_focus = True
                else:
                    state_name, args, kwargs = self.next_state
                    previous_state = self.current_state
                    self.current_state = self.instances[state_name]
                    regain_focus = False

                # start the next state
                self.current_state.state.screen_entrance(regain_focus,
                    previous_state, *args, **kwargs)
                self.next_state = None

            for event in pygame.event.get():
                self.idle_timer.reset()
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_state.state.screen_event(event)

            self.timer.update()
            self.current_state.state.screen_render(self.surface)
            self.scanline.render(self.surface)
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)

    @staticmethod
    def main_loop(state):
        UOS_StateMethods.machine.loop(state)
        pygame.quit()

    @staticmethod
    def screen_center():
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    @staticmethod
    def screen_position(x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '{0}, {1}'.format(x, y)
