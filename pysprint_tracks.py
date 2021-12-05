#pysprint_tracks.py
import math
import json
import random
from numpy import False_, object_, positive
from numpy.lib.index_tricks import _fill_diagonal_dispatcher
from numpy.lib.polynomial import poly
import pygame
from pygame import Surface, gfxdraw, draw

DEBUG_OBSTACLES = False
DEBUG_RAMPS = False

#Track 1 Setup
track1_json_filename = 'Assets/SuperSprintTrack1.json'

#Track 2 Setup
track2_json_filename = 'Assets/SuperSprintTrack2.json'

#Track 3 Setup
track3_json_filename = 'Assets/SuperSprintTrack3.json'

#Track 4 Setup
track4_json_filename = 'Assets/SuperSprintTrack4.json'

#Track 5 Setup
track5_json_filename = 'Assets/SuperSprintTrack5.json'

#Track 6 Setup
track6_json_filename = 'Assets/SuperSprintTrack6.json'

#Track 7 Setup
track7_json_filename = 'Assets/SuperSprintTrack7.json'

#Track 7 Setup
track8_json_filename = 'Assets/SuperSprintTrack8.json'

#Spills
oil_spill_image = None
water_spill_image = None
grease_spill_image = None
oil_spill_mask = None
water_spill_mask = None
grease_spill_mask = None

#Wrench
wrench_image = None
wrench_mask = None
wrench_position = None
wrench_display_interval = 7000
wrench_display_duration = 240000

#Traffic Cone
traffic_cone = None
traffic_cone_mask = None
traffic_cone_shade = None

#Tornado
tornado_frames = None
tornado_frames_masks = None
tornado_mask = None

#Bonus Frames
bonus_frames = None
bonus_frames_masks = None
bonus_shade_frames = None
bonus_position = None
bonus_display_interval = 6000
bonus_display_duration = 10000
tiny_font = None

#Poles Frames
poles_frames = None
poles_frames_masks = None
poles_gate = None
poles_pop_up_interval = 900
poles_stay_up_duration = 1800
#Max and min random time for a gate to be closed or open
max_random_time = 3000
min_random_time = 2000

game_display = None
display_width = None
display_height = None
road_gate_frames = None
road_gate_mask_frames = None
road_gate_shade_frames = None


def calculate_distance(point1,point2):
    return math.sqrt( ((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))

class Track:

    def __init__(self):
        self.difficulty_level = None
        self.wrenches = None
        self.background_filename = None
        self.track_mask_filename = None
        self.track_upper_mask_filename = None
        self.overlay_filename =  None
        self.thumbnail_filename = None
        self.background = None
        self.base_mask = None
        self.track_mask = None
        self.track_mask_mask = None
        self.track_upper_mask = None
        self.track_upper_mask_mask = None
        self.track_overlay = None
        self.thumbnail = None
        self.first_car_start_position = None
        self.flag_anchor = None
        self.track_number = None
        self.start_sprite_angle = None
        self.score_time_reference = None
        self.complete_lap_score = None
        self.external_borders = None
        self.internal_borders = None
        self.secondary_internal_borders = None
        self.finish_line_rect = None
        self.finish_line = None
        self.finish_line_direction = None
        #To check if players have driven through mandatory checkpoints (i.e. roundabouts)
        self.mandatory_gates = None
        #External gate points
        self.external_gate_points = None
        self.internal_gate_points = None
        self.gate_surfs = []
        self.gate_masks = []
        #Track Opening Gates
        self.road_gates_anchors = None
        self.road_gates_frames_index = []
        self.road_gates_timers = []
        self.road_gates_opening = []
        #Ramps
        self.ramp_gates = None
        self.ramp_masks = []
        self.ramp_surfs = []
        #Bridges
        self.bridge_gates = None
        self.bridge_masks = []
        self.bridge_surfs = []
        #When timer = next event time open or close the gate depending on status
        self.external_ai_gates_shortcuts = None
        self.internal_ai_gates_shortcuts = None
        self.ai_gate_surfs = []
        self.ai_gate_masks = []
        #Player Shortcuts
        self.external_player_gates_shortcut = None
        self.internal_player_gates_shortcut = None
        self.player_shortcut_bookend_gates = None
        #Timer for Bonus display animation
        self.bonus_timer = None
        self.bonus_displayed = False
        self.bonus_rolling = False
        self.bonus_frame_index = None
        self.bonus_value = None
        self.bonus_position = None
        self.on_bridge_or_ramp_bonus = False
        #Timer for Wrench display
        self.wrench_timer = None
        self.wrench_displayed = False
        self.wrench_position = None
        self.on_bridge_or_ramp_wrench = False
        #Obstacles
        self.display_pole = False
        self.display_tornado = False
        self.display_oil_spill = False
        self.display_grease_spill = False
        self.display_water_spill = False
        self.display_cones = False
        self.on_bridge_or_ramp_pole = False
        self.on_bridge_or_ramp_tornado = False
        self.on_bridge_or_ramp_oil_spill = False
        self.on_bridge_or_ramp_grease_spill = False
        self.on_bridge_or_ramp_water_spill = False
        self.on_bridge_or_ramp_cones = False

        self.cones_count = 0
        #Spills
        self.oil_spill_position = None
        self.water_spill_position = None
        self.grease_spill_position = None
        #Timer for Poles display animation
        self.poles_timer = None
        self.poles_popping_up = False
        self.poles_popping_down = False
        self.poles_frame_indexes = None
        self.poles_moving_index = None
        self.poles_gate_index = None
        self.pole_mask = None
        self.external_pole_position = None
        self.internal_pole_position = None
        self.middle_pole_position = None
        #Traffic Cones
        self.traffic_cones_positions = None
        self.on_bridge_or_ramp_grease_traffic_cones = None
        #All static Obstacles Gates
        self.obstacle_gates = []
        #Tornado
        self.tornado_position = None
        self.tornado_timer = None
        self.tornado_frame_index = None
        self.tornado_mask = None

    def load_track_definition(self, filename):
        with open(filename) as track_file:
            track_json = json.load(track_file)

        self.track_number = track_json["track_number"]
        self.difficulty_level = track_json["difficulty_level"]
        self.wrenches = track_json["wrenches"]
        self.background_filename = track_json["background_filename"]
        self.track_mask_filename = track_json["mask_filename"]
        if "upper_mask_filename" in track_json:
            self.track_upper_mask_filename = track_json["upper_mask_filename"]
        self.overlay_filename =  track_json["overlay_filename"]
        if "thumbnail_filename" in track_json:
            self.thumbnail_filename =  track_json["thumbnail_filename"]

        self.first_car_start_position = track_json["first_car_start_position"]
        self.flag_anchor = track_json["flag_anchor"]
        self.start_sprite_angle = track_json["start_sprite_angle"]
        self.score_time_reference = track_json["score_time_reference"]
        self.complete_lap_score = track_json["complete_lap_score"]
        self.external_borders = track_json["external_borders"]
        self.internal_borders = track_json["internal_borders"]
        if "secondary_internal_borders" in track_json:
            self.secondary_internal_borders = track_json["secondary_internal_borders"]
        self.finish_line_rect = track_json["finish_line_rect"]
        self.finish_line_direction = track_json["finish_line_direction"]

        self.external_gate_points = track_json["external_gate_points"]
        self.internal_gate_points = track_json["internal_gate_points"]
        for i in range(len(self.external_gate_points)):
            self.gate_surfs.append(pygame.Rect(min(self.internal_gate_points[i][0],self.external_gate_points[i][0]), min(self.internal_gate_points[i][1],self.external_gate_points[i][1]), abs(self.internal_gate_points[i][0]-self.external_gate_points[i][0])+1, abs(self.internal_gate_points[i][1]-self.external_gate_points[i][1])+1))


        if "mandatory_gates" in track_json:
            self.mandatory_gates = track_json["mandatory_gates"]
        if "road_gates_anchors" in track_json:
            self.road_gates_anchors = track_json["road_gates_anchors"]
        if "external_ai_gates_shortcuts" in track_json:
            self.external_ai_gates_shortcuts = track_json["external_ai_gates_shortcuts"]
        if "internal_ai_gates_shortcuts" in track_json:
            self.internal_ai_gates_shortcuts = track_json["internal_ai_gates_shortcuts"]
        if "external_player_gates_shortcut" in track_json:
            self.external_player_gates_shortcut = track_json["external_player_gates_shortcut"]
        if "internal_player_gates_shortcut" in track_json:
            self.internal_player_gates_shortcut = track_json["internal_player_gates_shortcut"]

        if "player_shortcut_ramp_gates" in track_json:
            self.ramp_gates = track_json["player_shortcut_ramp_gates"]
            for ramp in self.ramp_gates:
                new_ramp = []
                for polygon in ramp:
                    gate_points = []
                    i = 0
                    while i<len(polygon):
                        gate_points.append(self.external_player_gates_shortcut[polygon[i]])
                        i+=1
                    i = len(polygon) - 1
                    while i>=0:
                        gate_points.append(self.internal_player_gates_shortcut[polygon[i]])
                        i-=1
                    ramp_surf = pygame.Surface((display_width,display_height))
                    ramp_surf.fill((0,0,0))
                    ramp_surf.set_colorkey((0,0,0))
                    pygame.draw.polygon(ramp_surf,(34,170,102),gate_points)
                    ramp_mask = pygame.mask.from_surface(ramp_surf, 50)
                    new_ramp.append(ramp_mask)
                    self.ramp_surfs.append(ramp_surf)
                self.ramp_masks.append(new_ramp)
        if "player_shortcut_bookend_gates" in track_json:
            self.player_shortcut_bookend_gates = track_json["player_shortcut_bookend_gates"]

        if "ramp_gates" in track_json:
            self.ramp_gates = track_json["ramp_gates"]
            for ramp in self.ramp_gates:
                new_ramp = []
                for polygon in ramp:
                    gate_points = []
                    i = 0
                    while i<len(polygon):
                        gate_points.append(self.external_gate_points[polygon[i]])
                        i+=1
                    i = len(polygon) - 1
                    while i>=0:
                        gate_points.append(self.internal_gate_points[polygon[i]])
                        i-=1
                    ramp_surf = pygame.Surface((display_width,display_height))
                    ramp_surf.fill((0,0,0))
                    ramp_surf.set_colorkey((0,0,0))
                    pygame.draw.polygon(ramp_surf,(34,170,102),gate_points)
                    ramp_mask = pygame.mask.from_surface(ramp_surf, 50)
                    new_ramp.append(ramp_mask)
                    self.ramp_surfs.append(ramp_surf)
                self.ramp_masks.append(new_ramp)

        if "bridge_gates" in track_json:
            self.bridge_gates = track_json["bridge_gates"]
            for bridge in self.bridge_gates:
                new_bridge = []
                for polygon in bridge:
                    gate_points = []
                    i = 0
                    while i<len(polygon):
                        gate_points.append(self.external_gate_points[polygon[i]])
                        i+=1
                    i = len(polygon) - 1
                    while i>=0:
                        gate_points.append(self.internal_gate_points[polygon[i]])
                        i-=1
                    bridge_surf = pygame.Surface((display_width,display_height))
                    bridge_surf.fill((0,0,0))
                    bridge_surf.set_colorkey((0,0,0))
                    pygame.draw.polygon(bridge_surf,(34,170,102),gate_points)
                    bridge_mask = pygame.mask.from_surface(bridge_surf, 50)
                    new_bridge.append(bridge_mask)
                    self.bridge_surfs.append(bridge_surf)
                self.bridge_masks.append(new_bridge)


    def find_gate_point(self, position, gate_points):
        shortest_distance = -1
        shortest_index = -1
        for i in range (0, len(gate_points)):
            distance =  calculate_distance(gate_points[i], position)
            if (shortest_distance < 0) or (distance < shortest_distance):
                shortest_distance = distance
                shortest_index = i
        return shortest_index

    def find_shortcut_point(self, position, ai_shortcut_points, currentgate):
        shortest_distance = -1
        shortest_index = -1
        for i in range(0, len(self.road_gates_anchors)):
            for j in range (1, len(ai_shortcut_points[i])):
                distance =  calculate_distance(ai_shortcut_points[i][j], position)
                if (shortest_distance < 0) or (distance < shortest_distance):
                    shortest_distance = distance
                    shortest_index = (i,j)
        #Check if we have an open gate close by and if we can take the shortcut
        #if current gate is a tuple, we already engaged in a shortcut,
        #we need to continue on it regardless of teh gate status
        if currentgate is None or not type(currentgate) is tuple:
            #If we're not already in a shortcut then we only return a shortcut if the gate is open or opening
            if not self.road_gates_frames_index[i] == 4 or not self.road_gates_opening[i]:
                return -1
            #And if the shortcut gate detected is the first one of teh shortcut (i.e. index = 1)
            if shortest_index[1]>1:
                return -1
        return shortest_index


    def find_progress_gate(self, position, actual_gate_step = None, currentgate = None, car = None):
        #Check closest Internal and external gate point,
        int_index = self.find_gate_point(position, self.internal_gate_points)
        ext_index = self.find_gate_point(position, self.external_gate_points)


        closest_gate_index = None
        #If External & Internal Points belong to widely distant gates, return lowets gate
        #o rthe closest to the current gate when available
        if abs(ext_index-int_index)>= 3:
            if currentgate is None or type(currentgate) is tuple:
                if ext_index > int_index:
                    closest_gate_index = int_index
                else:
                    closest_gate_index = ext_index
            else:
                if abs(int_index-currentgate) < abs(ext_index-currentgate):
                    closest_gate_index = int_index
                else:
                    if abs(int_index-currentgate) > abs(ext_index-currentgate):
                        closest_gate_index = ext_index
                    else:
                        if ext_index > int_index:
                            closest_gate_index = int_index
                        else:
                            closest_gate_index = ext_index
            #Eliminate index for which Vector collides with track
            if not car is None:
                if car.test_vector_track_collision(self,int_index):
                    closest_gate_index = ext_index
                else:
                    if car.test_vector_track_collision(self,ext_index):
                        closest_gate_index = int_index
        else:
            #Return the highest index to ignore postion relative to borders
            if ext_index >= int_index:
                closest_gate_index = ext_index
            else:
                closest_gate_index = int_index

        closest_shortcut_index = None
        if not actual_gate_step is None and not  self.internal_ai_gates_shortcuts is None:
            int_shortcut = self.find_shortcut_point(position, self.internal_ai_gates_shortcuts, currentgate)
            ext_shortcut = self.find_shortcut_point(position, self.external_ai_gates_shortcuts, currentgate)

            if type(int_shortcut) is tuple and type(ext_shortcut) is tuple:
                #If External & Internal Points belong to wodely distant gates, return the lowest one
                if abs(ext_shortcut[1]-int_shortcut[1])>= 3:
                    if ext_shortcut[1] > int_shortcut[1]:
                        closest_shortcut_index = int_shortcut
                    else:
                        closest_shortcut_index = ext_shortcut
                else:
                    #Return the highest index to ignore postion relative to borders
                    if ext_shortcut[1] >= int_shortcut[1]:
                        closest_shortcut_index = ext_shortcut
                    else:
                        closest_shortcut_index = int_shortcut

        #if current gate is a tuple, we already engaged in a shortcut,
        #we need to continue on it regardless i.e. force usage of a shortcut gate
        #Except f we already are on the last gate of teh shortcut
        if not currentgate is None and type(currentgate) is tuple:
            if currentgate[1] < len(self.external_ai_gates_shortcuts[currentgate[0]]):
                if not closest_shortcut_index is None:
                    return closest_shortcut_index
        #if we detect a potential shortcut determine if the next gate is closer to the car than the shortcut gate
        if not closest_shortcut_index is None:
            next_gate_index = closest_gate_index + actual_gate_step
            if next_gate_index >= len(self.external_gate_points):
                next_gate_index -= len(self.external_gate_points)

            next_mid_point = ((self.external_gate_points[next_gate_index][0] + self.internal_gate_points[next_gate_index][0])/2, (self.external_gate_points[next_gate_index][1] + self.internal_gate_points[next_gate_index][1])/2)
            shortcut_mid_point = ((self.external_ai_gates_shortcuts[closest_shortcut_index[0]][closest_shortcut_index[1]][0] + self.internal_ai_gates_shortcuts[closest_shortcut_index[0]][closest_shortcut_index[1]][0])/2, (self.external_ai_gates_shortcuts[closest_shortcut_index[0]][closest_shortcut_index[1]][1] + self.internal_ai_gates_shortcuts[closest_shortcut_index[0]][closest_shortcut_index[1]][1])/2)
            if calculate_distance(next_mid_point, position)>calculate_distance(shortcut_mid_point,position):
                return closest_shortcut_index
        return closest_gate_index

    def get_score_from_laptime(self, laptime):
        if laptime == 0:
            return 0
        else:
            #calculate score based on difference between best laptime and reference lap time for the track
            score = math.ceil((500 * (1 + self.score_time_reference/(laptime/1000)) - 600) / 10) * 10
            if score < 0:
                return 0
            else:
                return score

    def update_score_from_position(self, car):
        if car.last_passed_gate is None:
            return
        index = car.last_passed_gate
        score_increment = 0
        if not type(index) is tuple:
            score_increment = math.ceil((car.lap_count+1) * (index/len(self.internal_borders))) * 30
        #Increment score if there has been progress since last score increment
        if score_increment > car.previous_score_increment:
            car.score += score_increment - car.previous_score_increment
            car.previous_score_increment = score_increment

    def blit_background(self,race_started):
        surf = self.background.copy()
        if not self.road_gates_anchors is None:
            if len(self.road_gates_timers)==0:
                #Initialise gates status and timers
                i = 0
                for anchor in self.road_gates_anchors:
                    self.road_gates_frames_index.append(0)
                    # if race_started then set timer (gates should be closed and frozen when "get ready" is desplayed
                    if race_started:
                        self.road_gates_timers.append(pygame.time.get_ticks() + i * 500)
                        self.road_gates_opening.append(False)
                        i+=1
            if race_started:
                now = pygame.time.get_ticks()
            for i in range(0, len(self.road_gates_anchors)):
                if race_started:
                    #If gate is closed or open (frame 0 or frame 4): blit the same frame until timer is reached
                    if self.road_gates_frames_index[i] == 0 or self.road_gates_frames_index[i] == 4:
                        if now >=self.road_gates_timers[i]:
                            self.road_gates_timers[i] = now + 100
                            if self.road_gates_frames_index[i] == 0:
                                self.road_gates_opening[i] = True
                                self.road_gates_frames_index[i] += 1
                            elif self.road_gates_frames_index[i] == 4:
                                self.road_gates_opening[i] = False
                                self.road_gates_frames_index[i] -= 1
                    #If gate is closing or opening (Frames 1,2 & 3): blit the next (or previous) frame until timer is reached
                    if self.road_gates_frames_index[i] > 0 and self.road_gates_frames_index[i] < 4:
                        if now >=self.road_gates_timers[i]:
                            if self.road_gates_opening[i]:
                                self.road_gates_frames_index[i] += 1
                                #if Gate is fully open, randomize timer to start closing it
                                if self.road_gates_frames_index[i] == 4:
                                    self.road_gates_timers[i] = now + random.randint(min_random_time,max_random_time)
                                else:
                                    self.road_gates_timers[i] = now + 100
                            else:
                                self.road_gates_frames_index[i] -= 1
                                #if Gate is fully closed, randomize timer to start opening it
                                if self.road_gates_frames_index[i] == 0:
                                    self.road_gates_timers[i] = now + random.randint(min_random_time,max_random_time)
                                else:
                                    self.road_gates_timers[i] = now + 10

                surf.blit(road_gate_frames[self.road_gates_frames_index[i]],(self.road_gates_anchors[i][0],self.road_gates_anchors[i][1]))
        self.update_track_mask()
        game_display.blit(surf,(0,0))


    def blit_overlay(self, race_started):
        surf = self.track_overlay.copy()
        if not self.road_gates_anchors is None:
            for i in range(0, len(self.road_gates_anchors)):
                surf.blit(road_gate_shade_frames[self.road_gates_frames_index[i]],(self.road_gates_anchors[i][0],self.road_gates_anchors[i][1]))

        if self.display_tornado:
            #Display Tornado
            if self.tornado_position is None:
                self.tornado_position = (random.randint(0, self.track_mask.get_width()-tornado_frames[0].get_width()),random.randint(0, self.track_mask.get_height()-tornado_frames[0].get_height()))
                self.tornado_frame_index = 0
                self.tornado_timer = pygame.time.get_ticks()
                self.tornado_mask = tornado_frames_masks[self.tornado_frame_index]
            if race_started:
                now =  pygame.time.get_ticks()
                if now >=self.tornado_timer:
                    if self.tornado_frame_index == 0:
                        self.tornado_frame_index = 1
                    else:
                        self.tornado_frame_index = 0
                    rand_x = random.randint(self.tornado_position[0]-5,self.tornado_position[0]+5)
                    if rand_x >= self.track_mask.get_width()-tornado_frames[0].get_width():
                        rand_x = self.tornado_position[0] - 5
                    if rand_x < 0:
                        rand_x = 0
                    rand_y = random.randint(self.tornado_position[1]-5,self.tornado_position[1]+5)
                    if rand_y >= self.track_mask.get_height()-tornado_frames[0].get_height():
                        rand_y = self.tornado_position[1] - 5
                    if rand_y<0:
                        rand_y = 0
                    self.tornado_position = (rand_x,rand_y)
                    self.tornado_timer = now + 100
                self.tornado_mask = tornado_frames_masks[self.tornado_frame_index]
                surf.blit(tornado_frames[self.tornado_frame_index],self.tornado_position)
        if DEBUG_RAMPS:
            for ramp in self.ramp_surfs:
                surf.blit(ramp,(0,0))
            for bridge in self.bridge_surfs:
                surf.blit(bridge,(0,0))
        game_display.blit(surf,(0,0))

    def update_track_mask(self):
        self.track_mask = self.base_mask.copy()
        if not self.road_gates_anchors is None:
            for i in range(0, len(self.road_gates_anchors)):
                self.track_mask.blit(road_gate_mask_frames[self.road_gates_frames_index[i]],(self.road_gates_anchors[i][0],self.road_gates_anchors[i][1]))
        self.track_mask_mask = pygame.mask.from_surface(self.track_mask, 50)

    def get_random_poles_position(self):
        #Pick a gate at random where teh gate is more than 70 pixels long
        random_gate = random.randint(1, len(self.external_gate_points)-1)
        while calculate_distance(self.external_gate_points[random_gate],self.internal_gate_points[random_gate])<70:
            random_gate = random.randint(0, len(self.external_gate_points)-1)
        return random_gate

    def test_object_on_track(self, position, width, height):
        object_mask = pygame.mask.from_surface(pygame.Surface((width,height)), 50)
        return  self.track_mask_mask.overlap(object_mask, (round(position[0]),round(position[1])))

    def test_object_on_bridge(self, position, width, height):
        object_mask = pygame.mask.from_surface(pygame.Surface((width,height)), 50)
        bridges_found = []
        for i in range(0, len(self.bridge_masks)):
            for j in range(0,len(self.bridge_masks[i])):
                bridge_mask = self.bridge_masks[i][j]
                if bridge_mask.overlap(object_mask, (round(position[0]),round(position[1]))):
                    bridges_found.append((i,j))
        return len(bridges_found)>0


    def test_object_on_ramp(self, position, width, height):
        object_mask = pygame.mask.from_surface(pygame.Surface((width,height)), 50)
        ramps_found = []
        for i in range(0, len(self.ramp_masks)):
            for j in range(0,len(self.ramp_masks[i])):
                ramp_mask = self.ramp_masks[i][j]
                if ramp_mask.overlap(object_mask, (round(position[0]),round(position[1]))):
                    ramps_found.append((i,j))
        return len(ramps_found)>0


    def get_random_position(self, height, width, force_gate = None):
        #Pick a gate at random and place the object randomly on the gate
        free_gate = False
        if force_gate is None:
            while not free_gate:
                random_gate = random.randint(0, len(self.external_gate_points)-1)
                free_gate = True
                for gate_index in self.obstacle_gates:
                    if random_gate == gate_index:
                        free_gate=False
        else:
            random_gate = force_gate

        self.obstacle_gates.append(random_gate)
        is_ramp_or_bridge_gate = False
        if not self.ramp_gates is None:
            for i in self.ramp_gates:
                for j in i:
                    for k in j:
                        if k==random_gate:
                            is_ramp_or_bridge_gate = True
        if not self.bridge_gates is None:
            for i in self.bridge_gates:
                for j in i:
                    for k in j:
                        if k==random_gate:
                            is_ramp_or_bridge_gate = True

        #define a box with the gate ahead of the one that was picked at randow and place the obstacle randomly inside it
        next_random_gate = random_gate + 1
        if next_random_gate>=len(self.external_gate_points):
            next_random_gate = 0

        ext_x = round(self.external_gate_points[random_gate][0] - (width/2))
        ext_y = round(self.external_gate_points[random_gate][1] - (height/2))
        int_x = round(self.internal_gate_points[next_random_gate][0] - (width/2))
        int_y = round(self.internal_gate_points[next_random_gate][1] - (height/2))

        if ext_x<int_x:
            min_x  = ext_x
            max_x = int_x
        else:
            min_x  = int_x
            max_x = ext_x

        random_x = random.randint(min_x,max_x)

        if ext_y<int_y:
            min_y  = ext_y
            max_y = int_y
        else:
            min_y  = int_y
            max_y = ext_y
        random_y = random.randint(min_y,max_y)

        #test if object is on track, if not move it closer to the most distant gate point
        if self.test_object_on_track((random_x,random_y),width,height):
            move_x = 0
            move_y = 0
            diff_max_x = max_x - random_x
            diff_min_x = min_x - random_x
            if abs(diff_max_x)>abs(diff_min_x):
                diff_x = diff_max_x
            else:
                diff_x = diff_min_x

            diff_max_y = max_y - random_y
            diff_min_y = min_y - random_y
            if abs(diff_max_y)>abs(diff_min_y):
                diff_y = diff_max_y
            else:
                diff_y = diff_min_y

            #move according to the most distant coordinate
            if abs(diff_x)>=(abs(diff_y)):
                if diff_x>0:
                    move_x=1
                elif diff_x<0:
                    move_x=-1
            else:
                if diff_y>0:
                    move_y=1
                elif diff_y<0:
                    move_y=-1

            while self.test_object_on_track((random_x,random_y),width,height):
                random_x+=move_x
                random_y+=move_y

            random_x+=move_x*3
            random_y+=move_y*3

        return ((random_x,random_y), is_ramp_or_bridge_gate)


    def hide_bonus(self):
        self.bonus_displayed = False
        self.bonus_rolling = False
        self.bonus_frame_index = -1
        self.bonus_timer = pygame.time.get_ticks() + bonus_display_interval

    def blit_bonus(self, race_started, overlay_blitted = False):
        #Initialize timer for bonus
        if self.bonus_timer is None:
            self.hide_bonus()
        if race_started:
            now = pygame.time.get_ticks()
            #if timer is reached: if Bonus displayed = False the we start rolling out the bonus, if False, we start rolling in.
            if now >=self.bonus_timer:
                if self.bonus_displayed:
                    if self.bonus_rolling:
                        #Animate the rolling out and display of the bonus
                        self.bonus_frame_index+=1
                        self.bonus_timer = now +100
                        if self.bonus_frame_index>3:
                            #Bonus fully displayed
                            self.bonus_frame_index=3
                            self.bonus_timer = now + bonus_display_duration
                            self.bonus_rolling = False
                    else:
                        #Now we hide the bonus
                        self.bonus_rolling = True
                        self.bonus_displayed = False
                        self.bonus_timer = now + 133
                else:
                    if self.bonus_rolling:
                        #Animate the rolling in and hiding of the bonus
                        self.bonus_frame_index-=1
                        self.bonus_timer = now + 133
                        if self.bonus_frame_index<0:
                            #Bonus Fully Hidden
                            self.bonus_frame_index=-1
                            self.bonus_timer = now + bonus_display_interval
                            self.bonus_rolling = False
                    else:
                        #Now we display the bonus
                        self.bonus_value = '{}'.format(random.randint(2,10) * 50)
                        result = self.get_random_position(16,30)
                        self.bonus_position = result[0]
                        self.on_bridge_or_ramp_bonus = result[1]
                        self.bonus_rolling = True
                        self.bonus_displayed = True
                        self.bonus_timer = now +100

        if self.bonus_frame_index>=0:
            if not overlay_blitted or self.on_bridge_or_ramp_bonus:
                slice_index = self.bonus_frame_index
                bonus_value_surf = tiny_font.render(self.bonus_value[0:slice_index], False, (255, 255, 255))
                game_display.blit(bonus_frames[self.bonus_frame_index],self.bonus_position)
                game_display.blit(bonus_value_surf,(self.bonus_position[0]+1,self.bonus_position[1]+3))
                if self.bonus_frame_index<=2:
                    game_display.blit(bonus_shade_frames[self.bonus_frame_index],self.bonus_position)


    def hide_wrench(self):
        self.wrench_displayed = False
        self.wrench_timer = pygame.time.get_ticks() + wrench_display_interval

    def blit_wrench(self, race_started, overlay_blitted = False):
        #Initialize timer for bonus
        if self.wrench_timer is None:
            self.hide_wrench()
        if race_started:
            now = pygame.time.get_ticks()
            #if timer is reached: if Wrench displayed = False the we display the wrench if not we hide it.
            if now >=self.wrench_timer:
                if self.wrench_displayed:
                    #Now we hide the wrench
                    self.hide_wrench()
                else:
                    #Now we display the wrench
                    result = self.get_random_position(12,26)
                    self.wrench_position = result[0]
                    self.on_bridge_or_ramp_wrench = result[1]
                    self.wrench_displayed = True
                    self.wrench_timer = now + wrench_display_duration
            if self.wrench_displayed:
                if not overlay_blitted or self.on_bridge_or_ramp_wrench:
                    game_display.blit(wrench_image,self.wrench_position)


    def test_pole_on_track(self, position):
        pole_mask = pygame.mask.from_surface(pygame.Surface((10,16)), 50)
        return  self.track_mask_mask.overlap(pole_mask, (round(position[0]),round(position[1])))


    def test_pole_on_bridge(self, position):
        object_mask = pygame.mask.from_surface(pygame.Surface((10,16)), 50)
        bridges_found = []
        for i in range(0, len(self.bridge_masks)):
            for j in range(0,len(self.bridge_masks[i])):
                bridge_mask = self.bridge_masks[i][j]
                if bridge_mask.overlap(object_mask, (round(position[0]),round(position[1]))):
                    bridges_found.append((i,j))
        return len(bridges_found)>0


    def test_pole_on_ramp(self, position):
        object_mask = pygame.mask.from_surface(pygame.Surface((10,16)), 50)
        ramps_found = []
        for i in range(0, len(self.ramp_masks)):
            for j in range(0,len(self.ramp_masks[i])):
                ramp_mask = self.ramp_masks[i][j]
                if ramp_mask.overlap(object_mask, (round(position[0]),round(position[1]))):
                    ramps_found.append((i,j))
        return len(ramps_found)>0


    def init_obstacles(self, race_counter):
        #Determine the number of obstacles
        nb_obstacles = 0
        min_obstacles = 0
        max_obstacles = 0
        nb_cones_max = 0

        #No obstacles the first 2 races
        if race_counter>2:
            #No more than 1 obstacles the 3rd to 5th race
            if race_counter <6:
                max_obstacles = 1
            #6th to 11th race: max obstacles depending on difficulty (wrenches)
            elif race_counter < 12:
                max_obstacles = self.wrenches
            #12th to 18th minimum 1 obstacle
            elif race_counter < 18:
                min_obstacles = 1
                max_obstacles = self.wrenches+1
            #we can now have 4 cones
            elif race_counter < 24:
                nb_cones_max = 4
                min_obstacles = 1
                max_obstacles = self.wrenches+1
            else:
            #Formula beyond 24 races
                min_obstacles = 2 + int(round((race_counter-24)/12))
                #3 spills + Tornado + Poles
                max_obstacles = 5
                nb_cones_max = 4 + 2 * int(round((race_counter-24)/6))

        nb_obstacles = random.randint(min_obstacles,max_obstacles)
        #if we have 5 obstacles, we display all of them
        #if less, we randomly pick the obstacles
        self.display_pole = False
        self.display_tornado = False
        self.display_oil_spill = False
        self.display_grease_spill = False
        self.display_water_spill = False

        if nb_obstacles < 5:
            obstacle_count = 0
            while obstacle_count < nb_obstacles:
                new_obstacle = random.randint(0,4)
                if new_obstacle == 0 and not self.display_pole:
                    obstacle_count+=1
                    self.display_pole = True
                elif new_obstacle == 1 and not self.display_tornado:
                    obstacle_count+=1
                    self.display_tornado = True
                elif new_obstacle == 2 and not self.display_oil_spill:
                    obstacle_count+=1
                    self.display_oil_spill = True
                elif new_obstacle == 3 and not self.display_grease_spill:
                    obstacle_count+=1
                    self.display_grease_spill = True
                elif new_obstacle == 4 and not self.display_water_spill:
                    obstacle_count+=1
                    self.display_water_spill = True

        self.display_cones = False
        self.cones_count = 0
        if nb_cones_max>0:
            if random.randint(0,1)>0:
                self.display_cones = True
            if self.display_cones:
                self.cones_count = random.randint(3,nb_cones_max)

        if DEBUG_OBSTACLES:
            self.display_pole = True
            self.display_tornado = True
            self.display_oil_spill = True
            self.display_grease_spill = True
            self.display_water_spill = True
            self.display_cones = True
            self.cones_count = 16

    def blit_obstacles(self, race_started, overlay_blitted = False):

        if self.display_pole:
            if self.poles_gate_index is None:
                self.poles_gate_index = self.get_random_poles_position()
                self.obstacle_gates.append(self.poles_gate_index)
                is_ramp_or_bridge_gate = False
                if not self.ramp_gates is None:
                    for i in self.ramp_gates:
                        for j in i:
                            for k in j:
                                if k==self.poles_gate_index:
                                    self.on_bridge_or_ramp_pole = True
                if not self.bridge_gates is None:
                    for i in self.bridge_gates:
                        for j in i:
                            for k in j:
                                if k==self.poles_gate_index:
                                    self.on_bridge_or_ramp_pole = True

                ext_x = self.external_gate_points[self.poles_gate_index][0] - 5
                ext_y = self.external_gate_points[self.poles_gate_index][1] - 8
                int_x = self.internal_gate_points[self.poles_gate_index][0] - 5
                int_y = self.internal_gate_points[self.poles_gate_index][1] - 8

                #test if pole is on track, if not move it closer to the opposite gate point
                if self.test_pole_on_track((int_x,int_y)):
                    move_x = 0
                    move_y = 0
                    diff_x = ext_x - int_x
                    diff_y = ext_y - int_y
                    #move according to the most distant coordinate
                    if abs(diff_x)>=(abs(diff_y)):
                        if diff_x>0:
                            move_x=1
                        elif diff_x<0:
                            move_x=-1
                    else:
                        if diff_y>0:
                            move_y=1
                        elif diff_y<0:
                            move_y=-1
                    while self.test_pole_on_track((int_x,int_y)):
                        int_x+=move_x
                        int_y+=move_y
                    int_x+=move_x*3
                    int_y+=move_y*3

                if self.test_pole_on_track((ext_x,ext_y)):
                    move_x = 0
                    move_y = 0
                    while self.test_pole_on_track((ext_x,ext_y)):
                        diff_x = int_x - ext_x
                        diff_y = int_y - ext_y
                        #move according to the most distant coordinate
                        if abs(diff_x)>=(abs(diff_y)):
                            if diff_x>0:
                                move_x=1
                            elif diff_x<0:
                                move_x=-1
                        else:
                            if diff_y>0:
                                move_y=1
                            elif diff_y<0:
                                move_y=-1
                        ext_x+=move_x
                        ext_y+=move_y
                    ext_x+=move_x*15
                    ext_y+=move_y*15

                self.external_pole_position = (ext_x,ext_y)
                self.internal_pole_position = (int_x,int_y)
                self.middle_pole_position = ((ext_x+int_x)/2,(ext_y+int_y)/2)

            if self.poles_timer is None:
                self.poles_timer =  pygame.time.get_ticks()
                self.poles_frame_indexes = [0,0,0]
                self.poles_moving_index = 0
                self.poles_popping_down = False
                self.poles_popping_up = True
            if race_started and not self.poles_gate_index is None:
                now =  pygame.time.get_ticks()
                if now >=self.poles_timer:
                    if self.poles_popping_up:
                        #Animate the popping up of the active pole
                        self.poles_frame_indexes[self.poles_moving_index]+=1
                        self.poles_timer = now +100
                        if self.poles_frame_indexes[self.poles_moving_index]>3:
                            #Pole fully popped up wait to pop down
                            self.poles_frame_indexes[self.poles_moving_index]=3
                            self.poles_timer = now + poles_stay_up_duration
                            self.poles_popping_up = False
                            self.poles_popping_down = True
                    elif self.poles_popping_down:
                        #Animate the popping down of the active pole
                        self.poles_frame_indexes[self.poles_moving_index]-=1
                        self.poles_timer = now +100
                        if self.poles_frame_indexes[self.poles_moving_index]<0:
                            #Pole fully popped up - move to the next pole and wait
                            self.poles_frame_indexes[self.poles_moving_index]=0
                            self.poles_timer = now + poles_pop_up_interval
                            self.poles_popping_up = True
                            self.poles_popping_down = False
                            self.poles_moving_index+=1
                            if self.poles_moving_index>2:
                                self.poles_moving_index = 0

                self.pole_mask = poles_frames_masks[0]
                if self.poles_frame_indexes[0]>0:
                    self.pole_mask = poles_frames_masks[self.poles_frame_indexes[0]]
                if self.poles_frame_indexes[1]:
                    self.pole_mask = poles_frames_masks[self.poles_frame_indexes[1]]
                if self.poles_frame_indexes[2]:
                    self.pole_mask = poles_frames_masks[self.poles_frame_indexes[2]]
                if not overlay_blitted or self.on_bridge_or_ramp_pole:
                    game_display.blit(poles_frames[self.poles_frame_indexes[0]],self.external_pole_position)
                    game_display.blit(poles_frames[self.poles_frame_indexes[1]],self.middle_pole_position)
                    game_display.blit(poles_frames[self.poles_frame_indexes[2]],self.internal_pole_position)

        #Display spills
        if self.display_oil_spill:
            if self.oil_spill_position is None:
                result = self.get_random_position(oil_spill_image.get_height(),oil_spill_image.get_width())
                self.oil_spill_position = result[0]
                self.on_bridge_or_ramp_oil_spill = result[1]
            if race_started:
                if not overlay_blitted or self.on_bridge_or_ramp_oil_spill:
                    game_display.blit(oil_spill_image,self.oil_spill_position)

        if self.display_water_spill:
            if self.water_spill_position is None:
                result = self.get_random_position(water_spill_image.get_height(),water_spill_image.get_width())
                self.water_spill_position = result[0]
                self.on_bridge_or_ramp_water_spill = result[1]
            if race_started:
                if not overlay_blitted or self.on_bridge_or_ramp_water_spill:
                    game_display.blit(water_spill_image,self.water_spill_position)
        if self.display_grease_spill:
            if self.grease_spill_position is None:
                result = self.get_random_position(grease_spill_image.get_height(),grease_spill_image.get_width())
                self.grease_spill_position = result[0]
                self.on_bridge_or_ramp_grease_spill = result[1]
            if race_started:
                if not overlay_blitted or self.on_bridge_or_ramp_grease_spill:
                    game_display.blit(grease_spill_image,self.grease_spill_position)

        #Display Traffic Cones
        if self.display_cones:
            if self.traffic_cones_positions is None:
                self.traffic_cones_positions = []
                self.on_bridge_or_ramp_grease_traffic_cones = []
                for i in range(1,self.cones_count):
                    result = self.get_random_position(traffic_cone.get_height(),traffic_cone_shade.get_width())
                    self.traffic_cones_positions.append(result[0])
                    self.on_bridge_or_ramp_grease_traffic_cones.append(result[1])

            if race_started:
                for i in range(0,len(self.traffic_cones_positions)):
                    if not overlay_blitted or self.on_bridge_or_ramp_grease_traffic_cones[i]:
                        game_display.blit(traffic_cone,self.traffic_cones_positions[i])
                        game_display.blit(traffic_cone_shade,self.traffic_cones_positions[i])