import os
import pygame
from .timer import UOS_TickTimer
from .scanline import UOS_Scanline
from .state import UOS_StateMethods, UOS_State

class UOS_StateMachine:
    def __init__(self, title, bus, width, height, flags=0):
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.current = None
        self.instances = {}
        self.delta = 0
        self.bus = bus

        self.timer = UOS_TickTimer()
        self.idle_timer = self.timer(30000, self.call_idle)
        self.scanline = UOS_Scanline(self.timer, self.rect)

        self.bus.listener('next state', self.listener_next_state)

        # changable variables
        self.running = False
        self.fps = 30

        UOS_StateMethods.machine = self

    def call_idle(self, timer):
        self.bus.register_event('next state', 'Idle')

    def listener_next_state(self, state_name, *args, **kwargs):
        # clean up
        if self.current:
            self.current.drop()

        if isinstance(state_name, UOS_State):
            self.current = state_name
            previous_state = None
            regain_focus = True
        else:
            regain_focus = False
            previous_state = self.current
            self.current = self.instances[state_name]

        # start the next state
        self.current.state.screen_entrance(regain_focus,
            previous_state, *args, **kwargs)

    def loop(self, state):
        # set the initial state
        self.listener_next_state(state)
        self.running = True
        while self.running:
            self.bus.process()
            for event in pygame.event.get():
                self.idle_timer.reset()
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current.state.screen_event(event)

            self.timer.update()
            self.current.state.screen_render(self.surface)
            self.scanline.render(self.surface)
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)

    def quit(self):
        self.running = False

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
