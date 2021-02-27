import pygame
import time
pygame.init()

 
display_width = 640
display_height = 405
 
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
circuit1 = pygame.image.load('Super Sprint Circuit 1.png')
blueCarH = pygame.image.load('BlueCarHorizontal.png')
clock = pygame.time.Clock()
 

start_x=325
start_y=65
accelerator_step=0.3
acceleration_max=9
deceleration_step=0.2
def game_loop():
    global pause
    x = start_x
    y = start_y
    acceleration = 0
    x_change = 0
    y_change = 0
 
 
    gameExit = False
 
    while not gameExit:
 
        if pygame.key.get_pressed()[pygame.K_RCTRL]:
            if acceleration < acceleration_max:
                acceleration+=accelerator_step                              
        else:            
            if acceleration > 0:
                acceleration -= deceleration_step
        
#         if not any(pygame.key.get_pressed()):
#             if acceleration > 0:
#                 acceleration -= deceleration_step
#         else:
#             if acceleration < acceleration_max:
#                 acceleration+=accelerator_step                              
     
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    if acceleration < acceleration_max:
                        acceleration+=accelerator_step                               
         
        
        x_change = -acceleration
        x += x_change
        if x < 0:
            x = 560
        gameDisplay.blit(circuit1, (0, 0))
        gameDisplay.blit(blueCarH, (x, y))                
        pygame.display.update()
        clock.tick(20)


game_loop()
