import os
import pygame
from .system import *
from .system.timer import TickTimerData

class UOS:
    State = UOS_State
    color = UOS_Color()
    interval = 30
    idle = False

    @classmethod
    def get_interval(cls):
        return cls.interval

    @classmethod
    def run(cls, state):
        UOS_StateMachine.main_loop(state)

    @classmethod
    def setup(cls):
        TickTimerData.setup(cls.get_interval)
        cls.bus = EventBus(cls)
        cls.data = UOS_Data()
        cls.drive = UOS_Drive(cls.bus)
        cls.path = cls.drive.path
        cls.sounds = UOS_Sounds()
        cls.user = UOS_User(cls.bus)
        cls.text = UOS_Text(cls.color)

        UOS_StateMachine.screen_center()
        machine = UOS_StateMachine('UOS', cls.bus, 512, 384)
        cls.color.instances = machine.instances
        pygame.key.set_repeat(80,80)
        cls.drive.setup()
        cls.user.load()
