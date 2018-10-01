import pygame
from uos import UOS
from uos.states import *

if __name__ == '__main__':
    pygame.init()
    UOS.setup()
    UOS.Timer.delay(500)
    Idle()
    Terminal()
    Explorer()
    Menu.setup()
    Minigame.setup()
    Editor.setup()
    UOS.State.next_state = Loading()._state.name
    UOS.run()
