import os
import pygame
from .system import *


class UOS:
    Screen = UOS_Screen
    Drive = UOS_Drive
    State = UOS_State
    Timer = UOS_Timer
    User = UOS_User
    Data = UOS_Data
    Variables = UOS_Variables

    sounds = UOS_Sounds()

    @classmethod
    def get_interval(cls):
        return cls.Variables.interval

    @classmethod
    def run(cls):
        cls.Screen.loop(30)

    @classmethod
    def setup(cls):
        cls.Screen.center()
        cls.Screen.create('UOS', (512, 384))
        cls.Drive.setup()
        cls.User.load()
        cls.text = UOS_Text()
