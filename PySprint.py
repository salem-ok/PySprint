from shapely import geometry
import pygame
import time
import math
pygame.init()

 
display_width = 640
display_height = 405
 
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

class Track:    
    background = pygame.image.load('Assets/SuperSprintTrack1.png')
    externalBorders = [
        (0,2),
        (0,405),
        (640,405),
        (640,335),
        (540,87),
        (605,91),
        (604,106),
        (604,121),
        (603,135),
        (604,147),
        (603,178),
        (607,324),
        (604,340),
        (591,354),
        (573,360),
        (558,366),
        (542,370),
        (443,371),
        (277,224),
        (259,225),
        (255,244),
        (257,256),
        (268,323),
        (267,354),
        (244,370),
        (97,369),
        (83,367),
        (63,361),
        (54,353),
        (40,339),
        (31,327),
        (36,111),
        (37,96),
        (47,84),
        (52,72),
        (63,62),
        (73,53),
        (87,52),
        (101,51),
        (545,50),
        (563,49),
        (578,57),
        (586,63),
        (597,73),
        (604,89),
        (640,83),
        (640,0)
    ]    
    
    line = geometry.LineString(externalBorders)        
    externalPolygon =  geometry.Polygon(line)

class Car:
    #Appearance
    color = "Blue"
    sprites = {
    0:pygame.image.load('Assets/BlueCar0.png'),
    1:pygame.image.load('Assets/BlueCar1.png'),
    2:pygame.image.load('Assets/BlueCar2.png'),
    3:pygame.image.load('Assets/BlueCar3.png'),
    4:pygame.image.load('Assets/BlueCar4.png'),
    5:pygame.image.load('Assets/BlueCar5.png'),
    6:pygame.image.load('Assets/BlueCar6.png'),
    7:pygame.image.load('Assets/BlueCar7.png'),
    8:pygame.image.load('Assets/BlueCar8.png'),
    9:pygame.image.load('Assets/BlueCar9.png'),
    10:pygame.image.load('Assets/BlueCar10.png'),
    11:pygame.image.load('Assets/BlueCar11.png'),
    12:pygame.image.load('Assets/BlueCar12.png'),
    13:pygame.image.load('Assets/BlueCar13.png'),
    14:pygame.image.load('Assets/BlueCar14.png'),
    15:pygame.image.load('Assets/BlueCar15.png')
    }
    
    spritesConv = {
    0:0,
    1:1,
    2:2,
    3:3,
    4:4,
    5:5,
    6:6,
    7:7,
    8:8,
    9:9,
    10:10,
    11:11,
    12:12,
    13:13,
    14:14,
    15:15,
    16:0,
    }

    angleVectorSign = {
    0:(0,-1),
    1:(1,-1),
    2:(1,-1),
    3:(1,-1),
    4:(1,0),
    5:(1,1),
    6:(1,1),
    7:(1,1),
    8:(0,1),
    9:(-1,1),
    10:(-1,1),
    11:(-1,1),    
    12:(-1,0),
    13:(-1,-1),
    14:(-1,-1),
    15:(-1,-1),
    16:(0,-1)
    }

    #Position & Vector
    x = 325
    y = 65
    sprite_angle = 12
    angle= 12
    speed = 0
    
    #Mechanics
    rotation_step=.30
    acceleration_step=0.3    
    deceleration_step=0.3
    speed_max=12
    decelerating=False
    rotating=False
    xVector=0
    yVector=0
    sin_angle=0
    
    def rotate(self, left):
        self.rotating=True
        if left:
            self.angle -= self.rotation_step 
        else:
            self.angle += self.rotation_step

        if self.angle<0:
            self.angle +=  16
        if self.angle>16:
            self.angle -= 16
        self.sprite_angle =  self.spritesConv[round(self.angle,0)]                        

    def accelerate(self):
         self.decelerating=False
         if self.speed < self.speed_max:
            self.speed+=self.acceleration_step

    def decelerate(self):
        self.decelerating=True
        self.speed-=self.deceleration_step
        if self.speed < 0:
            self.speed=0
            self.decelerating=False

    def updatePosition(self, track):                
        if not self.decelerating:
            #Calculate Vector - No skidding
            self.sin_angle = math.sin(math.radians(abs(self.sprite_angle*22.5-90)))
            
            self.yVector = abs(self.speed * self.sin_angle)
                                
            self.yVector = self.yVector * self.angleVectorSign[self.sprite_angle][1]
            
            self.xVector = math.sqrt(self.speed*self.speed-self.yVector*self.yVector)
            
            self.xVector = self.xVector * self.angleVectorSign[self.sprite_angle][0]
        else:
            if not self.rotating:
                #Staright Skidding - Ignore current Rotation sprite, update speed and use previous Angle and sign
                if abs(self.yVector)>0:
                    self.yVector = self.yVector * abs(self.speed * self.sin_angle) / abs(self.yVector)
                if abs(self.xVector)>0:
                    self.xVector = self.xVector * math.sqrt(self.speed*self.speed-self.yVector*self.yVector)  / abs(self.xVector)
        
        self.x += self.xVector
        self.y += self.yVector
        # print('sin(angle): {}\nSprite: {}'.format(self.angle,self.sprite_angle))
        # print('xVextor: {}\nyVector: {}'.format(self.xVector,self.yVector))
        self.rotating=False
        
        #Detect External Track Borders
        carLine = geometry.LineString([
            (self.x,self.y),
            (self.x+self.sprites[self.sprite_angle].get_width(),self.y),
            (self.x,self.y+self.sprites[self.sprite_angle].get_height()),
            (self.x+self.sprites[self.sprite_angle].get_width(),self.y+self.sprites[self.sprite_angle].get_height())            
            ])        
        carPolygon =  geometry.Polygon(carLine)        
        if track.externalPolygon.overlaps(carPolygon):
            print('Border Detected')
        #Asteroids Style - Screen Borders
        if self.x < 0:
            self.x = 640
        if self.x > 640:
            self.x = 0
            
        if self.y < 0:
            self.y = 405
        if self.y > 405:
            self.y = 0
            
    def blit(self,track):
        self.updatePosition(track)
        gameDisplay.blit(self.sprites[self.sprite_angle], (self.x, self.y))    


def game_loop():
    global pause
    blueCar = Car()
    track1= Track()
 
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
        
        gameDisplay.blit(track1.background, (0, 0))
        blueCar.blit(track1)
        pygame.display.update()
        clock.tick(30)


game_loop()
