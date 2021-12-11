7#pysprint_car.py
from typing import DefaultDict
from numpy import False_, True_, angle, result_type, select
from numpy.lib.polynomial import poly
from numpy.lib.type_check import _is_type_dispatcher
import pygame
from pygame import Surface, gfxdraw
import math
import random
#from pygame.constants import CONTROLLER_AXIS_RIGHTX

from pygame.key import name
from pygame.mask import from_threshold
import pysprint_tracks

from managers.sample_manager import SampleManager
from gfx.cone import Cone
from loguru import logger

game_display = None
DEBUG_FINISH = False
DEBUG_COLLISION = False
DEBUG__CAR_COLLISION = False
DEBUG_BUMP = False
DEBUG_CRASH = False
DEBUG_AI = False
DEBUG_GATE_TRACKING = False
DEBUG_RAMPS = False

#Timer during which 2 cars which collided can't collide again
car_collision_grace_period = 500

#Gravity for Jump Trajectory
gravity = 30 #-9.81

#Speed Modifier to get constant speed regardless of performance
frame_rate_speed_modifier = 1

#Rotation Modifier to get constant rotation regardless of performance
rotation_step_modifier = 1

race_laps = None
display_width = None
display_height = None
dust_cloud_frames = None
explosion_frames = None
transparency = None
vector_surf = None


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

    front_area = {
        0:[(8,2),(24,8)],
        1:[(16,2),(30,12)],
        2:[(20,4),(32,12)],
        3:[(20,6),(32,16)],
        4:[(22,8),(32,20)],
        5:[(18,12),(32,22)],
        6:[(12,14),(30,22)],
        7:[(12,18),(28,24)],
        8:[(8,16),(26,24)],
        9:[(4,16),(20,24)],
        10:[(2,14),(20,22)],
        11:[(0,12),(14,22)],
        12:[(0,8),(10,20)],
        13:[(0,6),(12,16)],
        14:[(0,4),(14,12)],
        15:[(4,2),(20,12)],
        16:[(8,2),(24,8)]
    }


    #30FPS Default Settings
    player_rotation_step = .26#.28
    player_acceleration_step = 0.3#0.18
    player_deceleration_step = 0.15#0.1
    player_bump_decelaration_step = 1.3
    player__bump_speed = 9
    player_speed = 7.5#8
    player_skidding_weight = 3
    #How much time after starting to skid before the car gaoins traction and turns
    skidding_traction_timer = 500

    #AI Default Characteristics
    drone_personalities = [
        ("Prudent",0),
        ("Normal",1),
        ("Aggressive",2)
    ]
    drone_personality_modifiers = [0.9,1,1.1]
    drone__invert_personality_modifiers = [1.1,1,0.9]
    drone_rotation_step = 0.4#.4
    drone_acceleration_step = 0.17#0.18
    drone_deceleration_step = 0.4#0.4
    drone_bump_decelaration_step = 0.3#0.3
    drone_bump_speed = 4#2
    drone_speed = 3#6
    drone_skidding_weight = 2
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

    #Engine sound timer
    acceleration_playing = False
    accel_decel_timer = None
    acceleration_duration = 1050
    deceleration_duration = 2000
    max_speed_playing = False
    deceleration_playing = False
    idle_playing = False

    #Collision Settings
    diagonal_detection_tolerance = 2
    vector_simulation_length = 10
    side_detection_tolerance = 7
    max_speed_crash_threshold = 3000#4000
    collision_area_threshold = 80#80#75
    #Threshold over which there is a higher chance to crash
    speed_crash_probability_threshold = 0.95#0.85
    #% increase of probability to crash if condition is true
    speed_crash_probability_penalty = 1.2#1.2
    sensitive_border_crash_probability_penalty = 1.4
    #Calculate Crash probability
    crash_basic_chance = 0
    crash_certainty_treshold = 85#85


    def __init__(self):

        # Sound
        self.smp_manager = SampleManager.get_manager("sfx")

        #Appearance
        #Color
        self.main_color = None
        self.secondary_color = None
        self.color_text = ""
        self.sprites = None
        self.sprites_masks = None
        self.first_car = None
        self.second_car = None
        self.third_car = None
        self.fourth_car = None
        self.start_screen_engine_position = None
        self.start_screen_thumb_position = None
        self.start_screen_text_position = None
        self.customization_string_position = None
        self.selection_wheel = None
        self.score_top_left = None
        self.prepare_to_race_counter = -1

        self.helicopter_frames = None
        self.vertical_helicopter_frames = None

        #Score
        self.score = 0
        self.wrench_count = 0
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

        self.x_position = 0
        self.y_position = 0
        self.sprite_angle = 12
        self.car_mask = None
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
        self.furthest_past_gate = None
        #Velocity for Jump trajectory
        self.fall_angle = None
        self.vx = None
        self.vy = None

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
        self.skidding_weight = 2

        self.super_traction = 0
        self.turbo_acceleration = 0
        self.higher_top_speed = 0


        self.drone_personality = 1

        #Car State
        #Track the last time score was incremented due to progress in race (lap_count, gate_number)
        self.skidding_timer = 0
        self.previous_score_increment = 0
        self.is_drone = True
        self.decelerating = False
        self.rotating = False
        self.bumping = False
        self.crashing = False
        self.spinning = False
        self.frontal_colliding = False
        self.falling = False
        self.side_colliding_offender = False
        self.side_colliding_offender_previous_speed = False
        self.side_colliding_victim = False
        self.side_colliding_offender_vector = None
        self.colliding_other_car = None
        self.car_collision_grace_timer = None
        self.on_spill = False
        self.hitting_cone = False
        self.on_tornado = False
        self.tornado_index = 0
        self.pole_bumping = False
        self.on_ramp = False
        self.on_bridge = False
        self.current_bridge_poly = None
        self.current_ramp_poly = None
        self.previous_ramp_poly = None
        self.jumping = False
        self.fall_start_timer = None
        self.take_off = False
        self.mid_air = False
        self.landing = False
        self.touch_down = False
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
        self.shortcut_gates_crossed = []

    def car_collision(self):
        return self.side_colliding_offender or self.side_colliding_victim or self.frontal_colliding

    def reset_racing_status(self, race_counter):
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
        self.shortcut_gates_crossed = []
        self.next_gate = None
        self.furthest_past_gate = None
        self.last_passed_gate = None
        self.most_recent_passed_gate = None
        self.progress_gate = -1
        self.ideal_vector = None
        self.next_mid_point = None
        self.next_gate = None
        for lap in self.lap_times:
            lap = 0
        self.best_lap = 0
        self.previous_score_increment = 0
        self.on_bridge = False
        self.on_ramp = False
        self.jumping = False
        self.mid_air = False
        self.landing = False
        self.previous_ramp_poly = None
        self.current_ramp_poly = None
        self.current_bridge_poly = None
        if not self.is_drone:
            #Apply Customization:
            self.speed_max = self.player_speed + self.higher_top_speed * 0.3
            self.rotation_step = self.player_rotation_step + self.super_traction * 0.015
            self.acceleration_step = self.player_acceleration_step + self.turbo_acceleration * 0.05
            self.deceleration_step = self.player_deceleration_step + self.super_traction * 0.025
            self.skidding_weight = self.player_skidding_weight - self.super_traction * 0.2
        else:
            #Increase Drone mechanics as game continues
            self.speed_max = self.speed_max + (race_counter//5) * 0.1
            self.rotation_step = self.rotation_step + (race_counter//5) * 0.05
            self.acceleration_step = self.acceleration_step + (race_counter//5) * 0.1
            self.deceleration_step = self.deceleration_step + (race_counter//5) * 0.025



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

    def set_spinning(self, is_spinning):
        self.spinning = is_spinning


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
        self.wrench_count = 0
        self.super_traction = 0
        self.turbo_acceleration = 0
        self.higher_top_speed = 0

    def start_game(self, play_sound = False):
        if self.game_over==False:
            self.reset_game_over()
        if self.is_drone:
            self.is_drone = False
            if play_sound:
                self.smp_manager.get_sample("start_race").play()
        self.ignore_controls = False
        self.speed_max = self.player_speed
        self.bump_speed = self.player__bump_speed
        self.rotation_step = self.player_rotation_step
        self.acceleration_step = self.player_acceleration_step
        self.deceleration_step = self.player_deceleration_step
        self.bump_decelaration_step = self.player_bump_decelaration_step
        self.skidding_weight = self.player_skidding_weight

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
        self.skidding_weight = self.drone_skidding_weight

    def rotate(self, left, track:pysprint_tracks.Track):
        self.rotating = True
        if left:
            self.angle -= self.rotation_step * rotation_step_modifier
        else:
            self.angle += self.rotation_step * rotation_step_modifier

        if self.angle < 0:
            self.angle += 16
        if self.angle >= 16:
            self.angle -= 16
        self.sprite_angle = round(self.angle,0)
        if self.sprite_angle == 16:
            self.sprite_angle = 0
        if self.on_ramp:
            self.fix_sprite_angle_on_ramp(track)

    def accelerate(self):
        #Reset skidding timer, as skidding stops once acceleration starts
        self.skidding_timer = 0
        self.decelerating = False
        if not self.mid_air and not self.take_off:
            if self.speed < self.speed_max:
                if not self.is_drone:
                    if self.deceleration_playing:
                        self.smp_manager.get_sample("engine_decelerate").stop()
                        self.deceleration_playing = False
                    if self.idle_playing:
                        self.smp_manager.get_sample("engine_idle").stop()
                        self.idle_playing = False
                    if not self.acceleration_playing:
                        if not self.max_speed_playing:
                            self.accel_decel_timer = pygame.time.get_ticks()
                            self.smp_manager.get_sample("engine_accelerate").play()
                            self.acceleration_playing = True
                    else:
                        if pygame.time.get_ticks() - self.accel_decel_timer >= self.acceleration_duration:
                            self.smp_manager.get_sample("engine_accelerate").stop()
                            self.acceleration_playing = False
                            self.smp_manager.get_sample("engine_max").play(-1)
                            self.max_speed_playing = True
                self.speed += self.acceleration_step
                if self.speed >= self.speed_max:
                    self.max_speed_reached = pygame.time.get_ticks()
                    if not self.is_drone:
                        if not self.max_speed_playing:
                            self.smp_manager.get_sample("engine_max").play(-1)
                            self.max_speed_playing = True


    def decelerate(self):
        #Reset skidding timer, as skidding stops once acceleration starts
        if self.skidding_timer == 0:
            self.skidding_timer = pygame.time.get_ticks()
        self.decelerating = True
        self.max_speed_reached = 0
        if not self.is_drone:
            if self.acceleration_playing:
                self.smp_manager.get_sample("engine_accelerate").stop()
                self.acceleration_playing = False
            if self.max_speed_playing:
                self.smp_manager.get_sample("engine_max").stop()
                self.max_speed_playing = False
            if self.speed == 0:
                if not self.is_drone:
                    if not self.idle_playing:
                        self.smp_manager.get_sample("engine_idle").play(-1)
                        self.idle_playing = True
            if not self.deceleration_playing:
                if not self.idle_playing:
                    self.accel_decel_timer = pygame.time.get_ticks()
                    self.smp_manager.get_sample("engine_decelerate").play()
                    self.deceleration_playing = True
            else:
                if pygame.time.get_ticks() - self.accel_decel_timer >= self.deceleration_duration:
                    self.smp_manager.get_sample("engine_decelerate").stop()
                    self.deceleration_playing = False
                    self.smp_manager.get_sample("engine_idle").play(-1)
                    self.idle_playing = True

        if self.bumping:
            self.speed -= self.bump_decelaration_step
        else:
            self.speed -= self.deceleration_step

        if self.speed < 0:
            self.speed = 0
        if self.speed == 0:
            if not self.is_drone:
                if not self.idle_playing:
                    self.smp_manager.get_sample("engine_idle").play(-1)
                    self.idle_playing = True

            self.decelerating = False
            if self.bumping:
                #Stop Bumping routine once speed down to 0 unless hittign a cone or landing from a jump in whihc case we let the dust cloud settle before ending the loop
                if not self.hitting_cone:
                    self.end_bump_loop()
                else:
                    if self.animation_index >= len(dust_cloud_frames):
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
                        logger.debug('found matching pair of points ({},{})'.format(polygon_border[i],polygon_border[next_index]))
                    self.a_intersect_side = polygon_border[i]
                    self.b_intersect_side = polygon_border[next_index]
                    if (abs(polygon_border[i][0]-polygon_border[next_index][0]) <= self.diagonal_detection_tolerance) and (abs(polygon_border[i][1]-polygon_border[next_index][1]) > self.diagonal_detection_tolerance):
                        if DEBUG_COLLISION:
                            logger.debug('x delta <={} - looks vertical enough'.format(self.diagonal_detection_tolerance))
                        if bumping:
                            self.bumping_vertical = True
                        return True
                    if (abs(polygon_border[i][0]-polygon_border[next_index][0])>self.diagonal_detection_tolerance) and (abs(polygon_border[i][1]-polygon_border[next_index][1])<=self.diagonal_detection_tolerance):
                        if DEBUG_COLLISION:
                            logger.debug('y delta <={} - looks horizontal enough'.format(self.diagonal_detection_tolerance))
                        if bumping:
                            self.bumping_horizontal = True
                        return True
                    if DEBUG_COLLISION:
                        logger.debug('Diagonal Bumping')
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

    def calculate_sprite_from_vector(self, new_vector):

        sprite_sin_angle = math.sin(math.radians(abs(self.sprite_angle*22.5-90)))
        sprite_y_vector = abs(self.speed * sprite_sin_angle)
        sprite_y_vector = sprite_y_vector * self.angle_vector_sign[self.sprite_angle][1]
        sprite_x_vector = math.sqrt(self.speed*self.speed-sprite_y_vector*sprite_y_vector)
        sprite_x_vector = sprite_x_vector * self.angle_vector_sign[self.sprite_angle][0]

        sine_angle = self.get_sine((sprite_x_vector,sprite_y_vector), new_vector)
        if DEBUG_RAMPS:
            logger.debug('sine:{} - sprite_angle = {}'.format(sine_angle,self.sprite_angle))

        if (sine_angle > self.turning_angle_threshold) or ( sine_angle < -self.turning_angle_threshold):
            if sine_angle < 0:
                self.sprite_angle-=1
                if self.sprite_angle<0:
                    self.sprite_angle+=16
            else:
                self.sprite_angle+=1
                if self.sprite_angle>=16:
                    self.sprite_angle-=16
        if DEBUG_RAMPS:
            logger.debug('New Sprite angle = {}'.format(self.sprite_angle))


    def calculate_jumping_vector(self,track: pysprint_tracks.Track):
        self.calculate_vector_from_sprite()

    def calculate_falling_vector(self,track: pysprint_tracks.Track):
        #dt = 0.02
        dt = (pygame.time.get_ticks() - self.fall_start_timer)/5000
        new_vector = (self.vx * dt, self.vy * dt)
        self.calculate_sprite_from_vector(new_vector)
        self.x_vector = new_vector[0]
        self.y_vector = new_vector[1]
        self.vy = self.vy + 0.5 * gravity * dt
        if DEBUG_RAMPS:
            logger.debug('(x,y): ({},{})  vector({},{}) - vx:{} - vy:{}'.format(self.x_position,self.y_position,self.x_vector,self.y_vector,self.vx,self.vy))

    def calculate_skidding_vector(self):
        #Start Skidding
        # v0.1 - Ignore current Rotation sprite, update speed and use previous Angle and sign
        # v0.11 - Incorporate the spinte angle in the skidding vector if rotating
        # v0.37 - issue #45 set a timer when teh car starts skidding and incorporate the sprite angle only after that timer expired
        skidding_x = self.x_vector
        skidding_y = self.y_vector
        regain_traction = self.bumping
        if (self.skidding_timer>0) and (pygame.time.get_ticks()-self.skidding_timer > self.skidding_traction_timer):
            regain_traction = True
        skidding_angle = self.sin_angle
        if regain_traction:
            if DEBUG_BUMP:
                logger.debug("Regaining traction on skidding")
            if not skidding_y == 0:
                skidding_y = skidding_y * abs(self.speed * skidding_angle) / abs(self.y_vector)

            if not skidding_x == 0:
                skidding_x = skidding_x * math.sqrt(abs(self.speed*self.speed-skidding_y*skidding_y))  / abs(skidding_x)
        else:
            if DEBUG_BUMP:
                logger.debug("Skidding without Traction")

        self.calculate_vector_from_sprite()
        self.x_vector = (self.x_vector + skidding_x*self.skidding_weight)/(self.skidding_weight+1)
        self.y_vector = (self.y_vector + skidding_y*self.skidding_weight)/(self.skidding_weight+1)
        if regain_traction:
            self.sin_angle = (self.sin_angle + skidding_angle*2)/3

        if self.x_vector==0 and self.y_vector==0 and self.speed>0:
            #Wrong situation: reset to default vector
            self.calculate_vector_from_sprite()

    def calculate_pole_vector(self,track: pysprint_tracks.Track):
        if not self.bumping_vector_initialized:
            self.x_vector = -self.x_vector
            self.y_vector = -self.y_vector
            self.bumping_vector_initialized = True


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

    def calculate_side_colliding_vector(self, other_car):
        if self.side_colliding_offender:
        #Offending Car: bumping aginst the victim car similarly to bumping against a border
            if not self.bumping_vector_initialized:
                if other_car.sprite_angle ==0 or other_car.sprite_angle ==8 or other_car.sprite_angle ==16 :
                    #Bump horizontally when hitting a vertical car diagonally or horizontally
                    #Invert X component fo the vector
                    self.x_vector = -self.x_vector
                    self.y_vector = 0
                else:
                    if other_car.sprite_angle ==4 or other_car.sprite_angle ==12:
                        #Bump vertically when hitting a horizontal border diagonally or vertically
                        #Invert Y component fo the vector
                        self.y_vector = -self.y_vector
                        self.x_vector = 0
                    else:
                        if self.bumping_diagonal:
                            #Diagonal Bumping: Bump Diagnoally if hit Horizontally - or Vertically  - Vert or Horiz Bump if hit diagonally
                            if self.x_vector == 0 or self.y_vector == 0:
                                #Car is moving Horizontally or Vertical - Force 45 degree angle
                                self.sin_angle = math.sin(math.radians(abs(45)))
                                new_vector = abs(self.speed * self.sin_angle)
                                if (other_car.sprite_angle > 4 and other_car.sprite_angle < 8) or (other_car.sprite_angle > 12 and other_car.sprite_angle < 16):
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
                                if (other_car.sprite_angle < 4 and other_car.sprite_angle > 0) or (other_car.sprite_angle < 12 and other_car.sprite_angle > 8):
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
        elif self.side_colliding_victim:
            #Victim Car: Vector is modified by offending car's vector
            #Sine method
            car_vector_length = math.sqrt(self.side_colliding_offender_vector[0]**2 + self.side_colliding_offender_vector[1]**2)
            cross_product = car_vector_length * math.sqrt(1)
            # using cross-product formula
            if cross_product ==0:
                offender_sin_angle = 0
            else:
                offender_sin_angle = (self.side_colliding_offender_vector[0] * 1 - self.side_colliding_offender_vector[1] * 0)/cross_product
            if offender_sin_angle == 0:
                offender_sin_angle = 1
            self.sin_angle = offender_sin_angle

            if not self.side_colliding_offender_vector[1] == 0:
                self.y_vector = abs(self.speed * self.sin_angle)
                self.y_vector = self.y_vector * self.side_colliding_offender_vector[1]/abs(self.side_colliding_offender_vector[1])
            else:
                self.y_vector = 0
            if not self.side_colliding_offender_vector[0] == 0:
                self.x_vector = math.sqrt(abs(self.speed*self.speed-self.y_vector*self.y_vector))
                self.x_vector = self.x_vector * self.side_colliding_offender_vector[0]/abs(self.side_colliding_offender_vector[0])
            else:
                self.x_vector = 0

        self.bumping_vector_initialized = True


    def test_car_collisions(self, cars):
        for i in range(0,len(cars)):
            #Check collision with other cars if they are on the same level
            if not cars[i].color_text==self.color_text and cars[i].on_ramp==self.on_ramp and cars[i].on_bridge==self.on_bridge:
                if not self.car_collision_grace_timer is None:
                    if pygame.time.get_ticks() < self.car_collision_grace_timer:
                        if DEBUG__CAR_COLLISION:
                            logger.debug('No Colllision (too recent): {}-sprite:{} - {}-sprite:{}'.format(cars[i].color_text,cars[i].sprite_angle,self.color_text,self.sprite_angle))
                    else:
                        self.car_collision_grace_timer = None
                if self.car_collision_grace_timer is None:
                    other_car_mask = cars[i].car_mask
                    collision = other_car_mask.overlap(self.car_mask, (round(self.x_position-cars[i].x_position),round(self.y_position-cars[i].y_position)))
                    if collision:
                        #Determine relative position of each car to determine the effect of the collision
                        angle_delta = self.sprite_angle - cars[i].sprite_angle
                        #Frontal Collision: sprite angles are opposite  and at least 50% max speed is reached
                        if (abs(angle_delta) < 10) and (abs(angle_delta) >6):
                            if self.speed>0.5*self.speed_max and cars[i].speed>0.5*cars[i].speed_max:
                                if DEBUG__CAR_COLLISION:
                                    logger.debug('Frontal Colllision: {}-sprite:{} - {}-sprite:{}'.format(cars[i].color_text,cars[i].sprite_angle,self.color_text,self.sprite_angle))
                                self.init_frontal_car_collision_loop(cars[i])
                                cars[i].init_frontal_car_collision_loop(self)
                        ##No Collision: sprite angles are equal or close (+/- 2 step)
                        elif abs(angle_delta) <= 2 or abs(angle_delta) >=13:
                            if DEBUG__CAR_COLLISION:
                                logger.debug('No Colllision: {}-sprite:{} - {}-sprite:{}'.format(cars[i].color_text,cars[i].sprite_angle,self.color_text,self.sprite_angle))
                        #Sprites angle is equidisant from right angles and cars opposite directions
                        # elif (abs(angle_delta)==6) or (abs(angle_delta)==10) and ((self.speed>0.75*self.speed_max and cars[i].speed>0.75*cars[i].speed_max) and (not self.is_drone or not cars[i].is_drone)):
                        #     #If cars are at high speed, force spinning (if one of them is not a drone, as drones are almost always at max speed)
                        #     if DEBUG__CAR_COLLISION:
                        #         logger.debug('High Speed Colllision: {}-sprite:{} - {}-sprite:{}'.format(cars[i].color_text,cars[i].sprite_angle,self.color_text,self.sprite_angle))
                        #     self.init_frontal_car_collision_loop(cars[i])
                        #     cars[i].init_frontal_car_collision_loop(self)
                        else:
                            ##Side Collision
                            #Check if the other car's front area is touching
                            #define reactangluar surfaces for the front area of each sprite
                            if (self.speed>0.75*self.speed_max and cars[i].speed>0.75*cars[i].speed_max) and (not self.is_drone or not cars[i].is_drone) and (abs(angle_delta)==5) or (abs(angle_delta)==11):
                                #If cars are at high speed, force spinning when angle is open (if one of them is not a drone, as drones are almost always at max speed)
                                if DEBUG__CAR_COLLISION:
                                    logger.debug('High Speed Colllision (open angle): {}-sprite:{} - {}-sprite:{}'.format(cars[i].color_text,cars[i].sprite_angle,self.color_text,self.sprite_angle))
                                self.init_frontal_car_collision_loop(cars[i])
                                cars[i].init_frontal_car_collision_loop(self)
                            elif (self.speed>0.75*self.speed_max and cars[i].speed>0.75*cars[i].speed_max) and (abs(angle_delta)==3) or (abs(angle_delta)==13):
                                #If cars are at high speed, ignore when angle is closed
                                if DEBUG__CAR_COLLISION:
                                    logger.debug('No Colllision (high speed-closed angle"): {}-sprite:{} - {}-sprite:{}'.format(cars[i].color_text,cars[i].sprite_angle,self.color_text,self.sprite_angle))
                            else:
                                other_front_collision = False
                                if collision[0]>=self.front_area[cars[i].sprite_angle][0][0] and collision[0]<=self.front_area[cars[i].sprite_angle][1][0]:
                                    if collision[1]>=self.front_area[cars[i].sprite_angle][0][1] and collision[1]<=self.front_area[cars[i].sprite_angle][1][1]:
                                        other_front_collision = True
                                front_collision = False
                                other_collision = self.car_mask.overlap(other_car_mask, (round(cars[i].x_position-self.x_position),round(cars[i].y_position-self.y_position)))
                                if other_collision:
                                    if other_collision[0]>=self.front_area[self.sprite_angle][0][0] and other_collision[0]<=self.front_area[self.sprite_angle][1][0]:
                                        if other_collision[1]>=self.front_area[self.sprite_angle][0][1] and other_collision[1]<=self.front_area[self.sprite_angle][1][1]:
                                            front_collision = True
                                else:
                                    other_collision = (-1,-1)
                                if DEBUG__CAR_COLLISION:
                                    logger.debug('Side Colllision: {}-sprite:{}-front:{} - {}-sprite:{}-front:{} - ({},{}) - ({},{})'.format(cars[i].color_text,cars[i].sprite_angle,other_front_collision,self.color_text,self.sprite_angle,front_collision,collision[0],collision[1],other_collision[0],other_collision[1]))
                                if not front_collision == other_front_collision:
                                    if other_front_collision:
                                        #Side collisions between drones are excluded
                                        if not(self.is_drone and cars[i].is_drone):
                                            if not self.side_colliding_victim:
                                                self.init_side_car_collision_victim_loop(cars[i], collision)
                                            if not cars[i].side_colliding_offender:
                                                cars[i].init_side_car_collision_offender_loop(self, collision)
                                            if DEBUG__CAR_COLLISION:
                                                logger.debug('Side Colllision: Victim: {} - Offender: {}'.format(self.color_text,cars[i].color_text))
                                    else:
                                        #Side collisions between drones are excluded
                                        if not(self.is_drone and cars[i].is_drone):
                                            if not self.side_colliding_offender:
                                                self.init_side_car_collision_offender_loop(cars[i], collision)
                                            if not cars[i].side_colliding_victim:
                                                cars[i].init_side_car_collision_victim_loop(self, collision)
                                            if DEBUG__CAR_COLLISION:
                                                logger.debug('Side Colllision: Victim: {} - Offender: {}'.format(cars[i].color_text,self.color_text))

    def get_simulation_vector(self):
        x_test = 0
        y_test = 0
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
        result  = (x_test,y_test)
        return result
    def is_on_ramp_or_bridge(self):
        return self.on_bridge or self.on_ramp

    def test_bonus(self, track: pysprint_tracks.Track):
        if track.bonus_frame_index >=0 and track.on_bridge_or_ramp_bonus==self.is_on_ramp_or_bridge():
            bonus_mask = pysprint_tracks.bonus_frames_masks[track.bonus_frame_index]
            x_test = 0
            y_test = 0
            return  bonus_mask.overlap(self.car_mask, (round(self.x_position-track.bonus_position[0]),round(self.y_position-track.bonus_position[1])))
        else:
            return False

    def test_wrench(self, track: pysprint_tracks.Track):
        if track.wrench_displayed and track.on_bridge_or_ramp_wrench==self.is_on_ramp_or_bridge():
            return  pysprint_tracks.wrench_mask.overlap(self.car_mask, (round(self.x_position-track.wrench_position[0]),round(self.y_position-track.wrench_position[1])))
        else:
            return False

    def test_spill(self,spill_mask, position):
        if not position is None:
            return  spill_mask.overlap(self.car_mask, (round(self.x_position-position[0]),round(self.y_position-position[1])))
        else:
            return False

    def test_pole(self, track: pysprint_tracks.Track, position):
        if not position is None:
            return  track.pole_mask.overlap(self.car_mask, (round(self.x_position-position[0]),round(self.y_position-position[1])))
        else:
            return False

    def test_tornado(self, track: pysprint_tracks.Track):
        if not track.tornado_position is None:
            return  track.tornado_mask.overlap(self.car_mask, (round(self.x_position-track.tornado_position[0]),round(self.y_position-track.tornado_position[1])))
        else:
            return False

    def test_cones(self, track: pysprint_tracks.Track) -> Cone:
        """Test collision between cones and current car positions

        Args:
            track (pysprint_tracks.Track): The current track

        Returns:
            Cone: if found, the cone which collided
        """
        for cone in track.traffic_cones:
            if cone.pos and cone.enabled and cone.is_on_bridge==self.is_on_ramp_or_bridge():
                if pysprint_tracks.traffic_cone_mask.overlap(self.car_mask, (round(self.x_position - cone.pos[0]), round(self.y_position - cone.pos[1]))):
                    logger.debug(f"Overlap between cone {cone.pos} in state {cone.enabled} and car {(self.x_position, self.y_position)}")
                    return cone
        return None

    def test_collision(self, track: pysprint_tracks.Track, simulate_next_step):
        x_test = 0
        y_test = 0
        if simulate_next_step:
            result = self.get_simulation_vector()
            x_test = result[0]
            y_test = result[1]
        if self.on_ramp or self.on_bridge:
            return track.track_upper_mask_mask.overlap(self.car_mask, ((round(self.x_position+x_test), round(self.y_position+y_test))))
        else:
            return track.track_mask_mask.overlap(self.car_mask, ((round(self.x_position+x_test), round(self.y_position+y_test))))

    def test_collision_area(self, track: pysprint_tracks.Track, simulate_next_step):
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

        if self.on_ramp or self.on_bridge:
            return track.track_upper_mask_mask.overlap_area(self.car_mask, ((round(self.x_position+x_test), round(self.y_position+y_test))))
        else:
            return track.track_mask_mask.overlap_area(self.car_mask, ((round(self.x_position+x_test), round(self.y_position+y_test))))


    def set_car_at_ramp_start(self,track: pysprint_tracks.Track):
        #Reposition the car at the start of the ramp
        self.y_vector = 0
        self.x_vector = 0
        if not self.current_ramp_poly is None:
            new_position_gate = track.ramp_gates[self.current_ramp_poly[0]][0][0]
        else:
            new_position_gate = self.last_passed_gate
        self.x_position = (track.external_gate_points[new_position_gate][0] + track.internal_gate_points[new_position_gate][0])/ 2
        self.y_position = (track.external_gate_points[new_position_gate][1] + track.internal_gate_points[new_position_gate][1])/ 2

        if track.internal_gate_points[track.ramp_gates[self.current_ramp_poly[0]][0][0]][0] > track.internal_gate_points[track.ramp_gates[self.current_ramp_poly[0]][0][len(track.ramp_gates[self.current_ramp_poly[0]][0])-1]][0]:
        #ramp going from right to left - Shifting car clockwise
            self.sprite_angle = 12
        else:
        #ramp going from left to right - shifting car conter-clockwise
            self.sprite_angle = 4





    def calculate_crashing_vector(self,track: pysprint_tracks.Track):

        if self.on_ramp or self.falling:
            self.set_car_at_ramp_start(track)
        else:
            #Reposition car in a suitable spot - Move car backwards until no collision detected.
            #Invert vector
            self.x_vector = -self.x_vector
            self.y_vector = -self.y_vector

            intersect_point = self.test_collision(track, True)
            #Test if the car is still collidign and keep moving backwards until not the case
            if intersect_point:
                if DEBUG_COLLISION:
                    logger.debug('Car stuck outside of borders at ({},{}) - Repositionning'.format(self.x_position, self.y_position))
                self.y_vector = 0
                self.x_vector = 0

                # Reposition the to the midpoint of the closest progress gate
                closest_gate_index = track.find_progress_gate((self.x_position, self.y_position))

                self.x_position = (track.external_gate_points[closest_gate_index][0] + track.internal_gate_points[closest_gate_index][0])/ 2
                self.y_position = (track.external_gate_points[closest_gate_index][1] + track.internal_gate_points[closest_gate_index][1])/ 2


                # #Reposition the to the midpoint of the latest progress gate or Start Line by default
                # if self.last_passed_gate is None:
                #     self.x_position = track.first_car_start_position[0]
                #     self.y_position = track.first_car_start_position[1]
                # else:
                #     self.x_position = (track.external_gate_points[self.last_passed_gate][0] + track.internal_gate_points[self.last_passed_gate][0])/ 2
                #     self.y_position = (track.external_gate_points[self.last_passed_gate][1] + track.internal_gate_points[self.last_passed_gate][1])/ 2
            else:
                result = self.get_simulation_vector()
                self.x_position = round(self.x_position+result[0])
                self.y_position = round(self.y_position+result[1])
                self.y_vector = 0
                self.x_vector = 0

    def detect_collision(self, track: pysprint_tracks.Track):
        if DEBUG_COLLISION:
            logger.debug('Checking for Collision at ({},{})'.format(self.x_position, self.y_position))
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
            if self.falling:
                #Crash is certain nonedd to test any other conditions
                self.init_crash_loop(intersect_point)
            else:
                if  self.detect_crash(track):
                    self.init_crash_loop(intersect_point)
                else:
                    self.init_bump_loop(track, intersect_point)

    def detect_crash(self, track: pysprint_tracks.Track):

        #if overlap between car and circuit mask > collision_area_threshold pixels  crash is forced to avoid traversing walls and gates
        area = self.test_collision_area(track,False)
        if DEBUG_CRASH:
            logger.debug('collision area : {}'.format(area))

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
            #Basic chance to crash which increased:
            crash_probability = self.crash_basic_chance
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

    def detect_spills(self, track: pysprint_tracks.Track):
        if track.display_oil_spill and track.on_bridge_oil_spill==self.is_on_ramp_or_bridge():
            if self.test_spill(pysprint_tracks.oil_spill_mask,track.oil_spill_position):
                if not self.on_spill:
                    self.init_oil_spill_loop()
                return True
        if track.display_water_spill and track.on_bridge_water_spill==self.is_on_ramp_or_bridge():
            if self.test_spill(pysprint_tracks.water_spill_mask,track.water_spill_position):
                if not self.on_spill:
                    self.init_water_spill_loop()
                return True
        if track.display_grease_spill and track.on_bridge_grease_spill==self.is_on_ramp_or_bridge():
            if self.test_spill(pysprint_tracks.grease_spill_mask,track.grease_spill_position):
                if not self.on_spill:
                    self.init_grease_spill_loop()
                return True

        return False

    def detect_tornado(self, track: pysprint_tracks.Track):
        if self.test_tornado(track):
            if not self.on_tornado:
                self.init_tornado_loop()
                return True
        return False

    def detect_poles(self, track: pysprint_tracks.Track):
        if  track.on_bridge_pole==self.is_on_ramp_or_bridge():
            position_to_test = None
            if track.poles_frame_indexes[0]>0:
                position_to_test = track.external_pole_position
            if track.poles_frame_indexes[1]:
                position_to_test = track.middle_pole_position
            if track.poles_frame_indexes[2]:
                position_to_test = track.internal_pole_position
            if self.test_pole(track,position_to_test):
                self.init_pole_loop(track,position_to_test)
                return True
        return False



    def detect_cones(self, track: pysprint_tracks.Track):
        cone_hit = self.test_cones(track)
        if cone_hit:
            self.init_cone_loop(cone_hit.pos)
            cone_hit.disable()
            logger.debug(f"Collision between car {self.main_color} and cone {cone_hit}")

    def init_pole_loop(self,track,position):
        if self.speed<self.speed_max:
            self.smp_manager.get_sample("bump").play()
            self.set_bumping(True)
            self.speed = self.bump_speed
            self.animation_index = 0
            self.x_intersect = position[0]
            self.y_intersect = position[1]
            self.pole_bumping = True
            self.collision_time = pygame.time.get_ticks()
        else:
            self.init_crash_loop(position)

    def init_cone_loop(self,cone_hit):
        self.smp_manager.get_sample("obstacle").play()
        self.set_bumping(True)
        self.hitting_cone = True
        self.speed = 0
        self.animation_index = 0
        self.x_intersect = cone_hit[0]
        self.y_intersect = cone_hit[1]
        self.collision_time = pygame.time.get_ticks()

    def init_tornado_loop(self):
        self.smp_manager.get_sample("spin").play()
        self.set_spinning(True)
        self.speed = self.player_speed *0.5
        self.deceleration_step = self.player_deceleration_step * 0.5
        self.animation_index = 0
        self.tornado_index = 0
        self.collision_time = pygame.time.get_ticks()

    def init_oil_spill_loop(self):
        self.smp_manager.get_sample("spin").play()
        self.set_spinning(True)
        self.speed = self.player_speed *0.5
        self.deceleration_step = self.player_deceleration_step * 0.5
        self.animation_index = 0
        self.collision_time = pygame.time.get_ticks()

    def init_water_spill_loop(self):
        self.smp_manager.get_sample("obstacle").play()
        self.speed = 0

    def init_grease_spill_loop(self):
        self.smp_manager.get_sample("obstacle").play()
        self.set_spinning(True)
        if self.is_drone:
            self.speed = self.speed_max *0.5
        else:
            self.speed = self.speed_max *0.3
        self.deceleration_step = self.drone_deceleration_step
        self.animation_index = 0
        self.collision_time = pygame.time.get_ticks()

    def init_frontal_car_collision_loop(self, other_car):
        self.smp_manager.get_sample("spin").play()
        self.set_spinning(True)
        self.speed = self.speed_max * 0.6
        self.frontal_colliding = True
        self.side_colliding_offender = False
        self.side_colliding_victim = False
        self.colliding_other_car = other_car
        self.animation_index = 0
        self.collision_time = pygame.time.get_ticks()

    def init_side_car_collision_offender_loop(self, victim, collision):
        self.smp_manager.get_sample("collision").play()
        self.set_bumping(True)
        self.side_colliding_offender_previous_speed = self.speed
        self.speed = self.player__bump_speed
        self.bump_decelaration_step = self.player_bump_decelaration_step * 6
        self.collision_time = pygame.time.get_ticks()
        self.car_collision_grace_timer = self.collision_time + car_collision_grace_period
        self.x_intersect = collision[0]
        self.y_intersect = collision[1]
        self.animation_index = 0
        self.frontal_colliding = False
        self.side_colliding_offender = True
        self.side_colliding_victim = False
        self.colliding_other_car = victim

    def init_side_car_collision_victim_loop(self, offender, collision):
        self.smp_manager.get_sample("collision").play()
        self.set_bumping(True)
        self.speed = self.player__bump_speed
        self.bump_decelaration_step = self.player_bump_decelaration_step * 6
        self.collision_time = pygame.time.get_ticks()
        self.car_collision_grace_timer = self.collision_time + car_collision_grace_period
        self.animation_index = 0
        self.x_intersect = collision[0]
        self.y_intersect = collision[1]
        self.frontal_colliding = False
        self.side_colliding_offender = False
        self.side_colliding_victim = True
        self.colliding_other_car = offender
        self.side_colliding_offender_vector = (offender.x_vector, offender.y_vector)

    def init_bump_loop(self, track: pysprint_tracks.Track, intersect_point):
        self.smp_manager.get_sample("bump").play()
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
                        logger.debug('No Macthing Border Side found')
                    self.end_bump_loop()
        if DEBUG_BUMP or DEBUG__CAR_COLLISION:
            logger.debug('{} - Bump Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0

    def init_crash_loop(self, intersect_point):
        self.smp_manager.get_sample("crash").play()
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
            logger.debug('{} - Crash Initiated({},{})'.format(self.collision_time, self.x_intersect, self.y_intersect))
        self.animation_index = 0
        self.helicopter_index = 0

    def fix_sprite_angle_on_ramp(self, track: pysprint_tracks.Track):
        #Shift carfrom Horizontal or vertical positions when on ramp
        if track.internal_gate_points[track.ramp_gates[self.current_ramp_poly[0]][self.current_ramp_poly[1]][0]][0] > track.internal_gate_points[track.ramp_gates[self.current_ramp_poly[0]][self.current_ramp_poly[1]][len(track.ramp_gates[self.current_ramp_poly[0]][self.current_ramp_poly[1]])-1]][0]:
            #ramp going from right to left - Shifting car clockwise if on the upwards ramp (first polygon), counter closckwise if on the downwards ramp (last polygon)
            if self.is_drone:
                self.sprite_angle = 13
            else:
                if self.current_ramp_poly[1] == 0:
                    if self.sprite_angle == 16 or self.sprite_angle == 0:
                        self.sprite_angle = 1
                    if self.sprite_angle == 8:
                        self.sprite_angle = 9
                    if self.sprite_angle == 4:
                        self.sprite_angle = 5
                    if self.sprite_angle == 12:
                        self.sprite_angle = 13
                elif self.current_ramp_poly[1] == 2:
                    if self.sprite_angle == 0 or self.sprite_angle == 16:
                        self.sprite_angle = 15
                    if self.sprite_angle == 8:
                        self.sprite_angle = 7
                    if self.sprite_angle == 4:
                        self.sprite_angle = 3
                    if self.sprite_angle == 12:
                        self.sprite_angle = 11
        else:
            #ramp going from left to right - shifting car conter-clockwise if on the upwards ramp (first polygon), clockwise if on the downwards ramp (last polygon)
            if self.is_drone:
                self.sprite_angle = 3
            else:
                if self.sprite_angle == 0 or self.sprite_angle == 16:
                    if self.sprite_angle == 0:
                        self.sprite_angle = 15
                    if self.sprite_angle == 8:
                        self.sprite_angle = 7
                    if self.sprite_angle == 4:
                        self.sprite_angle = 3
                    if self.sprite_angle == 12:
                        self.sprite_angle = 11
                elif self.current_ramp_poly[1] == 2:
                    if self.sprite_angle == 0 or self.sprite_angle == 16:
                        self.sprite_angle = 1
                    if self.sprite_angle == 8:
                        self.sprite_angle = 9
                    if self.sprite_angle == 4:
                        self.sprite_angle = 5
                    if self.sprite_angle == 12:
                        self.sprite_angle = 13

    def init_entering_ramp(self, track: pysprint_tracks.Track, ramp_index,polygon_index):
        self.previous_ramp_poly = self.current_ramp_poly
        self.current_ramp_poly = (ramp_index,polygon_index)
        if polygon_index ==1:
            if self.previous_ramp_poly is None:
                #Entering middle polygon while NOT on the ramp > Ignored
                self.current_ramp_poly = None
            else:
                #Entering middle polygon while on the ramp i.e. jumping
                self.init_jump_loop(track)
        else:
            self.on_ramp = True
            if not self.landing and track.player_shortcut_bookend_gates is None:
                if track.internal_gate_points[track.ramp_gates[ramp_index][polygon_index][0]][0] > track.internal_gate_points[track.ramp_gates[ramp_index][polygon_index][len(track.ramp_gates[ramp_index][polygon_index])-1]][0]:
                #ramp going from right to left - Shifting car clockwise
                    if self.current_ramp_poly[1] == 0:
                        self.sprite_angle += 1
                    else:
                        self.sprite_angle -= 1
                else:
                #ramp going from left to right - shifting car conter-clockwise
                    if self.current_ramp_poly[1] == 0:
                        self.sprite_angle -= 1
                    else:
                        self.sprite_angle += 1
                if self.sprite_angle >= 16:
                    self.sprite_angle -= 16
                if self.sprite_angle < 0:
                    self.sprite_angle += 16

                self.fix_sprite_angle_on_ramp(track)
        if DEBUG_RAMPS:
            logger.debug('{} - Entering (ramp,poly): ({},{})'.format(self.color_text,self.current_ramp_poly[0],self.current_ramp_poly[1]))

    def init_leaving_ramp(self, track: pysprint_tracks.Track):
        if DEBUG_RAMPS:
            logger.debug('{} - Leaving (ramp,poly): ({},{})'.format(self.color_text,self.current_ramp_poly[0],self.current_ramp_poly[1]))
        if self.take_off or self.mid_air or self.landing:
            #Leaving the ramp while mid-air, taking off or landing means crash
            self.init_crash_loop((self.x_intersect,self.y_position))
        elif not self.previous_ramp_poly is None and track.player_shortcut_bookend_gates is None:
            if track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][0]][0]>track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][len(track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]])-1]][0]:
            #ramp going from right to left - Shifting car clockwise if leaving downard ramp, counter-clockwise if leavint the upward ramp
                if self.previous_ramp_poly[1] == 2:
                    self.sprite_angle += 1
                else:
                    self.sprite_angle -= 1
            else:
            #ramp going from left to right  - Shifting car counter clockwise if leaving downard ramp, clockwise if leaving the upward ramp
                if self.current_ramp_poly[1] == 2:
                    self.sprite_angle -= 1
                else:
                    self.sprite_angle += 1
            if self.sprite_angle >= 16:
                self.sprite_angle -= 16
            if self.sprite_angle < 0:
                self.sprite_angle += 16


        self.previous_ramp_poly = None
        self.current_ramp_poly = None
        self.on_ramp = False
        self.jumping = False



    def init_entering_bridge(self, track: pysprint_tracks.Track, bridge_index):
        self.current_bridge_poly = bridge_index
        self.on_bridge = True
        if DEBUG_RAMPS:
            logger.debug('{} - Entering (bridge): ({})'.format(self.color_text,self.current_bridge_poly))

    def init_leaving_bridge(self, track: pysprint_tracks.Track):
        if DEBUG_RAMPS:
            logger.debug('{} - Leaving (bridge): ({})'.format(self.color_text,self.current_bridge_poly))
        self.current_bridge_poly = None
        self.on_bridge = False



    def init_jump_loop(self, track: pysprint_tracks.Track):
        #Force crash if speed under threshold
        falling = False
        if not self.is_drone and self.speed<0.15*self.player_speed:
            falling = True
        else:
            if track.player_shortcut_bookend_gates is None:
                if track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][0]][0] > track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][len(track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]])-1]][0]:
                    #ramp going from right to left
                    if self.previous_ramp_poly[1]==0:
                        correct_angle = 14
                    else:
                        #Jumping in reverse direction
                        correct_angle = 2
                else:
                    if self.previous_ramp_poly[1]==0:
                        correct_angle = 2
                    else:
                        #Jumping in reverse direction
                        correct_angle = 14
                #Fall if angle is not the correct angle
                if abs(self.sprite_angle-correct_angle)>1:
                    falling = True

        if falling:
            self.init_falling_loop(track)
        else:
            self.jumping = True
            self.take_off = True
            self.decelerating = True
            if DEBUG_RAMPS:
                logger.debug('{} - Jumping (ramp,poly): ({},{})'.format(self.color_text,self.current_ramp_poly[0],self.current_ramp_poly[1]))
            self.ignore_controls = True
            if track.player_shortcut_bookend_gates is None:
                if track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][0]][0] > track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][len(track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]])-1]][0]:
                #ramp going from right to left - Shifting car clockwise
                    if self.previous_ramp_poly[1] == 0:
                        self.sprite_angle += 1
                    else:
                        self.sprite_angle -= 1
                else:
                #ramp going from left to right - shifting car conter-clockwise
                    if self.previous_ramp_poly[1] == 0:
                        self.sprite_angle -= 1
                    else:
                        self.sprite_angle += 1
                if self.sprite_angle >= 16:
                    self.sprite_angle -= 16
                if self.sprite_angle < 0:
                    self.sprite_angle += 16

                self.fix_sprite_angle_on_ramp(track)


    def init_mid_air(self, track: pysprint_tracks.Track):
        if DEBUG_RAMPS:
            logger.debug('{} - Init Mid-Air'.format(self.color_text))
        self.take_off = False
        self.decelerating = True
        self.mid_air = True
        self.ignore_controls = True
        if track.player_shortcut_bookend_gates is None:
            #force the car to horizontal position
            if track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][0]][0]>track.internal_gate_points[track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]][len(track.ramp_gates[self.previous_ramp_poly[0]][self.previous_ramp_poly[1]])-1]][0]:
            #ramp going from right to left
                if self.previous_ramp_poly[1] == 0:
                    self.sprite_angle  = 12
                else:
                    self.sprite_angle = 4
            else:
            #ramp going from left to right
                if self.previous_ramp_poly[1] == 0:
                    self.sprite_angle  = 4
                else:
                    self.sprite_angle = 12

    def init_landing(self, track: pysprint_tracks.Track):
        if DEBUG_RAMPS:
            logger.debug('{} - Init Landing'.format(self.color_text))
        self.smp_manager.get_sample("collision").play()
        self.landing = True
        self.mid_air = False
        self.ignore_controls = True
        self.decelerating = False
        if track.player_shortcut_bookend_gates is None:
            #force the car to the angle fo the landing ramp
            if track.internal_gate_points[track.ramp_gates[self.current_ramp_poly[0]][self.current_ramp_poly[1]][0]][0]>track.internal_gate_points[track.ramp_gates[self.current_ramp_poly[0]][self.current_ramp_poly[1]][len(track.ramp_gates[self.current_ramp_poly[0]][self.current_ramp_poly[1]])-1]][0]:
            #ramp going from right to left
                if self.previous_ramp_poly[1] == 0:
                    self.sprite_angle  = 11
                else:
                    self.sprite_angle = 5
            else:
            #ramp going from left to right
                if self.previous_ramp_poly[1] == 0:
                    self.sprite_angle  = 5
                else:
                    self.sprite_angle = 11

    def init_falling_loop(self, track: pysprint_tracks.Track):
        self.falling = True
        self.ignore_controls = True
        self.fall_angle = abs(self.sprite_angle*22.5-90)
        self.vx = 20*self.speed * math.cos(math.radians(self.fall_angle))
        self.vy = 20*self.speed * math.sin(math.radians(self.fall_angle))
        self.fall_start_timer = pygame.time.get_ticks()
        if DEBUG_RAMPS:
            logger.debug('{} - Falling'.format(self.color_text))

    def end_fall_loop(self):
        self.falling = False
        self.fall_start_timer = None
        #Leave cotrols ignored as fall is followed by a crash
        if DEBUG_RAMPS:
            logger.debug('{} - End Falling Loop'.format(self.color_text))




    def end_jump_loop(self):
        self.jumping = False
        self.landing = False
        self.touch_down = True
        if DEBUG_RAMPS:
            logger.debug('{} - Ending Jump (ramp,poly): ({},{})'.format(self.color_text,self.previous_ramp_poly[0],self.previous_ramp_poly[1]))
        self.ignore_controls = False
        self.collision_time = pygame.time.get_ticks()
        self.animation_index = 0
        self.x_intersect = self.x_position
        self.y_intersect = self.y_position


    def end_bump_loop(self):
        self.bumping_diagonal = False
        self.bumping_horizontal = False
        self.bumping_vertical = False
        self.bumping_vector_initialized = False

        if self.car_collision():
            self.frontal_colliding = False
            if self.side_colliding_offender:
                self.speed = self.side_colliding_offender_previous_speed
            self.side_colliding_offender = False
            self.side_colliding_victim = False
            self.colliding_other_car = None
            if self.is_drone:
                self.bump_decelaration_step = self.drone_bump_decelaration_step
            else:
                self.bump_decelaration_step = self.player_bump_decelaration_step

        self.set_bumping(False)
        end_time = pygame.time.get_ticks()
        if DEBUG_BUMP or DEBUG__CAR_COLLISION:
            logger.debug('{} - Bump Terminated - Duration: {})'.format(end_time,end_time-self.collision_time))

    def end_crash_loop(self):
        self.crashing = False
        self.crash_finished = False
        if self.on_ramp:
            self.on_ramp = False
            self.current_ramp_poly = None
            self.previous_ramp_poly = None
        if self.falling:
            self.end_fall_loop()
        end_time = pygame.time.get_ticks()
        if DEBUG_CRASH:
            logger.debug('{} - Crash Terminated - Duration: {})'.format(end_time,end_time-self.collision_time))

    def end_spinning_loop(self):
        self.spinning = False
        if self.on_tornado:
            self.on_tornado = False
        if self.is_drone:
            self.deceleration_step = self.drone_deceleration_step
        else:
            self.deceleration_step = self.player_deceleration_step

    def update_position(self, track: pysprint_tracks.Track, cars):
        if self.crashing:
            self.calculate_crashing_vector(track)
        else:
            if not self.decelerating:
                #Calculate Vector - Accelarating means No skidding
                self.calculate_vector_from_sprite()
            else:
                #Calculate Vector - Skidding
                self.calculate_skidding_vector()
            if self.bumping:
                #Calculate Vector - Bumping
                if self.side_colliding_offender or self.side_colliding_victim:
                    self.calculate_side_colliding_vector(self.colliding_other_car)
                elif self.pole_bumping:
                    self.calculate_pole_vector(track)
                else:
                    self.calculate_bumping_vector(track)
            if self.jumping:
                self.calculate_jumping_vector(track)
            if self.falling:
                self.calculate_falling_vector(track)
        #Update Car Offset
        self.x_position += self.x_vector * frame_rate_speed_modifier
        self.y_position += self.y_vector * frame_rate_speed_modifier
        #Update Gate progress
        self.check_passed_gate(track)
        #If car runs on Bonus, increase score
        if self.test_bonus(track):
            self.score+=int(track.bonus_value)
            self.smp_manager.get_sample("bonus_pickup").play()
            track.hide_bonus()
        #If car runs on Wrench, increase Wrench count
        if self.test_wrench(track):
            self.wrench_count+=1
            self.smp_manager.get_sample("wrench_pickup").play()
            track.hide_wrench()
        if not self.crashing:
            #Reset Rotation Flag to match Key Pressed Status
            self.rotating = False
            self.test_on_ramp(track)
            self.test_on_bridge(track)
            #ignore obstacles and collisons while the car is mid-air
            if not (self.jumping and not self.landing and not self.falling):
                if track.display_tornado:
                    #Check for Tornado - priority behaviour over spills
                    self.on_tornado = self.detect_tornado(track)
                if not self.on_tornado:
                    #Check for all spills
                    self.on_spill = self.detect_spills(track)
                if track.display_cones:
                    #check for Traffic Cones
                    self.detect_cones(track)
                if track.display_pole:
                    #Check for Poles
                    self.detect_poles(track)
            if not self.on_spill and not self.on_tornado:
                #If the car is not stopped Detect Track Borders. If not let it rotate over the edges & ignore collisions
                if self.speed > 0:
                    #ignore obstacles and collisons while the car is mid-air
                    if not self.jumping and not self.landing and not self.mid_air and not self.take_off:
                        self.detect_collision(track)
                        if not self.car_collision():
                            self.test_car_collisions(cars)
                else:
                    if not self.jumping and not self.landing and not self.mid_air and not self.take_off:
                        #If car is not moving, check for colision area size. Force crash
                        area = self.test_collision_area(track,False)
                        if area>self.collision_area_threshold:
                            intersect_point = self.test_collision(track,False)
                            self.init_crash_loop(intersect_point)
                        if self.bumping:
                            #Stop Bumping routine once speed down to 0 unless hittign a cone in whihc case we let the dust cloud settle before ending the loop
                            if not self.hitting_cone:
                                self.end_bump_loop()
                            else:
                                if self.car_collision():
                                    self.end_bump_loop()
                                if self.animation_index >= len(dust_cloud_frames):
                                    self.end_bump_loop()
                if self.touch_down:
                    if self.animation_index >= len(dust_cloud_frames):
                        self.touch_down = False

        else:
            #Car is not moving anymore
            self.x_vector = 0
            self.y_vector = 0
            self.speed = 0
            #End Crash Routine if animation has run to the end.
            if self.crash_finished:
                self.end_crash_loop()

    def test_shortcut_gates(self, track: pysprint_tracks.Track):
        if self.shortcut_gates_crossed is None:
            return
        else:
            if type (self.next_gate) is tuple:
                if len(track.external_ai_gates_shortcuts[self.next_gate[0]])-1 > len(self.shortcut_gates_crossed):
                    #Check whcih is the next Mandatory gate to cross and add it as crossed if collision if not already added
                    next_gate_to_test = (self.next_gate[0],len(self.shortcut_gates_crossed)+1)
                    gate_rect = pygame.Rect(min(track.internal_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][0],track.external_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][0]), min(track.internal_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][1],track.external_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][1]),abs(track.internal_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][0]-track.external_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][0])+1, abs(track.internal_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][1]-track.external_ai_gates_shortcuts[next_gate_to_test[0]][next_gate_to_test[1]][1])+1)
                    sprite_rect = pygame.Rect(self.x_position, self.y_position, self.sprites[self.sprite_angle].get_width(), self.sprites[self.sprite_angle].get_height())
                    if sprite_rect.colliderect(gate_rect):
                        #if gate is passed
                        self.shortcut_gates_crossed.append(next_gate_to_test)

    #Check if the next gate is a next Mandatory gate to cross and add it as crossed if collision if not already added

    def check_mandatory_gate(self, gate_to_check, track: pysprint_tracks.Track):
        if not track.mandatory_gates is None:
            if gate_to_check in track.mandatory_gates:
                if not gate_to_check in self.mandatory_gates_crossed:
                    #Mandatory gates have to be passed in order - teh gate won't be granted if you haven't passed all the rpevious mandatory gates
                    all_previous_mandatory_gates_passed = True
                    for gate in track.mandatory_gates:
                        if gate < gate_to_check and not gate in self.mandatory_gates_crossed:
                                all_previous_mandatory_gates_passed = False

                    if all_previous_mandatory_gates_passed and len(track.mandatory_gates) > len(self.mandatory_gates_crossed):
                        self.mandatory_gates_crossed.append(gate_to_check)


    def check_passed_gate(self, track: pysprint_tracks.Track):

        #Check if a gate is the next Mandatory gate to cross and add it as crossed if collision if not already added
        if self.furthest_past_gate is None:
                next_gate = 0
        else:
            next_gate = self.furthest_past_gate + 1
        if next_gate >= len(track.internal_gate_points):
            next_gate -= len(track.internal_gate_points)
        #gate_rect = pygame.Rect(min(track.internal_gate_points[next_gate][0],track.external_gate_points[next_gate][0]), min(track.internal_gate_points[next_gate][1],track.external_gate_points[next_gate][1]), abs(track.internal_gate_points[next_gate][0]-track.external_gate_points[next_gate][0])+1, abs(track.internal_gate_points[next_gate][1]-track.external_gate_points[next_gate][1])+1)
        gate_rect = track.gate_surfs[next_gate]
        sprite_rect = pygame.Rect(self.x_position, self.y_position, self.sprites[self.sprite_angle].get_width(), self.sprites[self.sprite_angle].get_height())
        if sprite_rect.colliderect(gate_rect):
            #if gate is passed
            self.furthest_past_gate = next_gate
            self.last_passed_gate = self.furthest_past_gate
            if DEBUG_GATE_TRACKING and not self.is_drone:
                logger.debug('{} - Furthest passed gate = {} - mandatory:{} - Last Passed gate: {}'.format(self.color_text,self.furthest_past_gate, self.mandatory_gates_crossed,self.last_passed_gate))

        else:
            #Check if colliding with the closest gate to check for any other gate being passed than the next expected one (if driving aginst the race general direction)
            gate_to_check = track.find_progress_gate((self.x_position,self.y_position))
            #gate_rect = pygame.Rect(min(track.internal_gate_points[gate_to_check][0],track.external_gate_points[gate_to_check][0]), min(track.internal_gate_points[gate_to_check][1],track.external_gate_points[gate_to_check][1]), abs(track.internal_gate_points[gate_to_check][0]-track.external_gate_points[gate_to_check][0])+1, abs(track.internal_gate_points[gate_to_check][1]-track.external_gate_points[gate_to_check][1])+1)
            gate_rect = track.gate_surfs[gate_to_check]
            if sprite_rect.colliderect(gate_rect):
                #if gate is passed
                if abs(gate_to_check-self.last_passed_gate)==1:
                    #Only update last passed gate for closest gate adjacent to the next or previous gate
                    self.last_passed_gate = gate_to_check
                self.most_recent_passed_gate = gate_to_check
                if DEBUG_GATE_TRACKING and not self.is_drone:
                    logger.debug('{} - Furthest passed gate = {} - mandatory:{} - Last Passed gate: {} - Most Recent: {}'.format(self.color_text,self.furthest_past_gate, self.mandatory_gates_crossed,self.last_passed_gate, self.most_recent_passed_gate))

        #Check if colliding with the next mandatory gate
        if len(self.mandatory_gates_crossed)<len(track.mandatory_gates):
            gate_to_check = track.mandatory_gates[len(self.mandatory_gates_crossed)]
            #gate_rect = pygame.Rect(min(track.internal_gate_points[gate_to_check][0],track.external_gate_points[gate_to_check][0]), min(track.internal_gate_points[gate_to_check][1],track.external_gate_points[gate_to_check][1]), abs(track.internal_gate_points[gate_to_check][0]-track.external_gate_points[gate_to_check][0])+1, abs(track.internal_gate_points[gate_to_check][1]-track.external_gate_points[gate_to_check][1])+1)
            gate_rect = track.gate_surfs[gate_to_check]
            if sprite_rect.colliderect(gate_rect):
                #if gate is passed
                if abs(gate_to_check-self.last_passed_gate)==1:
                    #Only update last passed gate for closest gate adjacent to the next or previous gate
                    self.last_passed_gate = gate_to_check
                self.most_recent_passed_gate = gate_to_check
                self.check_mandatory_gate(gate_to_check,track)
                if DEBUG_GATE_TRACKING and not self.is_drone:
                    logger.debug('{} - Furthest passed gate = {} - mandatory:{} - Last Passed gate: {} - Most Recent: {}'.format(self.color_text,self.furthest_past_gate, self.mandatory_gates_crossed,self.last_passed_gate, self.most_recent_passed_gate))


    def test_on_ramp(self, track: pysprint_tracks.Track):
        #Check if car is on a ramp, via collision with track ramp polygons
        was_on_ramp = self.on_ramp
        if self.last_passed_gate is None:
            return
        if self.most_recent_passed_gate is None:
            return
        if track.ramp_gates is None:
            return
        else:
            ramps_found = []
            for i in range(0, len(track.ramp_masks)):
                test = False
                # #only test for the polygon if the last past gates is on of the ramp gate or the immediate successor or predecessor
                # if (self.last_passed_gate >= (track.ramp_gates[i][0][0] - 1)) and (self.last_passed_gate <= (track.ramp_gates[i][len(track.ramp_gates[i])-1][1] + 1)):
                #only test for the polygon if the MOST RECENT gates is on of the ramp gate or the immediate successor or predecessor
                if (self.most_recent_passed_gate >= (track.ramp_gates[i][0][0] - 1)) and (self.most_recent_passed_gate <= (track.ramp_gates[i][len(track.ramp_gates[i])-1][1] + 1)):
                    test = True

                #If there is a shortcut ramp then we test betwe
                if not self.is_drone and not track.player_shortcut_bookend_gates is None and (self.most_recent_passed_gate >= (track.player_shortcut_bookend_gates[0])) and (self.most_recent_passed_gate <= (track.player_shortcut_bookend_gates[1])):
                    if self.sprite_angle == 12:
                        test = True
                    else:
                        return

                if test:
                    for j in range(0,len(track.ramp_masks[i])):
                        ramp_mask = track.ramp_masks[i][j]
                        if ramp_mask.overlap(self.car_mask, (round(self.x_position),round(self.y_position))):
                            ramps_found.append((i,j))
            if len(ramps_found)==0:
                if was_on_ramp:
                    if self.jumping and not self.mid_air:
                        self.init_mid_air(track)
                    else:
                        if not self.falling and not self.mid_air:
                            self.on_ramp = False
                            self.init_leaving_ramp(track)
            else:
                if len(ramps_found)==1:
                    #car intersects with one polygon only
                    if not was_on_ramp:
                        self.init_entering_ramp(track, ramps_found[0][0],ramps_found[0][1])
                    else:
                        #If jumping and intersecting with only the middle poly: we are mid-air
                        if self.jumping and self.current_ramp_poly[1]==1 and not self.mid_air and not self.landing:
                            self.init_mid_air(track)
                        else:
                            if not self.previous_ramp_poly is None:
                                if self.previous_ramp_poly[1]==1 and self.landing:
                                #We are now fully landed on the second ramp after being mid-air
                                    self.end_jump_loop()
                        if not (self.current_ramp_poly[0]==ramps_found[0][0] and self.current_ramp_poly[1]==ramps_found[0][1]):
                            if self.mid_air:
                                self.init_landing(track)
                            self.init_entering_ramp(track, ramps_found[0][0],ramps_found[0][1])
                else:
                    #car intersects with 2 polygons  if not already jumping then force middle polygon = i.e. jump
                    if not self.jumping and (self.previous_ramp_poly is None):
                        self.init_entering_ramp(track, ramps_found[0][0],1)
                    else:
                        if self.mid_air:
                            self.init_landing(track)
                        else:
                            if self.jumping:
                                if ramps_found[0][1]==1:
                                    #while jumping register the new polygon entered if not already done (i.e. if the prvevious poly is not already the middle one).
                                    if self.previous_ramp_poly[1]==1:
                                        self.init_entering_ramp(track, ramps_found[1][0],ramps_found[1][1])
                                else:
                                    if self.previous_ramp_poly[1]==1:
                                        self.init_entering_ramp(track, ramps_found[0][0],ramps_found[0][1])


    def test_on_bridge(self, track: pysprint_tracks.Track):
        #Check if car is on a bridge, via collision with track bridge polygons
        was_on_bridge = self.on_bridge
        if self.last_passed_gate is None:
            return
        if self.most_recent_passed_gate is None:
            return
        if track.bridge_gates is None:
            return
        else:
            bridges_found = []
            for i in range(0, len(track.bridge_masks)):
                # #only test for the polygon if the last past gates is on of the bridge gate or the immediate successor or predecessor
                #only test for the polygon if the MOST RECENT gates is on of the bridge gate or the immediate successor or predecessor
                if (self.most_recent_passed_gate >= (track.bridge_gates[i][0][0] - 1)) and (self.most_recent_passed_gate <= (track.bridge_gates[i][0][len(track.bridge_gates[i][0])-1] + 1)):
                    for j in range(0,len(track.bridge_masks[i])):
                        bridge_mask = track.bridge_masks[i][j]
                        if bridge_mask.overlap(self.car_mask, (round(self.x_position),round(self.y_position))):
                            bridges_found.append((i,j))
            if len(bridges_found)==0:
                if was_on_bridge:
                    self.init_leaving_bridge(track)
            else:
                #car intersects with one polygon only for a bridge
                if not was_on_bridge:
                    self.init_entering_bridge(track, bridges_found[0][0])

    def test_finish_line(self, track: pysprint_tracks.Track):
        #Detect if car collides with Finish line in the expected direction
        sprite_rect = pygame.Rect(self.x_position, self.y_position, self.sprites[self.sprite_angle].get_width(), self.sprites[self.sprite_angle].get_height())
        if sprite_rect.colliderect(track.finish_line):
            if not self.on_finish_line:
                self.on_finish_line = True
                if self.x_vector * track.finish_line_direction > 0:
                    full_lap = False
                    if self.passed_finish_line_wrong_way:
                        self.passed_finish_line_wrong_way = False
                        if DEBUG_FINISH:
                            logger.debug('{} - Passed the line in the right direction after going the wrong way)'.format(pygame.time.get_ticks()))
                    else:
                        #Check if all mandatory gates were passed before awarding a new lap
                        if not track.mandatory_gates is None:
                            if len(self.mandatory_gates_crossed)==len(track.mandatory_gates):
                                full_lap = True
                                #reset Gates trackers for the next lap
                                self.mandatory_gates_crossed.clear()
                                self.furthest_past_gate = None
                        if full_lap:
                            finish_time = pygame.time.get_ticks()
                            self.lap_times[self.lap_count] = finish_time - self.current_lap_start
                            if DEBUG_FINISH:
                                logger.debug('{} - New Lap {} - Duration: {})'.format(finish_time, self.lap_count, self.lap_times[self.lap_count]))
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
                                    logger.debug('{} - Race Finished - Duration: {} - Average lap: {} - Best Lap: {})'.format(finish_time, sum(self.lap_times), self.average_lap, self.best_lap))
                                return True
                            self.current_lap_start = finish_time
                            return False
                        else:
                            if DEBUG_FINISH:
                                logger.debug('{} - Passed the line in the right directionbut not all mandatory gates passed)'.format(pygame.time.get_ticks()))
                else:
                    self.passed_finish_line_wrong_way = True
                    if DEBUG_FINISH:
                        logger.debug('{} - Passed the line in the wrong direction)'.format(pygame.time.get_ticks()))
        else:
            self.on_finish_line = False


    def draw(self, track: pysprint_tracks.Track, cars):
        #Draw Car
        if not self.bumping:
            self.update_position(track, cars)
            self.ignore_controls = False
        if self.bumping:
            #Ignore controls until Buming routine is finished - Force Skidding & Decelaration
            self.decelerating = True
            self.rotating = False
            self.update_position(track, cars)
        if self.spinning:
            #Ignore controls until Spinning routine is finished - Force Skidding & Decelaration
            self.decelerating = True
            self.rotating = False
            self.update_position(track, cars)
        if self.jumping:
            #Ignore controls until Jump routine is finished - Force constant speed
            self.rotating = False
            if self.take_off or self.mid_air:
                self.decelerating = True
            elif self.landing:
                self.decelerating = False
            self.update_position(track, cars)
            self.ignore_controls = True

    def blit(self, track: pysprint_tracks.Track, overlay_blitted):
        #Cars are blited under the overlay to be hidden but not dust clouds, explisions and the helicopter
        #cars are blitted ontop of the overlay if on a Ramp
        if not overlay_blitted or self.on_ramp or self.on_bridge:
            #Car is not visible durign explosion
            if not self.crashing:
                game_display.blit(self.sprites[self.sprite_angle], (self.x_position, self.y_position))
                self.car_mask = self.sprites_masks[self.sprite_angle]

            if DEBUG_AI:
                if self.is_drone:
                    gfxdraw.line(game_display,round(self.x_position), round(self.y_position), round(self.x_position) + round(self.x_vector)*10, round(self.y_position) + round(self.y_vector)*10, self.main_color)
                    if not self.ideal_vector is None:
                        gfxdraw.line(game_display,round(self.x_position), round(self.y_position), round(self.ideal_vector[0] + self.x_position), round(self.y_position + self.ideal_vector[1]), (255,255,255))
                    if not self.next_mid_point is None:
                        gfxdraw.circle(game_display, round(self.next_mid_point[0]), round(self.next_mid_point[1]), 5, self.main_color)

        if overlay_blitted:
            #Blit Dust Cloud if Bumping
            if self.bumping or self.touch_down:
                if DEBUG_BUMP:
                    logger.debug('{} - Blit Bump Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
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

    def display_spinning(self):
        #Spin the car
        self.animation_index+=1
        self.tornado_index+=1
        if self.animation_index <17:
            self.sprite_angle+=1
            if self.sprite_angle >=16:
                self.sprite_angle-=16
        else:
            if not self.on_tornado:
                self.end_spinning_loop()
            else:
                #1 fullrotation and a quarter when hitting a tornado
                if self.tornado_index >20:
                    self.end_spinning_loop()


    def display_bump_cloud(self):
        if DEBUG_BUMP or DEBUG__CAR_COLLISION:
            logger.debug('{} - Increment Bump Frame'.format(pygame.time.get_ticks()))
        if self.animation_index < len(dust_cloud_frames):
            self.animation_index += 1


    def display_explosion(self):
        if self.vertical_helicopter:
            self.display_explosion_vertical()
        else:
            self.display_explosion_horizontal()

    def display_explosion_horizontal(self):
        if DEBUG_CRASH:
            logger.debug('{} - Blit Crash Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
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
            logger.debug('{} - Blit Crash Frame - Index: {}'.format(pygame.time.get_ticks(), self.animation_index))
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

    def validate_next_tuple(self, track: pysprint_tracks.Track, new_next_gate):
        #If current gate is already a tuple
        if type(self.next_gate) is tuple:
            #Pointing to the next uncrossed gate
            if len(self.shortcut_gates_crossed) < len(track.internal_ai_gates_shortcuts[self.next_gate[0]])-1:
                self.next_gate = (self.next_gate[0], len(self.shortcut_gates_crossed)+1)

            if self.next_gate[1] == len(track.external_ai_gates_shortcuts[new_next_gate[0]])-1:
                if len(self.shortcut_gates_crossed) == len(track.internal_ai_gates_shortcuts[self.next_gate[0]])-1:
                    #Exiting a shortcut and resuming following the track if all shortcut cgates have been passed & point to the shortcut exit gate
                    self.next_gate = track.external_ai_gates_shortcuts[new_next_gate[0]][0][1]
                    self.shortcut_gates_crossed = None
                else:
                    #If next shortcut gate is ou of bounds, Pointing to the next uncrossed gate
                    self.next_gate = (self.next_gate[0], len(self.shortcut_gates_crossed)+1)
        else:
            #Check if previous gate is close to the "shortcut trigger gate" for the shortcut thta has been detected
            if abs(self.next_gate - track.external_ai_gates_shortcuts[new_next_gate[0]][0][0])<2:
                #check if the gate is open, if not, continue on track and ignore shortcut
                if track.road_gates_frames_index[new_next_gate[0]] == 4:
                    self.next_gate = new_next_gate
                    self.shortcut_gates_crossed = []
        #Test is vector collides with Track - if collision, ignore shortcuts and find the next normal track gate
        if type(self.next_gate) is tuple:
            if self.test_vector_track_collision(track,self.next_gate):
                self.next_gate = track.find_progress_gate((self.x_position, self.y_position))


    def test_vector_track_collision(self, track: pysprint_tracks.Track, new_next_gate):
        midpOint_modifier = self.get_mid_point_modifier()
        #Eliminate cases where the Vector is impossible to follow, i.e. collidign with the track mask
        #Gate index is a tuple means we deal witha an open gate shortcut
        if type(new_next_gate) is tuple:
            test_next_mid_point = ((track.external_ai_gates_shortcuts[new_next_gate[0]][new_next_gate[1]][0] + track.internal_ai_gates_shortcuts[new_next_gate[0]][new_next_gate[1]][0])/ 2, (track.external_ai_gates_shortcuts[new_next_gate[0]][new_next_gate[1]][1] + track.internal_ai_gates_shortcuts[new_next_gate[0]][new_next_gate[1]][1])/ 2)
        else:
            test_next_mid_point = ((track.external_gate_points[new_next_gate][0] + track.internal_gate_points[new_next_gate][0]) / midpOint_modifier, (track.external_gate_points[new_next_gate][1] + track.internal_gate_points[new_next_gate][1]) / midpOint_modifier)

        test_ideal_vector = (round(test_next_mid_point[0] - self.x_position), round(test_next_mid_point[1] - self.y_position))
        #drawing a transparent surface and blit the vector and checking if it collides with the Circuit mask
        vector_surf.fill((0,0,0))
        line_start = (round(self.x_position), round(self.y_position))
        line_end = (round(self.x_position) + test_ideal_vector[0], round(self.y_position) + test_ideal_vector[1])

        gfxdraw.line(vector_surf, line_start[0], line_start[1], line_end[0], line_end[1], (255,255,255))

        vector_mask = pygame.mask.from_surface(vector_surf, 50)
        if self.on_ramp or self.on_bridge:
            return track.track_upper_mask_mask.overlap(vector_mask, (0,0))
        else:
            return track.track_mask_mask.overlap(vector_mask, (0,0))


    def get_mid_point_modifier(self):
        return 2 * (1 + (self.drone_personality_modifiers[self.drone_personality]-1) / 8)

    def calculate_ideal_vector(self, track: pysprint_tracks.Track, actual_gate_step):
        new_next_gate = track.find_progress_gate((self.x_position, self.y_position),actual_gate_step, self.next_gate, self)

        #Midpoint modifier: Normal personality aime for the exact middle of the gate, prudent and aggressive symetrically outcentered
        if self.on_ramp or self.on_bridge:
            midpOint_modifier = 2
        else:
            midpOint_modifier = self.get_mid_point_modifier()

        #Gate is a tuple we deal with an open gate shortcut
        if type(new_next_gate) is tuple:
            self.validate_next_tuple(track,new_next_gate)

        if not type(new_next_gate) is tuple:
            old_next_gate = new_next_gate
            new_next_gate += actual_gate_step
            if new_next_gate>=len(track.external_gate_points):
                new_next_gate-= len(track.external_gate_points)
            if self.next_gate is None:
                self.next_gate = new_next_gate
            else:
                #Exiting a shortcut and resuming following the track if all shortcut gates have been passed & point to the shortcut exit gate
                if type(self.next_gate) is tuple:
                     if len(self.shortcut_gates_crossed) == len(track.internal_ai_gates_shortcuts[self.next_gate[0]])-1:
                        self.next_gate = track.external_ai_gates_shortcuts[self.next_gate[0]][0][1]
                        self.shortcut_gates_crossed = None
                else:
                    #Eliminate edge cases where a gate is detected on another part of the circuit, i.e further than the actual next gate
                    if abs(new_next_gate - self.next_gate) > (actual_gate_step+1) and abs(new_next_gate - self.next_gate) > len(track.external_gate_points) - (actual_gate_step+1):
                        self.next_gate+=actual_gate_step
                    else:
                        #Eliminate cases where the AI is tempte to cut the roundabout
                        if abs(new_next_gate - self.next_gate) > (actual_gate_step+1) and abs(new_next_gate - self.next_gate) < 6:
                            self.next_gate+=actual_gate_step
                        else:
                            #Eliminate edge cases where the new next gate is behind the previous next next gate
                            #Except if the previous next gate have a vector that collides with the track mask
                            if new_next_gate >= self.next_gate:
                                if self.test_vector_track_collision(track,new_next_gate):
                                    self.next_gate=old_next_gate
                                else:
                                    self.next_gate = new_next_gate
                            else:
                                if self.test_vector_track_collision(track,self.next_gate):
                                    self.next_gate = new_next_gate

                    if self.next_gate >= len(track.external_gate_points):
                        self.next_gate -= len(track.external_gate_points)

        #Gate index is a tuple means we deal witha an open gate shortcut
        if type(self.next_gate) is tuple:
            self.next_mid_point = ((track.external_ai_gates_shortcuts[self.next_gate[0]][self.next_gate[1]][0] + track.internal_ai_gates_shortcuts[self.next_gate[0]][self.next_gate[1]][0])/ 2, (track.external_ai_gates_shortcuts[self.next_gate[0]][self.next_gate[1]][1] + track.internal_ai_gates_shortcuts[self.next_gate[0]][self.next_gate[1]][1])/ 2)
        else:
            self.next_mid_point = ((track.external_gate_points[self.next_gate][0] + track.internal_gate_points[self.next_gate][0]) / midpOint_modifier, (track.external_gate_points[self.next_gate][1] + track.internal_gate_points[self.next_gate][1]) / midpOint_modifier)
        self.ideal_vector = (self.next_mid_point[0] - self.x_position, self.next_mid_point[1] - self.y_position)

    def get_cosine(self, original_vector,vector_to_compare):
        #cosine method
        dotProduct = vector_to_compare[0] * original_vector[0] + vector_to_compare[1] * original_vector[1]
        modOfVector1 = math.sqrt( vector_to_compare[0] * vector_to_compare[0] + vector_to_compare[1]*vector_to_compare[1])*math.sqrt(original_vector[0]*original_vector[0] + original_vector[1]*original_vector[1])
        if modOfVector1 ==0:
            return 0
        else:
            return math.degrees(math.acos(dotProduct/modOfVector1))

    def get_sine(self, original_vector, vector_to_compare):
        #sine method
        car_vector_length = math.sqrt(original_vector[0]**2 + original_vector[1]**2)
        cross_product = car_vector_length * math.sqrt(vector_to_compare[0]**2 + vector_to_compare[1]**2)
        # using cross-product formula
        if cross_product ==0:
            return 0
        else:
            factor = (original_vector[0] * vector_to_compare[1] - original_vector[1] * vector_to_compare[0])/(cross_product)
            if abs(factor) > 1.00000000000000011 and abs(factor) < 1.000011:
                factor = 1 * factor/abs(factor)
            return -math.degrees(math.asin(factor))


    def ai_drive(self, track: pysprint_tracks.Track):
        if self.is_drone and not track.internal_ai_gates_shortcuts is None:
            self.test_shortcut_gates(track)

        self.calculate_ideal_vector(track, self.gate_step)

        cosine_angle =self.get_cosine((self.x_vector,self.y_vector), self.ideal_vector)
        angle = self.get_sine((self.x_vector,self.y_vector), self.ideal_vector)

        if DEBUG_AI:
            logger.debug('{} - Next Gate:{} - Current Vector: ({:.2f},{:.2f}) - Ideal Vector: ({:.2f},{:.2f}) - Angle: {:.2f}° - Cosine Angle: {:.2f}°'.format(self.color_text, self.next_gate, self.x_vector, self.y_vector, self.ideal_vector[0], self.ideal_vector[1],angle, cosine_angle))
        need_to_turn = False
        if self.on_ramp:
            if (angle > self.turning_angle_threshold*2) or ( angle < -self.turning_angle_threshold*2):
                need_to_turn = True
        elif (angle > self.turning_angle_threshold) or ( angle < -self.turning_angle_threshold):
            need_to_turn = True

        if need_to_turn:
            if angle > 0:
                self.rotate(True, track)
                if DEBUG_AI:
                    print ('Turning Left')
            else:
                self.rotate(False, track)
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
            #If Vector angle is too wide review te next gate
            if (cosine_angle > (180-self.turning_angle_threshold)):
                i = 1
                while (abs(angle) < self.turning_angle_threshold*1.5) and (i<5):
                    #Check direction for Next Gate until we get a clear direction to turn to
                    if DEBUG_AI:
                        print ('{} - 180° - Checking {} Gate(s) further'.format(self.color_text, i))
                    self.calculate_ideal_vector(track, self.gate_step + i)
                    angle = self.get_sine((self.x_vector,self.y_vector), self.ideal_vector)
                    cosine_angle =self.get_cosine((self.x_vector,self.y_vector), self.ideal_vector)
                    i+=1
                    self.rotate(angle > 0, track)
                #Search for next gates fails, try previous gates
                if i>=5:
                    i = 1
                    while (abs(angle) < self.turning_angle_threshold*1.5) and (i<5):
                        #Check direction for Next Gate until we get a clear direction to turn to
                        if DEBUG_AI:
                            print ('{} - 180° - Checking {} Gate(s) backwards'.format(self.color_text, i))
                        self.calculate_ideal_vector(track, self.gate_step - i)
                        angle = self.get_sine((self.x_vector,self.y_vector), self.ideal_vector)
                        cosine_angle =self.get_cosine((self.x_vector,self.y_vector), self.ideal_vector)
                        i+=1
                        self.rotate(angle > 0, track)
                self.decelerate()
            else:
                self.accelerate()

