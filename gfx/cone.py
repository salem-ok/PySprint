import random

class Cone:

    def __init__(self, display, image, shade_image):
        self.display = display
        self.image = image
        self.shade_image = shade_image
        self.pos = None
        self.enabled = True

    def update(self, pos):
        self.pos = pos

    def blit(self):
        if self.enabled:
            self.display.blit(self.image, self.pos)
            self.display.blit(self.shade_image, self.pos)

    def disable(self):
        self.enabled = False



