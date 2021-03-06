from .timer import UOS_TickTimer

class UOS_StateMethods:
    machine = None

    def __init__(self, parent):
        self.parent = parent
        self.timer = UOS_TickTimer()
        self.previous_state = None

    def flip(self, classname, *args, **kwargs):
        self.machine.bus.register_event('next state', classname, *args, **kwargs)

    def flip_back(self, *args, **kwargs):
        self.machine.bus.register_event('next state', self.previous_state, *args, **kwargs)

    def screen_entrance(self, regain_focus, previous_state, *args, **kwargs):
        if previous_state:
            self.previous_state = previous_state

        self.timer.tick()
        self.timer.reset()
        self.parent.__dict__.update(kwargs)
        self.parent.entrance(regain_focus, *args)

    def screen_render(self, surface):
        self.parent.render(surface)
        self.timer.update()
        self.parent.update(self.timer.ticks, self.machine.delta)

    def screen_event(self, event):
        self.parent.event(event)

class UOS_State:
    def __init__(self, state_name=None):
        self.state = UOS_StateMethods(self)
        if state_name is None:
            state_name = self.__class__.__name__

        self.state.machine.instances[state_name] = self

    def render(self, surface):
        pass

    def drop(self):
        pass

    def entrance(self, regain_focus):
        pass

    def event(self, event):
        pass

    def color_change(self):
        pass

    def update(self, ticks, delta):
        pass
