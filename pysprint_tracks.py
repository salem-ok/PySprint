#pysprint_tracks.py
import math

def calculate_distance(point1,point2):
    return math.sqrt( ((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))


class Track:
    background_filename = 'Assets/SuperSprintTrack1.png'
    track_mask_filename = 'Assets/SuperSprintTrack1Mask.png'
    background = None
    track_mask = None
    first_car_start_position = (325, 55)
    flag_anchor = (320, 28)

    start_sprite_angle = 12
    score_time_reference = 6.6



    external_borders = [
        (101, 52, 0),
        (544, 53, 1),
        (560, 54, 1),
        (577, 59, 1),
        (591, 71, 1),
        (601, 84, 1),
        (606, 96, 1),
        (608, 110, 0),
        (610, 331, 1),
        (572, 364, 1),
        (545, 368, 1),
        (449, 371, 0),
        (437, 369, 0),
        (273, 224, 0),
        (263, 224, 1),
        (257, 229, 1),
        (256, 231, 1),
        (257, 258, 1),
        (257, 273, 1),
        (266, 318, 1),
        (266, 354, 1),
        (247, 373, 1),
        (99, 373, 0),
        (71, 368, 1),
        (35, 330, 1),
        (37, 112, 0),
        (40, 93, 1),
        (46, 79, 1),
        (64, 59, 1),
        (75, 55, 1),
        (84, 51, 1)
        ]

    internal_borders = [
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

    finish_line_rect = (346, 48,4,82)

    finish_line = None
    finish_line_direction = -1


    #External gate points

    external_gate_points = [
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
    internal_gate_points = [
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
        (170,146),
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
        int_index = self.find_gate_point(position, self.internal_gate_points)
        ext_index = self.find_gate_point(position, self.external_gate_points)
        #Check closest Internal and external gate point, return the highest index to ignore postion relative to borders
        if ext_index >= int_index:
            return ext_index
        else:
            return int_index

    def get_score_from_laptime(self, laptime):
        if laptime == 0:
            return 0
        else:
            score = math.ceil((500 * (1 + self.score_time_reference/(laptime/1000)) - 600) / 10) * 10
            if score < 0:
                return 0
            else:
                return score

