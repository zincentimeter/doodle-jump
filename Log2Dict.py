import os
from math import ceil, trunc

last_dict = {}

SCREEN_SIZE = (720, 1280)
dx, dy = 50, 50
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)
T = 10
raw_x = 5.5625 # [-raw_x , raw_x]
raw_y = (raw_x * 2) / SCREEN_SIZE[0] * SCREEN_SIZE[1] # [0, raw_y]


def resample(a : set):
    x, y = float(a[0]), float(a[1])
    x = trunc((x / raw_x + 1) * X * 0.5)
    y = trunc(y / raw_y * Y)
    return (x,y)

def desample(a : set):
    x, y = int(a[0]), int(a[1])
    x = (x * 2 / X - 1) * raw_x
    y = y / Y * raw_y
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

    for line in file:
        line = line.replace('(Clone)','')
        str_list = line.split(" ",1)
        list.append((str_list[0],str_list[1].replace('\n', '')))
    if len(list) == 0:
        return last_dict
    dict['numBoard'] = int(list[0][1])
    dict['raw_boards'] = []
    dict['boards'] = []
    for i in list[1:-3]:
        set = i[1].replace('(','').replace(')','').split(',')
        tuple = (float(set[0]),float(set[1]))
        resampled_tuple = resample(set)
        # dict['raw_boards'].append((tuple,i[0]))
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
    set = list[-3][1].replace('(', '').replace(')', '').split(',')
    tuple = (float(set[0]), float(set[1]))
    dict['agent_pos'] = tuple
    dict['agentSpeed'] = float(list[-2][1])
    dict['score'] = int(list[-1][1])
    last_dict = dict
    return dict


if __name__ == "__main__":
    print(logToDict())
    os.system("cls")
