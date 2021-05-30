#pysprint_car.py
from typing import DefaultDict
import pygame
from pygame import Surface, gfxdraw
import math
import random
import pysprint_tracks

game_display = None
DEBUG_FINISH = False
DEBUG_COLLISION = False
DEBUG_BUMP = False
DEBUG_CRASH = False
DEBUG_AI = False

race_laps = None
display_width = None
display_height = None
dust_cloud_frames = None
explosion_frames = None


class Car:
    #Appearance
    #Color
    main_color = None
    secondary_color = None
    color_text = ""
    sprites = None
    first_car = None
    second_car = None
    third_car = None
    fourth_car = None
    start_screen_engine_position = None
    start_screen_thumb_position = None
    start_screen_text_position = None
    score_top_left = None
    prepare_to_race_counter = -1

    helicopter_frames = None
    vertical_helicopter_frames = None

    #Score
    score = 0
    #Track the last time score was incremented dur to progress in race (lap_count, gate_number)
    previous_score_increment = 0

    #Position & Vector
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

    x_position = 0
    y_position = 0
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
    progress_gate = -1
    ideal_vector = None
    next_mid_point = None
    next_gate = None

    #Mechanics
    #Car Controls
    accelerate_key = None
    left_key = None
    right_key = None
    joystick = None
    ignore_controls = False
    control_method_index = None

    #30FPS Settings
    rotation_step = .26
    acceleration_step = 0.13
    deceleration_step = 0.2
    bump_decelaration_step = 0.3
    drone_speed = 8
    player_speed = 8
    speed_max = 3
    bump_speed = 2
    drone_bump_speed = 2
    player__bump_speed = 6.5

    #60FPS Settings - Calibrated to an unmodified car
    # rotation_step = .13
    # acceleration_step = 0.065
    # deceleration_step = 0.1
    # bump_decelaration_step = 0.15
    # speed_max = 4
    # bump_speed = 3.25

    bump_animation_timer = 30
    crash_animation_timer = 30
    helicopter_step = 10

    #Collision Settings
    diagonal_detection_tolerance = 2
    vector_simulation_length = 10
    side_detection_tolerance = 7
    max_speed_crash_threshold = 3000
    #Threshold over which theer is a higher chance to crash
    speed_crash_probability_threshold = 0.85
    #% increase of probability to crash if condition is true
    speed_crash_probability_penalty = 1.2
    sensitive_border_crash_probability_penalty = 1.4
    #Max Random number drawn to calculate Crash probability
    crash_random_max = 60
    crash_certainty_treshold = 80

    #Car State
    is_drone = True
    decelerating = False
    rotating = False
    bumping = False
    crashing = False
    vertical_helicopter = False
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
    on_finish_line = True
    passed_finish_line_wrong_way = False
    lap_count = 0
    current_lap_start = 0
    lap_times = []

    best_lap = 0
    average_lap = 0

    #Car Events
    BUMPCLOUD = 0
    EXPLOSION = 0

    def start_game(self):
        self.is_drone = False
        self.ignore_controls = False
        self.speed_max = self.player_speed
        self.bump_speed = self.player__bump_speed

    def end_game(self):
        self.is_drone = True
        self.ignore_controls = False
        self.speed_max = self.drone_speed
        self.bump_speed = self.drone_bump_speed

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
        track_mask = pygame.mask.from_surface(track.track_mask, 50)
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
            #Only for player cars
            if not self.is_drone:
                maxspeed_duration = pygame.time.get_ticks() - self.max_speed_reached
                #More than xxx ms at max_speed when coliding is a certain crash
                if maxspeed_duration <= self.max_speed_crash_threshold:
                    return False
                else:
                    return True
            else:
                return False
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
        vertical = random.randint(0,1)
        if vertical == 1:
            self.vertical_helicopter = True
            self.helicopter_x = self.x_intersect - self.vertical_helicopter_frames[0].get_width()
            self.helicopter_y = display_height + self.vertical_helicopter_frames[0].get_height()
        else:
            self.vertical_helicopter = False
            self.helicopter_x = - self.helicopter_frames[0].get_width()
            self.helicopter_y = self.y_intersect - self.helicopter_frames[0].get_height()


        self.collision_time = pygame.time.get_ticks()
        if DEBUG_CRASH:
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
        #Detect if car collides with Finish line in the expected direction
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
                        self.average_lap =  sum(self.lap_times)/self.lap_count
                        if self.best_lap == 0:
                            self.best_lap = self.lap_times[self.lap_count-1]
                        else:
                            if self.best_lap > self.lap_times[self.lap_count-1]:
                                self.best_lap = self.lap_times[self.lap_count-1]

                        if self.lap_count == race_laps:
                            #Race finished
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
            self.ignore_controls = False
        if self.bumping:
            #Ignore controls until Buming routine is finished - Force Skidding & Decelaration
            self.decelerating = True
            self.rotating = False
            self.update_position(track)

    def blit(self, track):
        #Car is not visible durign explosion
        if not self.crashing:
            game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))

        if DEBUG_AI:
            if self.is_drone:
                gfxdraw.line(game_display,round(self.x_position), round(self.y_position), round(self.x_position) + round(self.x_vector)*10, round(self.y_position) + round(self.y_vector)*10, self.main_color)
                gfxdraw.line(game_display,round(self.x_position), round(self.y_position), round(self.ideal_vector[0] + self.x_position), round(self.y_position + self.ideal_vector[1]), (255,255,255))
                gfxdraw.circle(game_display, round(self.next_mid_point[0]), round(self.next_mid_point[1]), 5, self.main_color)
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
            if self.vertical_helicopter:
                if self.helicopter_y <= self.y_position:
                    game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
                game_display.blit(self.vertical_helicopter_frames[self.helicopter_index], (self.helicopter_x, self.helicopter_y))
            else:
                if self.helicopter_x >= self.x_position:
                    game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
                game_display.blit(self.helicopter_frames[self.helicopter_index], (self.helicopter_x, self.helicopter_y))


    def display_bump_cloud(self):
        if DEBUG_BUMP:
            print('{} - Increment Bump Frame'.format(pygame.time.get_ticks()))
        if self.animation_index < len(dust_cloud_frames):
            self.animation_index += 1


    def display_explosion(self):
        if self.vertical_helicopter:
            self.display_explosion_vertical()
        else:
            self.display_explosion_horizontal()

    def display_explosion_horizontal(self):
        if DEBUG_CRASH:
            print('{} - Blit Crash Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
        if self.animation_index < len(explosion_frames):
            self.animation_index += 1
        if self.helicopter_x < display_width:
            self.helicopter_x += self.helicopter_step
            if self.helicopter_index == len(self.helicopter_frames)-1:
                self.helicopter_index = 0
            else:
                self.helicopter_index += 1
        else:
            self.crash_finished = True

    def display_explosion_vertical(self):
        if DEBUG_CRASH:
            print('{} - Blit Crash Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
        if self.animation_index < len(explosion_frames):
            self.animation_index += 1
        if self.helicopter_y > 0 - self.vertical_helicopter_frames[0].get_height():
            self.helicopter_y -= self.helicopter_step
            if self.helicopter_index == len(self.vertical_helicopter_frames)-1:
                self.helicopter_index = 0
            else:
                self.helicopter_index += 1
        else:
            self.crash_finished = True

    def ai_drive(self, track: pysprint_tracks.Track):
        new_next_gate = track.find_progress_gate((self.x_position, self.y_position))
        new_next_gate += 2
        if self.next_gate is None:
            self.next_gate = new_next_gate
        else:
            #Eliminate edge cases where a gate is detected on another part of the circuit, i.e further than the actual next gate
            if abs(new_next_gate - self.next_gate) > 3 and abs(new_next_gate - self.next_gate) >= len(track.external_gate_points) - 3:
                self.next_gate+=2
            else:
                self.next_gate = new_next_gate

        if self.next_gate >= len(track.external_gate_points):
            self.next_gate -= len(track.external_gate_points)

        self.next_mid_point = ((track.external_gate_points[self.next_gate][0] + track.internal_gate_points[self.next_gate][0]) / 2, (track.external_gate_points[self.next_gate][1] + track.internal_gate_points[self.next_gate][1]) / 2)
        self.ideal_vector = (self.next_mid_point[0] - self.x_position, self.next_mid_point[1] - self.y_position)


        #cosine method
        dotProduct = self.ideal_vector[0] * self.x_vector + self.ideal_vector[1] * self.y_vector
        modOfVector1 = math.sqrt( self.ideal_vector[0] * self.ideal_vector[0] + self.ideal_vector[1]*self.ideal_vector[1])*math.sqrt(self.x_vector*self.x_vector + self.y_vector*self.y_vector)
        if modOfVector1 ==0:
            cosine_angle = 0
        else:
            cosine_angle = math.degrees(math.acos(dotProduct/modOfVector1))

        #sine method
        car_vector_length = math.sqrt(self.x_vector**2 + self.y_vector**2)
        cross_product = car_vector_length * math.sqrt(self.ideal_vector[0]**2 + self.ideal_vector[1]**2)
        # using cross-product formula
        if cross_product ==0:
            angle = 0
        else:
            angle = -math.degrees(math.asin((self.x_vector * self.ideal_vector[1] - self.y_vector * self.ideal_vector[0])/(cross_product)))

        if DEBUG_AI:
            print('{} - Next Gate:{} - Current Vector: ({:.2f},{:.2f}) - Ideal Vector: ({:.2f},{:.2f}) - Angle: {:.2f}° - Cosine Angle: {:.2f}°'.format(self.color_text, self.next_gate, self.x_vector, self.y_vector, self.ideal_vector[0], self.ideal_vector[1],angle, cosine_angle))

        if (angle > 20) or ( angle < -20):
            if angle > 0:
                self.rotate(True)
                if DEBUG_AI:
                    print ('Turning Left')
            else:
                self.rotate(False)
                if DEBUG_AI:
                    print ('Turning Right')
            if self.speed < self.speed_max:
                self.accelerate()
            else:
                self.decelerate()
        else:
            if cosine_angle > 160:
                #Pick a side to turn at random
                left = random.randint(0,1)
                self.rotate(left==1)
                if DEBUG_AI:
                    print ('180° - Turning Left')
                self.decelerate()
            else:
                self.accelerate()

