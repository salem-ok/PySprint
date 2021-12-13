from loguru import logger
from screens.colors import *
from typing import Dict
import pygame

from screens.screen import Screen

class HighscoresScreen(Screen):

    def __init__(self, display, high_scores: Dict):
        super().__init__(display=display)

        self.high_scores = high_scores
        self.texture = self.tex_manager.get_texture("high_score_screen")

    def display(self):

        # small_font = self.font_manager.get_truetype_font("small_font")
        small_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf', 15)
        
        top3 = (250, 100)
        top12 = (60, 225)
        top21 = (245, 225)
        top30 = (425, 225)

        for i in range (0,3):
            score = self.high_scores["high_scores"][i]["score"]
            name = self.high_scores["high_scores"][i]["name"]

            self.game_display.blit(small_font.render('{:2d}'.format(i+1), False, white_color), (top3[0], top3[1] + i * 15))
            self.game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top3[0] + 25, top3[1] + i * 15))
            self.game_display.blit(small_font.render(name, False, white_color), (top3[0] + 110, top3[1] + i * 15))

        for i in range (0,9):
            score = self.high_scores["high_scores"][i+3]["score"]
            name = self.high_scores["high_scores"][i+3]["name"]
            if i+4<10:
                self.game_display.blit(small_font.render('{:2d}'.format(i+4), False, white_color), (top12[0] + 5, top12[1] + i * 15))
            else:
                self.game_display.blit(small_font.render('{:2d}'.format(i+4), False, white_color), (top12[0], top12[1] + i * 15))
            
            self.game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top12[0] + 30, top12[1] + i * 15))
            self.game_display.blit(small_font.render(name, False, white_color), (top12[0] + 110, top12[1] + i * 15))

        for i in range (0,9):
            score = self.high_scores["high_scores"][i+12]["score"]
            name = self.high_scores["high_scores"][i+12]["name"]
            
            self.game_display.blit(small_font.render('{:2d}'.format(i+13), False, white_color), (top21[0], top21[1] + i * 15))
            self.game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top21[0] + 30, top21[1] + i * 15))
            self.game_display.blit(small_font.render(name, False, white_color), (top21[0] + 115, top21[1] + i * 15))

        for i in range (0,9):
            score = self.high_scores["high_scores"][i+21]["score"]
            name = self.high_scores["high_scores"][i+21]["name"]
            
            self.game_display.blit(small_font.render('{:2d}'.format(i+22), False, white_color), (top30[0], top30[1] + i * 15))
            self.game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top30[0] + 30, top30[1] + i * 15))
            self.game_display.blit(small_font.render(name, False, white_color), (top30[0] + 115, top30[1] + i * 15))

    