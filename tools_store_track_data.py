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
external_borders_map = [459,380,558,380,588,375,605,367,626,343,626,325,627,207,622,183,614,171,598,155,578,147,561,144,498,145,381,115,310,113,197,143,139,143,127,147,116,161,112,288,127,302,381,305,401,295,402,244,402,107,401,79,398,58,394,45,374,28,361,20,337,17,83,15,57,21,43,27,28,44,21,56,18,78,18,329,18,349,38,369,54,375,80,381]
internal_borders_map = [461,318,503,319,509,313,513,231,506,223,383,192,307,194,206,218,199,223,198,239,288,239,289,111,289,92,279,81,105,80,97,87,98,313,104,319]
secondary_internal_borders_map = []
external_gate_points_map = [462,380,558,380,605,367,627,329,626,206,616,176,576,145,558,145,496,144,378,116,311,112,199,143,136,145,113,162,112,219,112,287,136,307,192,307,264,304,334,305,385,305,401,278,402,233,399,113,401,76,381,33,341,16,270,16,85,16,35,34,19,78,18,148,16,222,17,328,30,362,80,380,190,380,261,380,335,380,389,381]
internal_gate_points_map = [465,319,503,318,514,310,515,299,515,254,515,237,514,227,508,224,501,223,382,195,312,194,208,218,206,220,203,224,203,229,204,235,207,236,211,237,266,237,288,237,290,236,291,233,293,230,291,109,291,92,289,86,283,82,273,82,109,80,103,85,102,91,101,143,101,219,100,307,101,318,110,320,193,320,268,320,340,319,391,319]
gates_to_remove = []
filename = pysprint_tracks.track2_json_filename

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


#create_track_file(filename,external_borders_map,internal_borders_map, secondary_internal_borders_map,external_gate_points_map,internal_gate_points_map,gates_to_remove)

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


to_modify = [(23,358,111,292,109)]
modify_gates(pysprint_tracks.track2_json_filename, to_modify)


#to_modify = [(38,553,240,503,240),(39,569,212,513,212),(40,569,170,513,170)]
#modify_gates(pysprint_tracks.track5_json_filename, to_modify)

#to_remove = [26] #1,2,4,5,7,9,10,15,16,17,19,20,21,23,26,28,29,31,32,33,35,37,38,48,51,52,56,57,60,61,63,67,72,74,75,77,78,79,81]
#remove_gates(pysprint_tracks.track3_json_filename, to_remove)


# to_add = [(38,553,240,503,240)]
# insert_gates(pysprint_tracks.track5_json_filename,to_add)
