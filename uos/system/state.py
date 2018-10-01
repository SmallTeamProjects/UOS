from types import SimpleNamespace
from .timer import UOS_Timer
from .variables import UOS_Variables

class UOS_State:
    states = {}
    args = None
    current = None
    next_state = None
    flip_state = None
    on_color_change = []

    @classmethod
    def set_color(cls, color):
        UOS_Variables.color_key = color
        UOS_Variables.color = UOS_Variables.COLORS[color]
        for item in cls.on_color_change:
            item()
            
        for item in cls.states.values():
            item.color_change()

    def __init__(self, name=None, track=False):
        if name is None:
            name = self.__class__.__name__

        self._state = SimpleNamespace(name=name,
                                      state=self,
                                      track=None,
                                      trackable=track,
                                      timer=UOS_Timer())
        UOS_State.states[name] = self

    def screen_entrance(self, current):
        if self._state.trackable:
            self._state.track = current

        self.screen_flip()

    def screen_flip(self):
        self._state.timer.reset()
        args = UOS_State.args
        UOS_State.args = None
        if isinstance(args, (tuple, list)):
            self.entrance(*args)
        elif isinstance(args, dict):
            self.entrance(**args)
        else:
            self.entrance(args)

    def screen_render(self, surface):
        self._state.timer.update()
        self.render(surface)

    def color_change(self):
        pass

    def entrance(self, args):
        pass

    def event(self, event):
        pass

    def render(self, surface):
        pass

    def get_last_state(self):
        return self._state.track

    def last_state(self):
        UOS_State.flip_state = self._state.track

    def timer(self, interval, callback, callback_fast=None, pydata=None):
        return self._state.timer(interval, callback, callback_fast, pydata)
