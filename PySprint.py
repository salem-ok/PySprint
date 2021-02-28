import pygame
import time
pygame.init()

 
display_width = 640
display_height = 405
 
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
circuit1 = pygame.image.load('Super Sprint Circuit 1.png')
clock = pygame.time.Clock()

class Car:
    #Appearance
    color = "Blue"
    sprites = {
    2:pygame.image.load('BlueCar2.png'),
    3:pygame.image.load('BlueCar3.png'),
    4:pygame.image.load('BlueCar4.png'),
    6:pygame.image.load('BlueCar6.png'),
    8:pygame.image.load('BlueCar8.png'),
    9:pygame.image.load('BlueCar9.png'),
    10:pygame.image.load('BlueCar10.png'),
    12:pygame.image.load('BlueCar12.png')
    }    
    #Position & Vector
    x = 325
    y = 65
    sprite_angle = 9
    angle= 9
    speed = 0
    
    #Mechanics
    rotation_step=0.5
    acceleration_step=0.3    
    deceleration_step=0.2
    speed_max=9
    
    def rotate(self, left):
        if left:            
            if self.sprite_angle==2:
                self.sprite_angle =  12
            else:
                # Get next key in Dictionary 
                # Using index() + loop 
                temp = list(self.sprites) 
                try: 
                    self.sprite_angle = temp[temp.index(self.sprite_angle) - 1] 
                except (ValueError, IndexError): 
                    return
        else:
            if self.sprite_angle==12:
                self.sprite_angle = 2
            else:
                # Get next key in Dictionary 
                # Using index() + loop 
                temp = list(self.sprites)
                try: 
                    self.sprite_angle = temp[temp.index(self.sprite_angle) + 1] 
                except (ValueError, IndexError): 
                    return
        


    def accelerate(self):
         if self.speed < self.speed_max:
            self.speed+=self.acceleration_step

    def decelerate(self):
         if self.speed > 0:
            self.speed-=self.deceleration_step

    def updatePosition(self):                
        self.x -= self.speed
        if self.x < 0:
            self.x = 560
    def blit(self):
        self.updatePosition()
        gameDisplay.blit(self.sprites[self.sprite_angle], (self.x, self.y))    


def game_loop():
    global pause
    blueCar = Car()
 
 
    gameExit = False
 
    while not gameExit:
 
        if pygame.key.get_pressed()[pygame.K_RCTRL]:
            blueCar.accelerate()
        else:
            blueCar.decelerate()

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            blueCar.rotate(True)
        
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            blueCar.rotate(False)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    blueCar.accelerate()
                if event.key == pygame.K_LEFT:
                    blueCar.rotate(True)
                if event.key == pygame.K_RIGHT:
                    blueCar.rotate(False)
        
        gameDisplay.blit(circuit1, (0, 0))
        blueCar.blit()
        pygame.display.update()
        clock.tick(20)


game_loop()
