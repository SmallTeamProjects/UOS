from .uos import UOS
from .commands import Command

def uos_init():
    UOS.command = Command()
