import os
from math import ceil, trunc

last_dict = {}

SCREEN_SIZE = (720, 1280)
dx, dy = 50, 50
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)
T = 10
raw_x = 5.5625 # [-raw_x , raw_x]
raw_y = 10 # [-raw_y, raw_y]


def resample(a : tuple):
    x, y = a[0], a[1]
    x = trunc((x / raw_x + 1) * X * 0.5)
    y = trunc((y / raw_y + 1) * Y * 0.5)
    return (x,y)

def desample(a : set):
    x, y = int(a[0]), int(a[1])
    x = (x * 2 / X - 1) * raw_x
    y = (y * 2 / Y - 1) * raw_y
    return (x,y)

def logToDict():
    '''
    :return:
    dict GameState =
    {'numBoard': 12,
    'raw_boards': [((0.0, -7.5), 'Platform_Green'), ((2.5, -5.5), 'Platform_Green') ......],
    'agent_pos': (-0.1, -5.2),
    'agentSpeed': 19.5095,
    'score': 0}

    board_type definition:
    "Platform_Green" -> Normal
    "Platform_Brown" -> Chocolate
    "Platform_Blue"  -> Move_horizontal
    "Platform_White" -> Only_once
    "Propeller"      -> Triple_jump
    "Trampoline"     -> Double_jump
    "Spring"         -> Single_jump
    '''
    list = []
    dict = {}
    global last_dict
    file = open("game/logout.txt")
    try:
        for line in file:
            line = line.replace('(Clone)','')
            str_list = line.split(" ",1)
            list.append((str_list[0],str_list[1].replace('\n', '')))
        if len(list) == 0:
            return last_dict
        dict['numBoard'] = int(list[0][1])
        dict['raw_boards'] = []
        dict['boards'] = []

        # CameraY
        camera_y = dict['CameraY'] = float(list[-1][1])

        # agent position
        set = list[-4][1].replace('(', '').replace(')', '').split(',')
        tuple = (float(set[0]), float(set[1]) - camera_y)
        # input("raw_tuple %s" % set)
        dict['agent_pos'] = resample(tuple)
        # dict['raw_agent_pos'] = tuple
        for i in list[1:-4]:
            set = i[1].replace('(','').replace(')','').split(',')
            # input("tuple = %s" % str((float(set[0]),float(set[1]))))
            # input("tuple(relative) = %s" % str((float(set[0]),float(set[1])-camera_y)))
            tuple = (float(set[0]),float(set[1]) - camera_y)
            resampled_tuple = resample(tuple)
            if (i[0] == 'Platform_Green'):
                type_value = 0
            elif (i[0] == 'Platform_Brown'):
                type_value = 1
            elif (i[0] == 'Platform_Blue'):
                type_value = 2
            elif (i[0] == 'Platform_White'):
                type_value = 3
            elif (i[0] == 'Propeller'):
                type_value = 4
            elif (i[0] == 'Trampoline'):
                type_value = 5
            elif (i[0] == 'Spring'):
                type_value = 6
            dict['raw_boards'].append((tuple, type_value))
            dict['boards'].append((resampled_tuple, type_value))

        dict['agentSpeed'] = float(list[-3][1])
        dict['score'] = int(list[-2][1])
        last_dict = dict
        return dict
    except:
        return last_dict



if __name__ == "__main__":
    print(logToDict())
    os.system("cls")
