from managers.texture_manager import TextureManager
# from managers.font_manager import FontManager 
from loguru import logger
import pygame

class Screen:

    def __init__(self, display):
        self.game_display = display
        self.texture = None
        self.tex_manager = TextureManager.get_manager("sprites")
        # self.font_manager = FontManager.get_manager("fonts")

        self.transition_dots = self.tex_manager.get_textures(f"transition_dots")

    def fadein(self):

        if self.texture is None:
            raise ValueError("Screen texture must be set by subclass")

        frame = len(self.transition_dots)
        clock = pygame.time.Clock()

        while frame > 0:
            self.game_display.blit(self.texture, (0, 0))
            for i in range (0,40):
                for j in  range (0,24):
                    self.game_display.blit(self.transition_dots[frame-1], (i * 16, j *17))

            pygame.display.update()
            clock.tick(len(self.transition_dots)*1.5)
            frame -= 1

    def fadeout(self):

        clock = pygame.time.Clock()

        for frame in range (0,len(self.transition_dots)):
            for i in range (0,40):
                for j in  range (0,24):
                    self.game_display.blit(self.transition_dots[frame], (i * 16, j *17))

            pygame.display.update()
            clock.tick(len(self.transition_dots)*1.5)