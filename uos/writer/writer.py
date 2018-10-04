from random import randint
from .block import InputBlock, OutputBlock
from .carrot import Carrot
from ..uos import UOS

class Writer:
    def __init__(self, timer):
        self.timer = timer
        self.blocks = []

    # add(  # args, kwargs
    #   text,
    #   interval=-1,
    #   sound_keys=['typing multiple'],
    #   protect=False, # only for InputBlock
    #   newline=True,
    #   invisible=False)
    def add(self, index, *args, **kwarg):
        self.blocks[index].add(*args, **kwarg)

    def add_empty(self, index, count=1):
        self.blocks[index].add_empty(count)

    def add_input(self, rect, system=False, padding=0, reverse=False, carrot='> '):
        self.blocks.append(InputBlock(self.timer, rect, system, padding, reverse, carrot))

    def add_output(self, rect, padding=0, reverse=False):
        self.blocks.append(OutputBlock(self.timer, rect, padding, reverse))

    def clear(self, index):
        self.blocks[index].clear()

    def color_change(self):
        for block in self.blocks:
            block.color_change()

    def event_keydown(self, event):
        for block in self.blocks:
            if isinstance(block, InputBlock):
                block.text_line.event_keydown(event)
            if not block.is_finish():
                break

    def flush(self):
        for block in self.blocks:
            block.callback_timer.stop = True
            block.writer.flush()

    # returns WriterText
    def get_line(self, index, line_number):
        return self.blocks[index].writer.bufferbox.items[line_number]

    def is_finish(self):
        return False not in [b.is_finish() for b in self.blocks]

    def render(self, surface):
        self.pause_idle()
        for block in self.blocks:
            if block.callback_timer.stop:
                block.callback_timer.restart()

            block.render(surface)
            if not block.is_finish():
                break

    def pause_idle(self):
        if not self.is_finish():
            if not UOS.Screen.idle_timer.stop:
                UOS.Screen.idle_timer.stop = True
        elif UOS.Screen.idle_timer.stop and not UOS.Variables.idle:
            UOS.Screen.idle_timer.restart()
