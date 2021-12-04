
from typing import Dict
import pygame.mixer
from pathlib import Path
import json
from loguru import logger

class Sample():

    def __init__(self, path: Path):

        if not path.exists():
            raise ValueError(f"No sample found at {path}")

        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self, loops: int = 0, maxtime: int = 0, fade_start_ms : int = 0):
        logger.debug(f"Playing {self.path}")
        self.sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_start_ms)
        
    def stop(self, fadeout_ms: int = 0):
        
        if fadeout_ms == 0:
            self.sound.stop()
        else:
            self.sound.fadeout(fadeout_ms)

class SampleManager(object):

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
        
        logger.debug(f"Looking for Sample manager: {name}")
        if name in cls.managers.keys():
            return cls.managers[name]
        else:
            raise ValueError(f"Sample Manager '{name}' not found!")
            
    def __init__(self, configuration_path: str):
        self.samples = {}
        self.configuration_path = Path(configuration_path)

        if pygame.mixer:
            pygame.mixer.init()

        if not self.configuration_path.exists():
            raise ValueError(f"No sample manager configuration found at {self.configuration_path}")

        try:
            with open(self.configuration_path, "r") as f:
                configuration = json.load(f)
            assert len(configuration.keys()) > 0
        except Exception as e:
            raise ValueError(f"Invalid configuration in {self.configuration_path}: {e}")

        for name, path in configuration.items():
            self.samples[name] = Sample(Path(path))

    def get_sample(self, name: str) -> Sample:

        if name not in self.samples.keys():
            raise ValueError(f"Sample {name} in not defined in configuration! Only {list(self.samples.keys())}")

        return self.samples[name]

    def fadeout(self, time_ms) -> None:
        pygame.mixer.fadeout(time_ms)

    def mute(self) -> None:
        pygame.mixer.stop()
    

