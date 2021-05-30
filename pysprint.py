import pygame
import pygame.display
import numpy as np
import pysprint_car
import pysprint_tracks
import random

pygame.init()
pygame.joystick.init()

version = "0.0"
display_width = 640
display_height = 400
pysprint_car.display_width = 640
pysprint_car.display_height = 400

flags = 0
race_laps = 2
pysprint_car.race_laps = race_laps

game_display = pygame.display.set_mode((display_width, display_height), flags)

pygame.display.set_caption('PySprint v{}'.format(version))
icon = pygame.image.load('Assets/SuperSprintIcon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

pysprint_car.game_display = game_display

cars = [pysprint_car.Car(), pysprint_car.Car(), pysprint_car.Car(), pysprint_car.Car()]

#Scale screen
#flags = pygame.SCALED

FPS = 30
BITS_64 = True
DEBUG_BUMP = False
DEBUG_CRASH = False
pysprint_car.DEBUG_BUMP = DEBUG_BUMP
pysprint_car.DEBUG_CRASH = DEBUG_CRASH
DEBUG_FLAG = False
DEBUG_FPS = False

#Flag Events
GREENFLAG = pygame.USEREVENT + 1
WHITEFLAG = GREENFLAG + 1
CHECKEREDFLAG = WHITEFLAG + 1

JOYSTICK_BUTTON_PRESSED = -2

#Load Assets

small_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf',15)
shadow_font = pygame.font.Font('Assets/SupersprintST-Regular-Stroke.ttf',15)
big_font = pygame.font.Font('Assets/SupersprintST-Regular.ttf',20)
big_shadow_font = pygame.font.Font('Assets/SupersprintST-Regular-Stroke.ttf',20)

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


loading_screen_foreground = pygame.image.load('Assets/SuperSprintLoadingScreenForeground.png').convert_alpha()
credits_screen = pygame.image.load('Assets/SuperSprintCreditsScreen.png').convert_alpha()
splash_screen = pygame.image.load('Assets/SuperSprintSplashScreen.png').convert_alpha()
start_race_screen = pygame.image.load('Assets/SuperSprintStartRaceScreen.png').convert_alpha()
high_score_screen = pygame.image.load('Assets/SuperSprintHighScores.png').convert_alpha()
lap_records_screen = pygame.image.load('Assets/SuperSprintLapRecords.png').convert_alpha()
race_podium_screen = pygame.image.load('Assets/SuperSprintRacePodium.png').convert_alpha()


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


keyboard_1 = {}
keyboard_1['ACCELERATE'] = pygame.K_RCTRL
keyboard_1['LEFT'] = pygame.K_LEFT
keyboard_1['RIGHT'] = pygame.K_RIGHT
keyboard_1['METHOD'] = "KEYBOARD 1"

keyboard_2 = {}
keyboard_2['ACCELERATE'] = pygame.K_LCTRL
keyboard_2['LEFT'] = pygame.K_x
keyboard_2['RIGHT'] = pygame.K_c
keyboard_2['METHOD'] = "KEYBOARD 2"

joystick_1  ={
    'METHOD':"JOYSTICK 1"
}
joystick_2  ={
    'METHOD':"JOYSTICK 2"
}
joystick_3  ={
    'METHOD':"JOYSTICK 3"
}
joystick_4  ={
    'METHOD':"JOYSTICK 4"
}


control_methods = [keyboard_1, keyboard_2, joystick_1, joystick_2, joystick_3, joystick_4]


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
    score = 0
    name = 'xxx'
    for i in range (0,3):
        game_display.blit(small_font.render('{}'.format(i+1), False, white_color), (top3[0], top3[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top3[0] + 25, top3[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top3[0] + 110, top3[1] + i * 15))

    for i in range (0,9):
        game_display.blit(small_font.render('{}'.format(i+4), False, white_color), (top12[0], top12[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top12[0] + 25, top12[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top12[0] + 110, top12[1] + i * 15))

    for i in range (0,9):
        game_display.blit(small_font.render('{}'.format(i+13), False, white_color), (top21[0], top21[1] + i * 15))
        game_display.blit(small_font.render('{:06d}'.format(score,), False, white_color), (top21[0] + 30, top21[1] + i * 15))
        game_display.blit(small_font.render(name, False, white_color), (top21[0] + 115, top21[1] + i * 15))

    for i in range (0,9):
        game_display.blit(small_font.render('{}'.format(i+22), False, white_color), (top30[0], top30[1] + i * 15))
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
    time = 0.0
    name = 'xxx'
    for i in range(0,4):
        game_display.blit(small_font.render('Track', False, white_color), (top4[0], top4[1] + i * 15))
        game_display.blit(small_font.render('{}'.format(i+1), False, white_color), (top4[0] + 70, top4[1] + i * 15))
        game_display.blit(small_font.render('{}'.format(time), False, white_color), (top4[0] + 100, top4[1] + i * 15))
        game_display.blit(small_font.render('secs    {}'.format(name), False, white_color), (top4[0] + 145, top4[1] + i * 15))

    for i in range(0,4):
        game_display.blit(small_font.render('Track', False, white_color), (top8[0], top8[1] + i * 15))
        game_display.blit(small_font.render('{}'.format(i+4), False, white_color), (top8[0] + 70, top8[1] + i * 15))
        game_display.blit(small_font.render('{}'.format(time), False, white_color), (top8[0] + 100, top8[1] + i * 15))
        game_display.blit(small_font.render('secs    {}'.format(name), False, white_color), (top8[0] + 145, top8[1] + i * 15))

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


def print_press_acceltoplay(top_left, color, seconds):
    game_display.blit(small_font.render("PRESS", False, color), top_left)
    game_display.blit(small_font.render("ACCELERATE", False, color), (top_left[0] - 28, top_left[1] + 20))
    game_display.blit(small_font.render("TO PLAY".format(seconds), False, color), (top_left[0] - 10, top_left[1] + 40))
    game_display.blit(small_font.render("{}".format(seconds), False, color), (top_left[0] + 24, top_left[1] + 60))

def print_start_race_text(seconds):
    for car in cars:
        if car.is_drone:
            print_press_acceltoplay(car.start_screen_text_position, car.main_color, seconds)
        else:
            print_prepare_to_race(car.start_screen_text_position, car.main_color)
    skip_surf = small_font.render("PRESS SPACE TO SKIP", False, white_color)
    game_display.blit(skip_surf, ((600 - skip_surf.get_width())/2, 385))

def display_start_race_screen():
    seconds = 5
    screen_exit = False
    engine_idle_counter = 0

    #Add Green car
    screen_fadein(start_race_screen)
    print_start_race_text(seconds)
    for car in cars:
        game_display.blit(engine_idle[engine_idle_counter], car.start_screen_engine_position)
        car.prepare_to_race_counter = -1

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

        any_joystick_button_pressed()
        if key_pressed >= 0:
            accelerate_pressed(key_pressed)

        clock.tick(15)
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


    for score in range(0,1010,10):
        game_display.blit(composed_race_podium, (0, 0))
        for i in range (0, len(ranking)):
            #Blit Lap times
            game_display.blit(avg_lap_times[i], (text_positions[i][0] - avg_lap_times[i].get_width(), text_positions[i][3]))
            game_display.blit(best_lap_times[i], (text_positions[i][0] - best_lap_times[i].get_width(), text_positions[i][4]))

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
        clock.tick(10)

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
                                    car.joystick = None
                                    car.accelerate_key = None
                                    car.left_key = None
                                    car.right_key = None
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

def draw_score(car: pysprint_car.Car, track: pysprint_tracks.Track):
    track.update_score_from_position(car)
    #Car
    if car.is_drone:
        score_surf = small_font.render("DRONE", False, car.main_color)
        shadow_score_surf = shadow_font.render("DRONE", False, black_color)
    else:
        score_surf = small_font.render("CAR", False, car.main_color)
        shadow_score_surf = shadow_font.render("CAR", False, black_color)
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
    if DEBUG_FPS:
        print('{} - Duration: {}'.format(trace_event, pygame.time.get_ticks() - frame_start))

def accelerate_pressed(key_pressed):
    if key_pressed == JOYSTICK_BUTTON_PRESSED:
        return True
    for car in cars:
        if not car.accelerate_key is None:
            if key_pressed == car.accelerate_key:
                car.start_game()
                return True
    return False

def any_joystick_button_pressed():
    button_pressed = False
    for car in cars:
        if not car.joystick is None:
            joy = car.joystick
            buttons = joy.get_numbuttons()
            for j in range(buttons):
                button = joy.get_button(j)
                if button == 1:
                    button_pressed = True
                    car.start_game()
    return button_pressed


def get_progress(car):
    return car.lap_count * 1000 + car.progress_gate

def initialize_cars():
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


    #Initialize car Specific Event codes
    cars[0].BUMPCLOUD = CHECKEREDFLAG + 1
    cars[0].EXPLOSION = cars[0].BUMPCLOUD + 1
    #64 Bit version
    if BITS_64:
        cars[1].BUMPCLOUD = cars[0].EXPLOSION + 1
        cars[1].EXPLOSION = cars[1].BUMPCLOUD + 1
        cars[2].BUMPCLOUD = cars[1].EXPLOSION + 1
        cars[2].EXPLOSION = cars[2].BUMPCLOUD + 1
        cars[3].BUMPCLOUD = cars[2].EXPLOSION + 1
        cars[3].EXPLOSION = cars[3].BUMPCLOUD + 1
    else:
        cars[1].BUMPCLOUD = cars[0].BUMPCLOUD
        cars[1].EXPLOSION = cars[0].EXPLOSION
        cars[2].BUMPCLOUD = cars[1].BUMPCLOUD
        cars[2].EXPLOSION = cars[1].EXPLOSION
        cars[3].BUMPCLOUD = cars[2].BUMPCLOUD
        cars[3].EXPLOSION = cars[3].EXPLOSION


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
    for car in cars:
        car.lap_count = 0
        car.lap_times.clear()
        for i in range(0, race_laps):
            car.lap_times.append(0)

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



def game_loop():

    game_exit = False
    print('{} - Joystick(s) detected'.format(pygame.joystick.get_count()))

    for i in range (pygame.joystick.get_count()):
        joy = pygame.joystick.Joystick(i)
        print ('{}'.format(joy.get_name()))

    initialize_cars()

    mechanic_frames_list = [hammer_frames, saw_frames, head_scratch_frames, blow_frames]
    mechanic_index = random.randint(0,3)

    while not game_exit:
        key_pressed = -1
        key_pressed = display_loading_screen(False)
        #Attract mode
        while not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
            key_pressed = display_splash_screen()
            if (key_pressed == pygame.K_F1):
                display_options()
            if not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                key_pressed = display_high_scores()
            if (key_pressed == pygame.K_F1):
                display_options()
            if not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                key_pressed = display_lap_records()
            if (key_pressed == pygame.K_F1):
                display_options()
            if not (accelerate_pressed(key_pressed) or (key_pressed == pygame.K_ESCAPE)):
                key_pressed = display_credits_screen()
            if (key_pressed == pygame.K_F1):
                display_options()

        if accelerate_pressed(key_pressed):
            #Initiate Race
            key_pressed = display_start_race_screen()
            if not key_pressed == pygame.K_ESCAPE:
                activate_cars()
                track1 = pysprint_tracks.Track()
                track1.background = pygame.image.load(track1.background_filename)
                track1.track_mask = pygame.image.load(track1.track_mask_filename).convert_alpha()
                track1.finish_line = pygame.Rect(track1.finish_line_rect[0], track1.finish_line_rect[1], track1.finish_line_rect[2], track1.finish_line_rect[3])
                screen_fadein(track1.background)

                #Align Cars on Start Line
                for i in range (0,4):
                    cars[i].x_position = track1.first_car_start_position[0]
                    cars[i].y_position = track1.first_car_start_position[1] + i * 15
                    cars[i].sprite_angle = track1.start_sprite_angle
                    cars[i].angle = track1.start_sprite_angle
                    cars[i].lap_count = 0
                    cars[i].previous_score_increment = 0
                race_start = True
                last_lap = False
                race_finish = False
                animation_index = 0
                flag_waves = 0
                wave_up = True
                flag_waved = False
                podium_displayed = False
                race_start_time = pygame.time.get_ticks()
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
                            if car.bumping or race_finish:
                                car.ignore_controls = True
                            if not car.ignore_controls:
                                if car.is_drone:
                                    car.ai_drive(track1)
                                else:
                                    #If car if keyboard controlled
                                    if car.joystick is None:
                                        if pygame.key.get_pressed()[car.accelerate_key]:
                                            car.accelerate()
                                        else:
                                            car.decelerate()

                                        if pygame.key.get_pressed()[car.left_key]:
                                            car.rotate(True)

                                        if pygame.key.get_pressed()[car.right_key]:
                                            car.rotate(False)
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
                                            #Ignoring any axis beyong the first 2 which should be analog stick X
                                            #Any axis beyong that is probably an analog shoulder button
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
                                            car.rotate(True)
                                        else:
                                            if right_pressed:
                                                car.rotate(False)
                            else:
                                car.decelerate()
                        trace_frame_time("Checked Key input", frame_start)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: # If user clicked close.
                                game_exit = True
                                podium_displayed = True
                            for car in cars:
                                if not car.ignore_controls:
                                    if car.is_drone:
                                        car.ai_drive(track1)
                                    else:
                                        if event.type == pygame.KEYDOWN:
                                            #If car if keyboard controlled
                                            if car.joystick is None:
                                                if event.key == car.accelerate_key:
                                                    car.accelerate()
                                                if event.key == car.left_key:
                                                    car.rotate(True)
                                                if event.key == car.right_key:
                                                    car.rotate(False)
                                else:
                                    car.decelerate()
                                #Draw Dust Cloud
                                if event.type == car.BUMPCLOUD:
                                    if DEBUG_BUMP:
                                        print('{} - Bump Timer triggerred'.format(pygame.time.get_ticks()))
                                    if car.bumping:
                                        car.display_bump_cloud()
                                #Draw Explosion
                                if event.type == car.EXPLOSION:
                                    if DEBUG_CRASH:
                                        print('{} - Crash Timer triggerred'.format(pygame.time.get_ticks()))
                                    if car.crashing:
                                        car.display_explosion()
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

                        trace_frame_time("Managed all Events", frame_start)

                        for car in cars:
                            car.draw(track1)
                            trace_frame_time("Drawn car", frame_start)
                        if not race_finish:
                            for car in cars:
                                race_finish = car.test_finish_line(track1)
                                if race_finish == True:
                                    break
                            #Draw Checkered Flag and finish race
                            if race_finish:
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
                                animation_index = 0
                                flag_waves = 0
                                wave_up = True
                                last_lap = True
                                pygame.time.set_timer(WHITEFLAG, 40)
                                break

                        trace_frame_time("Test Finish ", frame_start)
                        game_display.blit(track1.background, (0, 0))
                        if race_start:
                            game_display.blit(green_flag_frames[animation_index],track1.flag_anchor)

                        if last_lap and not flag_waved:
                            game_display.blit(white_flag_frames[animation_index],track1.flag_anchor)

                        if race_finish and not flag_waved:
                            game_display.blit(checkered_flag_frames[animation_index],track1.flag_anchor)
                        for car in cars:
                            car.blit(track1)
                            draw_score(car, track1)

                        pygame.display.update()
                        trace_frame_time("Display Updated ", frame_start)
                        frame_duration = pygame.time.get_ticks() - frame_start
                        current_fps = round(1000/frame_duration)
                        if DEBUG_FPS:
                            print(' Frame: {} - {} FPS'.format(frame_duration, current_fps))
                        clock.tick(FPS)

                        #Display Podium Screen
                        if race_finish and flag_waved:
                            #Ranking Cars
                            ranking = [-1, -1, -1, -1]
                            #Evaluate progress
                            for i in range(0, len(cars)):
                                cars[i].progress_gate = track1.find_progress_gate((cars[i].x_position, cars[i].y_position))
                                ranking[i] = i
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
                                            if next_gate == len(track1.external_gate_points):
                                                next_gate = 0
                                            p1 = track1.internal_gate_points[next_gate]
                                            p2 = track1.external_gate_points[next_gate]
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
                            display_race_podium_screen(track1, mechanic_frames, ranking, composed_race_podium, crowd_background)
                            podium_displayed = True
                            #Game Over if behind a Drone
                            for i in range(0, len(cars)-1):
                                if cars[ranking[i]].is_drone:
                                    for j in range(i+1, len(cars)):
                                        cars[ranking[j]].end_game()
                            screen_fadeout()
            else:
                game_exit = True
        else:
            if key_pressed == pygame.K_ESCAPE:
                game_exit = True
    screen_fadeout()
game_loop()
