#pysprint_tracks.py
import math
import json


#Track 1 Setup
track1_json_filename = 'Assets/SuperSprintTrack1.json'

#Track 7 Setup
track7_json_filename = 'Assets/SuperSprintTrack7.json'


def calculate_distance(point1,point2):
    return math.sqrt( ((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))


class Track:
    background_filename = None
    track_mask_filename = None
    overlay_filename =  None
    background = None
    track_mask = None
    track_overlay = None
    first_car_start_position = None
    flag_anchor = None
    track_number = None

    start_sprite_angle = None
    score_time_reference = None
    complete_lap_score = None
    external_borders = None

    internal_borders = None

    finish_line_rect = None

    finish_line = None
    finish_line_direction = None


    #External gate points

    external_gate_points = []
    internal_gate_points = []

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
        self.finish_line_rect = track_json["finish_line_rect"]
        self.finish_line_direction = track_json["finish_line_direction"]
        self.external_gate_points = track_json["external_gate_points"]
        self.internal_gate_points = track_json["internal_gate_points"]




    def find_gate_point(self, position, gate_points):
        shortest_distance = -1
        shortest_index = -1
        for i in range (0, len(gate_points)):
            distance =  calculate_distance(gate_points[i], position)
            if (shortest_distance < 0) or (distance < shortest_distance):
                shortest_distance = distance
                shortest_index = i
        return shortest_index

    def find_progress_gate(self, position):
        #Check closest Internal and external gate point,
        int_index = self.find_gate_point(position, self.internal_gate_points)
        ext_index = self.find_gate_point(position, self.external_gate_points)

        #If External & Internal Points belobg to wodely distant gates, return teh lowest one
        if abs(ext_index-int_index)>= 3:
            if ext_index > int_index:
                return int_index
            else:
                return ext_index
        else:
            #Return the highest index to ignore postion relative to borders
            if ext_index >= int_index:
                return ext_index
            else:
                return int_index

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
        index = self.find_progress_gate((car.x_position, car.y_position))
        score_increment = math.ceil((car.lap_count+1) * (index/len(self.internal_borders))) * 10
        #Increment score if there has been progress wince last score increment
        if score_increment > car.previous_score_increment:
            car.score += score_increment
            car.previous_score_increment = score_increment