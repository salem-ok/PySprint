# PySprint
Remake the Atari ST port of Super Sprint by Electric Dreams from 1985 in Python with Pygame

![PySprint Splash Screen](https://repository-images.githubusercontent.com/342905347/8c764600-a6cd-11eb-8854-8a5d35ea4e94)

The idea is to:
- Get as close to the original as possible in terms of gameplay
- Fix the very few annoying things (mandatory wait of 5secs before each race for example)
- Add features like custom tracks and cars, custom music, and hopefully remote multiplayer...
- Learn Python and have fun!

## Prerequisites:

- The game requires the pygame and numpy packages to run if you download the source and want to run it interpreted.
- The first beta release is pre-compiled and packages for Linux, Mac OS & Windows just download, unzip and execute:
  [Download Binaries](https://github.com/salem-ok/PySprint/releases/tag/v0.29-beta)

## FAQ:
- Feel free to check existing questions and add you own:
  [Q&A](https://github.com/salem-ok/PySprint/discussions/categories/q-a)

## Game navigation

The game starts in **"Attract mode"** cycling through several screens -Spash Screen, High Scores, best Laps, Credits etc.:

![PySprint Attract Mode](https://github.com/salem-ok/PySprint/blob/main/ImageSource/Attract.gif?raw=true)

## Attract mode commands:
  - Hit F1 for Options:
       - Re-mapping of keyboard controls for 2 players
       - Re-assigning of Gamepads & keyboard controls to any car color

![PySprint Options Screen](https://github.com/salem-ok/PySprint/blob/main/ImageSource/OptionsScreen.png?raw=true)

  - Hit F11 to toggle Scaled Window Mode (crashes on Raspberry Pi)
  - Hit ESC or close the Window to Quit the Game
  - Hit acclerate for any player to start a game:
      - The first player to hit accelerate selects the track (left-right to choose, accelerate to select).
      - Other players can join during track selection

![PySprint Options Screen](https://github.com/salem-ok/PySprint/blob/main/ImageSource/SelectTrack.gif?raw=true)

- Once the track is selected the start screen is displayed:
        - Before each race any player can join the game by hitting accelerate
        - You can skip the countdown to start racing right away by hitting space

![PySprint Options Screen](https://github.com/salem-ok/PySprint/blob/main/ImageSource/StartRace.gif?raw=true)

## In game Controls:

- Hit ESC or close the Window to Quit the Game

## Default Car controls (can be adjusted in the Options screen)

### Blue car:
  - Accelerate: Right Ctrl
  - Left: Left
  - Right: Right

### Green car:
  - Accelerate: Left Ctrl
  - Left: X
  - Right: C

### Yellow car:
  - First Detected Joystick:
  - Any D-PAD or Analog Pad or Stick for Left and Right
  - Any button for accelerate

### Red car:
  - Second Detected Joystick
  - Any D-PAD or Analog Pad or Stick for Left and Right
  - Any button for accelerate
