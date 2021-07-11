#pysprint_car.py
from typing import DefaultDict
from numpy import True_, angle, select
import pygame
from pygame import Surface, gfxdraw
import math
import random

from pygame.key import name
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


    #30FPS Default Settings
    player_rotation_step = .26
    player_acceleration_step = 0.18
    player_deceleration_step = 0.2
    player_bump_decelaration_step = 0.3
    player__bump_speed = 4
    player_speed = 8

    #AI Default Characteristics
    drone_personalities = [
        ("Prudent",0),
        ("Normal",1),
        ("Aggressive",2)
    ]
    drone_personality_modifiers = [0.9,1,1.1]
    drone__invert_personality_modifiers = [1.1,1,0.9]
    drone_rotation_step = 0.4#.4
    drone_acceleration_step = 0.18#0.18
    drone_deceleration_step = 0.4#0.4
    drone_bump_decelaration_step = 0.3#0.3
    drone_bump_speed = 4#2
    drone_speed = 4#6
    turning_angle_threshold = 20
    gate_step = 1#2

    #60FPS Settings - Calibrated to an unmodified car
    # rotation_step = .13
    # acceleration_step = 0.065
    # deceleration_step = 0.1
    # bump_decelaration_step = 0.15
    # speed_max = 4
    # bump_speed = 3.25

    #Animation Constants
    bump_animation_timer = 33
    crash_animation_timer = 33
    helicopter_step = 15

    #Collision Settings
    diagonal_detection_tolerance = 2
    vector_simulation_length = 10
    side_detection_tolerance = 7
    max_speed_crash_threshold = 3000
    collision_area_threshold = 75
    #Threshold over which theer is a higher chance to crash
    speed_crash_probability_threshold = 0.85
    #% increase of probability to crash if condition is true
    speed_crash_probability_penalty = 1.2
    sensitive_border_crash_probability_penalty = 1.4
    #Max Random number drawn to calculate Crash probability
    crash_random_max = 60
    crash_certainty_treshold = 85#80


    def __init__(self):
        #Appearance
        #Color
        self.main_color = None
        self.secondary_color = None
        self.color_text = ""
        self.sprites = None
        self.first_car = None
        self.second_car = None
        self.third_car = None
        self.fourth_car = None
        self.start_screen_engine_position = None
        self.start_screen_thumb_position = None
        self.start_screen_text_position = None
        self.score_top_left = None
        self.prepare_to_race_counter = -1

        self.helicopter_frames = None
        self.vertical_helicopter_frames = None

        #Score
        self.score = 0
        self.game_over = False
        self.enter_high_score = False
        self.enter_best_lap = False
        self.lap_times = []
        self.best_lap = 0
        self.best_laps = []
        self.average_lap = 0
        self.high_score_rank = 0
        self.high_score_name = ""
        self.current_initial = 0

        #Track the last time score was incremented due to progress in race (lap_count, gate_number)
        self.previous_score_increment = 0

        self.x_position = 0
        self.y_position = 0
        self.sprite_angle = 12
        self.angle = 12
        self.speed = 0
        self.a_intersect_side = (0, 0)
        self.b_intersect_side = (0, 0)
        self.x_intersect = 0
        self.y_intersect = 0
        self.x_vector = 0
        self.y_vector = 0
        self.sin_angle = 0
        self.progress_gate = -1
        self.ideal_vector = None
        self.next_mid_point = None
        self.next_gate = None

        #Mechanics
        #Car Controls
        self.accelerate_key = None
        self.left_key = None
        self.right_key = None
        self.joystick = None
        self.ignore_controls = False
        self.control_method_index = None



        self.speed_max = 3
        self.bump_speed = 2
        self.rotation_step = .26
        self.acceleration_step = 0.13
        self.deceleration_step = 0.2
        self.bump_decelaration_step = 0.3

        self.drone_personality = 1

        #Car State
        self.is_drone = True
        self.decelerating = False
        self.rotating = False
        self.bumping = False
        self.crashing = False
        self.vertical_helicopter = False
        self.bumping_vector_initialized = False
        self.bumping_vertical = False
        self.bumping_horizontal = False
        self.bumping_diagonal = False
        self.crash_finished = False
        self.animation_index = 0
        self.helicopter_index = 0
        self.helicopter_x = 0
        self.helicopter_y = 0
        self.collision_time = 0
        self.max_speed_reached = 0
        self.on_finish_line = True
        self.passed_finish_line_wrong_way = False
        self.lap_count = 0
        self.current_lap_start = 0
        self.drone_repeat_bumping_counter = 0
        self.drone_repeat_bumping_timer = 0
        self.mandatory_gates_crossed = []

    def save_best_lap(self, track: pysprint_tracks.Track):
        saved = False
        if self.best_lap > 0:
            for lap_time in self.best_laps:
                if lap_time[1] == track.track_number:
                    if lap_time[0] > self.best_lap:
                        lap_time = (self.best_lap, track.track_number)
                        saved = True
            if not saved:
                self.best_laps.append((self.best_lap, track.track_number))

    def set_bumping(self, is_bumping):
        if self.is_drone:
            if is_bumping and not self.bumping and self.drone_repeat_bumping_counter==0 and self.drone_repeat_bumping_timer ==0:
                #First time the car is set to bumping
                self.drone_repeat_bumping_counter += 1
                self.drone_repeat_bumping_timer = pygame.time.get_ticks()
            else:
                if is_bumping and self.drone_repeat_bumping_counter>0:
                    #Subsequent Bumps - reset counters if more than  a second apart
                    if (pygame.time.get_ticks() - self.drone_repeat_bumping_timer) >= 1000:
                        self.drone_repeat_bumping_counter = 0
                        self.drone_repeat_bumping_timer = 0
                    else:
                        self.drone_repeat_bumping_counter += 1

        self.bumping = is_bumping


    def move_initial_character(self, left):
        current_code = ord(self.high_score_name[self.current_initial])
        if left:
            if (current_code > 48 and current_code <= 57) or (current_code > 65 and current_code <= 90):
                current_code -= 1
            else:
                if current_code == 48:
                    current_code = 90
                else:
                    if current_code == 65:
                        current_code = 57
        else:
            if (current_code >= 48 and current_code < 57) or (current_code >= 65 and current_code < 90):
                current_code += 1
            else:
                if current_code == 90:
                    current_code = 48
                else:
                    if current_code == 57:
                        current_code = 65
        name_list = list(self.high_score_name)
        name_list[self.current_initial] = chr(current_code)
        self.high_score_name = "".join(name_list)

    def validate_initial_character(self):
        self.current_initial += 1
        if self.current_initial <=2:
            if len(self.high_score_name)<=self.current_initial:
                name_list = list(self.high_score_name)
                name_list.append("A")
                self.high_score_name = "".join(name_list)

    def reset_game_over(self):
        self.game_over = False
        self.enter_high_score = False
        self.enter_best_lap = False
        self.lap_times = []
        self.best_lap = 0
        self.average_lap = 0
        self.score = 0
        self.high_score_rank = 0
        self.high_score_name = ""

    def start_game(self):
        if self.game_over==False:
            self.reset_game_over()
        self.is_drone = False
        self.ignore_controls = False
        self.speed_max = self.player_speed
        self.bump_speed = self.player__bump_speed
        self.rotation_step = self.player_rotation_step
        self.acceleration_step = self.player_acceleration_step
        self.deceleration_step = self.player_deceleration_step
        self.bump_decelaration_step = self.player_bump_decelaration_step

    def end_game(self):
        self.game_over = True
        self.is_drone = True
        self.ignore_controls = False
        self.speed_max = self.drone_speed
        self.bump_speed = self.drone_bump_speed
        self.rotation_step = self.drone_rotation_step
        self.acceleration_step = self.drone_acceleration_step
        self.deceleration_step = self.drone_deceleration_step
        self.bump_decelaration_step = self.drone_bump_decelaration_step

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
        if polygon_border is None:
            return False
        else:
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

    def calculate_bumping_vector(self,track: pysprint_tracks.Track):
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

    def test_collision(self, track: pysprint_tracks.Track, simulate_next_step):
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

    def test_collision_area(self, track: pysprint_tracks.Track, simulate_next_step):
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

        return track_mask.overlap_area(car_mask, ((round(self.x_position+x_test), round(self.y_position+y_test))))


    def calculate_crashing_vector(self,track: pysprint_tracks.Track):
        #Reposition car in a suitable spot - Move car backwards until no collision detected.
        #Invert vector
        self.x_vector = -self.x_vector
        self.y_vector = -self.y_vector

        intersect_point = self.test_collision(track, True)
        #Test if thr car is still collidign and keep moving backwards until not the case
        if intersect_point:
            #No movement as we're stuck
            if DEBUG_COLLISION:
                print('Stuck at ({},{})'.format(self.x_position, self.y_position))
            self.y_vector = 0
            self.x_vector = 0


    def detect_collision(self, track: pysprint_tracks.Track):
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
                self.init_crash_loop(intersect_point)
            else:
                self.init_bump_loop(track, intersect_point)

    def detect_crash(self, track: pysprint_tracks.Track):

        #if overlap between car and circuit mask > collision_area_threshold pixels  crash is forced to avoid traversing walls and gates
        area = self.test_collision_area(track,False)
        if DEBUG_CRASH:
            print('collision area : {}'.format(area))

        if  area > self.collision_area_threshold:
            return True

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
            if self.search_border_side(track.external_borders, False) or self.search_border_side(track.internal_borders, False) or self.search_border_side(track.secondary_internal_borders, False):
                if self.a_intersect_side[2] == 1 and self.b_intersect_side[2] == 1:
                    crash_probability = crash_probability * self.sensitive_border_crash_probability_penalty
            if crash_probability > self.crash_certainty_treshold:
                return True
            else:
                return False


    def init_bump_loop(self, track: pysprint_tracks.Track, intersect_point):
        self.set_bumping(True)
        self.speed = self.bump_speed
        #Determine the agle at which angle the car is intersecting with the Border: either right angle or not
        #Lookup in the map for the closest intersection point and the polygon side that is intersecting
        self.x_intersect = intersect_point[0]
        self.y_intersect = intersect_point[1]
        self.collision_time = pygame.time.get_ticks()
        #Search external borders other corners of the sprite in case no border poinst detected
        #Also search secondary Internal brders like roundabouts
        if not self.search_border_side(track.external_borders, True):
            if not self.search_border_side(track.internal_borders, True):
                if not self.search_border_side(track.secondary_internal_borders, True):
                    #Despite overlap detected no intersection with any side of the Track polygons has been found
                    #Unable to determine the orientation of the colliding border
                    if DEBUG_BUMP:
                        print('No Macthing Border Side found')
                    self.end_bump_loop()
        if DEBUG_BUMP:
            print('{} - Bump Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0

    def init_crash_loop(self, intersect_point):
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

    def end_bump_loop(self):
        self.bumping_diagonal = False
        self.bumping_horizontal = False
        self.bumping_vertical = False
        self.bumping_vector_initialized = False
        self.set_bumping(False)
        end_time = pygame.time.get_ticks()
        if DEBUG_BUMP:
            print('{} - Bump Terminated - Duration: {})'.format(end_time,end_time-self.collision_time))

    def end_crash_loop(self):
        self.crashing = False
        self.crash_finished = False
        end_time = pygame.time.get_ticks()
        if DEBUG_CRASH:
            print('{} - Crash Terminated - Duration: {})'.format(end_time,end_time-self.collision_time))


    def update_position(self, track: pysprint_tracks.Track):
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
                #If car is not moving, check for colision area size. Force crash
                area = self.test_collision_area(track,False)
                if area>self.collision_area_threshold:
                    intersect_point = self.test_collision(track,False)
                    self.init_crash_loop(intersect_point)
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

    def test_mandatory_gates(self, track: pysprint_tracks.Track):
        if track.mandatory_gates is None:
            return
        else:
            if len(track.mandatory_gates) > len(self.mandatory_gates_crossed):
                #Check whcih is the next Mandatory gate to cross and add it as crossed if collision if not already added
                next_gate = track.mandatory_gates[len(self.mandatory_gates_crossed)]
                gate_rect = pygame.Rect(min(track.internal_gate_points[next_gate][0],track.external_gate_points[next_gate][0]), min(track.internal_gate_points[next_gate][1],track.external_gate_points[next_gate][1]), abs(track.internal_gate_points[next_gate][0]-track.external_gate_points[next_gate][0]), abs(track.internal_gate_points[next_gate][1]-track.external_gate_points[next_gate][1]))
                sprite_rect = pygame.Rect(self.x_position, self.y_position, self.sprites[self.sprite_angle].get_width(), self.sprites[self.sprite_angle].get_height())
                if sprite_rect.colliderect(gate_rect):
                    #if gate is passed
                    self.mandatory_gates_crossed.append(next_gate)

    def test_finish_line(self, track: pysprint_tracks.Track):
        self.test_mandatory_gates(track)
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
                        #Check if all mandatory gates were passed before awarding a new lap
                        full_lap = False
                        if track.mandatory_gates is None:
                            full_lap = True
                        else:
                            if len(self.mandatory_gates_crossed)==len(track.mandatory_gates):
                                full_lap = True
                                #reset Gates tracker for the next lap
                                self.mandatory_gates_crossed.clear()
                        if full_lap:
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
                                    print('{} - Race Finished - Duration: {} - Average lap: {} - Best Lap: {})'.format(finish_time, sum(self.lap_times), self.average_lap, self.best_lap))
                                return True
                            self.current_lap_start = finish_time
                            return False
                        else:
                             print('{} - Passed the line in the right directionbut not all mandatory gates passed)'.format(pygame.time.get_ticks()))
                else:
                    self.passed_finish_line_wrong_way = True
                    if DEBUG_FINISH:
                        print('{} - Passed the line in the wrong direction)'.format(pygame.time.get_ticks()))
        else:
            self.on_finish_line = False


    def draw(self, track: pysprint_tracks.Track):
        #Draw Car
        if not self.bumping:
            self.update_position(track)
            self.ignore_controls = False
        if self.bumping:
            #Ignore controls until Buming routine is finished - Force Skidding & Decelaration
            self.decelerating = True
            self.rotating = False
            self.update_position(track)

    def blit(self, track: pysprint_tracks.Track, overlay_blitted):
        #Cars are blited under teh overlay to be hidden but not dust clouds, explisions and the helicopter
        if not overlay_blitted:
            #Car is not visible durign explosion
            if not self.crashing:
                game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
            # else:
            #     if self.vertical_helicopter:
            #         if self.helicopter_y <= self.y_position:
            #             game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
            #     else:
            #         if self.helicopter_x >= self.x_position:
            #             game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))

            if DEBUG_AI:
                if self.is_drone:
                    gfxdraw.line(game_display,round(self.x_position), round(self.y_position), round(self.x_position) + round(self.x_vector)*10, round(self.y_position) + round(self.y_vector)*10, self.main_color)
                    if not self.ideal_vector is None:
                        gfxdraw.line(game_display,round(self.x_position), round(self.y_position), round(self.ideal_vector[0] + self.x_position), round(self.y_position + self.ideal_vector[1]), (255,255,255))
                    if not self.next_mid_point is None:
                        gfxdraw.circle(game_display, round(self.next_mid_point[0]), round(self.next_mid_point[1]), 5, self.main_color)

        if overlay_blitted:
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
                    game_display.blit(self.vertical_helicopter_frames[self.helicopter_index], (self.helicopter_x, self.helicopter_y))
                else:
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

    def calculate_ideal_vector(self, track: pysprint_tracks.Track, actual_gate_step):
        new_next_gate = track.find_progress_gate((self.x_position, self.y_position))
        new_next_gate += actual_gate_step
        if self.next_gate is None:
            self.next_gate = new_next_gate
        else:
            #Eliminate edge cases where a gate is detected on another part of the circuit, i.e further than the actual next gate
            if abs(new_next_gate - self.next_gate) > (actual_gate_step+1) and abs(new_next_gate - self.next_gate) >= len(track.external_gate_points) - (actual_gate_step+1):
                self.next_gate+=actual_gate_step
            else:
                #Eliminate cases where the AI is tempte to cut the roundabout
                if abs(new_next_gate - self.next_gate) > (actual_gate_step+1) and abs(new_next_gate - self.next_gate) < 6:
                    self.next_gate+=actual_gate_step
                else:
                    #Eliminate edge cases where the new next gate is behind the previous next next gate
                    if new_next_gate >= self.next_gate:
                        self.next_gate = new_next_gate

        if self.next_gate >= len(track.external_gate_points):
            self.next_gate -= len(track.external_gate_points)

        #Midpoint modifier: Normal personality aime for the exact middle of the gate, prudent and aggressive symetrically outcentered
        midpOint_modifier = 2 * (1 + (self.drone_personality_modifiers[self.drone_personality]-1) / 8)

        self.next_mid_point = ((track.external_gate_points[self.next_gate][0] + track.internal_gate_points[self.next_gate][0]) / midpOint_modifier, (track.external_gate_points[self.next_gate][1] + track.internal_gate_points[self.next_gate][1]) / midpOint_modifier)
        self.ideal_vector = (self.next_mid_point[0] - self.x_position, self.next_mid_point[1] - self.y_position)

    def get_cosine(self):
        #cosine method
        dotProduct = self.ideal_vector[0] * self.x_vector + self.ideal_vector[1] * self.y_vector
        modOfVector1 = math.sqrt( self.ideal_vector[0] * self.ideal_vector[0] + self.ideal_vector[1]*self.ideal_vector[1])*math.sqrt(self.x_vector*self.x_vector + self.y_vector*self.y_vector)
        if modOfVector1 ==0:
            return 0
        else:
            return math.degrees(math.acos(dotProduct/modOfVector1))

    def get_sine(self):
        #sine method
        car_vector_length = math.sqrt(self.x_vector**2 + self.y_vector**2)
        cross_product = car_vector_length * math.sqrt(self.ideal_vector[0]**2 + self.ideal_vector[1]**2)
        # using cross-product formula
        if cross_product ==0:
            return 0
        else:
            return -math.degrees(math.asin((self.x_vector * self.ideal_vector[1] - self.y_vector * self.ideal_vector[0])/(cross_product)))


    def ai_drive(self, track: pysprint_tracks.Track):

        self.calculate_ideal_vector(track, self.gate_step)

        cosine_angle =self.get_cosine()
        angle = self.get_sine()

        if DEBUG_AI:
            print('{} - Next Gate:{} - Current Vector: ({:.2f},{:.2f}) - Ideal Vector: ({:.2f},{:.2f}) - Angle: {:.2f}° - Cosine Angle: {:.2f}°'.format(self.color_text, self.next_gate, self.x_vector, self.y_vector, self.ideal_vector[0], self.ideal_vector[1],angle, cosine_angle))

        if (angle > self.turning_angle_threshold) or ( angle < -self.turning_angle_threshold):
            if angle > 0:
                self.rotate(True)
                if DEBUG_AI:
                    print ('Turning Left')
            else:
                self.rotate(False)
                if DEBUG_AI:
                    print ('Turning Right')
            if self.drone_personality >= self.drone_personalities[0][1]:
                #Accelerate when Speed < Speed Max and decelerate if not when turning if Normal & Aggressive
                if self.speed < self.speed_max:
                    self.accelerate()
                else:
                    self.decelerate()
            else:
                self.decelerate()
        else:
            # If Vectr angle is too wide review te next gate
            if (cosine_angle > (180-self.turning_angle_threshold)):
                i = 1
                while (abs(angle) < self.turning_angle_threshold*1.5) and (i<5):
                    #Check direction for Next Gate until we get a clear direction to turn to
                    if DEBUG_AI:
                        print ('{} - 180° - Checking {} Gate(s) further'.format(self.color_text, i))
                    self.calculate_ideal_vector(track, self.gate_step + i)
                    angle = self.get_sine()
                    cosine_angle =self.get_cosine()
                    i+=1
                    self.rotate(angle > 0)
                #Search for next gates failes, try previous gates
                if i>=5:
                    i = 1
                    while (abs(angle) < self.turning_angle_threshold*1.5) and (i<5):
                        #Check direction for Next Gate until we get a clear direction to turn to
                        if DEBUG_AI:
                            print ('{} - 180° - Checking {} Gate(s) backwards'.format(self.color_text, i))
                        self.calculate_ideal_vector(track, self.gate_step - i)
                        angle = self.get_sine()
                        cosine_angle =self.get_cosine()
                        i+=1
                        self.rotate(angle > 0)
                self.decelerate()
            else:
                self.accelerate()

