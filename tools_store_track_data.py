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
external_borders_map = [257,396,558,397,587,393,604,385,624,363,627,335,619,305,598,282,562,272,383,263,381,136,379,124,385,119,585,133,605,127,627,102,628,78,617,46,597,27,578,18,561,18,288,16,265,21,253,25,235,45,226,65,224,78,226,175,241,192,430,194,547,193,554,202,551,207,515,207,194,209,195,79,191,57,182,43,164,26,146,18,131,17,80,17,55,20,47,25,25,47,19,63,16,76,16,360,40,386,77,396]
internal_borders_map = [254,336,542,336,546,329,539,322,328,308,320,306,314,297,310,287,306,120,317,93,323,83,348,74,547,81,555,75,550,67,364,64,339,68,292,68,290,145,563,144,598,154,616,172,625,192,624,231,602,256,585,261,153,258,128,238,128,91,122,83,91,83,82,89,81,207,208,336]
secondary_internal_borders_map = [83,336,149,336,82,271]
external_gate_points_map = [282,396,400,396,515,397,569,394,619,369,618,304,563,272,457,269,402,266,387,262,384,198,381,139,379,127,382,121,389,120,479,125,561,132,611,121,626,75,599,28,543,15,443,15,353,16,286,18,240,40,225,78,226,140,242,193,288,192,337,193,404,192,428,192,516,193,551,194,553,200,550,207,515,206,428,209,347,209,301,207,233,207,202,207,196,205,194,199,195,142,194,91,186,44,161,24,127,17,79,18,38,34,19,64,16,120,16,212,16,285,16,334,28,374,81,397,155,397,236,397]
internal_gate_points_map = [279,335,397,336,510,336,537,337,545,332,543,324,537,321,453,316,359,310,310,264,305,194,306,141,306,122,318,94,352,75,478,79,540,80,551,81,551,75,546,70,539,69,441,68,358,66,300,69,292,72,290,80,290,137,294,143,302,145,337,145,402,145,431,145,513,146,562,145,621,185,620,240,518,261,429,259,347,257,303,257,234,259,189,258,142,254,128,204,129,144,129,98,129,91,126,86,116,81,94,82,84,83,83,91,83,118,81,209,83,284,83,323,84,331,88,336,141,336,235,335]

gates_to_remove = []
#Change filename
filename = pysprint_tracks.track8_json_filename

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


# to_modify = [(16,195,378,203,306),(20,584,355,538,304),(21,625,297,544,297)]
# modify_gates(pysprint_tracks.track4_json_filename, to_modify)


# to_modify = [(5,55,181,98,143),(6,101,190,107,144),(12,177,304,177,355),(13,71,335,56,365),(14,63,301,23,301),(15,70,279,44,244),(16,177,290,177,225),(17,297,268,297,225),(18,351,268,351,225),(19,465,268,465,225),(20,563,274,593,244),(21,563,298,601,298),(22,561,319,588,336),(28,537,171,530,144),(29,565,165,541,141),(30,577,149,544,133),(31,597,120,545,120)]
# modify_gates(pysprint_tracks.track6_json_filename, to_modify)

# to_remove = [29,38] #1,2,4,5,7,9,10,15,16,17,19,20,21,23,26,28,29,31,32,33,35,37,38,48,51,52,56,57,60,61,63,67,72,74,75,77,78,79,81]
# remove_gates(pysprint_tracks.track8_json_filename, to_remove)


# to_add = [(18,350,226,350,291)]
# insert_gates(pysprint_tracks.track6_json_filename,to_add)
