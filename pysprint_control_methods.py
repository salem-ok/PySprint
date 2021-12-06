import pygame

keyboard_1 = {
    'ACCELERATE': pygame.K_RCTRL,
    'LEFT': pygame.K_LEFT,
    'RIGHT': pygame.K_RIGHT,
    'METHOD': 'KEYBOARD 1'
}

keyboard_2 = {
    'ACCELERATE': pygame.K_LCTRL,
    'LEFT': pygame.K_x,
    'RIGHT': pygame.K_c,
    'METHOD': 'KEYBOARD 2'
}

joystick_1 = {
    'METHOD': 'JOYSTICK 1'
}

joystick_2 = {
    'METHOD': 'JOYSTICK 2'
}

joystick_3 = {
    'METHOD': 'JOYSTICK 3'
}

joystick_4 = {
    'METHOD': 'JOYSTICK 4'
}

control_methods = [keyboard_1, keyboard_2, joystick_1, joystick_2,
                   joystick_3, joystick_4]
