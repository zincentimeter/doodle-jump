import os
last_dict = {}
def logToDict():
    '''
    :return:
    dict GameState =
    {'numBoard': 12,
    'boards': [((0.0, -7.5), 'Platform_Green'), ((2.5, -5.5), 'Platform_Green') ......],
    'agentPos': (-0.1, -5.2),
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
    file = open("game/log.txt")

    for line in file:
        line = line.replace('(Clone)','')
        str_list = line.split(" ",1)
        list.append((str_list[0],str_list[1].replace('\n', '')))
    if len(list) == 0:
        return last_dict
    dict['numBoard'] = int(list[0][1])
    dict['boards'] = []
    for i in list[1:-3]:
        set = i[1].replace('(','').replace(')','').split(',')
        tuple = (float(set[0]),float(set[1]))
        dict['boards'].append((tuple,i[0]))
    set = list[-3][1].replace('(', '').replace(')', '').split(',')
    tuple = (float(set[0]), float(set[1]))
    dict['agentPos'] = tuple
    dict['agentSpeed'] = float(list[-2][1])
    dict['score'] = int(list[-1][1])
    last_dict = dict
    return dict