import pysprint_tracks
import json


#Template for laoding HTML Maps into the existing Track JSON file
external_borders_map = [257,396,558,397,587,393,604,385,624,363,627,335,619,305,598,282,562,272,383,263,381,136,379,124,385,119,585,133,605,127,627,102,628,78,617,46,597,27,578,18,561,18,288,16,265,21,253,25,235,45,226,65,224,78,226,175,241,192,430,194,547,193,554,202,551,207,515,207,194,209,195,79,191,57,182,43,164,26,146,18,131,17,80,17,55,20,47,25,25,47,19,63,16,76,16,360,40,386,77,396]
internal_borders_map = [254,336,542,336,546,329,539,322,328,308,320,306,314,297,310,287,306,120,317,93,323,83,348,74,547,81,555,75,550,67,364,64,339,68,292,68,290,145,563,144,598,154,616,172,625,192,624,231,602,256,585,261,153,258,128,238,128,91,122,83,91,83,82,89,81,207,208,336]
secondary_internal_borders_map = [83,336,149,336,82,271]
external_gate_points_map = [282,396,400,396,515,397,569,394,619,369,618,304,563,272,457,269,402,266,387,262,384,198,381,139,379,127,382,121,389,120,479,125,561,132,611,121,626,75,599,28,543,15,443,15,353,16,286,18,240,40,225,78,226,140,242,193,288,192,337,193,404,192,428,192,516,193,551,194,553,200,550,207,515,206,428,209,347,209,301,207,233,207,202,207,196,205,194,199,195,142,194,91,186,44,161,24,127,17,79,18,38,34,19,64,16,120,16,212,16,285,16,334,28,374,81,397,155,397,236,397]
internal_gate_points_map = [279,335,397,336,510,336,537,337,545,332,543,324,537,321,453,316,359,310,310,264,305,194,306,141,306,122,318,94,352,75,478,79,540,80,551,81,551,75,546,70,539,69,441,68,358,66,300,69,292,72,290,80,290,137,294,143,302,145,337,145,402,145,431,145,513,146,562,145,621,185,620,240,518,261,429,259,347,257,303,257,234,259,189,258,142,254,128,204,129,144,129,98,129,91,126,86,116,81,94,82,84,83,83,91,83,118,81,209,83,284,83,323,84,331,88,336,141,336,235,335]

gates_to_remove = []

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


#Set filename
filename = pysprint_tracks.track6_json_filename

#Create a new Track File (see above for setting initial data via HTML Map points vectors)
#create_track_file(filename,external_borders_map,internal_borders_map, secondary_internal_borders_map,external_gate_points_map,internal_gate_points_map,gates_to_remove)

#Modify Gates
#to_modify = [(6,561,273,548,304),(7,457,270,454,300),(8,402,265,305,333),(9,386,263,267,265),(10,383,201,303,201),(11,350,130,310,130),(12,350,117,292,117),(13,368,110,364,65),(14,430,122,430,65)]
#to_modify = [(16,556,121,540,80),(17,581,101,550,79),(18,600,75,550,75)]
#to_modify = [(22,317,17,317,54),(23,284,17,296,57),(24,240,40,270,60),(25,224,78,255,78)]
#to_modify = [(26,238,140,288,140),(27,258,178,291,145),(28,290,180,291,145)]
to_modify = [(13,67,346,56,369),(14,52,301,26,301),(15,61,267,45,246)]

modify_gates(filename, to_modify)

#Remove Gates
# to_remove = [29,38] #1,2,4,5,7,9,10,15,16,17,19,20,21,23,26,28,29,31,32,33,35,37,38,48,51,52,56,57,60,61,63,67,72,74,75,77,78,79,81]
# remove_gates(filename, to_remove)

#Insert Gates
# to_add = [(18,350,226,350,291)]
# insert_gates(filename,to_add)
