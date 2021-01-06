import os
from math import ceil, trunc

last_gameState = {}

SCREEN_SIZE = (720, 1280)
dx, dy = 8, 8
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)  # = (90, 160)
T = 7  # State Size = 100800
raw_x = 5.5625  # [-raw_x , raw_x]
raw_y = 10  # [-raw_y, raw_y]

##############################################################


def manhattanDistance(a: tuple, b: tuple):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def add(a: tuple, b: tuple):
    return a[0] + b[0], a[1] + b[1]


def difference(a: tuple, b: tuple):
    return a[0] - b[0], a[1] - b[1]


def truncate(relatives: tuple):
    return trunc(relatives[0]), trunc(relatives[1])


def absoluteToRelative(absolultes: tuple, absolute_reference: tuple):
    absolute_x, absolute_y = difference(absolultes, absolute_reference)
    relative_x = (absolute_x + 2 * raw_x) * X / (4 * raw_x)
    relative_y = (absolute_y + 2 * raw_y) * Y / (4 * raw_y)
    return truncate((relative_x, relative_y))


def relativeToAbsolute(relatives: tuple, absolute_reference: tuple):
    relative_x, relative_y = relatives
    absolute_x = (relative_x * 4 * raw_x) / X - 2 * raw_x
    absolute_y = (relative_y * 4 * raw_y) / Y - 2 * raw_y
    return add((absolute_x, absolute_y), absolute_reference)

##############################################################
# Game -> Model Processing

def logToDict():
    '''
    :return:
    dict gameState =
    {'num_boards': 12,
    'raw_boards': [((0.0, -7.5), 'Platform_Green'), ((2.5, -5.5), 'Platform_Green') ......],
    'agent_pos': (-0.1, -5.2),
    'agent_speed': 19.5095,
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
    gameState = {}
    global last_gameState
    file = open("game/logout.txt")
    try:
        for line in file:
            line = line.replace('(Clone)', '')
            str_list = line.split(" ", 1)
            list.append((str_list[0], str_list[1].replace('\n', '')))
        if len(list) == 0:
            return last_gameState
        gameState['num_boards'] = int(list[0][1])
        gameState['raw_boards'] = []
        gameState['relative_boards'] = []

        # camera_y
        gameState['camera_y'] = float(list[-1][1])
        # agent position
        set = list[-4][1].replace('(', '').replace(')', '').split(',')
        agent_pos = (float(set[0]), float(set[1]))
        gameState['agent_pos'] = agent_pos

        for i in list[1:-4]:
            set = i[1].replace('(', '').replace(')', '').split(',')
            board_pos = (float(set[0]), float(set[1]))
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
            gameState['raw_boards'].append((board_pos, type_value))
            gameState['relative_boards'].append(
                (absoluteToRelative(board_pos, agent_pos), type_value))

        gameState['agent_speed'] = float(list[-3][1])
        gameState['score'] = int(list[-2][1])
        last_gameState = gameState
        return gameState
    except:
        print("error happened and last dict is given.")
        return last_gameState

##############################################################
# Model -> Game Processing

def findDestination(gameState: dict, action: tuple):
    boards = gameState['raw_boards']
    agent_pos = gameState['agent_pos']
    expected_pos = relativeToAbsolute(action, agent_pos)
    # input(agent_pos)
    # input(expected_pos)
    # input(boards)
    boards_sorted = sorted(boards,
                           key=lambda board_pos: manhattanDistance(board_pos[0], expected_pos))
    return boards_sorted[0]


def getDirection(gameState: dict, target_board_pos: tuple):
    agent_pos = gameState['agent_pos']
    x, y = difference(target_board_pos, agent_pos)
    input((x, y))
    if x == 0:
        return 0
    elif abs(x) <= raw_x:
        return 1 if x > 0 else -1
    else:  # abs(x) > raw_x ==> go to inverted way
        return -1 if x > 0 else 1


def writeBack(result: tuple):
    text = str(result[0])+' '+str(result[1])+' '+str(result[2])
    input(text)
    try:
        file_handle = open('game/login.txt', mode='w')
        file_handle.write(text)
        file_handle.close()
    except:
        print("error")
    return

##############################################################
# FOR Writing Back to LOG

def getFormated(gameState: dict, action: tuple):
    target_board = findDestination(gameState, action)
    target_board_pos = target_board[0]
    input(target_board)
    input(target_board_pos)
    return getDirection(gameState, target_board_pos), target_board_pos[0], target_board_pos[1]


if __name__ == "__main__":
    input(logToDict())
    gameState = logToDict()
    action = (48, 79)
    input(gameState['agent_pos'])
    writeBack(getFormated(gameState, action))
    os.system("cls")
