
class BufferBox:
    def __init__(self, rect, linesize, reverse):
        self.linesize = linesize
        self.reverse = reverse
        self.items = []
        self.position = rect.topleft
        self.set_rect(rect)

    def add(self, item):
        if isinstance(item, (tuple, list)):
            self.items.extend(item)
        else:
            self.items.append(item)

        length, offset = self.get_buffer_length()
        if length > self.max_lines:
            self.items = self.items[-(self.max_lines + offset):]

        self.update_position()

    def clear(self):
        self.position = self.rect.topleft
        self.items = []

    def get_buffer_length(self):
        length = sum([1 for item in self.items if item is None or item.newline])
        return length, len(self.items) - length

    def pop(self):
        items = self.items
        self.clear()
        return items

    def render(self, surface):
        for item in self.items:
            if item:
                item.render(surface, item.rect)

    def set_rect(self, rect):
        self.rect = rect
        self.max_lines = int(rect.h / self.linesize)

    def update_position(self):
        x = self.rect.left
        if self.reverse:
            items = self.items[::-1]
            y = self.rect.bottom
        else:
            items = self.items
            y = self.rect.top

        for item in items:
            if item:
                rect = item.get_rect()
                rect.topleft = x, y
                if item.image:
                    x += item.image.get_rect().width

                if item.newline:
                    x = self.rect.left
                    if not self.reverse:
                        rect.top = y
                        y += self.linesize
                        item.rect = rect
                    else:
                        y -= self.linesize
                        rect.bottom = y
                        item.rect = rect
                else:
                    item.rect = rect
            else:
                if self.reverse:
                    y -= self.linesize
                else:
                    y += self.linesize

        if self.reverse:
            self.position = x, y - self.linesize
        else:
            self.position = x, y
