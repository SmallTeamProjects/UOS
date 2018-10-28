import pygame
from uos import UOS, uos_init
from uos.states import load_states

if __name__ == '__main__':
    pygame.init()
    UOS.setup()
    uos_init()
    #UOS.Timer.delay(500)
    load_states.setup()
