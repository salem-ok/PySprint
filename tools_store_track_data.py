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



#Template for laoding HTML Maps into the existing Track JSON file
external_borders_map = [236,19,81,19,64,20,53,23,41,28,24,44,19,56,15,80,14,166,15,187,33,209,54,216,74,218,84,210,109,209,134,207,157,206,179,202,180,299,173,304,85,305,84,297,87,291,171,291,293,291,342,290,460,290,548,291,550,296,551,304,465,305,455,300,455,205,458,203,475,203,500,206,524,207,550,210,566,217,582,214,601,210,623,186,623,81,621,66,614,48,596,30,582,23,562,17,434,15,409,14,394,11,378,11,364,17,356,25,278,26,257,18]
internal_borders_map = [208,81,108,81,96,89,96,135,106,144,152,144,175,143,188,139,206,138,229,137,252,138,271,142,280,153,282,322,273,335,265,347,244,360,224,368,215,369,186,371,169,379,81,380,62,377,47,373,39,371,18,348,18,289,19,273,27,254,45,234,59,229,82,224,176,225,293,224,352,225,484,224,561,225,578,228,596,233,617,254,625,286,627,325,627,342,605,367,582,376,563,380,494,380,465,372,428,370,396,360,380,350,364,332,359,313,358,155,367,142,384,137,445,139,472,143,539,145,544,138,544,89,535,82,427,80,421,84,410,99,393,114,380,121,368,129,353,137,340,144,326,148,307,147,284,139,246,114,225,94,214,83]
secondary_internal_borders_map = [304,55,283,31,308,64,320,77,334,71,347,64,347,55]
external_gate_points_map = [135,16,84,17,35,39,18,80,18,153,30,200,96,215,168,203,176,203,180,205,182,296,180,299,176,304,90,304,89,296,91,290,177,290,296,290,464,290,545,289,551,293,551,303,470,305,464,302,459,299,459,210,466,203,546,208,607,206,631,174,627,118,625,81,610,40,564,19,497,16,440,17,370,16,346,62,322,81,301,58,272,25,237,16]
internal_gate_points_map = [132,82,106,83,100,87,97,93,98,134,101,139,107,141,170,142,272,144,283,205,282,292,247,358,173,374,48,374,13,307,76,226,176,225,299,224,464,226,597,235,621,329,562,378,466,376,386,356,358,289,355,213,372,141,529,143,541,141,542,133,544,121,543,92,542,84,536,82,499,82,441,80,424,82,394,113,318,150,250,118,226,89,209,82]

gates_to_remove = []
#Change filename
filename = pysprint_tracks.track6_json_filename

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


create_track_file(filename,external_borders_map,internal_borders_map, secondary_internal_borders_map,external_gate_points_map,internal_gate_points_map,gates_to_remove)

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


# to_modify = [(16,195,378,203,306),(20,584,355,538,304),(21,625,297,544,297)]
# modify_gates(pysprint_tracks.track4_json_filename, to_modify)


#to_modify = [(38,553,240,503,240),(39,569,212,513,212),(40,569,170,513,170)]
#modify_gates(pysprint_tracks.track5_json_filename, to_modify)

#to_remove = [26] #1,2,4,5,7,9,10,15,16,17,19,20,21,23,26,28,29,31,32,33,35,37,38,48,51,52,56,57,60,61,63,67,72,74,75,77,78,79,81]
#remove_gates(pysprint_tracks.track3_json_filename, to_remove)


# to_add = [(38,553,240,503,240)]
# insert_gates(pysprint_tracks.track5_json_filename,to_add)
