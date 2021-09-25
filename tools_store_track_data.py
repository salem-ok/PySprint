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
external_borders_map = [260,33,81,33,49,41,25,62,20,81,16,95,15,267,36,289,60,297,87,300,89,330,96,346,120,371,144,379,159,380,558,380,585,378,602,368,624,346,626,329,627,190,618,167,616,159,597,140,582,134,558,130,414,129,388,134,365,144,350,156,338,168,334,184,334,230,334,254,351,271,365,280,375,285,390,293,408,294,452,294,468,293,480,289,495,280,521,253,526,239,530,221,530,209,530,120,531,95,526,77,520,63,504,45,489,37,466,32]
internal_borders_map = [260,115,107,114,97,121,96,216,102,223,109,220,110,176,123,152,143,131,219,130,240,132,258,146,273,160,285,177,294,199,294,239,285,255,270,271,254,284,238,290,205,289,195,297,197,304,533,304,540,301,544,298,544,205,539,196,530,191,443,191,429,196,421,203,417,215,424,220,434,215,432,121,426,114]
secondary_internal_borders_map = [190,193,184,202,180,215,186,221,196,225,202,222,207,215,207,202,199,194]
#To many gates for Track 4
# external_gate_points_map = [259,34,161,31,81,33,38,47,19,75,18,99,17,182,16,247,32,285,64,301,90,302,200,294,242,291,282,262,296,244,295,205,282,173,253,144,219,130,151,131,124,150,111,177,109,220,88,327,97,350,122,374,165,381,295,382,392,382,506,382,560,382,590,376,620,355,627,335,626,278,626,198,621,160,599,138,560,131,539,131,479,131,414,131,372,143,345,165,333,189,334,228,340,258,371,285,393,294,462,293,495,278,521,253,531,226,529,119,527,79,502,45,465,34]
# internal_gate_points_map = [261,113,160,114,105,113,102,116,100,120,99,125,98,182,99,221,101,222,106,224,109,224,192,223,197,223,203,220,207,217,209,211,206,203,204,200,200,197,195,196,189,197,185,201,182,209,197,294,195,299,196,302,200,304,297,304,394,305,507,304,532,303,536,301,537,299,542,296,544,277,544,211,543,202,540,198,535,196,527,192,480,193,431,193,428,198,422,204,418,210,421,214,423,217,426,218,429,218,432,218,434,216,435,214,435,210,431,119,428,115,426,114,423,112]

external_gate_points_map = [260,33,167,31,82,33,33,54,18,97,19,182,17,249,87,299,200,291,277,266,289,184,226,130,151,130,109,174,106,222,95,338,122,373,254,378,413,380,545,382,598,371,628,339,627,203,616,160,559,129,414,127,363,145,334,228,403,287,498,263,527,211,530,97,508,49,464,33]
internal_gate_points_map = [261,117,166,117,110,117,102,123,99,130,97,181,100,221,108,224,196,227,205,222,207,208,198,196,186,201,183,209,183,218,197,302,202,305,256,306,410,307,527,305,538,303,544,296,544,215,543,202,537,195,433,196,423,205,420,214,425,221,434,219,438,212,433,120,428,117,420,116]

gates_to_remove = []
#Change filename
filename = pysprint_tracks.track4_json_filename

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


# to_modify = [(23,358,111,292,109)]
# modify_gates(pysprint_tracks.track2_json_filename, to_modify)


#to_modify = [(38,553,240,503,240),(39,569,212,513,212),(40,569,170,513,170)]
#modify_gates(pysprint_tracks.track5_json_filename, to_modify)

#to_remove = [26] #1,2,4,5,7,9,10,15,16,17,19,20,21,23,26,28,29,31,32,33,35,37,38,48,51,52,56,57,60,61,63,67,72,74,75,77,78,79,81]
#remove_gates(pysprint_tracks.track3_json_filename, to_remove)


# to_add = [(38,553,240,503,240)]
# insert_gates(pysprint_tracks.track5_json_filename,to_add)
