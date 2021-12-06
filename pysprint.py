import pygame
from pygame import draw
import pygame.display
import pygame.mixer
from pygame import gfxdraw, init
import numpy as np
import pysprint_car
import pysprint_tracks
import pysprint_control_methods as pysprint_cm
import random
import json

#New awesome imports from shazz
from managers.sample_manager import SampleManager
from pathlib import Path
from loguru import logger

pygame.init()
pygame.joystick.init()

version = "0.37"
display_width = 640
display_height = 400
pysprint_car.display_width = 640
pysprint_car.display_height = 400
pysprint_tracks.display_width = 640
pysprint_tracks.display_height = 400

# Create sample managers
FADEOUT_DURATION = 1000
SampleManager.create_manager("sfx", "Assets/sound/smp_sfx.json")
smp_manager = SampleManager.create_manager("music", "Assets/sound/smp_music.json")

with open(".highscores.json") as high_scores_file:
    high_scores = json.load(high_scores_file)

with open(".bestlaps.json") as best_laps_file:
    best_laps = json.load(best_laps_file)



race_laps = 4
pysprint_car.race_laps = race_laps
flags = 0
game_display = pygame.display.set_mode((display_width, display_height), flags)

pygame.display.set_caption('PySprint v{}'.format(version))
icon = pygame.image.load('Assets/SuperSprintIcon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

pysprint_car.game_display = game_display
pysprint_tracks.game_display = game_display

cars = []

tracks = {}


FPS = 30
DEBUG_BUMP = False
DEBUG_CRASH = False
DEBUG_FLAG = False
DISPLAY_FPS = True
DEBUG_FPS = False
DEBUG_FPS_DETAILED = False
DEBUG_AI = False
DISABLE_DRONES = False

#Flag Events
GREENFLAG = pygame.USEREVENT
WHITEFLAG = GREENFLAG + 1
CHECKEREDFLAG = WHITEFLAG + 1

JOYSTICK_BUTTON_PRESSED = -2

#Colors
black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (238, 0, 34)
blue_color = (68, 102, 238)
yellow_color = (238, 238, 102)
green_color = (34, 170, 102)
green_secondary_color = (170, 204, 102)
blue_secondary_color = (170, 204, 238)
red_secondary_color = (170, 0, 0)
yellow_secondary_color = (170, 170, 0)
grey_color = (170, 170, 170)

blue_engine = (72, 146)
green_engine = (390, 284)
yellow_engine = (390, 146)
red_engine = (72, 284)

blue_customization = (12, 202)
green_customization = (330, 340)
yellow_customization = (330, 202)
red_customization = (12, 340)


blue_thumb = (51, 120)
green_thumb = (369, 258)
yellow_thumb = (369, 120)
red_thumb = (51, 258)

press_start_blue = (30,6)
press_start_green = (510,6)
press_start_red = (190,6)
press_start_yellow = (350,6)

score_top_left_blue = (1,0)
score_top_left_green = (161,0)
score_top_left_red = (321,0)
score_top_left_yellow = (481,0)



#Load Assets

#Sound Assets
podium_tunes = [ sample for name, sample in smp_manager.samples.items() if name.startswith('podium_tune') ]

#Graphic assets
pysprint_car.transparency = pygame.image.load('Assets/Transparency.png').convert_alpha()
pysprint_car.vector_surf = pygame.Surface((display_width,display_height))
pysprint_car.vector_surf.fill((0,0,0))
pysprint_car.vector_surf.set_colorkey((0,0,0))


tiny_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf',10)
pysprint_tracks.tiny_font = tiny_font
small_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf',15)
shadow_font = pygame.font.Font('Assets/SupersprintST-Regular-Stroke.ttf',15)
big_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf',20)
big_shadow_font = pygame.font.Font('Assets/SupersprintST-Regular-Stroke.ttf',20)

loading_screen_foreground = pygame.image.load('Assets/SuperSprintLoadingScreenForeground.png').convert_alpha()
credits_screen = pygame.image.load('Assets/SuperSprintCreditsScreen.png').convert_alpha()
splash_screen = pygame.image.load('Assets/SuperSprintSplashScreen.png').convert_alpha()
start_race_screen = pygame.image.load('Assets/SuperSprintStartRaceScreen.png').convert_alpha()
high_score_screen = pygame.image.load('Assets/SuperSprintHighScores.png').convert_alpha()
lap_records_screen = pygame.image.load('Assets/SuperSprintLapRecords.png').convert_alpha()
race_podium_screen = pygame.image.load('Assets/SuperSprintRacePodium.png').convert_alpha()
checkered_background = pygame.image.load('Assets/CheckeredBackground.png').convert_alpha()
item_screen = pygame.image.load('Assets/SuperSprintItemScreen.png').convert_alpha()

blue_selection_wheel = pygame.image.load('Assets/BlueSelectionWheel.png').convert_alpha()
yellow_selection_wheel = pygame.image.load('Assets/YellowSelectionWheel.png').convert_alpha()
red_selection_wheel = pygame.image.load('Assets/RedSelectionWheel.png').convert_alpha()
green_selection_wheel = pygame.image.load('Assets/GreenSelectionWheel.png').convert_alpha()

#Traffic Cone
pysprint_tracks.traffic_cone = pygame.image.load('Assets/TrafficCone.png').convert_alpha()
pysprint_tracks.traffic_cone_shade = pygame.image.load('Assets/TrafficConeShade.png').convert_alpha()
pysprint_tracks.traffic_cone_mask =  pygame.mask.from_surface(pysprint_tracks.traffic_cone, 50)

#Tornado Frames:
pysprint_tracks.tornado_frames = {
    0:pygame.image.load('Assets/TornadoFrame0.png').convert_alpha(),
    1:pygame.image.load('Assets/TornadoFrame1.png').convert_alpha()
}
pysprint_tracks.tornado_frames_masks = {
    0:pygame.mask.from_surface(pysprint_tracks.tornado_frames[0], 50),
    1:pygame.mask.from_surface(pysprint_tracks.tornado_frames[1], 50)
}

#Poles Frames:
pysprint_tracks.poles_frames = {
    0:pygame.image.load('Assets/PoleFrame0.png').convert_alpha(),
    1:pygame.image.load('Assets/PoleFrame1.png').convert_alpha(),
    2:pygame.image.load('Assets/PoleFrame2.png').convert_alpha(),
    3:pygame.image.load('Assets/PoleFrame3.png').convert_alpha()
}

pysprint_tracks.poles_frames_masks = {
    0:pygame.mask.from_surface(pysprint_tracks.poles_frames[0], 50),
    1:pygame.mask.from_surface(pysprint_tracks.poles_frames[1], 50),
    2:pygame.mask.from_surface(pysprint_tracks.poles_frames[2], 50),
    3:pygame.mask.from_surface(pysprint_tracks.poles_frames[3], 50)
}


#Spills
pysprint_tracks.oil_spill_image = pygame.image.load('Assets/OilSpill.png').convert_alpha()
pysprint_tracks.oil_spill_mask = pygame.mask.from_surface(pysprint_tracks.oil_spill_image, 50)
pysprint_tracks.water_spill_image = pygame.image.load('Assets/WaterSpill.png').convert_alpha()
pysprint_tracks.water_spill_mask = pygame.mask.from_surface(pysprint_tracks.water_spill_image, 50)
pysprint_tracks.grease_spill_image = pygame.image.load('Assets/GreaseSpill.png').convert_alpha()
pysprint_tracks.grease_spill_mask = pygame.mask.from_surface(pysprint_tracks.grease_spill_image, 50)

#Wrenches
pysprint_tracks.wrench_image = pygame.image.load('Assets/Wrench.png').convert_alpha()
pysprint_tracks.wrench_mask = pygame.mask.from_surface(pysprint_tracks.oil_spill_image, 50)

wrench_count_sprites = {
    0:pygame.image.load('Assets/0_WrenchCount.png').convert_alpha(),
    1:pygame.image.load('Assets/1_WrenchCount.png').convert_alpha(),
    2:pygame.image.load('Assets/2_WrenchCount.png').convert_alpha(),
    3:pygame.image.load('Assets/3_WrenchCount.png').convert_alpha(),
    3:pygame.image.load('Assets/3_WrenchCount.png').convert_alpha(),
    4:pygame.image.load('Assets/4_WrenchCount.png').convert_alpha(),
    5:pygame.image.load('Assets/5_WrenchCount.png').convert_alpha(),
    6:pygame.image.load('Assets/6_WrenchCount.png').convert_alpha(),
    7:pygame.image.load('Assets/7_WrenchCount.png').convert_alpha(),
    8:pygame.image.load('Assets/8_WrenchCount.png').convert_alpha(),
    9:pygame.image.load('Assets/9_WrenchCount.png').convert_alpha(),
}



#Bonus Frames:
pysprint_tracks.bonus_frames = {
    0:pygame.image.load('Assets/BonusFrame0.png').convert_alpha(),
    1:pygame.image.load('Assets/BonusFrame1.png').convert_alpha(),
    2:pygame.image.load('Assets/BonusFrame2.png').convert_alpha(),
    3:pygame.image.load('Assets/BonusFrame3.png').convert_alpha()
}

pysprint_tracks.bonus_frames_masks = {
    0:pygame.mask.from_surface(pysprint_tracks.bonus_frames[0], 50),
    1:pygame.mask.from_surface(pysprint_tracks.bonus_frames[1], 50),
    2:pygame.mask.from_surface(pysprint_tracks.bonus_frames[2], 50),
    3:pygame.mask.from_surface(pysprint_tracks.bonus_frames[3], 50)
}


pysprint_tracks.bonus_shade_frames = {
    0:pygame.image.load('Assets/BonusFrame0Shade.png').convert_alpha(),
    1:pygame.image.load('Assets/BonusFrame1Shade.png').convert_alpha(),
    2:pygame.image.load('Assets/BonusFrame2Shade.png').convert_alpha()
}



# For the Background
pysprint_tracks.road_gate_frames = {
    0:pygame.image.load('Assets/Gate0.png').convert_alpha(),
    1:pygame.image.load('Assets/Gate1.png').convert_alpha(),
    2:pygame.image.load('Assets/Gate2.png').convert_alpha(),
    3:pygame.image.load('Assets/Gate3.png').convert_alpha(),
    4:pygame.image.load('Assets/Gate4.png').convert_alpha()
}

# For the Overlay
pysprint_tracks.road_gate_shade_frames = {
    0:pygame.image.load('Assets/GateShade0.png').convert_alpha(),
    1:pygame.image.load('Assets/GateShade1.png').convert_alpha(),
    2:pygame.image.load('Assets/GateShade2.png').convert_alpha(),
    3:pygame.image.load('Assets/GateShade3.png').convert_alpha(),
    4:pygame.image.load('Assets/GateShade4.png').convert_alpha()
}

# For the Overlay
pysprint_tracks.road_gate_mask_frames = {
    0:pygame.image.load('Assets/GateMask0.png').convert_alpha(),
    1:pygame.image.load('Assets/GateMask1.png').convert_alpha(),
    2:pygame.image.load('Assets/GateMask2.png').convert_alpha(),
    3:pygame.image.load('Assets/GateMask3.png').convert_alpha(),
    4:pygame.image.load('Assets/GateMask4.png').convert_alpha()
}



crowd_flags = {
    0:pygame.image.load('Assets/CrowdFlags0.png').convert_alpha(),
    1:pygame.image.load('Assets/CrowdFlags1.png').convert_alpha(),
    2:pygame.image.load('Assets/CrowdFlags2.png').convert_alpha(),
    3:pygame.image.load('Assets/CrowdFlags3.png').convert_alpha(),
    4:pygame.image.load('Assets/CrowdFlags4.png').convert_alpha(),
    5:pygame.image.load('Assets/CrowdFlags5.png').convert_alpha()
}

hammer_frames_loader = {
    0:pygame.image.load('Assets/Hammer0.png').convert_alpha(),
    1:pygame.image.load('Assets/Hammer1.png').convert_alpha(),
    2:pygame.image.load('Assets/Hammer2.png').convert_alpha()
}
hammer_frames = {
    0:hammer_frames_loader[0],
    1:hammer_frames_loader[1],
    2:hammer_frames_loader[2],
    3:hammer_frames_loader[2],
    4:hammer_frames_loader[2]
}

saw_frames_loader =  {
    0:pygame.image.load('Assets/Saw0.png').convert_alpha(),
    1:pygame.image.load('Assets/Saw1.png').convert_alpha(),
    2:pygame.image.load('Assets/Saw2.png').convert_alpha()
}

saw_frames =  {
    0:saw_frames_loader[0],
    1:saw_frames_loader[1],
    2:saw_frames_loader[2],
    3:saw_frames_loader[1],
    4:saw_frames_loader[0]
}

head_scratch_frames_loader =  {
    0:pygame.image.load('Assets/HeadScratch0.png').convert_alpha(),
    1:pygame.image.load('Assets/HeadScratch1.png').convert_alpha(),
    2:pygame.image.load('Assets/HeadScratch2.png').convert_alpha()
}


head_scratch_frames =  {
    0:head_scratch_frames_loader[0],
    1:head_scratch_frames_loader[1],
    2:head_scratch_frames_loader[0],
    3:head_scratch_frames_loader[1],
    4:head_scratch_frames_loader[0],
    5:head_scratch_frames_loader[1],
    6:head_scratch_frames_loader[1],
    7:head_scratch_frames_loader[2],
    8:head_scratch_frames_loader[2],
    9:head_scratch_frames_loader[2],
    10:head_scratch_frames_loader[1],
    11:head_scratch_frames_loader[2],
    12:head_scratch_frames_loader[1],
    13:head_scratch_frames_loader[2]
}

blow_frames_loader =  {
    0:pygame.image.load('Assets/Blow0.png').convert_alpha(),
    1:pygame.image.load('Assets/Blow1.png').convert_alpha(),
    2:pygame.image.load('Assets/Blow2.png').convert_alpha(),
    3:pygame.image.load('Assets/Blow3.png').convert_alpha(),
    4:pygame.image.load('Assets/Blow4.png').convert_alpha()
}


blow_frames =  {
    0:blow_frames_loader[1],
    1:blow_frames_loader[0],
    2:blow_frames_loader[1],
    3:blow_frames_loader[0],
    4:blow_frames_loader[1],
    5:blow_frames_loader[2],
    6:blow_frames_loader[3],
    7:blow_frames_loader[4],
    8:blow_frames_loader[4],
    9:blow_frames_loader[4],
    10:blow_frames_loader[4],
    11:blow_frames_loader[4],
    12:blow_frames_loader[4],
    13:blow_frames_loader[4],
    14:blow_frames_loader[4],
    15:blow_frames_loader[4],
    16:blow_frames_loader[4]
}

first_car_blue = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarBlueCar.png').convert_alpha()
first_car_red = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarRedCar.png').convert_alpha()
first_car_green = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarGreenCar.png').convert_alpha()
first_car_yellow = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarYellowCar.png').convert_alpha()

first_car_blue_drone = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarBlueCarDrone.png').convert_alpha()
first_car_red_drone = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarRedCarDrone.png').convert_alpha()
first_car_green_drone = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarGreenCarDrone.png').convert_alpha()
first_car_yellow_drone = pygame.image.load('Assets/SuperSprintRacePodiumFirstCarYellowCarDrone.png').convert_alpha()

second_car_blue = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarBlueCar.png').convert_alpha()
second_car_red = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarRedCar.png').convert_alpha()
second_car_green = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarGreenCar.png').convert_alpha()
second_car_yellow = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarYellowCar.png').convert_alpha()

second_car_blue_drone = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarBlueCarDrone.png').convert_alpha()
second_car_red_drone = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarRedCarDrone.png').convert_alpha()
second_car_green_drone = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarGreenCarDrone.png').convert_alpha()
second_car_yellow_drone = pygame.image.load('Assets/SuperSprintRacePodiumSecondCarYellowCarDrone.png').convert_alpha()

third_car_blue = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarBlueCar.png').convert_alpha()
third_car_red = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarRedCar.png').convert_alpha()
third_car_green = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarGreenCar.png').convert_alpha()
third_car_yellow = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarYellowCar.png').convert_alpha()

third_car_blue_drone = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarBlueCarDrone.png').convert_alpha()
third_car_red_drone = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarRedCarDrone.png').convert_alpha()
third_car_green_drone = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarGreenCarDrone.png').convert_alpha()
third_car_yellow_drone = pygame.image.load('Assets/SuperSprintRacePodiumThirdCarYellowCarDrone.png').convert_alpha()

fourth_car_blue = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarBlueCar.png').convert_alpha()
fourth_car_red = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarRedCar.png').convert_alpha()
fourth_car_green = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarGreenCar.png').convert_alpha()
fourth_car_yellow = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarYellowCar.png').convert_alpha()

fourth_car_blue_drone = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarBlueCarDrone.png').convert_alpha()
fourth_car_red_drone = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarRedCarDrone.png').convert_alpha()
fourth_car_green_drone = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarGreenCarDrone.png').convert_alpha()
fourth_car_yellow_drone = pygame.image.load('Assets/SuperSprintRacePodiumFourthCarYellowCarDrone.png').convert_alpha()


engine_idle = {
    0:pygame.image.load('Assets/EngineIdle0.png').convert_alpha(),
    1:pygame.image.load('Assets/EngineIdle1.png').convert_alpha(),
    2:pygame.image.load('Assets/EngineIdle2.png').convert_alpha(),
}

prepare_to_race = {
    0:pygame.image.load('Assets/PrePareToRace0.png').convert_alpha(),
    1:pygame.image.load('Assets/PrePareToRace1.png').convert_alpha(),
    2:pygame.image.load('Assets/PrePareToRace2.png').convert_alpha(),
    3:pygame.image.load('Assets/PrePareToRace3.png').convert_alpha(),
    4:pygame.image.load('Assets/PrePareToRace4.png').convert_alpha(),
    5:pygame.image.load('Assets/PrePareToRace5.png').convert_alpha(),
    6:pygame.image.load('Assets/PrePareToRace6.png').convert_alpha(),
    7:pygame.image.load('Assets/PrePareToRace7.png').convert_alpha(),
    8:pygame.image.load('Assets/PrePareToRace8.png').convert_alpha(),
    9:pygame.image.load('Assets/PrePareToRace2.png').convert_alpha(),
    10:pygame.image.load('Assets/PrePareToRace1.png').convert_alpha(),
    11:pygame.image.load('Assets/PrePareToRace0.png').convert_alpha(),
}
attract_mode_display_duration = 5000

transition_dots = {
    0:pygame.image.load('Assets/TransitionDot0.png').convert_alpha(),
    1:pygame.image.load('Assets/TransitionDot1.png').convert_alpha(),
    2:pygame.image.load('Assets/TransitionDot2.png').convert_alpha(),
    3:pygame.image.load('Assets/TransitionDot3.png').convert_alpha(),
    4:pygame.image.load('Assets/TransitionDot4.png').convert_alpha(),
    5:pygame.image.load('Assets/TransitionDot5.png').convert_alpha(),
    6:pygame.image.load('Assets/TransitionDot6.png').convert_alpha(),
    7:pygame.image.load('Assets/TransitionDot7.png').convert_alpha()
}


scrolling_font = {
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

green_flag_frames = {
    0:pygame.image.load('Assets/GreenFlag0.png').convert_alpha(),
    1:pygame.image.load('Assets/GreenFlag1.png').convert_alpha(),
    2:pygame.image.load('Assets/GreenFlag2.png').convert_alpha(),
    3:pygame.image.load('Assets/GreenFlag3.png').convert_alpha(),
    4:pygame.image.load('Assets/GreenFlag4.png').convert_alpha(),
    5:pygame.image.load('Assets/GreenFlag5.png').convert_alpha(),
    6:pygame.image.load('Assets/GreenFlag6.png').convert_alpha()
}

white_flag_frames = {
    0:pygame.image.load('Assets/WhiteFlag0.png').convert_alpha(),
    1:pygame.image.load('Assets/WhiteFlag1.png').convert_alpha(),
    2:pygame.image.load('Assets/WhiteFlag2.png').convert_alpha(),
    3:pygame.image.load('Assets/WhiteFlag3.png').convert_alpha(),
    4:pygame.image.load('Assets/WhiteFlag4.png').convert_alpha(),
    5:pygame.image.load('Assets/WhiteFlag5.png').convert_alpha(),
    6:pygame.image.load('Assets/WhiteFlag6.png').convert_alpha()
}

checkered_flag_frames = {
    0:pygame.image.load('Assets/CheckeredFlag0.png').convert_alpha(),
    1:pygame.image.load('Assets/CheckeredFlag1.png').convert_alpha(),
    2:pygame.image.load('Assets/CheckeredFlag2.png').convert_alpha(),
    3:pygame.image.load('Assets/CheckeredFlag3.png').convert_alpha(),
    4:pygame.image.load('Assets/CheckeredFlag4.png').convert_alpha(),
    5:pygame.image.load('Assets/CheckeredFlag5.png').convert_alpha(),
    6:pygame.image.load('Assets/CheckeredFlag6.png').convert_alpha()
}


yellow_helicopter_frames = {
    0:pygame.image.load('Assets/YellowHelicopter0.png').convert_alpha(),
    1:pygame.image.load('Assets/YellowHelicopter1.png').convert_alpha(),
    2:pygame.image.load('Assets/YellowHelicopter2.png').convert_alpha(),
    3:pygame.image.load('Assets/YellowHelicopter3.png').convert_alpha()
}

blue_helicopter_frames = {
    0:pygame.image.load('Assets/BlueHelicopter0.png').convert_alpha(),
    1:pygame.image.load('Assets/BlueHelicopter1.png').convert_alpha(),
    2:pygame.image.load('Assets/BlueHelicopter2.png').convert_alpha(),
    3:pygame.image.load('Assets/BlueHelicopter3.png').convert_alpha()
}

green_helicopter_frames = {
    0:pygame.image.load('Assets/GreenHelicopter0.png').convert_alpha(),
    1:pygame.image.load('Assets/GreenHelicopter1.png').convert_alpha(),
    2:pygame.image.load('Assets/GreenHelicopter2.png').convert_alpha(),
    3:pygame.image.load('Assets/GreenHelicopter3.png').convert_alpha()
}

red_helicopter_frames = {
    0:pygame.image.load('Assets/RedHelicopter0.png').convert_alpha(),
    1:pygame.image.load('Assets/RedHelicopter1.png').convert_alpha(),
    2:pygame.image.load('Assets/RedHelicopter2.png').convert_alpha(),
    3:pygame.image.load('Assets/RedHelicopter3.png').convert_alpha()
}

yellow_vertical_helicopter_frames = {
    0:pygame.image.load('Assets/YellowHelicopterV0.png').convert_alpha(),
    1:pygame.image.load('Assets/YellowHelicopterV1.png').convert_alpha(),
    2:pygame.image.load('Assets/YellowHelicopterV2.png').convert_alpha(),
    3:pygame.image.load('Assets/YellowHelicopterV3.png').convert_alpha()
}

blue_vertical_helicopter_frames = {
    0:pygame.image.load('Assets/BlueHelicopterV0.png').convert_alpha(),
    1:pygame.image.load('Assets/BlueHelicopterV1.png').convert_alpha(),
    2:pygame.image.load('Assets/BlueHelicopterV2.png').convert_alpha(),
    3:pygame.image.load('Assets/BlueHelicopterV3.png').convert_alpha()
}

green_vertical_helicopter_frames = {
    0:pygame.image.load('Assets/GreenHelicopterV0.png').convert_alpha(),
    1:pygame.image.load('Assets/GreenHelicopterV1.png').convert_alpha(),
    2:pygame.image.load('Assets/GreenHelicopterV2.png').convert_alpha(),
    3:pygame.image.load('Assets/GreenHelicopterV3.png').convert_alpha()
}

red_vertical_helicopter_frames = {
    0:pygame.image.load('Assets/RedHelicopterV0.png').convert_alpha(),
    1:pygame.image.load('Assets/RedHelicopterV1.png').convert_alpha(),
    2:pygame.image.load('Assets/RedHelicopterV2.png').convert_alpha(),
    3:pygame.image.load('Assets/RedHelicopterV3.png').convert_alpha()
}



dust_cloud_frames = {
    0:pygame.image.load('Assets/DustCloud0.png').convert_alpha(),
    1:pygame.image.load('Assets/DustCloud1.png').convert_alpha(),
    2:pygame.image.load('Assets/DustCloud2.png').convert_alpha(),
    3:pygame.image.load('Assets/DustCloud3.png').convert_alpha(),
    4:pygame.image.load('Assets/DustCloud4.png').convert_alpha()
}


explosion_frames = {
    0:pygame.image.load('Assets/Explosion0.png').convert_alpha(),
    1:pygame.image.load('Assets/Explosion1.png').convert_alpha(),
    2:pygame.image.load('Assets/Explosion2.png').convert_alpha(),
    3:pygame.image.load('Assets/Explosion3.png').convert_alpha(),
    4:pygame.image.load('Assets/Explosion4.png').convert_alpha(),
    5:pygame.image.load('Assets/Explosion5.png').convert_alpha(),
    6:pygame.image.load('Assets/Explosion6.png').convert_alpha(),
    7:pygame.image.load('Assets/Explosion7.png').convert_alpha(),
    8:pygame.image.load('Assets/Explosion8.png').convert_alpha(),
    9:pygame.image.load('Assets/Explosion9.png').convert_alpha(),
    10:pygame.image.load('Assets/Explosion10.png').convert_alpha(),
    11:pygame.image.load('Assets/Explosion11.png').convert_alpha(),
    12:pygame.image.load('Assets/Explosion12.png').convert_alpha(),
    13:pygame.image.load('Assets/Explosion13.png').convert_alpha(),
    14:pygame.image.load('Assets/Explosion14.png').convert_alpha(),
    15:pygame.image.load('Assets/Explosion15.png').convert_alpha(),
    16:pygame.image.load('Assets/Explosion16.png').convert_alpha(),
    17:pygame.image.load('Assets/Explosion17.png').convert_alpha(),
    18:pygame.image.load('Assets/Explosion18.png').convert_alpha()
}

blue_drone_sprites = {
        0:pygame.image.load('Assets/BlueCarDrone0.png').convert_alpha(),
        1:pygame.image.load('Assets/BlueCarDrone1.png').convert_alpha(),
        2:pygame.image.load('Assets/BlueCarDrone2.png').convert_alpha(),
        3:pygame.image.load('Assets/BlueCarDrone3.png').convert_alpha(),
        4:pygame.image.load('Assets/BlueCarDrone4.png').convert_alpha(),
        5:pygame.image.load('Assets/BlueCarDrone5.png').convert_alpha(),
        6:pygame.image.load('Assets/BlueCarDrone6.png').convert_alpha(),
        7:pygame.image.load('Assets/BlueCarDrone7.png').convert_alpha(),
        8:pygame.image.load('Assets/BlueCarDrone8.png').convert_alpha(),
        9:pygame.image.load('Assets/BlueCarDrone9.png').convert_alpha(),
        10:pygame.image.load('Assets/BlueCarDrone10.png').convert_alpha(),
        11:pygame.image.load('Assets/BlueCarDrone11.png').convert_alpha(),
        12:pygame.image.load('Assets/BlueCarDrone12.png').convert_alpha(),
        13:pygame.image.load('Assets/BlueCarDrone13.png').convert_alpha(),
        14:pygame.image.load('Assets/BlueCarDrone14.png').convert_alpha(),
        15:pygame.image.load('Assets/BlueCarDrone15.png').convert_alpha()
}

car_sprites_masks = {
        0:pygame.mask.from_surface(blue_drone_sprites[0], 50),
        1:pygame.mask.from_surface(blue_drone_sprites[1], 50),
        2:pygame.mask.from_surface(blue_drone_sprites[2], 50),
        3:pygame.mask.from_surface(blue_drone_sprites[3], 50),
        4:pygame.mask.from_surface(blue_drone_sprites[4], 50),
        5:pygame.mask.from_surface(blue_drone_sprites[5], 50),
        6:pygame.mask.from_surface(blue_drone_sprites[6], 50),
        7:pygame.mask.from_surface(blue_drone_sprites[7], 50),
        8:pygame.mask.from_surface(blue_drone_sprites[8], 50),
        9:pygame.mask.from_surface(blue_drone_sprites[9], 50),
        10:pygame.mask.from_surface(blue_drone_sprites[10], 50),
        11:pygame.mask.from_surface(blue_drone_sprites[11], 50),
        12:pygame.mask.from_surface(blue_drone_sprites[12], 50),
        13:pygame.mask.from_surface(blue_drone_sprites[13], 50),
        14:pygame.mask.from_surface(blue_drone_sprites[14], 50),
        15:pygame.mask.from_surface(blue_drone_sprites[15], 50)
}

blue_car_sprites = {
        0:pygame.image.load('Assets/BlueCar0.png').convert_alpha(),
        1:pygame.image.load('Assets/BlueCar1.png').convert_alpha(),
        2:pygame.image.load('Assets/BlueCar2.png').convert_alpha(),
        3:pygame.image.load('Assets/BlueCar3.png').convert_alpha(),
        4:pygame.image.load('Assets/BlueCar4.png').convert_alpha(),
        5:pygame.image.load('Assets/BlueCar5.png').convert_alpha(),
        6:pygame.image.load('Assets/BlueCar6.png').convert_alpha(),
        7:pygame.image.load('Assets/BlueCar7.png').convert_alpha(),
        8:pygame.image.load('Assets/BlueCar8.png').convert_alpha(),
        9:pygame.image.load('Assets/BlueCar9.png').convert_alpha(),
        10:pygame.image.load('Assets/BlueCar10.png').convert_alpha(),
        11:pygame.image.load('Assets/BlueCar11.png').convert_alpha(),
        12:pygame.image.load('Assets/BlueCar12.png').convert_alpha(),
        13:pygame.image.load('Assets/BlueCar13.png').convert_alpha(),
        14:pygame.image.load('Assets/BlueCar14.png').convert_alpha(),
        15:pygame.image.load('Assets/BlueCar15.png').convert_alpha()
}

red_drone_sprites = {
        0:pygame.image.load('Assets/RedCarDrone0.png').convert_alpha(),
        1:pygame.image.load('Assets/RedCarDrone1.png').convert_alpha(),
        2:pygame.image.load('Assets/RedCarDrone2.png').convert_alpha(),
        3:pygame.image.load('Assets/RedCarDrone3.png').convert_alpha(),
        4:pygame.image.load('Assets/RedCarDrone4.png').convert_alpha(),
        5:pygame.image.load('Assets/RedCarDrone5.png').convert_alpha(),
        6:pygame.image.load('Assets/RedCarDrone6.png').convert_alpha(),
        7:pygame.image.load('Assets/RedCarDrone7.png').convert_alpha(),
        8:pygame.image.load('Assets/RedCarDrone8.png').convert_alpha(),
        9:pygame.image.load('Assets/RedCarDrone9.png').convert_alpha(),
        10:pygame.image.load('Assets/RedCarDrone10.png').convert_alpha(),
        11:pygame.image.load('Assets/RedCarDrone11.png').convert_alpha(),
        12:pygame.image.load('Assets/RedCarDrone12.png').convert_alpha(),
        13:pygame.image.load('Assets/RedCarDrone13.png').convert_alpha(),
        14:pygame.image.load('Assets/RedCarDrone14.png').convert_alpha(),
        15:pygame.image.load('Assets/RedCarDrone15.png').convert_alpha()
}

red_car_sprites = {
        0:pygame.image.load('Assets/RedCar0.png').convert_alpha(),
        1:pygame.image.load('Assets/RedCar1.png').convert_alpha(),
        2:pygame.image.load('Assets/RedCar2.png').convert_alpha(),
        3:pygame.image.load('Assets/RedCar3.png').convert_alpha(),
        4:pygame.image.load('Assets/RedCar4.png').convert_alpha(),
        5:pygame.image.load('Assets/RedCar5.png').convert_alpha(),
        6:pygame.image.load('Assets/RedCar6.png').convert_alpha(),
        7:pygame.image.load('Assets/RedCar7.png').convert_alpha(),
        8:pygame.image.load('Assets/RedCar8.png').convert_alpha(),
        9:pygame.image.load('Assets/RedCar9.png').convert_alpha(),
        10:pygame.image.load('Assets/RedCar10.png').convert_alpha(),
        11:pygame.image.load('Assets/RedCar11.png').convert_alpha(),
        12:pygame.image.load('Assets/RedCar12.png').convert_alpha(),
        13:pygame.image.load('Assets/RedCar13.png').convert_alpha(),
        14:pygame.image.load('Assets/RedCar14.png').convert_alpha(),
        15:pygame.image.load('Assets/RedCar15.png').convert_alpha()
}

yellow_drone_sprites = {
        0:pygame.image.load('Assets/YellowCarDrone0.png').convert_alpha(),
        1:pygame.image.load('Assets/YellowCarDrone1.png').convert_alpha(),
        2:pygame.image.load('Assets/YellowCarDrone2.png').convert_alpha(),
        3:pygame.image.load('Assets/YellowCarDrone3.png').convert_alpha(),
        4:pygame.image.load('Assets/YellowCarDrone4.png').convert_alpha(),
        5:pygame.image.load('Assets/YellowCarDrone5.png').convert_alpha(),
        6:pygame.image.load('Assets/YellowCarDrone6.png').convert_alpha(),
        7:pygame.image.load('Assets/YellowCarDrone7.png').convert_alpha(),
        8:pygame.image.load('Assets/YellowCarDrone8.png').convert_alpha(),
        9:pygame.image.load('Assets/YellowCarDrone9.png').convert_alpha(),
        10:pygame.image.load('Assets/YellowCarDrone10.png').convert_alpha(),
        11:pygame.image.load('Assets/YellowCarDrone11.png').convert_alpha(),
        12:pygame.image.load('Assets/YellowCarDrone12.png').convert_alpha(),
        13:pygame.image.load('Assets/YellowCarDrone13.png').convert_alpha(),
        14:pygame.image.load('Assets/YellowCarDrone14.png').convert_alpha(),
        15:pygame.image.load('Assets/YellowCarDrone15.png').convert_alpha()
}

yellow_car_sprites = {
        0:pygame.image.load('Assets/YellowCar0.png').convert_alpha(),
        1:pygame.image.load('Assets/YellowCar1.png').convert_alpha(),
        2:pygame.image.load('Assets/YellowCar2.png').convert_alpha(),
        3:pygame.image.load('Assets/YellowCar3.png').convert_alpha(),
        4:pygame.image.load('Assets/YellowCar4.png').convert_alpha(),
        5:pygame.image.load('Assets/YellowCar5.png').convert_alpha(),
        6:pygame.image.load('Assets/YellowCar6.png').convert_alpha(),
        7:pygame.image.load('Assets/YellowCar7.png').convert_alpha(),
        8:pygame.image.load('Assets/YellowCar8.png').convert_alpha(),
        9:pygame.image.load('Assets/YellowCar9.png').convert_alpha(),
        10:pygame.image.load('Assets/YellowCar10.png').convert_alpha(),
        11:pygame.image.load('Assets/YellowCar11.png').convert_alpha(),
        12:pygame.image.load('Assets/YellowCar12.png').convert_alpha(),
        13:pygame.image.load('Assets/YellowCar13.png').convert_alpha(),
        14:pygame.image.load('Assets/YellowCar14.png').convert_alpha(),
        15:pygame.image.load('Assets/YellowCar15.png').convert_alpha()
}

green_drone_sprites = {
        0:pygame.image.load('Assets/GreenCarDrone0.png').convert_alpha(),
        1:pygame.image.load('Assets/GreenCarDrone1.png').convert_alpha(),
        2:pygame.image.load('Assets/GreenCarDrone2.png').convert_alpha(),
        3:pygame.image.load('Assets/GreenCarDrone3.png').convert_alpha(),
        4:pygame.image.load('Assets/GreenCarDrone4.png').convert_alpha(),
        5:pygame.image.load('Assets/GreenCarDrone5.png').convert_alpha(),
        6:pygame.image.load('Assets/GreenCarDrone6.png').convert_alpha(),
        7:pygame.image.load('Assets/GreenCarDrone7.png').convert_alpha(),
        8:pygame.image.load('Assets/GreenCarDrone8.png').convert_alpha(),
        9:pygame.image.load('Assets/GreenCarDrone9.png').convert_alpha(),
        10:pygame.image.load('Assets/GreenCarDrone10.png').convert_alpha(),
        11:pygame.image.load('Assets/GreenCarDrone11.png').convert_alpha(),
        12:pygame.image.load('Assets/GreenCarDrone12.png').convert_alpha(),
        13:pygame.image.load('Assets/GreenCarDrone13.png').convert_alpha(),
        14:pygame.image.load('Assets/GreenCarDrone14.png').convert_alpha(),
        15:pygame.image.load('Assets/GreenCarDrone15.png').convert_alpha()
}

green_car_sprites = {
        0:pygame.image.load('Assets/GreenCar0.png').convert_alpha(),
        1:pygame.image.load('Assets/GreenCar1.png').convert_alpha(),
        2:pygame.image.load('Assets/GreenCar2.png').convert_alpha(),
        3:pygame.image.load('Assets/GreenCar3.png').convert_alpha(),
        4:pygame.image.load('Assets/GreenCar4.png').convert_alpha(),
        5:pygame.image.load('Assets/GreenCar5.png').convert_alpha(),
        6:pygame.image.load('Assets/GreenCar6.png').convert_alpha(),
        7:pygame.image.load('Assets/GreenCar7.png').convert_alpha(),
        8:pygame.image.load('Assets/GreenCar8.png').convert_alpha(),
        9:pygame.image.load('Assets/GreenCar9.png').convert_alpha(),
        10:pygame.image.load('Assets/GreenCar10.png').convert_alpha(),
        11:pygame.image.load('Assets/GreenCar11.png').convert_alpha(),
        12:pygame.image.load('Assets/GreenCar12.png').convert_alpha(),
        13:pygame.image.load('Assets/GreenCar13.png').convert_alpha(),
        14:pygame.image.load('Assets/GreenCar14.png').convert_alpha(),
        15:pygame.image.load('Assets/GreenCar15.png').convert_alpha()
}

control_methods = pysprint_cm.control_methods


def screen_fadeout():
    for frame in range (0,len(transition_dots)):
        for i in range (0,40):
            for j in  range (0,24):
                game_display.blit(transition_dots[frame], (i * 16, j *17))
        pygame.display.update()
        clock.tick(len(transition_dots)*1.5)


def screen_fadein(screen):
    frame = len(transition_dots)
    while frame > 0:
        game_display.blit(screen, (0, 0))
        for i in range (0,40):
            for j in  range (0,24):
                game_display.blit(transition_dots[frame-1], (i * 16, j *17))
        pygame.display.update()
        clock.tick(len(transition_dots)*1.5)
        frame -= 1

def display_loading_screen(loop):
    screen_fadein(loading_screen_foreground)
    screen_exit = False
    key_pressed = False
    scroll_message = "SUPER SPRINT REMADE WITH PYGAME BY SALEM_OK. THANKS TO JOHNATHAN THOMAS FOR THE SPRITES RIP AND COGWEASEL FOR THE SPLASH SCREEN. ORIGINAL CREATED FOR THE MIGHTY ATARI ST BY STATE OF THE ART. PROGRAMMING: NALIN SHARMA  MARTIN GREEN  JON STEELE. GRAPHICS: CHRIS GIBBS. SOUND: MARK TISDALE. A SOFTWARE STUDIOS PRODUCTION..."
    right_end = 490
    left_end = 148
    scroll_y = 370
    background = pygame.Surface((display_width,display_height))
    background.fill(black_color)
    text = pygame.Surface(((scrolling_font['A'].get_width() + 1) * len(scroll_message) + right_end - left_end, scrolling_font['A'].get_height()))
    x_offset = right_end - left_end
    for char in scroll_message:
        text.blit(scrolling_font[char], (x_offset, 0))
        x_offset += scrolling_font[char].get_width() + 1
    dx = 0
    if FPS == 30:
        scroll_increment = -6
    if FPS == 60:
        scroll_increment = -3
    while not screen_exit:
        if dx >= text.get_width() and not loop:
            screen_exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                screen_exit = True
                key_pressed = event.key
        if any_joystick_button_pressed():
            screen_exit = True
            key_pressed = JOYSTICK_BUTTON_PRESSED
        game_display.blit(background, (0, 0))
        game_display.blit(text, (left_end, scroll_y))
        game_display.blit(loading_screen_foreground, (0, 0))
        pygame.display.update()
        text.scroll(scroll_increment)
        dx -= scroll_increment
        clock.tick(FPS)
    screen_fadeout()
    return key_pressed

def display_credits_screen():
    screen_exit = False
    key_pressed = False
    screen_fadein(credits_screen)
    pygame.display.update()
    screen_start_time = pygame.time.get_ticks()
    while not screen_exit:
        if pygame.time.get_ticks() - screen_start_time >= attract_mode_display_duration:
            screen_exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                screen_exit = True
                key_pressed = event.key
        if any_joystick_button_pressed():
            screen_exit = True
            key_pressed = JOYSTICK_BUTTON_PRESSED

    screen_fadeout()
    return key_pressed

def display_splash_screen():
    screen_exit = False
    key_pressed = False
    screen_fadein(splash_screen)
    pygame.display.update()
    screen_start_time = pygame.time.get_ticks()
    while not screen_exit:
        if pygame.time.get_ticks() - screen_start_time >= attract_mode_display_duration:
            screen_exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                screen_exit = True
                key_pressed = event.key
        if any_joystick_button_pressed():
            screen_exit = True
            key_pressed = JOYSTICK_BUTTON_PRESSED

    screen_fadeout()
    return key_pressed

def display_high_scores():
    screen_exit = False
    key_pressed = False
    screen_fadein(high_score_screen)
    top3 = (250, 100)
    top12 = (60, 225)
    top21 = (245, 225)
    top30 = (425, 225)
    for i in range (0,3):
        score = high_scores["high_scores"][i]["score"]
        name = high_scores["high_scores"][i]["name"]
        game_display.blit(small_font.render('{:2d}'.format(i+1), False, white_color), (top3[0], top3[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top3[0] + 25, top3[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top3[0] + 110, top3[1] + i * 15))

    for i in range (0,9):
        score = high_scores["high_scores"][i+3]["score"]
        name = high_scores["high_scores"][i+3]["name"]
        if i+4<10:
            game_display.blit(small_font.render('{:2d}'.format(i+4), False, white_color), (top12[0] + 5, top12[1] + i * 15))
        else:
            game_display.blit(small_font.render('{:2d}'.format(i+4), False, white_color), (top12[0], top12[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top12[0] + 30, top12[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top12[0] + 110, top12[1] + i * 15))

    for i in range (0,9):
        score = high_scores["high_scores"][i+12]["score"]
        name = high_scores["high_scores"][i+12]["name"]
        game_display.blit(small_font.render('{:2d}'.format(i+13), False, white_color), (top21[0], top21[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top21[0] + 30, top21[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top21[0] + 115, top21[1] + i * 15))

    for i in range (0,9):
        score = high_scores["high_scores"][i+21]["score"]
        name = high_scores["high_scores"][i+21]["name"]
        game_display.blit(small_font.render('{:2d}'.format(i+22), False, white_color), (top30[0], top30[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top30[0] + 30, top30[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top30[0] + 115, top30[1] + i * 15))

    pygame.display.update()
    screen_start_time = pygame.time.get_ticks()
    while not screen_exit:
        if pygame.time.get_ticks() - screen_start_time >= attract_mode_display_duration:
            screen_exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                screen_exit = True
                key_pressed = event.key
        if any_joystick_button_pressed():
            screen_exit = True
            key_pressed = JOYSTICK_BUTTON_PRESSED
    screen_fadeout()

    return key_pressed

def display_lap_records():
    screen_exit = False
    key_pressed = -1
    screen_fadein(lap_records_screen)
    top4 = (55, 270)
    top8 = (335, 270)
    for i in range(0,4):
        time = best_laps["best_laps"][i]["time"]
        name = best_laps["best_laps"][i]["name"]
        game_display.blit(small_font.render('Track', False, white_color), (top4[0], top4[1] + i * 15))
        game_display.blit(small_font.render('{}'.format(i+1), False, white_color), (top4[0] + 70, top4[1] + i * 15))
        game_display.blit(small_font.render('{:04.1f}'.format(time), False, white_color), (top4[0] + 95, top4[1] + i * 15))
        game_display.blit(small_font.render('secs  {}'.format(name), False, white_color), (top4[0] + 150, top4[1] + i * 15))

    for i in range(0,4):
        time = best_laps["best_laps"][i+4]["time"]
        name = best_laps["best_laps"][i+4]["name"]
        game_display.blit(small_font.render('Track', False, white_color), (top8[0], top8[1] + i * 15))
        game_display.blit(small_font.render('{}'.format(i+5), False, white_color), (top8[0] + 70, top8[1] + i * 15))
        game_display.blit(small_font.render('{:04.1f}'.format(time), False, white_color), (top8[0] + 95, top8[1] + i * 15))
        game_display.blit(small_font.render('secs  {}'.format(name), False, white_color), (top8[0] + 150, top8[1] + i * 15))

    pygame.display.update()
    screen_start_time = pygame.time.get_ticks()
    while not screen_exit:
        if pygame.time.get_ticks() - screen_start_time >= attract_mode_display_duration:
            screen_exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                screen_exit = True
                key_pressed = event.key
        if any_joystick_button_pressed():
            screen_exit = True
            key_pressed = JOYSTICK_BUTTON_PRESSED
    screen_fadeout()
    return key_pressed


def print_get_ready():
    prepare_surf = big_font.render("GET READY", False, white_color)
    shadow_prepare_surf = big_shadow_font.render("GET READY", False, black_color)
    game_display.blit(shadow_prepare_surf, (220, 190))
    game_display.blit(prepare_surf, (220, 190))


def print_prepare_to_race(top_left, color):
    prepare_surf = big_font.render("PREPARE", False, color)
    shadow_prepare_surf = big_shadow_font.render("PREPARE", False, black_color)
    game_display.blit(shadow_prepare_surf, top_left)
    game_display.blit(prepare_surf, top_left)
    to_surf = big_font.render("TO", False, color)
    shadow_to_surf = big_shadow_font.render("TO", False, black_color)
    game_display.blit(shadow_to_surf, ((top_left[0] + (prepare_surf.get_width() - to_surf.get_width())/2), top_left[1] + 25))
    game_display.blit(to_surf, ((top_left[0] + (prepare_surf.get_width() - to_surf.get_width())/2), top_left[1] + 25))
    race_surf = big_font.render("RACE", False, color)
    shadow_race_surf = big_shadow_font.render("RACE", False, black_color)
    game_display.blit(shadow_race_surf, (top_left[0] + (prepare_surf.get_width() - race_surf.get_width())/2, top_left[1] + 50))
    game_display.blit(race_surf, (top_left[0] + (prepare_surf.get_width() - race_surf.get_width())/2, top_left[1] + 50))

def print_game_over(top_left, color):
    prepare_surf = big_font.render("GAME", False, color)
    shadow_prepare_surf = big_shadow_font.render("GAME", False, black_color)
    game_display.blit(shadow_prepare_surf, top_left)
    game_display.blit(prepare_surf, top_left)
    to_surf = big_font.render("OVER", False, color)
    shadow_to_surf = big_shadow_font.render("OVER", False, black_color)
    game_display.blit(shadow_to_surf, ((top_left[0] + (prepare_surf.get_width() - to_surf.get_width())/2), top_left[1] + 25))
    game_display.blit(to_surf, ((top_left[0] + (prepare_surf.get_width() - to_surf.get_width())/2), top_left[1] + 25))

def print_enter_initials(car: pysprint_car.Car):
    game_display.blit(small_font.render("ENTER", False, car.main_color), car.start_screen_text_position)
    game_display.blit(small_font.render("INITIALS", False, car.main_color), (car.start_screen_text_position[0] - 28, car.start_screen_text_position[1] + 20))
    if car.enter_high_score:
        game_display.blit(small_font.render("POSITION {}".format(car.high_score_rank), False, car.main_color), (car.start_screen_text_position[0] - 32, car.start_screen_text_position[1] + 40))
    else:
        game_display.blit(small_font.render("BEST LAP", False, car.main_color), (car.start_screen_text_position[0] - 24, car.start_screen_text_position[1] + 40))
    initials_surf = big_font.render(car.high_score_name, False, car.main_color)
    shadow_initials_surf = big_shadow_font.render(car.high_score_name, False, black_color)
    game_display.blit(shadow_initials_surf, (car.start_screen_text_position[0] - 10, car.start_screen_text_position[1] + 60))
    game_display.blit(initials_surf, (car.start_screen_text_position[0] - 10, car.start_screen_text_position[1] + 60))


def print_press_acceltoplay(top_left, color, seconds, game_over):
    game_display.blit(small_font.render("PRESS", False, color), top_left)
    game_display.blit(small_font.render("ACCELERATE", False, color), (top_left[0] - 28, top_left[1] + 20))
    if game_over:
        game_display.blit(small_font.render("TO CONTINUE", False, color), (top_left[0] - 32, top_left[1] + 40))
    else:
        game_display.blit(small_font.render("TO PLAY", False, color), (top_left[0] - 10, top_left[1] + 40))
    if not seconds=='':
        if seconds <= 5:
            game_display.blit(small_font.render("{}".format(seconds), False, color), (top_left[0] + 24, top_left[1] + 60))

def print_start_race_text(seconds):
    for car in cars:
        if car.is_drone:
            print_press_acceltoplay(car.start_screen_text_position, car.main_color, seconds, car.game_over)
        else:
            print_prepare_to_race(car.start_screen_text_position, car.main_color)
    if not seconds == "":
        skip_surf = small_font.render("PRESS SPACE TO SKIP", False, white_color)
        game_display.blit(skip_surf, ((600 - skip_surf.get_width())/2, 385))

def print_game_over_text():
    for car in cars:
        if car.enter_best_lap or car.enter_high_score:
            print_enter_initials(car)
        else:
            if car.is_drone and car.game_over:
                print_game_over(car.start_screen_text_position, car.main_color)
            else:
                if car.is_drone == False:
                    print_prepare_to_race(car.start_screen_text_position, car.main_color)

def display_start_race_screen():
    seconds = 8
    screen_exit = False
    engine_idle_counter = 0

    #Add Green car
    screen_fadein(start_race_screen)
    smp_manager.get_sample("prepare_to_race_music").play()
    print_start_race_text(seconds)
    game_over_screen = False
    for car in cars:
        game_display.blit(engine_idle[engine_idle_counter], car.start_screen_engine_position)
        car.prepare_to_race_counter = -1

        if car.game_over:
            game_over_screen = True
            if car.score > high_scores["high_scores"][len(high_scores["high_scores"])-1]["score"]:
                car.enter_high_score = True
                car.high_score_name = "A"
                high_scores["high_scores"][len(high_scores["high_scores"])-1]["score"] = car.score
                high_scores["high_scores"][len(high_scores["high_scores"])-1]["name"] = car.high_score_name
                rank_found = False
                rank = len(high_scores["high_scores"])-1
                while rank_found == False:
                    if high_scores["high_scores"][rank-1]["score"]> car.score:
                        rank_found = True
                    else:
                        #Swap score table position
                        high_scores["high_scores"][rank]["score"] = high_scores["high_scores"][rank-1]["score"]
                        high_scores["high_scores"][rank-1]["score"] = car.score
                        high_scores["high_scores"][rank]["name"] = high_scores["high_scores"][rank-1]["name"]
                        high_scores["high_scores"][rank-1]["name"] = car.high_score_name
                        rank -= 1
                        if rank==0:
                            rank_found = True

                car.high_score_rank = rank+1
            for lap_time in car.best_laps:
                if lap_time[0] > 0 and lap_time[0]/1000 < best_laps["best_laps"][lap_time[1]-1]["time"]:
                    car.enter_best_lap = True
                    car.high_score_name = "A"
                    best_laps["best_laps"][lap_time[1]-1]["time"] = round(lap_time[0]/1000,1)
                    best_laps["best_laps"][lap_time[1]-1]["name"] = car.high_score_name

    pygame.display.update()
    countdown = pygame.time.get_ticks()
    while not screen_exit:
        game_display.blit(start_race_screen, (0, 0))
        engine_idle_counter +=1
        if engine_idle_counter > 2:
            engine_idle_counter = 0
            for car in cars:
                if not car.is_drone:
                    car.prepare_to_race_counter += 1

        time = pygame.time.get_ticks()
        if time - countdown >= 1000:
            seconds -= 1
            countdown = time
        print_start_race_text(seconds)
        for car in cars:
            game_display.blit(engine_idle[engine_idle_counter], car.start_screen_engine_position)
            if car.prepare_to_race_counter >0 and car.prepare_to_race_counter <= 11:
                game_display.blit(prepare_to_race[car.prepare_to_race_counter], car.start_screen_thumb_position)
            if not car.is_drone:
                if car.super_traction >0 or car.turbo_acceleration >0 or car.higher_top_speed >0:
                    cust_surf = small_font.render("CUSTOMIZED CAR INCLUDES", False, white_color)
                    level_string = ""
                    if car.super_traction >0:
                        level_string = level_string + "TRACTION {} ".format(car.super_traction)
                    if car.higher_top_speed >0:
                        level_string = level_string + "SPEED {} ".format(car.higher_top_speed)
                    if car.turbo_acceleration >0:
                        level_string = level_string + "TURBO {} ".format(car.turbo_acceleration)
                    level_surf = small_font.render(level_string, False, white_color)
                    game_display.blit(cust_surf,car.customization_string_position)
                    game_display.blit(level_surf,(car.customization_string_position[0], car.customization_string_position[1]+15))

        pygame.display.update()
        key_pressed = -1
        if seconds == 0:
            screen_exit = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                return pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                if event.key == pygame.K_SPACE:
                    screen_exit = True
                if event.key == pygame.K_ESCAPE:
                    screen_exit = True
                    return pygame.K_ESCAPE

        any_joystick_button_pressed(True)
        if key_pressed >= 0:
            accelerate_pressed(key_pressed,True)

        clock.tick(15)

    if game_over_screen:
        screen_exit = False
        countdown = pygame.time.get_ticks()
        while not screen_exit:
            game_display.blit(start_race_screen, (0, 0))
            print_game_over_text()
            engine_idle_counter +=1
            if engine_idle_counter > 2:
                engine_idle_counter = 0
            time = pygame.time.get_ticks()
            if engine_idle_counter == 0:
                for car in cars:
                    game_display.blit(engine_idle[engine_idle_counter], car.start_screen_engine_position)
                    if car.enter_best_lap or car.enter_high_score:
                        if car.current_initial <= 2:
                            #ignore countdown
                            countdown = time
                            #If car if keyboard controlled
                            if car.joystick is None:
                                if pygame.key.get_pressed()[car.left_key]:
                                    car.move_initial_character(True)

                                if pygame.key.get_pressed()[car.right_key]:
                                    car.move_initial_character(False)
                            else:
                                buttons = car.joystick.get_numbuttons()
                                button_pressed = False
                                for i in range(buttons):
                                    button = car.joystick.get_button(i)
                                    if button == 1:
                                        button_pressed = True

                                if button_pressed:
                                    car.validate_initial_character()

                                left_pressed = False
                                right_pressed = False
                                axes = car.joystick.get_numaxes()
                                for i in range(axes):
                                    axis = car.joystick.get_axis(i)
                                    #Ignoring any axis beyond the first 2 which should be analog stick X
                                    #Any axis beyond that is probably an analog shoulder button
                                    if i < 2:
                                        if axis < 0 and axis < -0.5:
                                            left_pressed = True
                                        if axis > 0 and axis > 0.5:
                                            right_pressed = True

                                hats = car.joystick.get_numhats()
                                for i in range(hats):
                                    hat = car.joystick.get_hat(i)
                                    if hat[0] == -1:
                                        left_pressed = True

                                    if hat[0] == 1:
                                        right_pressed = True

                                if left_pressed:
                                    car.move_initial_character(True)
                                else:
                                    if right_pressed:
                                        car.move_initial_character(False)
                for event in pygame.event.get():
                    for car in cars:
                        if car.enter_best_lap or car.enter_high_score:
                            if car.current_initial <= 2:
                                if event.type == pygame.KEYDOWN:
                                    #If car if keyboard controlled
                                    if car.joystick is None:
                                        if event.key == car.accelerate_key:
                                            car.validate_initial_character()
                                        if event.key == car.left_key:
                                            car.move_initial_character(True)
                                        if event.key == car.right_key:
                                            car.move_initial_character(False)
            pygame.display.update()
            clock.tick(15)
            if time - countdown >= 2000:
                screen_exit = True
                for car in cars:
                    if car.game_over:
                        if car.enter_high_score:
                            high_scores["high_scores"][car.high_score_rank-1]["name"] = car.high_score_name
                        if car.enter_best_lap:
                            for lap_time in car.best_laps:
                                if lap_time[0] > 0 and lap_time[0]/1000 <= best_laps["best_laps"][lap_time[1]-1]["time"]:
                                    best_laps["best_laps"][lap_time[1]-1]["name"] = car.high_score_name


                        car.reset_game_over()


        with open(".highscores.json","w") as high_scores_file:
            json.dump(high_scores, high_scores_file)

        with open(".bestlaps.json","w") as best_laps_file:
            json.dump(best_laps, best_laps_file)
    smp_manager.get_sample("prepare_to_race_music").stop(fadeout_ms=FADEOUT_DURATION)
    screen_fadeout()
    return pygame.K_SPACE

def display_race_podium_screen(track, mechanic_frames, ranking, composed_race_podium, crowd_background):

    #Animate Score Increases
    text_positions = [(359, 433, 135, 153, 171) , (192, 265, 239, 257, 275) , (503, 576, 239, 257, 275) , (155, 228, 337, 355, 373)]
    score_positions = [1000, 500, 250, 0]
    best_lap_scores = []
    avg_lap_scores = []
    avg_lap_times = []
    best_lap_times =  []
    best_lap_scores_surfs = []
    avg_lap_scores_surfs = []
    score_position_surfs = []

    for i in range(0, len(ranking)):
        #Pre-render lap times
        avg_lap_times.append(small_font.render('{:2.1f}'.format(cars[ranking[i]].average_lap/1000), False, black_color))
        best_lap_times.append(small_font.render('{:2.1f}'.format(cars[ranking[i]].best_lap/1000), False, black_color))
        #Pre_calculate and pre-render scores based on lap_times
        avg_lap_scores.append(track.get_score_from_laptime(cars[ranking[i]].average_lap))
        avg_lap_scores_surfs.append(small_font.render('{}'.format(avg_lap_scores[i]), False, black_color))
        best_lap_scores.append(track.get_score_from_laptime(cars[ranking[i]].best_lap))
        best_lap_scores_surfs.append(small_font.render('{}'.format(best_lap_scores[i]), False, black_color))
        score_position_surfs.append(small_font.render('{}'.format(score_positions[i]), False, black_color))
        skip_surf = small_font.render("PRESS SPACE TO SKIP", False, black_color)

    key_pressed = -1
    screen_exit = False

    for score in range(0,1010,10):
        game_display.blit(composed_race_podium, (0, 0))
        for i in range (0, len(ranking)):
            #Blit Lap times
            game_display.blit(avg_lap_times[i], (text_positions[i][0] - avg_lap_times[i].get_width(), text_positions[i][3]))
            game_display.blit(best_lap_times[i], (text_positions[i][0] - best_lap_times[i].get_width(), text_positions[i][4]))
            game_display.blit(skip_surf, ((600 - skip_surf.get_width())/2, 385))
            #Render main score
            if score < score_positions[i]:
                score_surf = small_font.render('{}'.format(score), False, black_color)
            else:
                score_surf = score_position_surfs[i]

            #Render Average lap score
            if score <= avg_lap_scores[i]:
                avg_score_surf = small_font.render('{}'.format(score), False, black_color)
            else:
                avg_score_surf = avg_lap_scores_surfs[i]

            #Render Best lap score
            if score <= best_lap_scores[i]:
                best_score_surf = small_font.render('{}'.format(score), False, black_color)
            else:
                best_score_surf = best_lap_scores_surfs[i]

            game_display.blit(score_surf, (text_positions[i][1] - score_surf.get_width(), text_positions[i][2]))
            game_display.blit(avg_score_surf, (text_positions[i][1] - avg_score_surf.get_width(), text_positions[i][3]))
            game_display.blit(best_score_surf, (text_positions[i][1] - best_score_surf.get_width(), text_positions[i][4]))
            draw_score(cars[ranking[i]], track)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                if event.key == pygame.K_SPACE:
                    screen_exit = True
                if event.key == pygame.K_ESCAPE:
                    screen_exit = True

        if screen_exit:
            break

        clock.tick(10)
    if not screen_exit:
        #Update Score on top screen
        for i in range(0, len(ranking)):
            #Pre_calculate and pre-render scores based on lap_times
            cars[ranking[i]].score += avg_lap_scores[i]
            cars[ranking[i]].score += best_lap_scores[i]
            cars[ranking[i]].score += score_positions[i]

        #Animate Crowd Flags - Wave Flags 12 times & Animate Mechanic
        wave_count = 0
        frame_count = 0
        mechanic_index = 0
        for waves in range (0, 11, 1):
            for index in range (0, len(crowd_flags), 1):
                game_display.blit(crowd_background, (0, 0))
                game_display.blit(race_podium_screen, (0,0))
                game_display.blit(crowd_flags[index], (0,0))
                game_display.blit(cars[ranking[0]].first_car, (0,0))
                game_display.blit(cars[ranking[1]].second_car, (0,0))
                game_display.blit(cars[ranking[2]].third_car, (0,0))
                game_display.blit(cars[ranking[3]].fourth_car, (0,0))
                game_display.blit(mechanic_frames[mechanic_index], (0,0))


                for i in range (0, len(ranking)):
                    #Blit Lap times & scores
                    game_display.blit(avg_lap_times[i], (text_positions[i][0] - avg_lap_times[i].get_width(), text_positions[i][3]))
                    game_display.blit(best_lap_times[i], (text_positions[i][0] - best_lap_times[i].get_width(), text_positions[i][4]))
                    game_display.blit(score_position_surfs[i], (text_positions[i][1] - score_position_surfs[i].get_width(), text_positions[i][2]))
                    game_display.blit(avg_lap_scores_surfs[i], (text_positions[i][1] - avg_lap_scores_surfs[i].get_width(), text_positions[i][3]))
                    game_display.blit(best_lap_scores_surfs[i], (text_positions[i][1] - best_lap_scores_surfs[i].get_width(), text_positions[i][4]))
                    draw_score(cars[ranking[i]], track)
                game_display.blit(skip_surf, ((600 - skip_surf.get_width())/2, 385))
                pygame.display.update()
                index += 1
                if index > len(crowd_flags)-1:
                    index = 0
                frame_count += 1
                if frame_count % 4 ==0:
                    mechanic_index += 1
                    if mechanic_index == len(mechanic_frames):
                        mechanic_index = 0
                        frame_count = 0
                clock.tick(18)
            wave_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                key_pressed = pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                if event.key == pygame.K_SPACE:
                    screen_exit = True
                if event.key == pygame.K_ESCAPE:
                    screen_exit = True
            if screen_exit:
                break
    if key_pressed==-1:
        return pygame.K_SPACE
    else:
        return key_pressed


def print_car_name_and_control_method(top_left, color, color_text, control_method, joy_name):
    color_surf = big_font.render(color_text, False, color)
    game_display.blit(color_surf, top_left)
    car_surf = big_font.render("CAR", False, color)
    game_display.blit(car_surf, (top_left[0] + (color_surf.get_width() - car_surf.get_width())/2, top_left[1] + 25))
    ctrl_method = small_font.render(control_method, False, white_color)
    game_display.blit(ctrl_method, (top_left[0] + (color_surf.get_width() - ctrl_method.get_width())/2, top_left[1] + 50))
    if len(joy_name)>10:
        joy_name = joy_name[0:10]
    joy__name_surf = small_font.render(joy_name, False, white_color)
    game_display.blit(joy__name_surf, (top_left[0] + (color_surf.get_width() - joy__name_surf.get_width())/2, top_left[1] + 65))

def print_options_text(conflict):
    game_display.blit(small_font.render("USE FUNCTION KEYS TO SELECT CONTROL FOR CARS", False, grey_color), (50, 345))
    game_display.blit(small_font.render("F2-BLUE CAR  F3-RED CAR  F4-YELLOW CAR  F5-GREEN CAR", False, white_color), (20, 365))
    exit_surf = small_font.render("F6-MAP KEYBOARD 1  F7-MAP KEYBOARD 2  F10-EXIT", False, white_color)
    game_display.blit(exit_surf, ((600 - exit_surf.get_width())/2, 385))
    if conflict:
        game_display.blit(small_font.render("YOU CANNOT HAVE THE SAME CONTROL METHOD FOR 2 CARS", False, white_color), (20, 215))

def print_redefine_keys(redefine_keys, control_name, key_already_used):
    key_def_surf = small_font.render("{} ACC-{} LEFT-{} RIGHT-{} ".format(control_methods[redefine_keys]['METHOD'], pygame.key.name(control_methods[redefine_keys]['ACCELERATE']), pygame.key.name(control_methods[redefine_keys]['LEFT']), pygame.key.name(control_methods[redefine_keys]['RIGHT'])), False, white_color)
    game_display.blit(key_def_surf, ((600 - key_def_surf.get_width())/2, 210))
    instruct_surf = small_font.render("F8-END MAP   PRESS {}".format(control_name), False, grey_color)
    game_display.blit(instruct_surf, ((600 - instruct_surf.get_width())/2, 225))
    if key_already_used:
        already_surf = small_font.render("KEY ALREADY USED", False, white_color)
        game_display.blit(already_surf, ((600 - already_surf.get_width())/2, 240))

def display_options():
    screen_exit = False
    engine_idle_counter = 0
    conflict = False
    #Add Green car
    screen_fadein(start_race_screen)
    for car in cars:
        game_display.blit(engine_idle[engine_idle_counter], car.start_screen_engine_position)
        print_car_name_and_control_method(car.start_screen_text_position, car.main_color, car.color_text, control_methods[car.control_method_index]['METHOD'], '')

    print_options_text(conflict)
    pygame.display.update()
    redefine_keys = -1
    key_already_used = False
    control_name = ''
    while not screen_exit:
        game_display.blit(start_race_screen, (0, 0))
        engine_idle_counter +=1
        if engine_idle_counter > 2:
            engine_idle_counter = 0
        for car in cars:
            game_display.blit(engine_idle[engine_idle_counter], car.start_screen_engine_position)
            joy_name = ''
            if car.control_method_index > 1:
                if pygame.joystick.get_count() > car.control_method_index - 2:
                    joy_name = pygame.joystick.Joystick(car.control_method_index - 2).get_name()
                else:
                    joy_name = "NOT DETECTED"
            print_car_name_and_control_method(car.start_screen_text_position, car.main_color, car.color_text, control_methods[car.control_method_index]['METHOD'], joy_name)
        if redefine_keys > -1:
            conflict = False
            print_redefine_keys(redefine_keys, control_name, key_already_used)
        print_options_text(conflict)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                conflict = False
                if event.key == pygame.K_F10:
                    for i in range(0,len(cars)):
                        for j in range(0,len(cars)):
                            if (not i == j) and (cars[i].control_method_index == cars[j].control_method_index):
                                conflict = True
                    if conflict == False:
                        screen_exit = True
                        for car in cars:
                            car.joystick = None
                            car.accelerate_key = None
                            car.left_key = None
                            car.right_key = None
                            if car.control_method_index < 2:
                                #Keyboard 1 or 2
                                car.accelerate_key = control_methods[car.control_method_index]['ACCELERATE']
                                car.left_key = control_methods[car.control_method_index]['LEFT']
                                car.right_key = control_methods[car.control_method_index]['RIGHT']
                            else:
                                if pygame.joystick.get_count() > car.control_method_index - 2:
                                    car.joystick = pygame.joystick.Joystick(car.control_method_index - 2)
                                    car.joystick.init()
                                else:
                                    car.is_drone = True
                                    car.speed_max = car.drone_speed
                                    car.bump_speed = car.drone_bump_speed


                if event.key == pygame.K_F2:
                    cars[0].control_method_index += 1
                    if cars[0].control_method_index >= len(control_methods):
                        cars[0].control_method_index = 0
                elif event.key == pygame.K_F3:
                    cars[3].control_method_index += 1
                    if cars[3].control_method_index >= len(control_methods):
                        cars[3].control_method_index = 0
                elif event.key == pygame.K_F4:
                    cars[2].control_method_index += 1
                    if cars[2].control_method_index >= len(control_methods):
                        cars[2].control_method_index = 0
                elif event.key == pygame.K_F5:
                    cars[1].control_method_index += 1
                    if cars[1].control_method_index >= len(control_methods):
                        cars[1].control_method_index = 0
                elif event.key == pygame.K_F6:
                    redefine_keys = 0
                    control_name = 'ACCELERATE'
                elif event.key == pygame.K_F7:
                    redefine_keys = 1
                    control_name = 'ACCELERATE'
                elif event.key == pygame.K_F8:
                    redefine_keys = -1
                    control_name = ''
                else:
                    if redefine_keys>-1 and len(control_name)>0:
                        key_already_used = False
                        for i in (0,1):
                            if control_methods[i]['ACCELERATE'] == event.key or control_methods[i]['LEFT'] == event.key or control_methods[i]['RIGHT'] == event.key:
                                key_already_used = True
                        if not key_already_used:
                            control_methods[redefine_keys][control_name] = event.key
                            if control_name == 'ACCELERATE':
                                control_name = 'LEFT'
                            elif control_name == 'LEFT':
                                control_name = 'RIGHT'
                            elif control_name == 'RIGHT':
                                control_name = 'ACCELERATE'
        clock.tick(15)
    screen_fadeout()

def display_track_selection():
    screen_exit = False
    track_index = 0
    track_selection_background = checkered_background
    screen_fadein(track_selection_background)
    master_car_index = 0
    for i in range(len(cars)):
        if not cars[i].is_drone:
            master_car_index = i
            break
    car = cars[master_car_index]
    smp_manager.get_sample("track_select_music").play()

    while not screen_exit:
        if track_index<0:
            track_index = len(tracks)-1
        elif track_index>=len(tracks):
            track_index = 0
        track = tracks[track_index]
        game_display.blit(track_selection_background, (0, 0))

        print_start_race_text("")
        game_display.blit(track.thumbnail,(185,115))
        game_display.blit(big_shadow_font.render("SELECT TRACK", False, black_color), (218,90))
        game_display.blit(big_font.render("SELECT TRACK", False, car.main_color), (218,90))

        wrenches = ""
        if track.wrenches>0:
            wrenches = "- {} WRENCHES".format(track.wrenches)
        surf = small_font.render("TRACK {} - {} {}".format(track.track_number,track.difficulty_level,wrenches), False, car.main_color)
        shadow_surf = shadow_font.render("TRACK {} - {} {}".format(track.track_number,track.difficulty_level,wrenches), False, black_color)
        game_display.blit(shadow_surf, (round((display_width-surf.get_width())/2),290))
        game_display.blit(surf, (round((display_width-surf.get_width())/2),290))

        pygame.display.update()

        key_pressed = -1
        left_pressed = False
        right_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                return pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                if event.key == pygame.K_ESCAPE:
                    screen_exit = True
                    return pygame.K_ESCAPE
                if event.key == car.left_key:
                    left_pressed = True
                if event.key == car.right_key:
                    right_pressed = True

        if not car.joystick is None:
            axes = car.joystick.get_numaxes()
            for i in range(axes):
                axis = car.joystick.get_axis(i)
                #Ignoring any axis beyond the first 2 which should be analog stick X
                #Any axis beyond that is probably an analog shoulder button
                if i < 2:
                    if axis < 0 and axis < -0.5:
                        left_pressed = True
                    if axis > 0 and axis > 0.5:
                        right_pressed = True

            hats = car.joystick.get_numhats()
            for i in range(hats):
                hat = car.joystick.get_hat(i)
                if hat[0] == -1:
                    left_pressed = True

                if hat[0] == 1:
                    right_pressed = True

        if left_pressed:
            track_index-=1
        else:
            if right_pressed:
                track_index+=1

        #If other cars than the master press accelerate register game started
        any_joystick_button_pressed()
        if key_pressed >= 0:
            accelerate_pressed(key_pressed)

        #If the First car that pushed accelerate to start a new game (i.e; Master car) presses accelerate, the Track is selected
        if key_pressed == cars[master_car_index].accelerate_key:
            screen_exit = True

        if not cars[master_car_index].joystick is None:
            joy = cars[master_car_index].joystick
            buttons = joy.get_numbuttons()
            for j in range(buttons):
                button = joy.get_button(j)
                if button == 1:
                    screen_exit = True

        clock.tick(15)
    smp_manager.get_sample("track_select_music").stop(fadeout_ms=FADEOUT_DURATION)
    screen_fadeout()
    return track_index


def display_car_item_selection(car:pysprint_car.Car):
    screen_exit = False
    selected_item = 3
    item_frame_positions = [(12,127),(12,253),(334,253),(334,127)]
    selection_wheel_angles = [90,180,270,0]
    wheel_angle = selection_wheel_angles[selected_item]
    white_background = pygame.Surface((display_width,display_height))
    white_background.fill(white_color)

    selected_item_background = pygame.Surface((294,106))
    selected_item_background.fill(car.main_color)

    car_item_background = pygame.Surface((display_width,display_height))
    car_item_background.blit(white_background,(0,0))
    car_item_background.blit(item_screen,(0,0))

    surf_numbers = {
        1:small_font.render("1", False, white_color),
        2:small_font.render("2", False, white_color),
        3:small_font.render("3", False, white_color),
        4:small_font.render("4", False, white_color),
        5:small_font.render("5", False, white_color)
    }

    surf_selected_numbers = {
        1:small_font.render("1", False, car.main_color),
        2:small_font.render("2", False, car.main_color),
        3:small_font.render("3", False, car.main_color),
        4:small_font.render("4", False, car.main_color),
        5:small_font.render("5", False, car.main_color)
    }

    screen_fadein(car_item_background)
    blink_timer = pygame.time.get_ticks()
    flash_selection = True
    selection_confirmed = False
    grant_item_counter = -1
    grant_item_timer = -1
    smp_manager.get_sample("track_select_music").play()
    while not screen_exit:
        car_item_background.blit(white_background,(0,0))

        if pygame.time.get_ticks()-blink_timer>=200:
            flash_selection = not flash_selection
        if flash_selection:
            car_item_background.blit(selected_item_background,item_frame_positions[selected_item])

        if car.higher_top_speed==5:
            car_item_background.blit(selected_item_background,item_frame_positions[3])
        if car.super_traction==5:
            car_item_background.blit(selected_item_background,item_frame_positions[0])
        if car.turbo_acceleration==5:
            car_item_background.blit(selected_item_background,item_frame_positions[1])

        if selection_confirmed:
            car_item_background.blit(selected_item_background,item_frame_positions[selected_item])

        car_item_background.blit(item_screen,(0,0))

        game_display.blit(car_item_background, (0, 0))
        if abs(wheel_angle - selection_wheel_angles[selected_item])>=270:
            if abs(wheel_angle - selection_wheel_angles[selected_item])<350:
                wheel_angle -= 10 * (selection_wheel_angles[selected_item]-wheel_angle)/abs(selection_wheel_angles[selected_item]-wheel_angle)
            else:
                wheel_angle = selection_wheel_angles[selected_item]
        else:
            if abs(wheel_angle - selection_wheel_angles[selected_item])>10:
                wheel_angle += 10 * (selection_wheel_angles[selected_item]-wheel_angle)/abs(selection_wheel_angles[selected_item]-wheel_angle)
            else:
                wheel_angle = selection_wheel_angles[selected_item]

        originPos = (car.selection_wheel.get_width()/2, car.selection_wheel.get_height()/2)
        pos = (278 + car.selection_wheel.get_width()/2, 203 + car.selection_wheel.get_height()/2)

        # offset from pivot to center
        image_rect = car.selection_wheel.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-wheel_angle)

        # roatetd image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(car.selection_wheel, wheel_angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        # rotate and blit the image
        game_display.blit(rotated_image, rotated_image_rect)

        if selection_confirmed:
            if grant_item_counter==0:
                grant_item_timer = pygame.time.get_ticks()
                grant_item_counter+=1
            else:
                if pygame.time.get_ticks()-grant_item_timer>=395:
                    if grant_item_counter==1:
                        smp_manager.get_sample("item_choice").play()
                    grant_item_counter+=1
                    grant_item_timer = pygame.time.get_ticks()
                    if grant_item_counter>=1:
                        car.wrench_count-=1
                        if selected_item==2:
                            car.score+=1000
            if grant_item_counter>4:
                screen_exit = True

        surf = big_font.render("{} CAR".format(car.color_text), False, car.main_color)
        shadow_surf = big_shadow_font.render("{} CAR".format(car.color_text), False, black_color)
        game_display.blit(shadow_surf, (round((display_width-surf.get_width())/2),65))
        game_display.blit(surf, (round((display_width-surf.get_width())/2),65))

        surf  = big_font.render("SELECT AN ITEM FOR YOUR CAR", False, car.main_color)
        shadow_surf  = big_shadow_font.render("SELECT AN ITEM FOR YOUR CAR", False, black_color)
        game_display.blit(shadow_surf, (round((display_width-surf.get_width())/2),90))
        game_display.blit(surf, (round((display_width-surf.get_width())/2),90))

        surf  = big_font.render("SUPER", False, white_color)
        shadow_surf  = big_shadow_font.render("SUPER", False, black_color)
        game_display.blit(shadow_surf, (30,148))
        game_display.blit(surf, (30,148))
        surf  = big_font.render("TRACTION", False, white_color)
        shadow_surf  = big_shadow_font.render("TRACTION", False, black_color)
        game_display.blit(shadow_surf, (30,173))
        game_display.blit(surf, (30,173))

        for i in range (1,6):
            if car.super_traction>=i:
                game_display.blit(surf_selected_numbers[i],(100 + 23*i,210))
            else:
                game_display.blit(surf_numbers[i],(100 + 23 * i,210))



        surf  = big_font.render("TURBO", False, white_color)
        shadow_surf  = big_shadow_font.render("TURBO", False, black_color)
        game_display.blit(shadow_surf, (30,274))
        game_display.blit(surf, (30,274))
        surf  = big_font.render("ACCELERATION", False, white_color)
        shadow_surf  = big_shadow_font.render("ACCELERATION", False, black_color)
        game_display.blit(shadow_surf, (30,299))
        game_display.blit(surf, (30,299))

        for i in range (1,6):
            if car.turbo_acceleration>=i:
                game_display.blit(surf_selected_numbers[i],(100 + 23*i,336))
            else:
                game_display.blit(surf_numbers[i],(100 + 23 * i,336))


        surf  = big_font.render("HIGHER", False, white_color)
        shadow_surf  = big_shadow_font.render("HIGHER", False, black_color)
        game_display.blit(shadow_surf, (412,148))
        game_display.blit(surf, (412,148))
        surf  = big_font.render("TOP SPEED", False, white_color)
        shadow_surf  = big_shadow_font.render("TOP SPEED", False, black_color)
        game_display.blit(shadow_surf, (412,173))
        game_display.blit(surf, (412,173))

        for i in range (1,6):
            if car.higher_top_speed>=i:
                game_display.blit(surf_selected_numbers[i],(485 + 23*i,210))
            else:
                game_display.blit(surf_numbers[i],(485 + 23 * i,210))


        surf  = big_font.render("INCREASE", False, white_color)
        shadow_surf  = big_shadow_font.render("INCREASE", False, black_color)
        game_display.blit(shadow_surf, (412,274))
        game_display.blit(surf, (412,274))
        surf  = big_font.render("SCORE", False, white_color)
        shadow_surf  = big_shadow_font.render("SCORE", False, black_color)
        game_display.blit(shadow_surf, (412,299))
        game_display.blit(surf, (412,299))

        surf  = small_font.render("LEVEL", False, white_color)
        game_display.blit(surf, (27,210))
        game_display.blit(surf, (27,336))
        game_display.blit(surf, (412,210))
        draw_score(car,None)



        pygame.display.update()

        key_pressed = -1
        left_pressed = False
        right_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen_exit = True
                return pygame.K_ESCAPE
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
                if event.key == pygame.K_ESCAPE:
                    screen_exit = True
                    return pygame.K_ESCAPE
                if event.key == car.left_key:
                    left_pressed = True
                if event.key == car.right_key:
                    right_pressed = True
        if not selection_confirmed:
            if not car.joystick is None:
                axes = car.joystick.get_numaxes()
                for i in range(axes):
                    axis = car.joystick.get_axis(i)
                    #Ignoring any axis beyond the first 2 which should be analog stick X
                    #Any axis beyond that is probably an analog shoulder button
                    if i < 2:
                        if axis < 0 and axis < -0.5:
                            left_pressed = True
                        if axis > 0 and axis > 0.5:
                            right_pressed = True

                hats = car.joystick.get_numhats()
                for i in range(hats):
                    hat = car.joystick.get_hat(i)
                    if hat[0] == -1:
                        left_pressed = True

                    if hat[0] == 1:
                        right_pressed = True

            if left_pressed:
                selected_item+=1
            else:
                if right_pressed:
                    selected_item-=1
            if selected_item >3:
                selected_item = 0
            if selected_item <0:
                selected_item = 3
            #If the First car that pushed accelerate to start a new game (i.e; Master car) presses accelerate, the Track is selected
            if key_pressed == car.accelerate_key:
                selection_confirmed = True
                smp_manager.get_sample("track_select_music").stop(fadeout_ms=FADEOUT_DURATION)

            if not car.joystick is None:
                joy = car.joystick
                buttons = joy.get_numbuttons()
                for j in range(buttons):
                    button = joy.get_button(j)
                    if button == 1:
                        selection_confirmed = True
            if selection_confirmed:
                grant_item_counter = 0
                if selected_item ==0:
                    if car.super_traction<5:
                        car.super_traction+=1
                if selected_item ==1:
                    if car.turbo_acceleration<5:
                        car.turbo_acceleration+=1
                if selected_item ==3:
                    if car.higher_top_speed<5:
                        car.higher_top_speed+=1
        clock.tick(15)
    screen_fadeout()


def draw_score(car: pysprint_car.Car, track: pysprint_tracks.Track):
    if not track is None:
        track.update_score_from_position(car)
    #Car
    if car.is_drone:
        score_surf = small_font.render("DRONE", False, car.main_color)
        shadow_score_surf = shadow_font.render("DRONE", False, black_color)
    else:
        score_surf = small_font.render("CAR", False, car.main_color)
        shadow_score_surf = shadow_font.render("CAR", False, black_color)
        #Wrenches
        game_display.blit(pysprint_tracks.wrench_image, (car.score_top_left[0] + 50,car.score_top_left[1]))
        wrench_index = car.wrench_count
        if car.wrench_count > 9:
            wrench_index = 9
        game_display.blit(wrench_count_sprites[wrench_index], (car.score_top_left[0] + 80,car.score_top_left[1]))

    game_display.blit(shadow_score_surf, car.score_top_left)
    game_display.blit(score_surf, car.score_top_left)
    #Lap
    score_surf = small_font.render("LAP", False, car.main_color)
    shadow_score_surf = shadow_font.render("LAP", False, black_color)
    game_display.blit(shadow_score_surf, (car.score_top_left[0] + 98, car.score_top_left[1]))
    game_display.blit(score_surf, (car.score_top_left[0] + 98, car.score_top_left[1]))
    #Score
    score_surf = big_font.render("{}".format(car.score), False, car.main_color)
    shadow_score_surf = big_shadow_font.render("{}".format(car.score), False, black_color)
    game_display.blit(shadow_score_surf, (car.score_top_left[0] , car.score_top_left[1]+15))
    game_display.blit(score_surf, (car.score_top_left[0] , car.score_top_left[1]+15))
    #Lap_COUNT
    score_surf = big_font.render("{}".format(car.lap_count), False, car.main_color)
    shadow_score_surf = big_shadow_font.render("{}".format(car.lap_count), False, black_color)
    game_display.blit(shadow_score_surf, (car.score_top_left[0] + 111, car.score_top_left[1] + 15))
    game_display.blit(score_surf, (car.score_top_left[0] + 111, car.score_top_left[1] + 15))




def trace_frame_time(trace_event, frame_start):
    if DEBUG_FPS_DETAILED:
        print('{} - Duration: {}'.format(trace_event, pygame.time.get_ticks() - frame_start))

def accelerate_pressed(key_pressed, play_sound = False):
    if key_pressed == JOYSTICK_BUTTON_PRESSED:
        return True
    for car in cars:
        if not car.accelerate_key is None:
            if key_pressed == car.accelerate_key:
                if not car.is_drone and not car.game_over:
                    return True
                car.start_game(play_sound)
                return True
    return False

def any_joystick_button_pressed(play_sound = False):
    button_pressed = False
    for car in cars:
        if not car.joystick is None:
            joy = car.joystick
            buttons = joy.get_numbuttons()
            for j in range(buttons):
                button = joy.get_button(j)
                if button == 1:
                    button_pressed = True
                    if not car.is_drone and not car.game_over:
                        return True
                    car.start_game(play_sound)
    return button_pressed


def get_progress(car):
    return car.lap_count * 1000 + car.progress_gate

def initialize_cars():
    for i in range(0,4):
        car = pysprint_car.Car()
        car.sprites_masks = car_sprites_masks
        cars.append(car)

    #Initiate Cars as Drones.
    pysprint_car.dust_cloud_frames = dust_cloud_frames
    pysprint_car.explosion_frames = explosion_frames

    cars[0].helicopter_frames = blue_helicopter_frames
    cars[1].helicopter_frames = green_helicopter_frames
    cars[2].helicopter_frames = yellow_helicopter_frames
    cars[3].helicopter_frames = red_helicopter_frames

    cars[0].vertical_helicopter_frames = blue_vertical_helicopter_frames
    cars[1].vertical_helicopter_frames = green_vertical_helicopter_frames
    cars[2].vertical_helicopter_frames = yellow_vertical_helicopter_frames
    cars[3].vertical_helicopter_frames = red_vertical_helicopter_frames

    cars[0].start_screen_engine_position = blue_engine
    cars[1].start_screen_engine_position = green_engine
    cars[2].start_screen_engine_position = yellow_engine
    cars[3].start_screen_engine_position = red_engine

    cars[0].customization_string_position = blue_customization
    cars[1].customization_string_position = green_customization
    cars[2].customization_string_position = yellow_customization
    cars[3].customization_string_position = red_customization

    cars[0].selection_wheel = blue_selection_wheel
    cars[1].selection_wheel = green_selection_wheel
    cars[2].selection_wheel = yellow_selection_wheel
    cars[3].selection_wheel = red_selection_wheel

    cars[0].start_screen_thumb_position = blue_thumb
    cars[1].start_screen_thumb_position = green_thumb
    cars[2].start_screen_thumb_position = yellow_thumb
    cars[3].start_screen_thumb_position = red_thumb

    cars[0].start_screen_text_position = press_start_blue
    cars[1].start_screen_text_position = press_start_green
    cars[2].start_screen_text_position = press_start_yellow
    cars[3].start_screen_text_position = press_start_red

    cars[0].score_top_left = score_top_left_blue
    cars[1].score_top_left = score_top_left_green
    cars[2].score_top_left = score_top_left_yellow
    cars[3].score_top_left = score_top_left_red

    cars[0].main_color = blue_color
    cars[1].main_color = green_color
    cars[2].main_color = yellow_color
    cars[3].main_color = red_color

    cars[0].color_text = "BLUE"
    cars[1].color_text = "GREEN"
    cars[2].color_text = "YELLOW"
    cars[3].color_text = "RED"

    #Initialize Default Controls
    #Default for Blue Car is keyboard
    cars[0].accelerate_key = keyboard_1['ACCELERATE']
    cars[0].left_key = keyboard_1['LEFT']
    cars[0].right_key = keyboard_1['RIGHT']
    cars[0].control_method_text = keyboard_1['METHOD']
    cars[0].control_method_index = 0

    #Default for Green Car is keyboard
    cars[1].accelerate_key = keyboard_2['ACCELERATE']
    cars[1].left_key = keyboard_2['LEFT']
    cars[1].right_key = keyboard_2['RIGHT']
    cars[1].control_method_index = 1

    #Default for Yellow Car is Joystick 1 if detected.
    cars[2].control_method_index = 2
    if pygame.joystick.get_count() > 0:
        cars[2].joystick = pygame.joystick.Joystick(0)
        cars[2].joystick.init()

    #Default for Red Car is Joystick 2 if detected
    cars[3].control_method_index = 3
    if pygame.joystick.get_count() > 1:
        cars[3].joystick = pygame.joystick.Joystick(1)
        cars[3].joystick.init()

def activate_cars():
    nb_drones = []

    for car in cars:
        car.lap_count = 0
        if car.is_drone:
            nb_drones.append(0)
        car.lap_times.clear()
        for i in range(0, race_laps):
            car.lap_times.append(0)
    if len(nb_drones)>=1:
        #Assign slightly different AI characteristics to each drone when more than 1 is in play
        personalities = [0,1,2]
        if len(nb_drones)<4:
            for car in cars:
                if car.is_drone:
                    unmodified = True
                    while unmodified:
                        i = random.randint(0,len(car.drone_personalities)-1)
                        if personalities[i]>=0:
                            car.drone_personality = i
                            if DEBUG_AI:
                                print('{} Drone Personality : {}'.format(car.color_text, car.drone_personalities[car.drone_personality][0]))
                            car.speed_max = car.drone_speed * car.drone_personality_modifiers[i]
                            car.bump_speed = car.drone_bump_speed * car.drone_personality_modifiers[i]
                            car.rotation_step = car.drone_rotation_step * car.drone__invert_personality_modifiers[i]
                            car.acceleration_step = car.drone_acceleration_step * car.drone_personality_modifiers[i]
                            car.deceleration_step = car.drone_deceleration_step * car.drone__invert_personality_modifiers[i]
                            car.bump_decelaration_step = car.drone_bump_speed * car.drone__invert_personality_modifiers[i]
                            car.turning_angle_threshold = car.turning_angle_threshold * car.drone_personality_modifiers[i]
                            car.skidding_weight = car.drone_skidding_weight
                            car.crash_certainty_treshold += 5
                            personalities[i]=-1
                            unmodified = False

    if cars[0].is_drone:
        cars[0].sprites = blue_drone_sprites
        cars[0].first_car = first_car_blue_drone
        cars[0].second_car = second_car_blue_drone
        cars[0].third_car = third_car_blue_drone
        cars[0].fourth_car = fourth_car_blue_drone
    else:
        cars[0].sprites = blue_car_sprites
        cars[0].first_car = first_car_blue
        cars[0].second_car = second_car_blue
        cars[0].third_car = third_car_blue
        cars[0].fourth_car = fourth_car_blue

    if cars[1].is_drone:
        cars[1].sprites = green_drone_sprites
        cars[1].first_car = first_car_green_drone
        cars[1].second_car = second_car_green_drone
        cars[1].third_car = third_car_green_drone
        cars[1].fourth_car = fourth_car_green_drone
    else:
        cars[1].sprites = green_car_sprites
        cars[1].first_car = first_car_green
        cars[1].second_car = second_car_green
        cars[1].third_car = third_car_green
        cars[1].fourth_car = fourth_car_green

    if cars[2].is_drone:
        cars[2].sprites = yellow_drone_sprites
        cars[2].first_car = first_car_yellow_drone
        cars[2].second_car = second_car_yellow_drone
        cars[2].third_car = third_car_yellow_drone
        cars[2].fourth_car = fourth_car_yellow_drone
    else:
        cars[2].sprites = yellow_car_sprites
        cars[2].first_car = first_car_yellow
        cars[2].second_car = second_car_yellow
        cars[2].third_car = third_car_yellow
        cars[2].fourth_car = fourth_car_yellow

    if cars[3].is_drone:
        cars[3].sprites = red_drone_sprites
        cars[3].first_car = first_car_red_drone
        cars[3].second_car = second_car_red_drone
        cars[3].third_car = third_car_red_drone
        cars[3].fourth_car = fourth_car_red_drone
    else:
        cars[3].sprites = red_car_sprites
        cars[3].first_car = first_car_red
        cars[3].second_car = second_car_red
        cars[3].third_car = third_car_red
        cars[3].fourth_car = fourth_car_red
    return len(nb_drones)



def init_track(filename):

    track = pysprint_tracks.Track()

    #TODO: validate json with jsonschema 
    track.load_track_definition(filename)
    track.background = pygame.image.load(track.background_filename)

    if not track.thumbnail_filename is None:
        track.thumbnail = pygame.image.load(track.thumbnail_filename)
    track.base_mask = pygame.image.load(track.track_mask_filename).convert_alpha()
    
    if not track.track_upper_mask_filename is None:
        track.track_upper_mask = pygame.image.load(track.track_upper_mask_filename).convert_alpha()
        track.track_upper_mask_mask =  pygame.mask.from_surface(track.track_upper_mask, 50)
    track.track_overlay = pygame.image.load(track.overlay_filename).convert_alpha()
    track.finish_line = pygame.Rect(track.finish_line_rect[0], track.finish_line_rect[1], track.finish_line_rect[2], track.finish_line_rect[3])
    
    logger.debug(f"Adding track {track.track_number} to the track list")
    tracks[track.track_number-1] = track

def initialize_tracks():

        p = Path(r'Assets/tracks').glob('**/*.json')
        for track in [x for x in p if x.is_file()]:
            init_track(track)

def check_option_key_pressed(key_pressed,scaled_screen):
    if (key_pressed == pygame.K_F1):
        display_options()
        return scaled_screen
    if (key_pressed == pygame.K_F4):
        try:
            if scaled_screen:
                game_display = pygame.display.set_mode((display_width, display_height), 0)
                return False
            else:
                game_display = pygame.display.set_mode((display_width, display_height), pygame.SCALED)
                return True
        except:
            print("Could not Scale Window - probably an old version of pygame Library < 2.0.0")

def game_loop():

    game_exit = False
    race_finished = False
    scaled_screen = False
    print('{} - Joystick(s) detected'.format(pygame.joystick.get_count()))

    for i in range (pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        print ('{}'.format(joy.get_name()))

    initialize_tracks()
    initialize_cars()
    track_index = 0
    next_track = [2,4,6,0,7,1,5,3]

    mechanic_frames_list = [hammer_frames, saw_frames, head_scratch_frames, blow_frames]
    mechanic_index = random.randint(0,3)

    while not game_exit:
        key_pressed = -1
        if not race_finished:
            track_index = 0
            race_counter = 0
            key_pressed = display_loading_screen(False)
            #Attract mode
            while not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                key_pressed = display_splash_screen()
                scaled_screen = check_option_key_pressed(key_pressed,scaled_screen)
                if not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                    key_pressed = display_high_scores()
                scaled_screen = check_option_key_pressed(key_pressed,scaled_screen)
                if not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                    key_pressed = display_lap_records()
                scaled_screen = check_option_key_pressed(key_pressed,scaled_screen)
                if not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                    key_pressed = display_credits_screen()
                scaled_screen = check_option_key_pressed(key_pressed,scaled_screen)
        if accelerate_pressed(key_pressed) or race_finished:
            #Initiate Race
            if race_counter == 0:
                track_index = display_track_selection()
                for car in cars:
                    if not car.is_drone:
                        car.wrench_count = tracks[track_index].wrenches
            for car in cars:
                if not car.is_drone:
                    while car.wrench_count>=4:
                        display_car_item_selection(car)
            if not key_pressed == pygame.K_ESCAPE:
                key_pressed = display_start_race_screen()
            if not key_pressed == pygame.K_ESCAPE:
                race_finished = False
                nb_drones = activate_cars()
                if nb_drones < 4:
                    track = tracks[track_index]
                    track_index = next_track[track_index]
                    race_counter += 1
                    if track_index>= len(tracks):
                        track_index = 0

                    screen_fadein(track.background)

                    #Align Cars on Start Line
                    for i in range (0,4):
                        cars[i].x_position = track.first_car_start_position[0]
                        cars[i].y_position = track.first_car_start_position[1] + i * 15
                        cars[i].sprite_angle = track.start_sprite_angle
                        cars[i].angle = track.start_sprite_angle
                        cars[i].reset_racing_status(race_counter)

                    race_start = True
                    last_lap = False
                    race_finish = False
                    animation_index = 0
                    flag_waves = 0
                    wave_up = True
                    flag_waved = False
                    podium_displayed = False
                    #Generate Obstacles and traps
                    track.init_obstacles(race_counter)

                    get_ready_time  = pygame.time.get_ticks()
                    smp_manager.get_sample("get_ready").play()
                    while pygame.time.get_ticks() - get_ready_time < 1500:
                        track.blit_background(False)
                        track.blit_obstacles(False)
                        track.blit_bonus(False)
                        track.blit_wrench(False)
                        for car in cars:
                            car.blit(track, False)
                        track.blit_overlay(False)
                        track.blit_obstacles(True)
                        track.blit_bonus(True)
                        track.blit_wrench(True)
                        for car in cars:
                            car.blit(track, True)
                        print_get_ready()
                        pygame.display.update()


                    race_start_time = pygame.time.get_ticks()
                    avg_fps = []
                    fps_refresh_time = race_start_time
                    fps_surf = small_font.render(" FPS", False, white_color)
                    for car in cars:
                        car.current_lap_start = race_start_time
                    pygame.time.set_timer(GREENFLAG, 40)
                    while not podium_displayed:
                        frame_start = pygame.time.get_ticks()
                        trace_frame_time("Frame start", frame_start)
                        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                            game_exit = True
                            podium_displayed = True
                        else:
                            for car in cars:
                                if car.bumping or car.spinning or race_finish or car.jumping:
                                    car.ignore_controls = True
                                if not car.ignore_controls:
                                    if car.is_drone:
                                        if not DISABLE_DRONES:
                                            car.ai_drive(track)
                                    else:
                                        #If car if keyboard controlled
                                        if car.joystick is None:
                                            if pygame.key.get_pressed()[car.accelerate_key]:
                                                car.accelerate()
                                            else:
                                                car.decelerate()

                                            if pygame.key.get_pressed()[car.left_key]:
                                                car.rotate(True,track)

                                            if pygame.key.get_pressed()[car.right_key]:
                                                car.rotate(False,track)
                                        else:
                                            buttons = car.joystick.get_numbuttons()
                                            button_pressed = False
                                            for i in range(buttons):
                                                button = car.joystick.get_button(i)
                                                if button == 1:
                                                    button_pressed = True

                                            if button_pressed:
                                                car.accelerate()
                                            else:
                                                car.decelerate()

                                            left_pressed = False
                                            right_pressed = False
                                            axes = car.joystick.get_numaxes()
                                            for i in range(axes):
                                                axis = car.joystick.get_axis(i)
                                                #Ignoring any axis beyond the first 2 which should be analog stick X
                                                #Any axis beyond that is probably an analog shoulder button
                                                if i < 2:
                                                    if axis < 0 and axis < -0.5:
                                                        left_pressed = True
                                                    if axis > 0 and axis > 0.5:
                                                        right_pressed = True

                                            hats = car.joystick.get_numhats()
                                            for i in range(hats):
                                                hat = car.joystick.get_hat(i)
                                                if hat[0] == -1:
                                                    left_pressed = True

                                                if hat[0] == 1:
                                                    right_pressed = True

                                            if left_pressed:
                                                car.rotate(True,track)
                                            else:
                                                if right_pressed:
                                                    car.rotate(False,track)
                                else:
                                    if not car.jumping:
                                        car.decelerate()
                            trace_frame_time("Checked Key input", frame_start)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT: # If user clicked close.
                                    game_exit = True
                                    podium_displayed = True
                                for car in cars:
                                    if not car.ignore_controls:
                                        if car.is_drone:
                                            if not DISABLE_DRONES:
                                                car.ai_drive(track)
                                        else:
                                            if event.type == pygame.KEYDOWN:
                                                #If car if keyboard controlled
                                                if car.joystick is None:
                                                    if event.key == car.accelerate_key:
                                                        car.accelerate()
                                                    if event.key == car.left_key:
                                                        car.rotate(True, track)
                                                    if event.key == car.right_key:
                                                        car.rotate(False, track)
                                    else:
                                        if not car.jumping:
                                            car.decelerate()
                                #Draw Green Flag at Race Start
                                if event.type == GREENFLAG:
                                    if DEBUG_FLAG:
                                        print('{} - Green Flag Timer triggerred'.format(pygame.time.get_ticks()))
                                    if wave_up:
                                        animation_index += 1
                                    else:
                                        animation_index -= 1
                                    if animation_index >= len(green_flag_frames):
                                        animation_index -= 1
                                        flag_waves += 1
                                        wave_up = False

                                    if animation_index < 0:
                                        animation_index += 1
                                        wave_up = True

                                    if flag_waves > 5:
                                        race_start = False
                                        pygame.time.set_timer(GREENFLAG, 00)

                                #Draw White Flag for Last lap
                                if event.type == WHITEFLAG:
                                    if DEBUG_FLAG:
                                        print('{} - White Flag Timer triggerred'.format(pygame.time.get_ticks()))
                                    if wave_up:
                                        animation_index += 1
                                    else:
                                        animation_index -= 1
                                    if animation_index >= len(white_flag_frames):
                                        animation_index -= 1
                                        flag_waves += 1
                                        wave_up = False

                                    if animation_index < 0:
                                        animation_index += 1
                                        wave_up = True

                                    if flag_waves > 5:
                                        flag_waved = True
                                        pygame.time.set_timer(WHITEFLAG, 00)

                                #Draw Checkered Flag
                                if event.type == CHECKEREDFLAG:
                                    if DEBUG_FLAG:
                                        print('{} - Checkered Flag Timer triggerred'.format(pygame.time.get_ticks()))
                                    if wave_up:
                                        animation_index += 1
                                    else:
                                        animation_index -= 1
                                    if animation_index >= len(checkered_flag_frames):
                                        animation_index -= 1
                                        flag_waves += 1
                                        wave_up = False

                                    if animation_index < 0:
                                        animation_index += 1
                                        wave_up = True

                                    if flag_waves > 5:
                                        flag_waved = True
                                        pygame.time.set_timer(CHECKEREDFLAG, 00)

                            #Check animation timers for spins, crashes and bumps
                            current_ticks = pygame.time.get_ticks()
                            for car in cars:
                                #Spin the car
                                if car.spinning and (current_ticks - car.collision_time) >= car.bump_animation_timer:
                                    if DEBUG_BUMP:
                                        print('{} - Spin Timer triggerred'.format(current_ticks))
                                    car.display_spinning()
                                    car.collision_time = current_ticks
                                #Draw Dust Cloud
                                if (car.bumping or car.touch_down) and (current_ticks - car.collision_time) >= car.bump_animation_timer:
                                    if DEBUG_BUMP:
                                        print('{} - Bump Timer triggerred'.format(current_ticks))
                                    car.display_bump_cloud()
                                    car.collision_time = current_ticks
                                #Draw Explosion
                                if car.crashing and (current_ticks - car.collision_time) >= car.crash_animation_timer:
                                    if DEBUG_CRASH:
                                        print('{} - Crash Timer triggerred'.format(current_ticks))
                                    car.display_explosion()
                                    car.collision_time = current_ticks

                            trace_frame_time("Managed all Events & Timers", frame_start)

                            for car in cars:
                                if DISABLE_DRONES:
                                    if not car.is_drone:
                                        car.draw(track,cars)
                                else:
                                    car.draw(track,cars)
                                trace_frame_time("Drawn car", frame_start)
                            if not race_finish and not race_start:
                                for car in cars:
                                    race_finish = car.test_finish_line(track)
                                    if race_finish == True:
                                        break
                                #Draw Checkered Flag and finish race
                                if race_finish:
                                    smp_manager.get_sample("end_race").play()
                                    animation_index = 0
                                    flag_waves = 0
                                    flag_waved = False
                                    wave_up = True
                                    for car in cars:
                                        car.speed = 0
                                    pygame.time.set_timer(CHECKEREDFLAG, 40)


                            for car in cars:
                                #Draw White Flag for Last lap
                                if not last_lap and car.lap_count == race_laps -1:
                                    smp_manager.get_sample("last_lap").play()
                                    animation_index = 0
                                    flag_waves = 0
                                    wave_up = True
                                    last_lap = True
                                    pygame.time.set_timer(WHITEFLAG, 40)
                                    break

                            trace_frame_time("Test Finish ", frame_start)
                            track.blit_background(True)
                            track.blit_obstacles(True)
                            track.blit_bonus(True)
                            track.blit_wrench(True)
                            for car in cars:
                                car.blit(track, False)
                            track.blit_overlay(True)
                            track.blit_obstacles(True)
                            track.blit_bonus(True)
                            track.blit_wrench(True)
                            for car in cars:
                                car.blit(track, True)
                            for car in cars:
                                draw_score(car, track)
                            if race_start:
                                game_display.blit(green_flag_frames[animation_index],track.flag_anchor)

                            if last_lap and not flag_waved:
                                game_display.blit(white_flag_frames[animation_index],track.flag_anchor)

                            if race_finish and not flag_waved:
                                game_display.blit(checkered_flag_frames[animation_index],track.flag_anchor)

                            # if last_lap:
                            #     pysprint_tracks.DEBUG_RAMPS = True

                            if DEBUG_AI:# or last_lap:
                                for i in range(0,len(track.external_gate_points),1):
                                    gfxdraw.line(game_display,track.external_gate_points[i][0], track.external_gate_points[i][1], track.internal_gate_points[i][0], track.internal_gate_points[i][1], white_color)
                                    index_surf = small_font.render("{}".format(i), False, white_color)
                                    midpoint = ((track.external_gate_points[i][0] + track.internal_gate_points[i][0]) / 2, (track.external_gate_points[i][1] + track.internal_gate_points[i][1]) / 2)
                                    game_display.blit(index_surf, midpoint)
                                if not track.road_gates_anchors is None:
                                    for i in range(0, len(track.road_gates_anchors)):
                                        if track.road_gates_frames_index[i] == 4:
                                            shortcut_color = green_color
                                        else:
                                            shortcut_color = red_color
                                        for j in range (1, len(track.internal_ai_gates_shortcuts[i])):
                                            gfxdraw.line(game_display, track.internal_ai_gates_shortcuts[i][j][0],track.internal_ai_gates_shortcuts[i][j][1], track.external_ai_gates_shortcuts[i][j][0],track.external_ai_gates_shortcuts[i][j][1], shortcut_color)
                                            index_surf = small_font.render("{}".format(j), False, shortcut_color)
                                            midpoint = ((track.external_ai_gates_shortcuts[i][j][0] + track.internal_ai_gates_shortcuts[i][j][0]) / 2, (track.external_ai_gates_shortcuts[i][j][1] + track.internal_ai_gates_shortcuts[i][j][1]) / 2)
                                            game_display.blit(index_surf, midpoint)
                                if not track.external_player_gates_shortcut is None:
                                    for i in range(0,len(track.external_player_gates_shortcut),1):
                                        gfxdraw.line(game_display,track.external_player_gates_shortcut[i][0], track.external_player_gates_shortcut[i][1], track.internal_player_gates_shortcut[i][0], track.internal_player_gates_shortcut[i][1], white_color)
                                        index_surf = small_font.render("{}".format(i), False, white_color)
                                        midpoint = ((track.external_gate_points[i][0] + track.internal_gate_points[i][0]) / 2, (track.external_gate_points[i][1] + track.internal_gate_points[i][1]) / 2)
                                        game_display.blit(index_surf, midpoint)


                            if DEBUG_BUMP or DEBUG_CRASH:
                                for i in range(0,len(track.external_borders)-1,1):
                                    gfxdraw.line(game_display,track.external_borders[i][0], track.external_borders[i][1], track.external_borders[i+1][0], track.external_borders[i+1][1], white_color)
                                    index_surf = small_font.render("{}".format(i), False, white_color)
                                    game_display.blit(index_surf, (track.external_borders[i][0], track.external_borders[i][1]))

                                for i in range(0,len(track.internal_borders)-1,1):
                                    gfxdraw.line(game_display,track.internal_borders[i][0], track.internal_borders[i][1], track.internal_borders[i+1][0], track.internal_borders[i+1][1], white_color)
                                    index_surf = small_font.render("{}".format(i), False, white_color)
                                    game_display.blit(index_surf, (track.internal_borders[i][0], track.internal_borders[i][1]))

                            frame_duration = pygame.time.get_ticks() - frame_start
                            current_fps = round(1000/frame_duration)
                            if current_fps <= 90 and current_fps > 0:
                                pysprint_car.frame_rate_speed_modifier = 1 + (100/current_fps)/11
                                pysprint_car.rotation_step_modifier =  1 + (100/current_fps)/14
                            else:
                                pysprint_car.frame_rate_speed_modifier = 1
                                pysprint_car.rotation_step_modifier =  1

                            if DISPLAY_FPS:
                                avg_fps.append(current_fps)
                                if (pygame.time.get_ticks() - fps_refresh_time>500):
                                    if len(avg_fps)>1:
                                        average_fps = round(sum(avg_fps)/(len(avg_fps)-1))
                                    else:
                                        average_fps = current_fps
                                    avg_fps.clear()
                                    fps_refresh_time = pygame.time.get_ticks()
                                    fps_surf = small_font.render("{} FPS".format(average_fps), False, white_color)
                                game_display.blit(fps_surf, (565,385))


                            pygame.display.update()
                            trace_frame_time("Display Updated ", frame_start)
                            if DEBUG_FPS:
                                print(' Frame: {}ms - {} FPS'.format(frame_duration, current_fps))

                            clock.tick(FPS)

                            #Display Podium Screen
                            if race_finish and flag_waved:
                                #Stop out all sounds
                                smp_manager.mute()

                                #Ranking Cars
                                ranking = [-1, -1, -1, -1]
                                #Evaluate progress and save Best Lap for Track
                                for i in range(0, len(cars)):
                                    cars[i].progress_gate = track.find_progress_gate((cars[i].x_position, cars[i].y_position))
                                    ranking[i] = i
                                    if not cars[i].is_drone:
                                        cars[i].save_best_lap(track)
                                #Ranking cars
                                sorted = False
                                while sorted == False:
                                    switched = False
                                    for i in range(0, len(cars)):
                                        if i < len(cars) - 1 :
                                            swap_needed = False
                                            if get_progress(cars[ranking[i]]) < get_progress(cars[ranking[i+1]]):
                                                swap_needed = True
                                            #Checking for cars in the same gate
                                            if get_progress(cars[ranking[i]]) == get_progress(cars[ranking[i+1]]):
                                                #Check distance to the next gate
                                                #p3 = car position P&1,p2 = gate = line between closest internal and external point
                                                next_gate = cars[ranking[i]].progress_gate + 1
                                                if next_gate == len(track.external_gate_points):
                                                    next_gate = 0
                                                p1 = track.internal_gate_points[next_gate]
                                                p2 = track.external_gate_points[next_gate]
                                                p3 = (cars[ranking[i]].x_position, cars[ranking[i]].y_position)

                                                p1=np.array(p1)
                                                p2=np.array(p2)
                                                p3=np.array(p3)

                                                current_car_dist = np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

                                                p3 = (cars[ranking[i+1]].x_position, cars[ranking[i+1]].y_position)
                                                p3=np.array(p3)

                                                next_car_dist = np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

                                                #Switch order if next cars is closer to the next gate
                                                if next_car_dist < current_car_dist:
                                                    swap_needed = True
                                            if swap_needed:
                                                swap = ranking[i]
                                                ranking[i] = ranking[i + 1]
                                                ranking[i + 1] = swap
                                                switched = True
                                    if switched == False:
                                        sorted = True

                                mechanic_index += 1
                                if mechanic_index >= len(mechanic_frames_list):
                                    mechanic_index = 0
                                mechanic_frames = mechanic_frames_list[mechanic_index]

                                crowd_background = pygame.Surface((display_width,120))

                                crowd_background.fill(cars[ranking[0]].main_color)

                                composed_race_podium = pygame.Surface((display_width, display_height))
                                composed_race_podium.blit(crowd_background, (0, 0))
                                composed_race_podium.blit(race_podium_screen, (0,0))
                                composed_race_podium.blit(crowd_flags[0], (0,0))
                                composed_race_podium.blit(cars[ranking[0]].first_car, (0,0))
                                composed_race_podium.blit(cars[ranking[1]].second_car, (0,0))
                                composed_race_podium.blit(cars[ranking[2]].third_car, (0,0))
                                composed_race_podium.blit(cars[ranking[3]].fourth_car, (0,0))
                                composed_race_podium.blit(mechanic_frames[0], (0,0))

                                screen_fadein(composed_race_podium)
                                podium_tunes[mechanic_index].play()
                                key_pressed = display_race_podium_screen(track, mechanic_frames, ranking, composed_race_podium, crowd_background)
                                smp_manager.fadeout(500)
                                if key_pressed == pygame.K_ESCAPE:
                                    game_exit = True

                                podium_displayed = True
                                #Game Over if behind a Drone
                                for i in range(0, len(cars)-1):
                                    if cars[ranking[i]].is_drone:
                                        for j in range(i+1, len(cars)):
                                            if not cars[ranking[j]].is_drone:
                                                cars[ranking[j]].end_game()
                                screen_fadeout()
                                race_finished = True
                else:
                    #Game Over, we start againt at difficulty zero
                    race_counter = 0
            else:
                game_exit = True
        else:
            if key_pressed == pygame.K_ESCAPE:
                game_exit = True
    screen_fadeout()
game_loop()
