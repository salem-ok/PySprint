import pygame

from screens.screen import Screen

class CreditsScreen(Screen):

    def __init__(self, display) :
        super().__init__(display=display)

        self.texture = self.tex_manager.get_texture("credits_screen")

