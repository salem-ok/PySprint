import pygame
import time
import math

pygame.init()

display_width = 640
display_height = 400
flags = 0
#Scale screen
#flags = pygame.SCALED
DEBUG_COLLISION = False
DEBUG_BUMP = True
DEBUG_CRASH = False

gameDisplay = pygame.display.set_mode((display_width, display_height), flags)
clock = pygame.time.Clock()



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
    18:pygame.image.load('Assets/Explosion18.png').convert_alpha(),
}



class Track:
    background = pygame.image.load('Assets/SuperSprintTrack1.png')
    trackMask = pygame.image.load('Assets/SuperSprintTrack1Mask.png').convert_alpha()




    externalBorders = [
        (101, 52),
        (544, 53),
        (560, 54),
        (577, 59),
        (591, 71),
        (601, 84),
        (606, 96),
        (608, 110),
        (610, 331),
        (572, 364),
        (545, 368),
        (449, 371),
        (437, 369),
        (273, 224),
        (263, 224),
        (257, 229),
        (256, 231),
        (257, 258),
        (257, 273),
        (266, 318),
        (266, 354),
        (247, 373),
        (99, 373),
        (71, 368),
        (35, 330),
        (37, 112),
        (40, 93),
        (46, 79),
        (64, 59),
        (75, 55),
        (84, 51)
        ]

    internalBorders = [
        (133, 134),
        (129, 143),
        (125, 153),
        (124, 295),
        (132, 305),
        (143, 307),
        (157, 298),
        (161, 163),
        (178, 148),
        (292, 148),
        (314, 152),
        (333, 161),
        (489, 306),
        (499, 307),
        (504, 302),
        (512, 299),
        (512, 141),
        (503, 131),
        (137, 130)
    ]

class Car:
    #Appearance
    sprites = {
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

    angleVectorSign = {
        0:(0, -1),
        1:(1, -1),
        2:(1, -1),
        3:(1, -1),
        4:(1, 0),
        5:(1, 1),
        6:(1, 1),
        7:(1, 1),
        8:(0, 1),
        9:(-1, 1),
        10:(-1, 1),
        11:(-1, 1),
        12:(-1, 0),
        13:(-1, -1),
        14:(-1, -1),
        15:(-1, -1),
        16:(0, -1)
    }

    #Position & Vector
    x_position = 325
    y_position = 65
    sprite_angle = 12
    angle = 12
    speed = 0
    a_intersectSide = (0, 0)
    b_intersectSide = (0, 0)
    x_intersect = 0
    y_intersect = 0
    x_vector = 0
    y_vector = 0
    sin_angle = 0

    #Mechanics
    #30FPS Settings
    # rotation_step = .30
    # acceleration_step = 0.3
    # deceleration_step = 0.45
    # bump_decelaration_step = 1.5
    # speed_max = 9
    # bump_speed = 6

    #60FPS Settings
    rotation_step = .19
    acceleration_step = 0.10
    deceleration_step = 0.15
    bump_decelaration_step = 0.7
    speed_max = 6
    bump_speed = 5

    #Collision Settings
    diagonal_detection_tolerance = 2
    vector_simulation_length = 10
    side_detection_tolerance = 7
    max_speed_crash_threshold = 500
    max_crash_duration = 500

    #Car State
    decelerating = False
    rotating = False
    bumping = False
    crashing = False
    bumping_vector_initialized = False
    bumpingVertical = False
    bumpingHorizontal = False
    bumpingDiagonal = False
    crash_finished = False
    animation_index = 0
    collision_time = 0
    max_speed_reached = 0

    #Car Events
    BUMPCLOUD = pygame.USEREVENT + 1
    EXPLOSION = BUMPCLOUD + 1

    def rotate(self, left):
        self.rotating = True
        if left:
            self.angle -= self.rotation_step
        else:
            self.angle += self.rotation_step

        if self.angle < 0:
            self.angle += 16
        if self.angle >= 16:
            self.angle -= 16
        self.sprite_angle = round(self.angle,0)
        if self.sprite_angle == 16:
            self.sprite_angle = 0

    def accelerate(self):
        self.decelerating = False
        if self.speed < self.speed_max:
            self.speed += self.acceleration_step
            if self.speed >= self.speed_max:
                self.max_speed_reached = pygame.time.get_ticks()

    def decelerate(self):
        self.decelerating = True
        self.max_speed_reached = 0
        if self.bumping:
            self.speed -= self.bump_decelaration_step
        else:
            self.speed -= self.deceleration_step

        if self.speed < 0:
            self.speed = 0
        if self.speed == 0:
            self.decelerating = False
            if self.bumping:
                #Stop Bumping routine once speed down to 0
                self.end_bump_loop()

    def searchBorderSide(self, polygonBorder):
        self.bumpingDiagonal = False
        self.bumpingHorizontal = False
        self.bumpingVertical = False
        for i in range(0, len(polygonBorder)):
            nextIndex = i+1
            if nextIndex == len(polygonBorder):
                nextIndex = 0
            top = 0
            left = 0
            if polygonBorder[i][0] <= polygonBorder[nextIndex][0]:
                top = polygonBorder[i][0]
            else:
                top = polygonBorder[nextIndex][0]
            if polygonBorder[i][1] <= polygonBorder[nextIndex][1]:
                left = polygonBorder[i][1]
            else:
                left = polygonBorder[nextIndex][1]

            rect_width = abs(polygonBorder[nextIndex][0]-polygonBorder[i][0])
            if rect_width == 0:
                rect_width = 1
            rect_height = abs(polygonBorder[nextIndex][1]-polygonBorder[i][1])
            if rect_height == 0:
                rect_height = 1
            wall_rect = pygame.Rect(top, left, rect_width, rect_height)
            #Enlarge detection Box to maximize chance of hitting a polygon side
            sprite_rect = pygame.Rect(self.x_intersect-self.side_detection_tolerance, self.y_intersect-self.side_detection_tolerance, self.side_detection_tolerance*2, self.side_detection_tolerance*2)

            if sprite_rect.colliderect(wall_rect):
                if DEBUG_COLLISION:
                    print('found matching pair of points ({},{})'.format(polygonBorder[i],polygonBorder[nextIndex]))
                self.a_intersectSide = polygonBorder[i]
                self.b_intersectSide = polygonBorder[nextIndex]
                if (abs(polygonBorder[i][0]-polygonBorder[nextIndex][0]) <= self.diagonal_detection_tolerance) and (abs(polygonBorder[i][1]-polygonBorder[nextIndex][1]) > self.diagonal_detection_tolerance):
                    if DEBUG_COLLISION:
                        print('x delta <={} - looks vertical enough'.format(self.diagonal_detection_tolerance))
                    self.bumpingVertical = True
                    return True
                if (abs(polygonBorder[i][0]-polygonBorder[nextIndex][0])>self.diagonal_detection_tolerance) and (abs(polygonBorder[i][1]-polygonBorder[nextIndex][1])<=self.diagonal_detection_tolerance):
                    if DEBUG_COLLISION:
                        print('y delta <={} - looks horizontal enough'.format(self.diagonal_detection_tolerance))
                    self.bumpingHorizontal = True
                    return True
                if DEBUG_COLLISION:
                    print('Diagonal Bumping')
                self.bumpingDiagonal = True
                self.bumpingHorizontal = False
                self.bumpingVertical = False
                return True
        return False

    def calculate_vector_from_sprite(self):
        self.sin_angle = math.sin(math.radians(abs(self.sprite_angle*22.5-90)))
        self.y_vector = abs(self.speed * self.sin_angle)
        self.y_vector = self.y_vector * self.angleVectorSign[self.sprite_angle][1]
        self.x_vector = math.sqrt(self.speed*self.speed-self.y_vector*self.y_vector)
        self.x_vector = self.x_vector * self.angleVectorSign[self.sprite_angle][0]

    def calculate_skidding_vector(self):
        #Start Skidding - Ignore current Rotation sprite, update speed and use previous Angle and sign
        if not self.y_vector == 0:
            self.y_vector = self.y_vector * abs(self.speed * self.sin_angle) / abs(self.y_vector)

        if not self.x_vector == 0:
            self.x_vector = self.x_vector * math.sqrt(self.speed*self.speed-self.y_vector*self.y_vector)  / abs(self.x_vector)

        if self.x_vector==0 and self.y_vector==0 and self.speed>0:
            #Wrong situation: reset to default vector
            self.calculate_vector_from_sprite()

    def calculate_bumping_vector(self,track):
        if not self.bumping_vector_initialized:
            if self.bumpingVertical:
                #Bump horizontally when hitting a vertical border diagonally or horizontally
                if self.x_vector == 0:
                    #Edge case: bumping into a Vertical wall while car is vertical
                    self.x_vector = self.y_vector
                    intersect_point = self.test_collision(track, True)
                    #Test if the vector is set away or towards the wall, and invert if necessary
                    if intersect_point:
                        self.x_vector = -self.x_vector
                else:
                    #Invert X component fo the vector
                    self.x_vector = -self.x_vector
                self.y_vector = 0
            else:
                if self.bumpingHorizontal:
                    #Bump vertically when hitting a horizontal border diagonally or vertically
                    if self.y_vector == 0:
                        #Edge case: bumping into a Horizontal wall while car is horizontal
                        self.y_vector = self.x_vector
                        intersect_point = self.test_collision(track, True)
                        #Test if the vector is set away or towards the wall, and invert if necessary
                        if intersect_point:
                            self.y_vector = -self.y_vector
                    else:
                        #Invert Y component fo the vector
                        self.y_vector = -self.y_vector
                    self.x_vector = 0
                else:
                    if self.bumpingDiagonal:
                        #Diagonal Bumping: Bump Diagnoally if hit Horizontally - or Vertically  - Vert or Horiz Bump if hit diagonally
                        aPoint = self.a_intersectSide
                        bPoint = self.b_intersectSide

                        if self.x_vector == 0 or self.y_vector == 0:
                            #Car is moving Horizontally or Vertical - Force 45 degree angle
                            self.sin_angle = math.sin(math.radians(abs(45)))
                            newVector = abs(self.speed * self.sin_angle)

                            if (aPoint[0] < bPoint[0] and aPoint[1] < bPoint[1]) or (aPoint[0] > bPoint[0] and aPoint[1] > bPoint[1]):
                                #Top-Right or Bottom Left Diagonal
                                if self.y_vector > 0 or self.x_vector < 0:
                                    #Bottom Left Diagonal - Invert Y Component
                                    self.x_vector = newVector
                                    self.y_vector = -newVector
                                else:
                                    if self.y_vector < 0 or self.x_vector > 0:
                                        #Top Right Diagonal - Invert X Component
                                        self.x_vector = -newVector
                                        self.y_vector = newVector

                            if (aPoint[0] > bPoint[0] and aPoint[1] < bPoint[1]) or (aPoint[0] < bPoint[0] and aPoint[1] > bPoint[1]):
                                #Top-left or Bottom Right Diagonal
                                if self.y_vector < 0 or self.x_vector < 0:
                                    #Top Left Diagonal - No Changes on vector
                                    self.x_vector = newVector
                                    self.y_vector = newVector
                                else:
                                    if self.y_vector > 0 or self.x_vector > 0:
                                        #Bottom Right Diagonal - Invert Vector
                                        self.x_vector = -newVector
                                        self.y_vector = -newVector
                        else:
                            #Car is Diagonal - Assuming Orthogonal to the Border - Normal Bump - Invert Vector
                            self.x_vector = -self.x_vector
                            self.y_vector = -self.y_vector
                            #Vector Sanity Check
                            #Test if the vector is set away or towards the wall, and Refine direction if not
                            intersect_point = self.test_collision(track, False)
                            if intersect_point:
                                #Reset Vector to initial value
                                self.x_vector = -self.x_vector
                                self.y_vector = -self.y_vector
                                #Default Bump Vector - Max component of Vector
                                newVector = max(abs(self.x_vector),abs(self.y_vector))
                                #Force the Vector Diagonally if the car is diagonal and "parallel" to the Border
                                if (aPoint[0] < bPoint[0] and aPoint[1] < bPoint[1]) or (aPoint[0] > bPoint[0] and aPoint[1] > bPoint[1]):
                                    #Top-Right or Bottom Left Diagonal
                                    self.x_vector = newVector
                                    self.y_vector = -newVector

                                if (aPoint[0] > bPoint[0] and aPoint[1] < bPoint[1]) or (aPoint[0] < bPoint[0] and aPoint[1] > bPoint[1]):
                                    #Top-left or Bottom Right Diagonal
                                    self.x_vector = -newVector
                                    self.y_vector = -newVector
                    #Vector Sanity Check
                    #Test if the vector is set away or towards the wall, and invert if necessary
                    intersect_point = self.test_collision(track, True)
                    if intersect_point:
                        #Try inverting X
                        self.x_vector = -self.x_vector
                        intersect_point = self.test_collision(track, True)
                        if intersect_point:
                            #Try Inverting Y
                            self.x_vector = -self.x_vector
                            self.y_vector = -self.y_vector
                            intersect_point = self.test_collision(track, True)
                            if intersect_point:
                            #try inverting both
                                self.x_vector = -self.x_vector
                                intersect_point = self.test_collision(track, True)
                                if intersect_point:
                                #No movement as we're stuck
                                    self.y_vector = 0
                                    self.x_vector = 0
        self.bumping_vector_initialized = True

    def test_collision(self, track, simulate_next_step):
        track_mask = pygame.mask.from_surface(track.trackMask, 50)
        car_mask = pygame.mask.from_surface(self.sprites[self.sprite_angle], 50)
        x_test = 0
        y_test = 0
        if simulate_next_step:
            if self.x_vector > 0:
                x_test = self.vector_simulation_length
            else:
                if self.x_vector < 0:
                    x_test = -self.vector_simulation_length
            if self.y_vector > 0:
                y_test = self.vector_simulation_length
            else:
                if self.y_vector < 0:
                    y_test = -self.vector_simulation_length

        return track_mask.overlap(car_mask, ((round(self.x_position+x_test), round(self.y_position+y_test))))

    def calculate_crashing_vector(self,track):
        #Reposition car in a suitable spot - Move car backwards until no collision detected.
        #Invert vector
        self.x_vector = -self.x_vector
        self.y_vector = -self.y_vector

        intersect_point = self.test_collision(track, True)
        #Test if thr car is still collidign and keep moving backwards until not the case
        if intersect_point:
            #No movement as we're stuck
            self.y_vector = 0
            self.x_vector = 0


    def detect_collision(self, track):
        if DEBUG_COLLISION:
            print('Checking for Collision at ({},{})'.format(self.x_position, self.y_position))
        intersect_point = self.test_collision(track,False)
        collision = False
        if intersect_point:
            if not self.decelerating:
                #Check if the car is going into a border a going away from it (i.e. the tail touching the border)
                #If it is going away from the border then skip the Bump routine
                #Simulate  Vector of same direction as current vector and check if still colliding
                intersect_point2 = self.test_collision(track,True)
                if intersect_point2:
                    #Collision confirmed by next incremental move
                    collision = True
                else:
                    #Moving away from wall - Force End Bump routine
                    self.end_bump_loop()
            else:
                collision = True
        if collision:
            if self.max_speed_reached > 0:
                maxspeed_duration = pygame.time.get_ticks() - self.max_speed_reached
                #Less than 3 seconds at max_speed when coliding is a Bump
                if maxspeed_duration <= self.max_speed_crash_threshold:
                    self.init_bump_loop(track, intersect_point)
                else:
                    self.init_crash_loop(track, intersect_point)
            else:
                self.init_bump_loop(track, intersect_point)

    def init_bump_loop(self, track, intersect_point):
        self.bumping = True
        self.speed = self.bump_speed
        #Determine the agle at which angle the car is intersecting with the Border: either right angle or not
        #Lookup in the map for the closest intersection point and the polygon side that is intersecting
        self.x_intersect = intersect_point[0]
        self.y_intersect = intersect_point[1]
        self.collision_time = pygame.time.get_ticks()
        if DEBUG_BUMP:
            print('{} - Bump Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0
        pygame.time.set_timer(self.BUMPCLOUD, 20)
        #Search external borders other corners of the sprite in case no border poinst detected
        if not self.searchBorderSide(track.externalBorders):
            if not self.searchBorderSide(track.internalBorders):
                #Despite overlap detected no intersection with any side of the Track polygons has been found
                #Unable to determine the orientation of the colliding border
                if DEBUG_BUMP:
                    print('No Macthing Border Side found')
                self.end_bump_loop()

    def init_crash_loop(self, track, intersect_point):
        self.crashing = True
        self.crash_finished = False
        self.speed = 0
        self.x_intersect = intersect_point[0]
        self.y_intersect = intersect_point[1]

        self.collision_time = pygame.time.get_ticks()
        print('{} - Crash Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0
        pygame.time.set_timer(self.EXPLOSION, 28)

    def end_bump_loop(self):
        self.bumpingDiagonal = False
        self.bumpingHorizontal = False
        self.bumpingVertical = False
        self.bumping_vector_initialized = False
        self.bumping = False
        end_time = pygame.time.get_ticks()
        if DEBUG_BUMP:
            print('{} - Bump Terminated - Duration: {})'.format(end_time,end_time-self.collision_time))
        pygame.time.set_timer(self.BUMPCLOUD,0)

    def end_crash_loop(self):
        self.crashing = False
        self.crash_finished = False
        end_time = pygame.time.get_ticks()
        if DEBUG_CRASH:
            print('{} - Crash Terminated - Duration: {})'.format(end_time,end_time-self.collision_time))
        pygame.time.set_timer(self.EXPLOSION,0)


    def update_position(self, track):
        if self.crashing:
            self.calculate_crashing_vector(track)
        else:
            if not self.decelerating:
                #Calculate Vector - Accelarating means No skidding
                self.calculate_vector_from_sprite()
            else:
                if not self.rotating:
                    #Calculate Vector - Skidding
                    self.calculate_skidding_vector()
            if self.bumping:
                #Calculate Vector - Bumping
                self.calculate_bumping_vector(track)

        #Update Car Offset
        self.x_position += self.x_vector
        self.y_position += self.y_vector

        if not self.crashing:
            #Reset Rotation Flag to match Key Pressed Status
            self.rotating = False
            #If the car is not stopped Detect Track Borders. If not let it rotate over the edges & ignore collisions
            if self.speed > 0:
                self.detect_collision(track)
            else:
                if self.bumping:
                    #Force end of Bump Routine if car is not moving
                    self.end_bump_loop()
        else:
            #Car is not moving anymore
            self.x_vector = 0
            self.y_vector = 0
            self.speed = 0
            #End Crash Routine if animation has run to the end.
            if self.crash_finished:
                self.end_crash_loop()

    def blit(self, track):
        if not self.bumping:
            self.update_position(track)
        if self.bumping:
            #Ignore controls until Buming routine is finished - Force Skidding & Decelaration
            self.decelerating = True
            self.rotating = False
            self.update_position(track)
        #Car is not visible durign explosion
        if not self.crashing:
            gameDisplay.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
        #Blit Dust Cloud
        if self.bumping:
            event = pygame.event.wait()
            if event.type == self.BUMPCLOUD:
                self.displayBumpCloud()
            if self.animation_index <= 4:
                gameDisplay.blit(dust_cloud_frames[self.animation_index], (self.x_intersect, self.y_intersect))
        #Blit Explosion
        if self.crashing:
            event = pygame.event.wait()
            if event.type == self.EXPLOSION:
                self.displayExplosion()
                crash_duration = pygame.time.get_ticks() - self.collision_time
                if crash_duration >= self.max_crash_duration:
                    self.crash_finished = True
            if self.animation_index <= 4:
                gameDisplay.blit(explosion_frames[self.animation_index], (self.x_intersect, self.y_intersect))


    def displayBumpCloud(self):
        if DEBUG_BUMP:
            print('{} - Bump Timer triggerred'.format(pygame.time.get_ticks()))
        if self.animation_index < len(dust_cloud_frames):
            self.animation_index += 1

    def displayExplosion(self):
        if DEBUG_CRASH:
            print('{} - Crash Timer triggerred'.format(pygame.time.get_ticks()))
        if self.animation_index < len(explosion_frames):
            self.animation_index += 1


def game_loop():
    blueCar = Car()
    track1 = Track()

    gameExit = False

    while not gameExit:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            gameExit = True
        else:
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
            clock.tick(60)


game_loop()
