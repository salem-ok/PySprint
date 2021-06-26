#pysprint_tracks.py
import math


#Track 1 Setup
track1_background_filename = 'Assets/SuperSprintTrack1.png'
track1_mask_filename = 'Assets/SuperSprintTrack1Mask.png'
track1_overlay_filename =  'Assets/SuperSprintTrack1OverLay.png'

track1_external_borders = [
    (264,367,0),
    (265,354,0),
    (264,316,0),
    (262,316,0),
    (262,301,0),
    (259,301,0),
    (260,288,0),
    (259,287,0),
    (258,275,0),
    (256,274,0),
    (256,261,0),
    (254,258,0),
    (254,238,0),
    (259,235,0),
    (274,235,0),
    (299,261,0),
    (306,260,0),
    (338,295,0),
    (365,318,0),
    (384,335,0),
    (412,362,0),
    (425,372,0),
    (429,374,0),
    (432,375,0),
    (435,377,0),
    (438,377,0),
    (445,380,0),
    (494,381,0),
    (495,379,0),
    (544,380,0),
    (549,378,0),
    (553,378,0),
    (556,377,0),
    (560,375,0),
    (564,374,0),
    (575,373,0),
    (581,371,0),
    (586,369,0),
    (598,356,0),
    (602,352,0),
    (605,349,0),
    (607,345,0),
    (606,331,0),
    (610,329,0),
    (610,110,0),
    (608,106,0),
    (607,97,0),
    (607,96,0),
    (605,89,0),
    (603,88,0),
    (602,83,0),
    (600,79,0),
    (599,75,0),
    (583,59,0),
    (579,58,0),
    (577,58,0),
    (577,56,0),
    (574,56,0),
    (574,54,0),
    (569,54,0),
    (570,52,0),
    (562,52,0),
    (561,50,0),
    (545,51,0),
    (544,48,0),
    (140,48,0),
    (140,47,0),
    (96,47,0),
    (96,51,0),
    (94,49,0),
    (80,50,0),
    (70,52,0),
    (52,67,0),
    (41,80,0),
    (36,89,0),
    (36,96,0),
    (33,97,0),
    (33,111,0),
    (32,112,0),
    (31,311,0),
    (32,330,0),
    (33,346,0),
    (57,368,0),
    (64,372,0),
    (75,375,0),
    (83,376,0),
    (95,377,0),
    (97,380,0),
    (236,380,0),
    (245,379,0),
    (249,376,0),
    (253,376,0),
    (255,375,0),
    (255,374,0)
]

track1_internal_borders = [
    (133, 134,1),
    (129, 143,1),
    (125, 153,1),
    (124, 295,1),
    (132, 305,1),
    (143, 307,1),
    (157, 298,1),
    (161, 163,1),
    (178, 148,1),
    (292, 148,1),
    (314, 152,1),
    (333, 161,1),
    (489, 306,1),
    (499, 307,1),
    (504, 302,1),
    (512, 299,1),
    (512, 141,1),
    (503, 131,1),
    (137, 130,1)
]

track1_external_gate_points = [
    (331,50),
    (281,49),
    (221,50),
    (174,50),
    (122,49),
    (70,55),
    (40,84),
    (34,114),
    (34,153),
    (32,200),
    (33,229),
    (33,271),
    (33,297),
    (33,330),
    (51,357),
    (84,373),
    (120,375),
    (165,376),
    (210,376),
    (236,375),
    (265,358),
    (268,330),
    (258,282),
    (256,249),
    (255,229),
    (275,226),
    (289,240),
    (302,252),
    (327,274),
    (355,304),
    (385,328),
    (407,350),
    (430,369),
    (449,375),
    (485,375),
    (525,376),
    (561,374),
    (589,356),
    (609,334),
    (608,302),
    (610,255),
    (609,213),
    (608,167),
    (607,128),
    (606,95),
    (591,68),
    (570,55),
    (544,49),
    (485,48),
    (434,48),
    (380,50)
]
track1_internal_gate_points = [
    (330,130),
    (281,129),
    (217,131),
    (170,130),
    (136,129),
    (131,133),
    (129,138),
    (128,142),
    (126,151),
    (126,198),
    (125,230),
    (125,270),
    (124,292),
    (126,295),
    (129,299),
    (133,301),
    (141,303),
    (149,302),
    (153,300),
    (156,296),
    (158,292),
    (158,287),
    (158,281),
    (159,253),
    (158,228),
    (160,167),
    (250,146),
    (298,147),
    (331,159),
    (381,201),
    (410,234),
    (444,261),
    (463,282),
    (480,296),
    (495,306),
    (501,303),
    (506,298),
    (508,296),
    (510,293),
    (512,289),
    (510,253),
    (510,215),
    (511,165),
    (509,137),
    (510,133),
    (509,131),
    (507,129),
    (504,128),
    (486,128),
    (430,128),
    (380,129)
]


track1_finish_line_rect = (346, 48,4,82)
track1_first_car_start_position = (325, 55)
track1_flag_anchor = (320, 28)
track1_start_sprite_angle = 12
track1_score_time_reference = 6.6
track1_complete_lap_score = 55
track1_finish_line_direction = -1


#Track 7 Setup
track7_background_filename = 'Assets/SuperSprintTrack7.png'
track7_mask_filename = 'Assets/SuperSprintTrack7Mask.png'
track7_overlay_filename =  'Assets/SuperSprintTrack7Overlay.png'

track7_external_borders = [
    (147,370,0),
    (504,371,0),
    (556,374,0),
    (589,374,0),
    (616,355,0),
    (625,341,0),
    (626,335,0),
    (628,332,0),
    (629,223,0),
    (623,197,0),
    (618,189,0),
    (602,172,0),
    (586,164,0),
    (566,162,1),
    (504,161,1),
    (487,173,1),
    (474,182,1),
    (465,197,1),
    (462,206,1),
    (465,226,1),
    (459,229,1),
    (452,227,1),
    (451,208,1),
    (455,191,1),
    (460,184,1),
    (474,168,1),
    (478,161,1),
    (491,152,1),
    (500,148,1),
    (564,149,0),
    (576,147,0),
    (587,147,0),
    (605,138,0),
    (612,131,0),
    (625,120,0),
    (626,108,0),
    (626,106,0),
    (629,104,0),
    (628,75,0),
    (623,56,0),
    (619,44,0),
    (598,25,0),
    (585,19,0),
    (579,19,0),
    (575,16,0),
    (380,16,0),
    (369,19,0),
    (355,19,0),
    (348,22,0),
    (323,24,0),
    (310,30,0),
    (281,36,0),
    (264,40,0),
    (238,39,0),
    (223,38,0),
    (218,35,0),
    (207,33,0),
    (198,30,0),
    (181,21,0),
    (173,19,0),
    (161,18,0),
    (151,16,0),
    (79,16,0),
    (75,18,0),
    (66,17,0),
    (62,19,0),
    (56,20,0),
    (49,23,0),
    (44,25,0),
    (40,32,0),
    (29,41,0),
    (24,47,0),
    (20,55,0),
    (20,64,0),
    (17,65,0),
    (18,77,0),
    (16,79,0),
    (16,167,0),
    (17,172,0),
    (20,178,0),
    (21,178,0),
    (39,197,0),
    (50,203,0),
    (57,206,0),
    (63,206,0),
    (64,208,0),
    (97,209,0),
    (146,209,1),
    (206,210,1),
    (218,211,1),
    (216,219,1),
    (219,221,1),
    (211,223,1),
    (136,222,1),
    (131,220,0),
    (97,219,0),
    (95,217,0),
    (73,216,0),
    (61,220,0),
    (52,223,0),
    (42,223,0),
    (32,234,0),
    (20,245,0),
    (15,254,0),
    (9,267,0),
    (9,278,0),
    (7,294,0),
    (9,312,0),
    (6,315,0),
    (7,337,0),
    (12,349,0),
    (25,358,0),
    (45,367,0),
    (49,371,0),
    (74,371,0),
    (79,373,0),
    (148,373,0),
    (148,369,0),
    (147,370,0)
]

track7_internal_borders = [
    (100,306,1),
    (522,306,1),
    (548,282,1),
    (546,241,1),
    (543,239,1),
    (536,241,1),
    (536,269,1),
    (534,275,1),
    (526,281,1),
    (518,290,1),
    (515,292,1),
    (410,291,1),
    (405,288,1),
    (399,288,1),
    (387,278,1),
    (387,270,1),
    (386,118,1),
    (387,114,1),
    (396,104,1),
    (408,96,1),
    (421,94,1),
    (487,95,1),
    (492,94,1),
    (491,88,1),
    (489,83,1),
    (482,81,1),
    (404,81,1),
    (389,82,1),
    (364,85,1),
    (345,91,1),
    (327,93,1),
    (315,95,1),
    (306,97,1),
    (299,101,1),
    (288,106,1),
    (284,110,1),
    (278,112,1),
    (259,114,1),
    (250,117,1),
    (241,117,1),
    (235,117,1),
    (227,116,1),
    (223,114,1),
    (209,111,1),
    (196,110,1),
    (192,109,1),
    (188,108,1),
    (180,105,1),
    (178,104,1),
    (174,100,1),
    (173,98,1),
    (162,92,1),
    (157,91,1),
    (151,87,1),
    (146,84,1),
    (141,81,1),
    (134,81,1),
    (117,81,1),
    (107,81,1),
    (96,92,1),
    (97,99,1),
    (97,103,1),
    (93,104,1),
    (93,141,1),
    (99,146,1),
    (106,148,1),
    (164,148,1),
    (177,145,1),
    (193,144,1),
    (203,139,1),
    (226,136,1),
    (237,134,1),
    (273,135,1),
    (286,136,1),
    (305,141,1),
    (316,147,1),
    (325,156,1),
    (331,164,1),
    (338,177,1),
    (341,184,1),
    (340,199,1),
    (338,214,1),
    (336,232,1),
    (332,242,1),
    (306,263,1),
    (284,275,1),
    (263,282,1),
    (242,286,1),
    (217,288,1),
    (213,290,1),
    (205,293,1),
    (191,291,1),
    (104,290,1),
    (99,290,1),
    (98,298,1),
    (97,305,1),
    (97,305,1),
    (100,306)
]

track7_external_gate_map = [343,370,369,370,395,369,455,371,483,371,520,371,582,372,622,345,625,257,622,205,606,177,582,162,536,162,504,160,475,179,461,201,463,222,461,225,461,228,459,230,456,230,455,230,454,230,453,228,451,224,450,223,451,198,457,182,465,172,474,163,485,156,496,151,509,148,539,146,582,146,618,124,629,80,620,48,595,24,570,15,525,16,474,17,440,15,401,15,369,19,321,24,283,33,262,39,240,40,229,39,215,35,186,25,156,17,119,17,76,18,43,26,22,51,15,110,15,150,18,174,43,198,121,209,160,209,179,207,190,207,203,207,215,208,219,209,222,211,223,213,224,215,225,218,225,220,224,222,223,222,220,224,217,225,213,225,210,225,207,225,195,225,178,224,155,224,119,222,79,220,42,226,21,246,9,273,8,313,17,351,45,367,96,372,127,372,142,372,168,370,198,370,225,370,256,370,289,370,316,369]

track7_internal_gate_map = [339,303,371,304,404,303,452,305,476,304,512,304,530,294,546,277,546,245,545,243,542,241,540,240,536,240,535,241,534,242,533,246,535,257,536,270,519,289,494,289,464,290,435,290,403,288,387,274,385,245,385,224,384,193,385,164,384,136,384,115,404,96,435,95,467,95,487,93,490,92,491,89,493,86,492,84,491,83,487,82,485,83,466,82,435,81,404,82,376,82,343,91,315,98,282,111,252,115,225,114,195,106,165,93,141,81,122,81,106,81,101,87,99,97,95,119,95,137,97,145,106,145,130,147,161,147,187,144,208,137,235,133,264,133,290,136,312,141,326,157,337,169,337,187,337,208,335,228,329,241,313,255,287,270,270,278,250,282,227,288,198,291,172,290,139,289,113,289,104,289,102,290,101,292,101,293,101,296,101,299,101,302,103,305,114,304,136,305,171,305,200,304,229,305,253,305,290,304,318,303]

track7_finish_line_rect = (325, 305,4,82)
track7_first_car_start_position = (325, 310)
track7_flag_anchor = (330, 285)
track7_start_sprite_angle = 4
track7_score_time_reference = 11.5
track7_complete_lap_score = 80
track7_finish_line_direction = 1



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