class Spill:

    def __init__(self, display, image):
        self.display = display
        self.image = image
        self.pos = None
        self.enabled = True

    def update(self, pos):
        self.pos = pos

    def blit(self):
        if self.enabled:
            self.display.blit(self.image, self.pos)

    def disable(self):
        self.enabled = False



