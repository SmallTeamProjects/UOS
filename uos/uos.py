import os
import pygame
from .system import *


class UOS:
    UOS_User.variable_setup()

    Drive = UOS_Drive
    State = UOS_State
    User = UOS_User
    Data = UOS_Data
    Variables = UOS_Variables

    @classmethod
    def get_interval(cls):
        return cls.Variables.interval

    @classmethod
    def run(cls, state):
        UOS_StateMachine.main_loop(state)

    @classmethod
    def setup(cls):
        UOS_StateMachine.screen_center()
        UOS_StateMachine.create('UOS', 512, 384)
        pygame.key.set_repeat(80,80)
        cls.sounds = UOS_Sounds()
        cls.Drive.setup()
        cls.User.load()
        cls.text = UOS_Text()
