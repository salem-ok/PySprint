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


with open(pysprint_tracks.track7_json_filename) as track7_file:
    track_json = json.load(track7_file)


track_json["track_number"] = track7.track_number
track_json["background_filename"] = track7.background_filename
track_json["mask_filename"] = track7.track_mask_filename
track_json["overlay_filename"] = track7.overlay_filename
track_json["start_sprite_angle"] = track7.start_sprite_angle
track_json["score_time_reference"] = track7.score_time_reference
track_json["complete_lap_score"] = track7.complete_lap_score
track_json["finish_line_direction"] = track7.finish_line_direction


track_json["first_car_start_position"] = [track7.first_car_start_position[0], track7.first_car_start_position[1]]
track_json["flag_anchor"] = [track7.flag_anchor[0], track7.flag_anchor[1]]

track_json["finish_line_rect"] = [track7.finish_line_rect[0], track7.finish_line_rect[1], track7.finish_line_rect[2], track7.finish_line_rect[3]]

track_json["external_borders"] = []
for border in track7.external_borders:
    track_json["external_borders"].append([border[0],border[1], border[2]])

track_json["internal_borders"] = []
for border in track7.internal_borders:
    track_json["internal_borders"].append([border[0],border[1], border[2]])

track_json["external_gate_points"] = []
for gate_point in track7.external_gate_points:
    track_json["external_gate_points"].append([gate_point[0],gate_point[1]])

track_json["internal_gate_points"] = []
for gate_point in track7.internal_gate_points:
    track_json["internal_gate_points"].append([gate_point[0],gate_point[1]])


with open(pysprint_tracks.track7_json_filename,"w") as track7_file:
    json.dump(track_json, track7_file)


