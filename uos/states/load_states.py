from .terminal import Terminal
from .explorer import Explorer
from .loading import Loading
from .editor import Editor
from .menu import MenuMenu
from .minigame import Minigame
from .idle import Idle
from ..uos import UOS

def setup():
    Idle()
    Terminal()
    Explorer()
    MenuMenu()
    Minigame.setup()
    Editor.setup()
    UOS.run(Loading())
