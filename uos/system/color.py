class UOS_Color:
    def __init__(self):
        self.COLORS = {'green':(11, 188, 12),
                       'amber':(255, 182, 66),
                       'blue':(46, 207, 255)}

        self.on_color_change = []

    def setup(self, color_key):
        self.key = color_key
        self.color = self.COLORS[color_key]

    def change_color(self, color):
        self.key = color
        self.color = self.COLORS[color]
        for item in self.on_color_change:
            item()

        for item in self.instances.values():
            item.color_change()
