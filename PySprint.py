from shapely import geometry
from shapely import ops
import pygame
import time
import math
pygame.init()
 
display_width = 640
display_height = 405
flags = 0
#Scale screen
#flags = pygame.SCALED

gameDisplay = pygame.display.set_mode((display_width,display_height),flags)
clock = pygame.time.Clock()

class Track:    
    background = pygame.image.load('Assets/SuperSprintTrack1.png')
    externalBorders = [   
        (116,46),
        (92,47),
        (74,50),
        (54,62),
        (43,73),
        (37,92),
        (37,112),
        (34,326),
        (45,346),
        (65,362),
        (95,371),
        (242,369),
        (265,355),
        (265,318),
        (256,238),
        (259,226),
        (269,221),
        (280,228),
        (425,358),
        (439,368),
        (542,367),
        (565,366),
        (583,358),
        (597,345),
        (608,333),
        (609,111),
        (607,95),
        (600,81),
        (593,68),
        (577,52),
        (562,47)
        ]

    internalBorders=[
        (131,131),
        (128,291),
        (142,305),
        (160,296),
        (161,160),
        (178,143),
        (310,145),
        (328,151),
        (494,302),
        (513,298),
        (513,136),
        (504,129),
        (132,129),
        (131,131)       
    ]

    line = geometry.LineString(externalBorders)        
    externalPolygon =  geometry.Polygon(line)
    line = geometry.LineString(internalBorders)
    internalPolygon =  geometry.Polygon(line)
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
    aIntersectSide=(0,0)
    bIntersectSide=(0,0)
    xVector=0
    yVector=0
    sin_angle=0
    
    #Mechanics
    rotation_step=.30
    acceleration_step=0.3        
    deceleration_step=0.3
    bump_decelaration_step=1.5   
    speed_max=12
    bump_speed=6
    decelerating=False
    rotating=False
    bumping=False
    bumpingVertical=False
    bumpingHorizontal=False
    bumpingDiagonal=False
    
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
        if self.bumping:
            self.speed-=self.bump_decelaration_step
        else:
            self.speed-=self.deceleration_step

        if self.speed < 0:
            self.speed=0
            self.decelerating=False
            #Stop Bumping routine once speed down to 0
            self.bumping=False
            self.bumpingDiagonal=False
            self.bumpingHorizontal=False
            self.bumpingVertical=False

    def searchBorderSide(self, polygonBorder,xIntersect,yIntersect):
        for i in range(0,len(polygonBorder)):
            nextIndex = i+1
            if nextIndex == len(polygonBorder):
                nextIndex=0
            if (polygonBorder[i][0]<=xIntersect and polygonBorder[nextIndex][0]>=xIntersect) or (polygonBorder[i][0]>=xIntersect and polygonBorder[nextIndex][0]<=xIntersect) or (abs(polygonBorder[i][0]-xIntersect)<=3 and abs(polygonBorder[nextIndex][0]-xIntersect)<=3):
                if (polygonBorder[i][1]<=yIntersect and polygonBorder[nextIndex][1]>=yIntersect) or (polygonBorder[i][1]>=yIntersect and polygonBorder[nextIndex][1]<=yIntersect) or (abs(polygonBorder[i][1]-yIntersect)<=3 and abs(polygonBorder[nextIndex][1]-yIntersect)<=3):
                    print('found matching pair of points ({},{})'.format(polygonBorder[i],polygonBorder[nextIndex]))
                    self.aIntersectSide=polygonBorder[i]
                    self.bIntersectSide=polygonBorder[nextIndex]
                    if (abs(polygonBorder[i][0]-polygonBorder[nextIndex][0])<=5) and (abs(polygonBorder[i][1]-polygonBorder[nextIndex][1])>5):
                        print('x delta <=5 - looks vertical enough)')
                        self.bumpingVertical = True
                    if (abs(polygonBorder[i][0]-polygonBorder[nextIndex][0])>5) and (abs(polygonBorder[i][1]-polygonBorder[nextIndex][1])<=5):
                        print('y delta <=5 - looks horizontal enough)')
                        self.bumpingHorizontal = True
                    if self.bumpingVertical == self.bumpingHorizontal:
                        self.bumpingDiagonal = True
                        self.bumpingHorizontal = False
                        self.bumpingVertical = False
                    return True
        return False


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
                #Start Skidding - Ignore current Rotation sprite, update speed and use previous Angle and sign
                #if not self.bumpingDiagonal:
                if abs(self.yVector)>0:
                    self.yVector = self.yVector * abs(self.speed * self.sin_angle) / abs(self.yVector)
                if abs(self.xVector)>0:
                    self.xVector = self.xVector * math.sqrt(self.speed*self.speed-self.yVector*self.yVector)  / abs(self.xVector)
                # else:
                #     if self.yVector>0:
                #         self.yVector=self.speed
                #     else:
                #         if self.yVector<0:
                #             self.yVector=-self.speed
                #     if self.xVector>0:
                #         self.xVector=self.speed
                #     else:
                #         if self.xVector<0:
                #             self.xVector=-self.speed

        if self.bumping:            
            if self.bumpingVertical and not self.angleVectorSign[self.sprite_angle][1]==0:
                #Bump horizontally when hitting a vertical border diagonally
                self.yVector = 0
            if self.bumpingHorizontal and not self.angleVectorSign[self.sprite_angle][0]==0:
                #Bump vertically when hitting a horizontal border diagonally
                self.xVector = 0
            # if self.bumpingDiagonal:
            #     #Diagonal Bumping: Bump Vertically if hit Horizontally - Bump Horizontally if hit Vertically  
            #     aPoint=self.aIntersectSide
            #     bPoint=self.bIntersectSide

            #     if (aPoint[0]<bPoint[0] and aPoint[1]<bPoint[1]) or (aPoint[0]>bPoint[0] and aPoint[1]>bPoint[1]):
            #         #Top-Right or Bottom Left Diagonal - Bump Vertically if hit Horizontally - Bump Horizontally if hit Vertically                    
            #         if self.angleVectorSign[self.sprite_angle][1]==0:
            #             self.yVector = self.xVector
            #             self.xVector=0
            #         else:
            #             if self.angleVectorSign[self.sprite_angle][0]==0:
            #                 self.xVector = self.yVector
            #                 self.yVector=0
            #     if (aPoint[0]>bPoint[0] and aPoint[1]<bPoint[1]) or (aPoint[0]<bPoint[0] and aPoint[1]>bPoint[1]):
            #         #Top-left or Bottom Right Diagonal - Bump Vertically if hit Horizontally - Bump Horizontally if hit Vertically                    
            #         if self.angleVectorSign[self.sprite_angle][1]==0:
            #             self.yVector = -self.xVector
            #             self.xVector=0
            #         else:
            #             if self.angleVectorSign[self.sprite_angle][0]==0:
            #                 self.xVector = -self.yVector
            #                 self.yVector=0


            self.x -= self.xVector
            self.y -= self.yVector
        else:
            self.x += self.xVector
            self.y += self.yVector
        self.rotating=False
        
        #Detect Track Borders
        carLine = geometry.LineString([
            (self.x,self.y),
            (self.x+self.sprites[self.sprite_angle].get_width(),self.y),
            (self.x,self.y+self.sprites[self.sprite_angle].get_height()),
            (self.x+self.sprites[self.sprite_angle].get_width(),self.y+self.sprites[self.sprite_angle].get_height())            
            ])        
        carPolygon =  geometry.Polygon(carLine)         
        if track.externalPolygon.overlaps(carPolygon):
            self.bumping = True
            self.speed=self.bump_speed
            #Determine the agle at which angle the car is intersecting with the Border: either right angle or not
            #Lookup in the map for the closest intersection point and the polygon side that is intersecting
            intersect_points = ops.nearest_points(track.externalPolygon,carPolygon)
            xIntersect = round(intersect_points[0].x)
            yIntersect = round(intersect_points[0].y)
            print('Ext Border Detected ({},{})'.format(xIntersect,yIntersect))
            #Search other corners of the sprite in case no border poinst detected
            if not self.searchBorderSide(track.externalBorders, xIntersect, yIntersect):
                if not self.searchBorderSide(track.externalBorders, xIntersect+self.sprites[self.sprite_angle].get_width(), yIntersect):
                    self.searchBorderSide(track.externalBorders, xIntersect, yIntersect+self.sprites[self.sprite_angle].get_height())

        else:
            if track.internalPolygon.overlaps(carPolygon):
                self.bumping = True
                self.speed=self.bump_speed
                intersect_points = ops.nearest_points(track.internalPolygon,carPolygon)                
                xIntersect = round(intersect_points[0].x)
                yIntersect = round(intersect_points[0].y)
                print('Int Border Detected ({},{})'.format(xIntersect,yIntersect))
                if not self.searchBorderSide(track.internalBorders, xIntersect, yIntersect):
                    if not self.searchBorderSide(track.internalBorders, xIntersect+self.sprites[self.sprite_angle].get_width(), yIntersect):
                        self.searchBorderSide(track.internalBorders, xIntersect, yIntersect+self.sprites[self.sprite_angle].get_height())
    def blit(self,track):
        self.updatePosition(track)
        if self.bumping:
            self.decelerating=True
            self.rotating=False
            self.updatePosition(track)        
        gameDisplay.blit(self.sprites[self.sprite_angle], (self.x, self.y))    


def game_loop():
    blueCar = Car()
    track1= Track()
 
    gameExit = False
 
    while not gameExit:
        if not blueCar.bumping:
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
        else:
            blueCar.decelerate()
        gameDisplay.blit(track1.background, (0, 0))
        blueCar.blit(track1)
        pygame.display.update()
        clock.tick(30)


game_loop()
