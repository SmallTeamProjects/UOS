import os
import pygame
from types import SimpleNamespace
from .system import *
from .system.statemachine.timer import TickTimerData

class UOS:
    State = UOS_State
    color = UOS_Color()
    interval = 30
    volume = 1.0
    bypass = 0
    idle = False

    @classmethod
    def get_interval(cls):
        return cls.interval

    @classmethod
    def load_settings(cls):
        # default settings
        cls.settings = SimpleNamespace(interval=30,
                                       header='Welcome to ROBCO Industries (TM) Termlink',
                                       color='green',
                                       volume=1.0)

        # load save settings
        if os.path.exists(cls.path.settings):
            vars(cls.settings).update(**cls.drive.deserialize_data(cls.path.settings))

    @classmethod
    def run(cls, state):
        UOS_StateMachine.main_loop(state)

    @classmethod
    def save_settings(cls):
        cls.drive.serialize_data(vars(cls.settings), cls.path.settings)

    @classmethod
    def setup(cls):
        cls.bus = EventBus(cls)
        cls.drive = UOS_Drive(cls.bus)
        cls.path = cls.drive.path
        cls.load_settings()
        cls.interval = cls.settings.interval
        cls.color.setup(cls.settings.color)
        cls.volume = cls.settings.volume
        TickTimerData.setup(cls.get_interval)
        cls.data = UOS_Data()
        cls.sounds = UOS_Sounds()

        cls.user = UOS_User(cls.bus)
        cls.text = UOS_Text(cls.color)

        UOS_StateMachine.screen_center()
        machine = UOS_StateMachine('UOS', cls.bus, 512, 384)
        cls.color.instances = machine.instances
        pygame.key.set_repeat(80,80)
        cls.drive.setup()
        cls.user.load()
