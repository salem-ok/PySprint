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

#Track 5 Setup
track5_json_filename = 'Assets/SuperSprintTrack5.json'

#Track 7 Setup
track7_json_filename = 'Assets/SuperSprintTrack7.json'

#Spills
oil_spill_image = None
water_spill_image = None
grease_spill_image = None

#Bonus Frames
bonus_frames = None
bonus_shade_frames = None
bonus_position = None
bonus_display_interval = 6000
bonus_display_duration = 10000
tiny_font = None

#Poles Frames
poles_frames = None
poles_gate = None
poles_pop_up_interval = 900
poles_stay_up_duration = 1300

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
        self.external_ai_gates_shortcuts = None
        self.internal_ai_gates_shortcuts = None
        #Timer for Bonus display animation
        self.bonus_timer = None
        self.bonus_displayed = False
        self.bonus_rolling = False
        self.bonus_frame_index = None
        self.bonus_value = None
        self.bonus_position = None
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
        self.external_pole_position = None
        self.internal_pole_position = None
        self.middle_pole_position = None


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
            #If we're not already in a shortcut then we only return a shortcut if the gate is open or opening
            if not self.road_gates_frames_index[i] == 4 or not self.road_gates_opening[i]:
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
        index = self.find_progress_gate((car.x_position, car.y_position),car.gate_step)
        score_increment = 0
        if not type(index) is tuple:
            score_increment = math.ceil((car.lap_count+1) * (index/len(self.internal_borders))) * 30
            if not car.is_drone:
                car.progress_gate = index
        #Increment score if there has been progress wince last score increment
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

    def get_random_poles_position(self):
        #Pick a gate at random where teh gate is more than 40 pixels long
        random_gate = random.randint(1, len(self.external_gate_points)-1)
        while calculate_distance(self.external_gate_points[random_gate],self.internal_gate_points[random_gate])<40:
            random_gate = random.randint(0, len(self.external_gate_points)-1)

        return random_gate

    def get_random_position(self, height, width):
        #Pick a gate at random and place the bonus randomly on the gate
        random_gate = random.randint(0, len(self.external_gate_points)-1)

        if self.external_gate_points[random_gate][0]<self.internal_gate_points[random_gate][0]:
            min_x  = self.external_gate_points[random_gate][0]
            max_x = self.internal_gate_points[random_gate][0]
        else:
            min_x  = self.internal_gate_points[random_gate][0]
            max_x = self.external_gate_points[random_gate][0]

        random_x = random.randint(min_x,max_x)
        if random_x + width > max_x:
            random_x = self.internal_gate_points[random_gate][0] - (width+3)
        elif random_x < min_x:
            random_x = min_x + 3

        if self.external_gate_points[random_gate][1]<self.internal_gate_points[random_gate][1]:
            min_y  = self.external_gate_points[random_gate][1]
            max_y = self.internal_gate_points[random_gate][1]
        else:
            min_y  = self.internal_gate_points[random_gate][1]
            max_y = self.external_gate_points[random_gate][1]

        random_y = random.randint(min_y,max_y)
        if random_y + height > max_y:
            random_y = self.internal_gate_points[random_gate][0] - (height+2)
        elif random_y < min_y:
            random_y = min_y + 2

        return (random_x,random_y)


    def hide_bonus(self):
        self.bonus_displayed = False
        self.bonus_rolling = False
        self.bonus_frame_index = -1
        self.bonus_timer = pygame.time.get_ticks() + bonus_display_interval

    def blit_bonus(self, race_started):
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
                        self.bonus_position = self.get_random_position(16,30)
                        self.bonus_rolling = True
                        self.bonus_displayed = True
                        self.bonus_timer = now +100

        if self.bonus_frame_index>=0:
            slice_index = self.bonus_frame_index
            bonus_value_surf = tiny_font.render(self.bonus_value[0:slice_index], False, (255, 255, 255))
            game_display.blit(bonus_frames[self.bonus_frame_index],self.bonus_position)
            game_display.blit(bonus_value_surf,(self.bonus_position[0]+1,self.bonus_position[1]+3))
            if self.bonus_frame_index<=2:
                game_display.blit(bonus_shade_frames[self.bonus_frame_index],self.bonus_position)

    def test_pole_on_track(self, position):
        test_track_mask = pygame.mask.from_surface(self.track_mask, 50)
        pole_mask = pygame.mask.from_surface(pygame.Surface((10,16)), 50)
        return  test_track_mask.overlap(pole_mask, (round(position[0]),round(position[1])))


    def blit_obstacles(self, race_started):
        #Display an oil spill
        if self.oil_spill_position is None:
            self.oil_spill_position = self.get_random_position(oil_spill_image.get_height(),oil_spill_image.get_width())
        if self.water_spill_position is None:
            self.water_spill_position = self.get_random_position(water_spill_image.get_height(),water_spill_image.get_width())
        if self.grease_spill_position is None:
            self.grease_spill_position = self.get_random_position(grease_spill_image.get_height(),grease_spill_image.get_width())

        if race_started:
            game_display.blit(oil_spill_image,self.oil_spill_position)
            game_display.blit(water_spill_image,self.water_spill_position)
            game_display.blit(grease_spill_image,self.grease_spill_position)

        #Display poles
        if self.poles_gate_index is None:
            self.poles_gate_index = self.get_random_poles_position()
            ext_x = self.external_gate_points[self.poles_gate_index][0] - 5
            ext_y = self.external_gate_points[self.poles_gate_index][1] - 8
            int_x = self.internal_gate_points[self.poles_gate_index][0] - 5
            int_y = self.internal_gate_points[self.poles_gate_index][1] - 8

            #test if pole is on track, if not move it closer to the opposite gate point
            if self.test_pole_on_track((int_x,int_y)):
                move_x = 0
                move_y = 0
                while self.test_pole_on_track((int_x,int_y)):
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
        if race_started:
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

            game_display.blit(poles_frames[self.poles_frame_indexes[0]],self.external_pole_position)
            game_display.blit(poles_frames[self.poles_frame_indexes[1]],self.middle_pole_position)
            game_display.blit(poles_frames[self.poles_frame_indexes[2]],self.internal_pole_position)
            self.track_mask = self.base_mask.copy()
            if self.poles_frame_indexes[0]>0:
                self.track_mask.blit(poles_frames[self.poles_frame_indexes[0]],self.external_pole_position)
            if self.poles_frame_indexes[1]:
                self.track_mask.blit(poles_frames[self.poles_frame_indexes[1]],self.middle_pole_position)
            if self.poles_frame_indexes[2]:
                self.track_mask.blit(poles_frames[self.poles_frame_indexes[2]],self.internal_pole_position)
