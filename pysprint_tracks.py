#pysprint_tracks.py
import math
import json
import random
import pygame
from pygame import Surface, gfxdraw


#Track 1 Setup
track1_json_filename = 'Assets/SuperSprintTrack1.json'

#Track 3 Setup
track3_json_filename = 'Assets/SuperSprintTrack3.json'

#Track 7 Setup
track7_json_filename = 'Assets/SuperSprintTrack7.json'

#Max and min random time for a gate to be closed or open
max_random_time = 2500
min_random_time = 1500

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
        self.background_filename = None
        self.track_mask_filename = None
        self.overlay_filename =  None
        self.background = None
        self.base_mask = None
        self.track_mask = None
        self.track_overlay = None
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
        #Track Opening Gates
        self.road_gates_anchors = None
        self.road_gates_frames_index = []
        self.road_gates_timers = []
        self.road_gates_opening = []
        #When timer = next event time open or close the gate depending on status
        self.road_gates_next_event_time = []
        self.external_ai_gates_shortcuts = None
        self.internal_ai_gates_shortcuts = None


    def load_track_definition(self, filename):
        with open(filename) as track_file:
            track_json = json.load(track_file)

        self.track_number = track_json["track_number"]
        self.background_filename = track_json["background_filename"]
        self.track_mask_filename = track_json["mask_filename"]
        self.overlay_filename =  track_json["overlay_filename"]

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
        if "mandatory_gates" in track_json:
            self.mandatory_gates = track_json["mandatory_gates"]
        if "road_gates_anchors" in track_json:
            self.road_gates_anchors = track_json["road_gates_anchors"]
        if "external_ai_gates_shortcuts" in track_json:
            self.external_ai_gates_shortcuts = track_json["external_ai_gates_shortcuts"]
        if "internal_ai_gates_shortcuts" in track_json:
            self.internal_ai_gates_shortcuts = track_json["internal_ai_gates_shortcuts"]



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
            #If we're not already in a shortcut then we only return a shortcut if the gate is open
            if not self.road_gates_frames_index[i] == 4:
                return -1
            #And if the shortcut gate detected is the first one of teh shortcut (i.e. index = 1)
            if shortest_index[1]>1:
                return -1
        return shortest_index


    def find_progress_gate(self, position, actual_gate_step = None, currentgate = None):
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
        else:
            #Return the highest index to ignore postion relative to borders
            if ext_index >= int_index:
                closest_gate_index = ext_index
            else:
                closest_gate_index = int_index

        closest_shortcut_index = None
        if not actual_gate_step is None:
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
        index = self.find_progress_gate((car.x_position, car.y_position),car.gate_step)
        score_increment = 0
        if not type(index) is tuple:
            score_increment = math.ceil((car.lap_count+1) * (index/len(self.internal_borders))) * 10
        #Increment score if there has been progress wince last score increment
        if score_increment > car.previous_score_increment:
            car.score += score_increment
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


    def blit_overlay(self):
        surf = self.track_overlay.copy()
        if not self.road_gates_anchors is None:
            for i in range(0, len(self.road_gates_anchors)):
                surf.blit(road_gate_shade_frames[self.road_gates_frames_index[i]],(self.road_gates_anchors[i][0],self.road_gates_anchors[i][1]))
        game_display.blit(surf,(0,0))

    def update_track_mask(self):
        self.track_mask = self.base_mask.copy()
        if not self.road_gates_anchors is None:
            for i in range(0, len(self.road_gates_anchors)):
                self.track_mask.blit(road_gate_mask_frames[self.road_gates_frames_index[i]],(self.road_gates_anchors[i][0],self.road_gates_anchors[i][1]))
