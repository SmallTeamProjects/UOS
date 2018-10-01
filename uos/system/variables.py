
# UOS_Variables are for variables that has to be share in system and/or
# other parts of the program. No imports from UOS should exists here.

class UOS_Variables:
    COLORS = {'green':(11, 188, 12), 'amber':(255, 182, 66), 'blue':(46, 207, 255)}

    color = COLORS['green']
    color_key = 'green'
    interval = 40
    group = None
    idle = False
