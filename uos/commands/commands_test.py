from .basecommand import BaseCommand
from ..uos import UOS


class TestCommands(BaseCommand):
    def command_minigame(self):
        self.link.action.flip('Minigame')
