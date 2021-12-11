class Cone:

    def __init__(self, display, image, shade_image):
        self.display = display
        self.image = image
        self.shade_image = shade_image
        self.pos = None
        self.enabled = True
        self.is_on_bridge= False

    def set_on_bridge_or_ramp(self, on_object):
        self.is_on_bridge= on_object

    def update(self, pos):
        self.pos = pos

    def blit(self):
        if self.enabled:
            self.display.blit(self.image, self.pos)
            self.display.blit(self.shade_image, self.pos)

    def disable(self):
        self.enabled = False



