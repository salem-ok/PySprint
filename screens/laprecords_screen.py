from loguru import logger
from screens.colors import *
from typing import Dict
import pygame

from screens.screen import Screen

class LapRecordsScreen(Screen):

    def __init__(self, display, best_laps: Dict):
        super().__init__(display=display)

        self.best_laps = best_laps
        self.texture = self.tex_manager.get_texture("lap_records_screen")

    def display(self):

        # small_font = self.font_manager.get_truetype_font("small_font")
        small_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf', 15)
        
        top4 = (55, 270)
        top8 = (335, 270)

        for i in range(4):
            time = self.best_laps["best_laps"][i]["time"]
            name = self.best_laps["best_laps"][i]["name"]
            self.game_display.blit(small_font.render('Track', False, white_color), (top4[0], top4[1] + i * 15))
            self.game_display.blit(small_font.render('{}'.format(i+1), False, white_color), (top4[0] + 70, top4[1] + i * 15))
            self.game_display.blit(small_font.render('{:04.1f}'.format(time), False, white_color), (top4[0] + 95, top4[1] + i * 15))
            self.game_display.blit(small_font.render('secs  {}'.format(name), False, white_color), (top4[0] + 150, top4[1] + i * 15))

        for i in range(4):
            time = self.best_laps["best_laps"][i+4]["time"]
            name = self.best_laps["best_laps"][i+4]["name"]
            
            self.game_display.blit(small_font.render('Track', False, white_color), (top8[0], top8[1] + i * 15))
            self.game_display.blit(small_font.render('{}'.format(i+5), False, white_color), (top8[0] + 70, top8[1] + i * 15))
            self.game_display.blit(small_font.render('{:04.1f}'.format(time), False, white_color), (top8[0] + 95, top8[1] + i * 15))
            self.game_display.blit(small_font.render('secs  {}'.format(name), False, white_color), (top8[0] + 150, top8[1] + i * 15))


    