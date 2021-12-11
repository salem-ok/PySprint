
from typing import List, Dict
from pathlib import Path
import json
from loguru import logger
from pygame import Surface
import pygame


class FontManager(object):

    # Class variables
    managers = {}
    
    # Class methonds
    @classmethod
    def create_manager(cls, name: str, configuration_path: str):
        
        mgr = cls(configuration_path)
        cls.managers[name] = mgr

        return mgr

    @classmethod
    def get_manager(cls, name: str):
        
        logger.debug(f"Looking for Font manager: {name}")
        if name in cls.managers.keys():
            return cls.managers[name]
        else:
            raise ValueError(f"Font Manager '{name}' not found!")
            
    def __init__(self, configuration_path: str):
        self.ttfs = {}
        self.bitmap_fonts = {}
        self.configuration_path = Path(configuration_path)

        if not self.configuration_path.exists():
            raise ValueError(f"No Font manager configuration found at {self.configuration_path}")

        try:
            with open(self.configuration_path, "r") as f:
                configuration = json.load(f)
            assert len(configuration.keys()) > 0
        except Exception as e:
            raise ValueError(f"Invalid configuration in {self.configuration_path}: {e}")

        # preload
        for name, details in configuration['truetype'].items():
            self.ttfs[name] = pygame.font.Font(details['ttf_file'], details['size'])

        for name, details in configuration['bitmap'].items():

            self.bitmap_fonts[name] = {}
            for letter, path in details.items():
                self.bitmap_fonts[name][letter] = pygame.image.load(str(path)).convert_alpha()

    def get_truetype_font(self, name):

        if name not in self.ttfs.keys():
            raise ValueError(f"Truetype font {name} in not defined in configuration! Only {list(self.ttf.keys())}")

        return self.ttfs[name]

    def get_bitmap_font(self, name):

        if name not in self.bitmap_fonts.keys():
            raise ValueError(f"Bitmap font {name} in not defined in configuration! Only {list(self.bitmap_fonts.keys())}")

        return self.bitmap_fonts[name]
