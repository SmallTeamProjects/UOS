import pygame
from uos import UOS
from uos.states import load_states

if __name__ == '__main__':
    pygame.init()
    UOS.setup()
    #UOS.Timer.delay(500)
    load_states.setup()
