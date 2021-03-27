import pygame
import time
import math
import random

pygame.init()

display_width = 640
display_height = 400
flags = 0
race_laps = 100

#Scale screen
#flags = pygame.SCALED
DEBUG_FINISH = True
DEBUG_COLLISION = False
DEBUG_BUMP = False
DEBUG_CRASH = False
DEBUG_FLAG = False

game_display = pygame.display.set_mode((display_width, display_height), flags)
clock = pygame.time.Clock()

#Flag Events
GREENFLAG = pygame.USEREVENT + 50
WHITEFLAG = GREENFLAG + 1
CHECKEREDFLAG = WHITEFLAG + 1


green_flag_frames = {
    0:pygame.image.load('Assets/GreenFlag0.png').convert_alpha(),
    1:pygame.image.load('Assets/GreenFlag1.png').convert_alpha(),
    2:pygame.image.load('Assets/GreenFlag2.png').convert_alpha(),
    3:pygame.image.load('Assets/GreenFlag3.png').convert_alpha(),
    4:pygame.image.load('Assets/GreenFlag4.png').convert_alpha(),
    5:pygame.image.load('Assets/GreenFlag5.png').convert_alpha(),
    6:pygame.image.load('Assets/GreenFlag6.png').convert_alpha(),
}

helicopter_frames = {
    0:pygame.image.load('Assets/Helicopter0.png').convert_alpha(),
    1:pygame.image.load('Assets/Helicopter1.png').convert_alpha(),
    2:pygame.image.load('Assets/Helicopter2.png').convert_alpha(),
}

helicopter_step = 10

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

    flag_anchor = (320, 28)

    external_borders = [
        (101, 52, 0),
        (544, 53, 1),
        (560, 54, 1),
        (577, 59, 1),
        (591, 71, 1),
        (601, 84, 1),
        (606, 96, 1),
        (608, 110, 0),
        (610, 331, 1),
        (572, 364, 1),
        (545, 368, 1),
        (449, 371, 0),
        (437, 369, 0),
        (273, 224, 0),
        (263, 224, 1),
        (257, 229, 1),
        (256, 231, 1),
        (257, 258, 1),
        (257, 273, 1),
        (266, 318, 1),
        (266, 354, 1),
        (247, 373, 1),
        (99, 373, 0),
        (71, 368, 1),
        (35, 330, 1),
        (37, 112, 0),
        (40, 93, 1),
        (46, 79, 1),
        (64, 59, 1),
        (75, 55, 1),
        (84, 51, 1)
        ]

    internal_borders = [
        (133, 134,1),
        (129, 143,1),
        (125, 153,1),
        (124, 295,1),
        (132, 305,1),
        (143, 307,1),
        (157, 298,1),
        (161, 163,1),
        (178, 148,1),
        (292, 148,1),
        (314, 152,1),
        (333, 161,1),
        (489, 306,1),
        (499, 307,1),
        (504, 302,1),
        (512, 299,1),
        (512, 141,1),
        (503, 131,1),
        (137, 130,1)
    ]

    finish_line = pygame.Rect(346, 48,4,82)
    finish_line_direction = -1


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

    angle_vector_sign = {
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
    a_intersect_side = (0, 0)
    b_intersect_side = (0, 0)
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

    #60FPS Settings - Calibrated to an unmodified car
    rotation_step = .16
    acceleration_step = 0.065
    deceleration_step = 0.9
    bump_decelaration_step = 0.25
    speed_max = 4
    bump_speed = 3.25



    bump_animation_timer = 30
    crash_animation_timer = 40

    #Collision Settings
    diagonal_detection_tolerance = 2
    vector_simulation_length = 10
    side_detection_tolerance = 7
    max_speed_crash_threshold = 2000
    #Threshold over which theer is a higher chance to crash
    speed_crash_probability_threshold = 0.8
    #% increase of probability to crash if condition is true
    speed_crash_probability_penalty = 1.2
    sensitive_border_crash_probability_penalty = 1.4
    #Max Random number drawn to calculate Crash probability
    crash_random_max = 60
    crash_certainty_treshold = 80

    #Car State
    decelerating = False
    rotating = False
    bumping = False
    crashing = False
    bumping_vector_initialized = False
    bumping_vertical = False
    bumping_horizontal = False
    bumping_diagonal = False
    crash_finished = False
    animation_index = 0
    helicopter_index = 0
    helicopter_x = 0
    helicopter_y = 0
    collision_time = 0
    max_speed_reached = 0
    on_finish_line = False
    passed_finish_line_wrong_way = False
    lap_count = 0
    current_lap_start = 0
    lap_times = [0,0,0,0]
    best_lap = 0
    average_Lap = 0

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

    def search_border_side(self, polygon_border, bumping):
        if bumping:
            self.bumping_diagonal = False
            self.bumping_horizontal = False
            self.bumping_vertical = False
        for i in range(0, len(polygon_border)):
            next_index = i+1
            if next_index == len(polygon_border):
                next_index = 0
            top = 0
            left = 0
            if polygon_border[i][0] <= polygon_border[next_index][0]:
                top = polygon_border[i][0]
            else:
                top = polygon_border[next_index][0]
            if polygon_border[i][1] <= polygon_border[next_index][1]:
                left = polygon_border[i][1]
            else:
                left = polygon_border[next_index][1]

            rect_width = abs(polygon_border[next_index][0]-polygon_border[i][0])
            if rect_width == 0:
                rect_width = 1
            rect_height = abs(polygon_border[next_index][1]-polygon_border[i][1])
            if rect_height == 0:
                rect_height = 1
            wall_rect = pygame.Rect(top, left, rect_width, rect_height)
            #Enlarge detection Box to maximize chance of hitting a polygon side
            sprite_rect = pygame.Rect(self.x_intersect-self.side_detection_tolerance, self.y_intersect-self.side_detection_tolerance, self.side_detection_tolerance*2, self.side_detection_tolerance*2)

            if sprite_rect.colliderect(wall_rect):
                if DEBUG_COLLISION:
                    print('found matching pair of points ({},{})'.format(polygon_border[i],polygon_border[next_index]))
                self.a_intersect_side = polygon_border[i]
                self.b_intersect_side = polygon_border[next_index]
                if (abs(polygon_border[i][0]-polygon_border[next_index][0]) <= self.diagonal_detection_tolerance) and (abs(polygon_border[i][1]-polygon_border[next_index][1]) > self.diagonal_detection_tolerance):
                    if DEBUG_COLLISION:
                        print('x delta <={} - looks vertical enough'.format(self.diagonal_detection_tolerance))
                    if bumping:
                        self.bumping_vertical = True
                    return True
                if (abs(polygon_border[i][0]-polygon_border[next_index][0])>self.diagonal_detection_tolerance) and (abs(polygon_border[i][1]-polygon_border[next_index][1])<=self.diagonal_detection_tolerance):
                    if DEBUG_COLLISION:
                        print('y delta <={} - looks horizontal enough'.format(self.diagonal_detection_tolerance))
                    if bumping:
                        self.bumping_horizontal = True
                    return True
                if DEBUG_COLLISION:
                    print('Diagonal Bumping')
                if bumping:
                    self.bumping_diagonal = True
                    self.bumping_horizontal = False
                    self.bumping_vertical = False
                return True
        return False

    def calculate_vector_from_sprite(self):
        self.sin_angle = math.sin(math.radians(abs(self.sprite_angle*22.5-90)))
        self.y_vector = abs(self.speed * self.sin_angle)
        self.y_vector = self.y_vector * self.angle_vector_sign[self.sprite_angle][1]
        self.x_vector = math.sqrt(self.speed*self.speed-self.y_vector*self.y_vector)
        self.x_vector = self.x_vector * self.angle_vector_sign[self.sprite_angle][0]

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
            if self.bumping_vertical:
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
                if self.bumping_horizontal:
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
                    if self.bumping_diagonal:
                        #Diagonal Bumping: Bump Diagnoally if hit Horizontally - or Vertically  - Vert or Horiz Bump if hit diagonally
                        a_point = self.a_intersect_side
                        b_point = self.b_intersect_side

                        if self.x_vector == 0 or self.y_vector == 0:
                            #Car is moving Horizontally or Vertical - Force 45 degree angle
                            self.sin_angle = math.sin(math.radians(abs(45)))
                            new_vector = abs(self.speed * self.sin_angle)

                            if (a_point[0] < b_point[0] and a_point[1] < b_point[1]) or (a_point[0] > b_point[0] and a_point[1] > b_point[1]):
                                #Top-Right or Bottom Left Diagonal
                                if self.y_vector > 0 or self.x_vector < 0:
                                    #Bottom Left Diagonal - Invert Y Component
                                    self.x_vector = new_vector
                                    self.y_vector = -new_vector
                                else:
                                    if self.y_vector < 0 or self.x_vector > 0:
                                        #Top Right Diagonal - Invert X Component
                                        self.x_vector = -new_vector
                                        self.y_vector = new_vector

                            if (a_point[0] > b_point[0] and a_point[1] < b_point[1]) or (a_point[0] < b_point[0] and a_point[1] > b_point[1]):
                                #Top-left or Bottom Right Diagonal
                                if self.y_vector < 0 or self.x_vector < 0:
                                    #Top Left Diagonal - No Changes on vector
                                    self.x_vector = new_vector
                                    self.y_vector = new_vector
                                else:
                                    if self.y_vector > 0 or self.x_vector > 0:
                                        #Bottom Right Diagonal - Invert Vector
                                        self.x_vector = -new_vector
                                        self.y_vector = -new_vector
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
                                new_vector = max(abs(self.x_vector),abs(self.y_vector))
                                #Force the Vector Diagonally if the car is diagonal and "parallel" to the Border
                                if (a_point[0] < b_point[0] and a_point[1] < b_point[1]) or (a_point[0] > b_point[0] and a_point[1] > b_point[1]):
                                    #Top-Right or Bottom Left Diagonal
                                    self.x_vector = new_vector
                                    self.y_vector = -new_vector

                                if (a_point[0] > b_point[0] and a_point[1] < b_point[1]) or (a_point[0] < b_point[0] and a_point[1] > b_point[1]):
                                    #Top-left or Bottom Right Diagonal
                                    self.x_vector = -new_vector
                                    self.y_vector = -new_vector
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
            if  self.detect_crash(track):
                self.init_crash_loop(track, intersect_point)
            else:
                self.init_bump_loop(track, intersect_point)

    def detect_crash(self, track):
        if self.max_speed_reached > 0:
            maxspeed_duration = pygame.time.get_ticks() - self.max_speed_reached
            #More than xxx ms at max_speed when coliding is a certain crash
            if maxspeed_duration <= self.max_speed_crash_threshold:
                return False
            else:
                return True
        else:
            #There is a random chance to Crash, increased:
            crash_probability = random.randint(1,self.crash_random_max)
            #1- If Speed is higher than xx% of max speed
            if self.speed >= self.speed_crash_probability_threshold * self.speed_max:
                crash_probability = crash_probability * self.speed_crash_probability_penalty
            #2- If A sensitive Border has been hit
            if self.search_border_side(track.external_borders, False) or self.search_border_side(track.internal_borders, False):
                if self.a_intersect_side[2] == 1 and self.b_intersect_side[2] == 1:
                    crash_probability = crash_probability * self.sensitive_border_crash_probability_penalty
            if crash_probability > self.crash_certainty_treshold:
                return True
            else:
                return False


    def init_bump_loop(self, track, intersect_point):
        self.bumping = True
        self.speed = self.bump_speed
        #Determine the agle at which angle the car is intersecting with the Border: either right angle or not
        #Lookup in the map for the closest intersection point and the polygon side that is intersecting
        self.x_intersect = intersect_point[0]
        self.y_intersect = intersect_point[1]
        self.collision_time = pygame.time.get_ticks()
        #Search external borders other corners of the sprite in case no border poinst detected
        if not self.search_border_side(track.external_borders, True):
            if not self.search_border_side(track.internal_borders, True):
                #Despite overlap detected no intersection with any side of the Track polygons has been found
                #Unable to determine the orientation of the colliding border
                if DEBUG_BUMP:
                    print('No Macthing Border Side found')
                self.end_bump_loop()
        if DEBUG_BUMP:
            print('{} - Bump Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0
        pygame.time.set_timer(self.BUMPCLOUD, self.bump_animation_timer)

    def init_crash_loop(self, track, intersect_point):
        self.crashing = True
        self.crash_finished = False
        self.speed = 0
        self.x_intersect = intersect_point[0]
        self.y_intersect = intersect_point[1]
        self.helicopter_x = - helicopter_frames[0].get_width()
        self.helicopter_y = self.y_intersect - helicopter_frames[0].get_height()
        self.collision_time = pygame.time.get_ticks()
        print('{} - Crash Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0
        self.helicopter_index = 0
        pygame.time.set_timer(self.EXPLOSION, self.crash_animation_timer)

    def end_bump_loop(self):
        self.bumping_diagonal = False
        self.bumping_horizontal = False
        self.bumping_vertical = False
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

    def test_finish_line(self, track):
        #Detech if car collides with Finish line in the expected direction
        sprite_rect = pygame.Rect(self.x_position, self.y_position, self.sprites[self.sprite_angle].get_width(), self.sprites[self.sprite_angle].get_height())
        if sprite_rect.colliderect(track.finish_line):
            if not self.on_finish_line:
                self.on_finish_line = True
                if self.x_vector * track.finish_line_direction > 0:
                    if self.passed_finish_line_wrong_way:
                        self.passed_finish_line_wrong_way = False
                        if DEBUG_FINISH:
                            print('{} - Passed the line in the right direction after going the wrong way)'.format(pygame.time.get_ticks()))
                    else:
                        finish_time = pygame.time.get_ticks()
                        self.lap_times[self.lap_count] = finish_time - self.current_lap_start
                        if DEBUG_FINISH:
                            print('{} - New Lap {} - Duration: {})'.format(finish_time, self.lap_count, self.lap_times[self.lap_count]))
                        self.lap_count+=1
                        if self.lap_count == race_laps:
                            #Race finished
                            self.average_Lap =  sum(self.lap_times)/race_laps
                            self.best_lap = min(self.lap_times)
                            if DEBUG_FINISH:
                                print('{} - Race Finished - Duration: {} - Average lap: {} - Best Lap: {})'.format(finish_time, sum(self.lap_times), self.average_Lap, self.best_lap))
                            return True
                        self.current_lap_start = finish_time
                        return False
                else:
                    self.passed_finish_line_wrong_way = True
                    if DEBUG_FINISH:
                        print('{} - Passed the line in the wrong direction)'.format(pygame.time.get_ticks()))
        else:
            self.on_finish_line = False


    def draw(self, track):
        #Draw Car
        if not self.bumping:
            self.update_position(track)
        if self.bumping:
            #Ignore controls until Buming routine is finished - Force Skidding & Decelaration
            self.decelerating = True
            self.rotating = False
            self.update_position(track)

    def blit(self, track):
        #Car is not visible durign explosion
        if not self.crashing:
            game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
        #Blit Dust Cloud if Bumping
        if self.bumping:
            if DEBUG_BUMP:
                print('{} - Blit Bump Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
            if self.animation_index <= 4:
                game_display.blit(dust_cloud_frames[self.animation_index], (self.x_intersect, self.y_intersect))
        #Blit Explosion & Helicopter
        if self.crashing:
            if self.animation_index <= 4:
                game_display.blit(explosion_frames[self.animation_index], (self.x_intersect, self.y_intersect))
            if self.helicopter_x >= self.x_position:
                game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
            game_display.blit(helicopter_frames[self.helicopter_index], (self.helicopter_x, self.helicopter_y))


    def display_bump_cloud(self):
        if DEBUG_BUMP:
            print('{} - Increment Bump Frame'.format(pygame.time.get_ticks()))
        if self.animation_index < len(dust_cloud_frames):
            self.animation_index += 1

    def display_explosion(self):
        if DEBUG_CRASH:
            print('{} - Blit Crash Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
        if self.animation_index < len(explosion_frames):
            self.animation_index += 1
        if self.helicopter_x < display_width:
            self.helicopter_x += helicopter_step
            if self.helicopter_index == len(helicopter_frames)-1:
                self.helicopter_index = 0
            else:
                self.helicopter_index += 1
        else:
            self.crash_finished = True


def game_loop():
    blue_car = Car()
    track1 = Track()

    game_exit = False
    race_start = True
    animation_index = 0
    flag_waves = 0
    wave_up = True
    pygame.time.set_timer(GREENFLAG, 40)
    while not game_exit:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            game_exit = True
        else:
            if not blue_car.bumping:
                if pygame.key.get_pressed()[pygame.K_RCTRL]:
                    blue_car.accelerate()
                else:
                    blue_car.decelerate()

                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    blue_car.rotate(True)

                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    blue_car.rotate(False)
            else:
                blue_car.decelerate()

            for event in pygame.event.get():
                if not blue_car.bumping:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RCTRL:
                            blue_car.accelerate()
                        if event.key == pygame.K_LEFT:
                            blue_car.rotate(True)
                        if event.key == pygame.K_RIGHT:
                            blue_car.rotate(False)
                else:
                    blue_car.decelerate()
                #Draw Dust Cloud
                if event.type == blue_car.BUMPCLOUD:
                    if DEBUG_BUMP:
                        print('{} - Bump Timer triggerred'.format(pygame.time.get_ticks()))
                    if blue_car.bumping:
                        blue_car.display_bump_cloud()
                #Draw Explosion
                if event.type == blue_car.EXPLOSION:
                    if DEBUG_CRASH:
                        print('{} - Crash Timer triggerred'.format(pygame.time.get_ticks()))
                    if blue_car.crashing:
                        blue_car.display_explosion()
                #Draw Green Flag at Race Start
                if event.type == GREENFLAG:
                    if DEBUG_FLAG:
                        print('{} - Flag Timer triggerred'.format(pygame.time.get_ticks()))
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
            blue_car.draw(track1)
            game_display.blit(track1.background, (0, 0))
            if race_start:
                game_display.blit(green_flag_frames[animation_index],track1.flag_anchor)
            blue_car.blit(track1)
            game_exit = blue_car.test_finish_line(track1)
            pygame.display.update()
            clock.tick(60)

game_loop()
