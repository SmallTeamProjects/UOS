import pygame
from .variables import UOS_Variables

class UOS_Timer:
    ticks = 0
    delta = 0
    delay_tick = 0

    @classmethod
    def tick(cls):
        ticks = pygame.time.get_ticks()
        cls.delta = ticks - cls.ticks
        cls.ticks = ticks

    @classmethod
    def delay(cls, tick):
        cls.delay_tick = tick

    def __init__(self):
        self.timers = {}
        self.id = 0

    def __call__(self, interval, callback, callback_fast=None, pydata=None):
        timer = TickTimer(self.id, interval, callback, callback_fast, pydata)
        self.timers[self.id] = timer
        self.id += 1
        return timer

    def update(self, bypass=False):
        if UOS_Timer.delay_tick > 0 and not bypass:
            UOS_Timer.delay_tick -= UOS_Timer.delta
            for timer in self.timers.values():
                timer.idle()
        else:
            for timer in self.timers.values():
                timer.update()

    def reset(self):
        for timer in self.timers.values():
            timer.reset()

class TickTimer:
    def __init__(self, id, interval, callback, callback_fast=None, pydata=None):
        self.id = id
        self.next_tick = UOS_Timer.ticks + interval
        self.interval = interval
        self.callback = callback
        self.callback_fast = callback_fast
        self.pydata = pydata
        self.stop = False

    def reset(self):
        self.next_tick = UOS_Timer.ticks
        self.update_next_tick()

    def restart(self):
        self.stop = False
        self.next_tick = UOS_Timer.ticks
        self.update_next_tick()

    def idle(self):
        self.next_tick += UOS_Timer.delta

    def update(self):
        if not self.stop:
            if UOS_Timer.ticks > self.next_tick:
                # avoid infinite loop
                if self.interval != 0:
                    while UOS_Timer.ticks > self.next_tick:
                        self.update_next_tick()

                        if self.callback_fast:
                            self.callback_fast(self)

                self.callback(self)

    def update_next_tick(self):
        if self.interval < 0:
            self.next_tick += UOS_Variables.interval
        else:
            self.next_tick += self.interval

    def __str__(self):
        return 'Timer' + str(self.__dict__)
