from loguru import logger
from screens.colors import *
from typing import Dict
import pygame

from screens.screen import Screen

class LoadingScreen(Screen):

    def __init__(self, display, fps: int, display_width: int, display_height: int, scroll_loop: bool = False):
        super().__init__(display=display)

        self.texture = self.tex_manager.get_texture("loading_screen_foreground")

        # TODO: enable when PR accepted
        # self.scrolling_font = self.font_manager.get_bitmap_font("scrolling")
        self._load_scrolling_font()

        self.display_width = display_width
        self.display_height = display_height
        self.scroll_loop = scroll_loop

        if fps == 30:
            self.scroll_increment = -6
        elif fps == 60:
            self.scroll_increment = -3
        else:
            raise ValueError(f"Unssupported FPS: {fps}")

        self.scroll_message = "SUPER SPRINT REMADE WITH PYGAME BY SALEM_OK. THANKS TO SHAZZ: CODE REVIEW AND REFACTORING. JOHNATHAN THOMAS: SPRITES RIP. COGWEASEL: SPLASH SCREEN. ORIGINAL CREATED FOR THE MIGHTY ATARI ST BY STATE OF THE ART. PROGRAMMING: NALIN SHARMA  MARTIN GREEN  JON STEELE. GRAPHICS: CHRIS GIBBS. SOUND: MARK TISDALE. A SOFTWARE STUDIOS PRODUCTION..."        
        self.dx = 0
        self.text = None
        self.background = pygame.Surface((self.display_width, self.display_height))

        self.right_end = 490
        self.left_end = 148
        self.scroll_y = 370
        

    def display(self):

        self.background.fill(black_color)
        self.text = pygame.Surface((
            (self.scrolling_font['A'].get_width() + 1) * len(self.scroll_message) + self.right_end - self.left_end, 
            self.scrolling_font['A'].get_height()
        ))
        
        x_offset = self.right_end - self.left_end
        for char in self.scroll_message:
            self.text.blit(self.scrolling_font[char], (x_offset, 0))
            x_offset += self.scrolling_font[char].get_width() + 1

    def update(self):

        if self.dx >= self.text.get_width() and not self.scroll_loop:
            return True

        self.game_display.blit(self.background, (0, 0))
        self.game_display.blit(self.text, (self.left_end, self.scroll_y))
        self.game_display.blit(self.texture, (0, 0))

        pygame.display.update()
        
        self.text.scroll(self.scroll_increment)
        self.dx -= self.scroll_increment

        return False

    def _load_scrolling_font(self):
        self.scrolling_font = {
            'A':pygame.image.load('Assets/ScrollingFontA.png').convert_alpha(),
            'B':pygame.image.load('Assets/ScrollingFontB.png').convert_alpha(),
            'C':pygame.image.load('Assets/ScrollingFontC.png').convert_alpha(),
            'D':pygame.image.load('Assets/ScrollingFontD.png').convert_alpha(),
            'E':pygame.image.load('Assets/ScrollingFontE.png').convert_alpha(),
            'F':pygame.image.load('Assets/ScrollingFontF.png').convert_alpha(),
            'G':pygame.image.load('Assets/ScrollingFontG.png').convert_alpha(),
            'H':pygame.image.load('Assets/ScrollingFontH.png').convert_alpha(),
            'I':pygame.image.load('Assets/ScrollingFontI.png').convert_alpha(),
            'J':pygame.image.load('Assets/ScrollingFontJ.png').convert_alpha(),
            'K':pygame.image.load('Assets/ScrollingFontK.png').convert_alpha(),
            'L':pygame.image.load('Assets/ScrollingFontL.png').convert_alpha(),
            'M':pygame.image.load('Assets/ScrollingFontM.png').convert_alpha(),
            'N':pygame.image.load('Assets/ScrollingFontN.png').convert_alpha(),
            'O':pygame.image.load('Assets/ScrollingFontO.png').convert_alpha(),
            'P':pygame.image.load('Assets/ScrollingFontP.png').convert_alpha(),
            'Q':pygame.image.load('Assets/ScrollingFontQ.png').convert_alpha(),
            'R':pygame.image.load('Assets/ScrollingFontR.png').convert_alpha(),
            'S':pygame.image.load('Assets/ScrollingFontS.png').convert_alpha(),
            'T':pygame.image.load('Assets/ScrollingFontT.png').convert_alpha(),
            'U':pygame.image.load('Assets/ScrollingFontU.png').convert_alpha(),
            'V':pygame.image.load('Assets/ScrollingFontV.png').convert_alpha(),
            'W':pygame.image.load('Assets/ScrollingFontW.png').convert_alpha(),
            'X':pygame.image.load('Assets/ScrollingFontX.png').convert_alpha(),
            'Y':pygame.image.load('Assets/ScrollingFontY.png').convert_alpha(),
            'Z':pygame.image.load('Assets/ScrollingFontZ.png').convert_alpha(),
            '.':pygame.image.load('Assets/ScrollingFontDOT.png').convert_alpha(),
            ' ':pygame.image.load('Assets/ScrollingFontSPACE.png').convert_alpha(),
            '_':pygame.image.load('Assets/ScrollingFont_.png').convert_alpha(),
            ':':pygame.image.load('Assets/ScrollingFontSemiColon.png').convert_alpha()
        }        