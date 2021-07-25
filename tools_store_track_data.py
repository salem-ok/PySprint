import pysprint_tracks
import json


# track1 = pysprint_tracks.Track()
# track1.track_number = 1
# track1.background_filename = pysprint_tracks.track1_background_filename
# track1.track_mask_filename = pysprint_tracks.track1_mask_filename
# track1.overlay_filename =  pysprint_tracks.track1_overlay_filename
# track1.first_car_start_position = pysprint_tracks.track1_first_car_start_position
# track1.flag_anchor = pysprint_tracks.track1_flag_anchor
# track1.start_sprite_angle = pysprint_tracks.track1_start_sprite_angle
# track1.score_time_reference = pysprint_tracks.track1_score_time_reference
# track1.complete_lap_score = pysprint_tracks.track1_complete_lap_score
# track1.external_borders = pysprint_tracks.track1_external_borders
# track1.internal_borders = pysprint_tracks.track1_internal_borders
# track1.finish_line_rect = pysprint_tracks.track1_finish_line_rect
# track1.finish_line_direction = pysprint_tracks.track1_finish_line_direction
# track1.external_gate_points = pysprint_tracks.track1_external_gate_points
# track1.internal_gate_points = pysprint_tracks.track1_internal_gate_points

# with open(pysprint_tracks.track1_json_filename,"w") as track1_file:
#     json.dump(track1_json, track1_file)


# track7 = pysprint_tracks.Track()
# track7.track_number = 7
# track7.background_filename = pysprint_tracks.track7_background_filename
# track7.track_mask_filename = pysprint_tracks.track7_mask_filename
# track7.overlay_filename =  pysprint_tracks.track7_overlay_filename
# track7.first_car_start_position = pysprint_tracks.track7_first_car_start_position
# track7.flag_anchor = pysprint_tracks.track7_flag_anchor
# track7.start_sprite_angle = pysprint_tracks.track7_start_sprite_angle
# track7.score_time_reference = pysprint_tracks.track7_score_time_reference
# track7.complete_lap_score = pysprint_tracks.track7_complete_lap_score
# track7.external_borders = pysprint_tracks.track7_external_borders
# track7.internal_borders = pysprint_tracks.track7_internal_borders
# track7.finish_line_rect = pysprint_tracks.track7_finish_line_rect
# track7.finish_line_direction = pysprint_tracks.track7_finish_line_direction


# #for i in range(0,len(pysprint_tracks.track7_external_gate_map),2):
# i = 0
# while i < len(pysprint_tracks.track7_external_gate_map):
#     if (i>= 124) and i<= 164 or (i>= 80 and i<= 104):
#         i+=2
#     track7.external_gate_points.append((pysprint_tracks.track7_external_gate_map[i],pysprint_tracks.track7_external_gate_map[i+1]))
#     track7.internal_gate_points.append((pysprint_tracks.track7_internal_gate_map[i],pysprint_tracks.track7_internal_gate_map[i+1]))
#     i+=2


# with open(pysprint_tracks.track7_json_filename) as track7_file:
#     track_json = json.load(track7_file)


# track_json["track_number"] = track7.track_number
# track_json["background_filename"] = track7.background_filename
# track_json["mask_filename"] = track7.track_mask_filename
# track_json["overlay_filename"] = track7.overlay_filename
# track_json["start_sprite_angle"] = track7.start_sprite_angle
# track_json["score_time_reference"] = track7.score_time_reference
# track_json["complete_lap_score"] = track7.complete_lap_score
# track_json["finish_line_direction"] = track7.finish_line_direction


# track_json["first_car_start_position"] = [track7.first_car_start_position[0], track7.first_car_start_position[1]]
# track_json["flag_anchor"] = [track7.flag_anchor[0], track7.flag_anchor[1]]

# track_json["finish_line_rect"] = [track7.finish_line_rect[0], track7.finish_line_rect[1], track7.finish_line_rect[2], track7.finish_line_rect[3]]

# track_json["external_borders"] = []
# for border in track7.external_borders:
#     track_json["external_borders"].append([border[0],border[1], border[2]])

# track_json["internal_borders"] = []
# for border in track7.internal_borders:
#     track_json["internal_borders"].append([border[0],border[1], border[2]])

# track_json["external_gate_points"] = []
# for gate_point in track7.external_gate_points:
#     track_json["external_gate_points"].append([gate_point[0],gate_point[1]])

# track_json["internal_gate_points"] = []
# for gate_point in track7.internal_gate_points:
#     track_json["internal_gate_points"].append([gate_point[0],gate_point[1]])


# with open(pysprint_tracks.track7_json_filename,"w") as track7_file:
#     json.dump(track_json, track7_file)



#Template for laoding HTML Maps into the Track JSON format
external_borders_map = [558,32,80,32,50,38,28,59,18,80,16,93,15,153,14,180,33,201,44,208,358,210,362,221,353,224,145,221,71,216,41,225,21,242,14,255,9,272,11,340,29,358,49,368,106,376,130,379,562,381,588,375,603,366,618,355,627,343,635,326,635,308,623,302,607,288,588,272,588,259,603,250,618,242,634,222,625,216,622,205,593,181,585,172,587,164,592,159,601,155,622,143,630,131,631,123,625,121,627,96,621,74,616,60,598,42,577,33]
internal_borders_map = [505,113,138,113,133,121,134,128,376,127,397,132,409,134,434,159,448,175,446,184,453,187,455,204,455,246,447,261,428,277,408,289,125,289,115,295,115,304,508,304,509,295,506,285,486,280,466,265,470,245,485,230,495,222,506,222,510,217,510,207,496,202,469,188,470,169,472,159,486,150,501,144,511,136,510,120]
secondary_internal_borders_map = []
external_gate_points_map = [321,32,152,32,80,32,30,58,14,92,14,156,49,206,135,209,174,208,268,207,320,207,358,208,363,214,364,221,358,224,322,223,238,222,172,222,146,220,72,218,19,240,9,288,11,339,60,371,121,378,172,378,246,379,350,380,429,380,536,381,597,372,605,343,610,309,589,266,588,218,588,169,586,114,586,76,561,44,519,31]
internal_gate_points_map = [324,113,152,113,139,116,135,119,135,124,136,125,138,126,146,127,173,128,275,128,322,127,393,130,444,171,449,258,407,289,322,288,239,286,171,289,145,288,124,288,120,291,117,295,119,300,123,302,131,303,172,303,253,303,351,305,431,306,502,306,511,306,513,304,514,302,514,267,513,213,513,165,514,121,515,119,515,116,512,114]
gates_to_remove = []
filename = pysprint_tracks.track5_json_filename

def create_track_file(filename,external_borders_map,internal_borders_map, secondary_internal_borders_map,external_gate_points_map,internal_gate_points_map,gates_to_remove):
    with open(filename) as track_file:
        track_json = json.load(track_file)



    track_json["external_borders"] = []

    i = 0
    while i < len(external_borders_map):
        track_json["external_borders"].append([external_borders_map[i],external_borders_map[i+1], 0])
        i+=2

    track_json["internal_borders"] = []
    i = 0
    while i < len(internal_borders_map):
        track_json["internal_borders"].append([internal_borders_map[i],internal_borders_map[i+1], 1])
        i+=2

    track_json["secondary_internal_borders"] = []
    i = 0
    while i < len(secondary_internal_borders_map):
        track_json["secondary_internal_borders"].append([secondary_internal_borders_map[i],secondary_internal_borders_map[i+1], 1])
        i+=2

    track_json["external_gate_points"] = []
    i = 0
    j = 0

    while i < len(external_gate_points_map):
        track_json["external_gate_points"].append([external_gate_points_map[i],external_gate_points_map[i+1]])
        i+=2
        j+=1

    track_json["internal_gate_points"] = []
    i = 0
    j = 0
    while i < len(internal_gate_points_map):
        track_json["internal_gate_points"].append([internal_gate_points_map[i],internal_gate_points_map[i+1]])
        i+=2
        j+=1

    with open(filename,"w") as track_file:
        json.dump(track_json, track_file)


# create_track_file(filename,external_borders_map,internal_borders_map, secondary_internal_borders_map,external_gate_points_map,internal_gate_points_map,gates_to_remove)

# #Tweak Track 1 file

# with open(pysprint_tracks.track1_json_filename) as track_file:
#     track_json = json.load(track_file)



# i = 0
# to_remove = [1,3,5,7,10,11,13,15,17,19,21,23,27,29,31,33,35,37,39,41,43,45,47,49]
# removed = 0
# for i in to_remove:
#     track_json["external_gate_points"].pop(i-removed)
#     track_json["internal_gate_points"].pop(i-removed)
#     removed+=1


# with open(pysprint_tracks.track1_json_filename,"w") as track_file:
#     json.dump(track_json, track_file)

#Remove gates from a file

def remove_gates(filename, to_remove):

    with open(filename) as track_file:
        track_json = json.load(track_file)
    i = 0

    removed = 0
    for i in to_remove:
        track_json["external_gate_points"].pop(i-removed)
        track_json["internal_gate_points"].pop(i-removed)
        removed+=1


    with open(filename,"w") as track_file:
        json.dump(track_json, track_file)





#Modify Gates in a file (gate_number,external_x,external_y,internal_x,internal_y)

def modify_gates(filename, to_modify):

    with open(filename) as track_file:
        track_json = json.load(track_file)

    i = 0

    for gate in to_modify:
        track_json["external_gate_points"][gate[0]] = (gate[1],gate[2])
        track_json["internal_gate_points"][gate[0]] = (gate[3],gate[4])



    with open(filename,"w") as track_file:
        json.dump(track_json, track_file)



#Insert Gates in a file (gate_number,external_x,external_y,internal_x,internal_y)

def insert_gates(filename, to_add):

    with open(filename) as track_file:
        track_json = json.load(track_file)

    i = 0

    for gate in to_add:
        track_json["external_gate_points"].insert(gate[0], (gate[1],gate[2]))
        track_json["internal_gate_points"].insert(gate[0], (gate[3],gate[4]))



    with open(filename,"w") as track_file:
        json.dump(track_json, track_file)

to_modify = [(38,553,240,503,240),(39,569,212,513,212),(40,569,170,513,170)]
modify_gates(pysprint_tracks.track5_json_filename, to_modify)

#to_remove = [26] #1,2,4,5,7,9,10,15,16,17,19,20,21,23,26,28,29,31,32,33,35,37,38,48,51,52,56,57,60,61,63,67,72,74,75,77,78,79,81]
#remove_gates(pysprint_tracks.track3_json_filename, to_remove)


# to_add = [(38,553,240,503,240)]
# insert_gates(pysprint_tracks.track5_json_filename,to_add)
