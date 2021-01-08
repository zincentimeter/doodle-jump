import os
import utils
import numpy as np
import ast
from utils import *

##############################################################
# Game -> Model Processing

def getGameState():
    received_dict = receiveDict()
    
    # print("received_dict : %s." % str(received_dict))
    raw_boards = list()
    relative_boards = list()
    agent_pos = received_dict['agent_pos']
    num_boards = 0
    for raw_board in received_dict['raw_boards']:
        # relative_boards.append()
        raw_board_pos = raw_board[0]
        board_type = raw_board[1]
        relative_board_pos = absoluteToRelative(raw_board_pos, agent_pos)
        if (0 <= relative_board_pos[1] <= Y):
            relative_boards.append((relative_board_pos, board_type))
            raw_boards.append((raw_board_pos, board_type))
            num_boards += 1

    received_dict['num_boards'] = num_boards
    received_dict['raw_boards'] = raw_boards
    received_dict['relative_boards'] = relative_boards
    # print("filtered_dict : %s." % str(received_dict))
    # if (received_dict['is_died']):
    #     print("died at this moment!")
    # if (received_dict['is_hit']):
    #     print("hit the wall!")
    # else:
    #     print("NOT hit the wall!")


    return received_dict

    # input(dict_received)


def receiveDict():
    utils.connection, utils.address = utils.s.accept()
    # print("connection accpeted.\nreceiving...")
    bytes_received = utils.connection.recv(8192)
    dict_received = bytes_received.decode('ASCII')
    # print("gotcha. length : %s." % str(len(dict_received)))
    # print("payload : %s." % str(ast.literal_eval(dict_received)))
    return ast.literal_eval(dict_received)


def retrieveGameState():
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
    read_buffer = []
    gameState = {}
    file = open("game/logout.txt")
    try:
        for line in file:
            line = line.replace('(Clone)', '')
            str_list = line.split(" ", 1)
            read_buffer.append((str_list[0], str_list[1].replace('\n', '')))
        # When file R/W conflict happens, give last gameState
        if len(read_buffer) == 0:
            return utils.last_gameState

        # camera_y - DEPRECATED
        gameState['camera_y'] = float(read_buffer[-1][1])

        # agent position
        temp_set = read_buffer[-4][1].replace(
            '(', '').replace(')', '').split(',')
        agent_pos = (float(temp_set[0]), float(temp_set[1]))
        gameState['agent_pos'] = agent_pos
        # get boards info
        gameState['num_boards'] = int(read_buffer[0][1])
        gameState['raw_boards'] = []
        gameState['relative_boards'] = []
        # input("c")
        for i in read_buffer[1:-4]:
            temp_set = i[1].replace('(', '').replace(')', '').split(',')
            absolute_board_pos = (float(temp_set[0]), float(temp_set[1]))
            relative_board_pos = absoluteToRelative(
                absolute_board_pos, agent_pos)
            type_value = getTypeValue(i[0])
            if relative_board_pos[1] <= Y:
                gameState['raw_boards'].append(
                    (absolute_board_pos, type_value))
                gameState['relative_boards'].append(
                    (relative_board_pos, type_value))
            else:
                # not counted when the board is not visible from the current screen
                gameState['num_boards'] -= 1
        # input("d")

        # agent speed
        gameState['agent_speed'] = float(read_buffer[-3][1])

        # score : used for reward
        gameState['score'] = int(read_buffer[-2][1])
        utils.last_gameState = gameState
        utils.text = read_buffer
        return gameState
    except:
        print("error happened and last dict is given.")

        return utils.last_gameState


##############################################################
# Model -> Game Processing

# return a tuple :  ( (board_pos : 2 tuple), board_type : int )
def findDestination(gameState: dict, action: tuple):
    boards = gameState['raw_boards']
    agent_pos = gameState['agent_pos']
    expected_pos = relativeToAbsolute(action, agent_pos)
    boards_sorted = sorted(boards,
                           key=lambda board_pos: manhattanDistance(board_pos[0], expected_pos))
    return boards_sorted[0]


def findDestination_absolute(gameState: dict, absolute_y: float):
    closest_entry = min(gameState["raw_boards"],
                        key=lambda board: abs(absolute_y - board[0][1]))
    # print("closest_entry %s" % str(closest_entry))
    return closest_entry

    # for board in gameState["raw_boards"]:
    #     input(absolute_y - board[0][1])
    #     if absolute_y == board[0][1]:
    #         input(board)
    #         return board
# return:


def getDirection(gameState: dict, target_board_pos: tuple):
    agent_pos = gameState['agent_pos']
    x, y = difference(target_board_pos, agent_pos)
    if x == 0:
        return 0
    # elif abs(x) <= raw_x:
    #     return 1 if x > 0 else -1
    # else:  # abs(x) > raw_x ==> go to inverted way
    #     return -1 if x > 0 else 1
    else:
        return 1 if x > 0 else -1


# def writeBack(result: tuple):
#     text = str(result[0])+' '+str(result[1])+' '+str(result[2])
#     # input(text)
#     try:
#         file_handle = open('game/login.txt', mode='w')
#         file_handle.write(text)
#         file_handle.close()
#     except:
#         print("error")
#     return

def writeBack(text: str):
    bytes_to_send = bytes(text, 'ASCII')
    # print("sending...")
    utils.connection.sendall(bytes_to_send)
    # print("sent...")
    utils.connection.close()
    # try:
    #     file_handle = open('game/login.txt', mode='w')
    #     file_handle.write(text)
    #     file_handle.close()
    # except:
    #     print("error")
    # return

##############################################################
# FOR Writing Back to LOG


def getFormated(gameState: dict, action_absolute: float, q_dict_str_debug : str, debug=False):
    target_board = findDestination_absolute(gameState, action_absolute)
    target_board_pos = target_board[0]
    print(target_board_pos)
    destinationX, absolute_y = target_board_pos
    rightDir = 0
    leftDir = 0
    offset = 0.5
    playerX = gameState['agent_pos'][0]
    # print("player x %s" % str(playerX))
    if playerX > destinationX + offset:
        rightDir = 5.5625 - playerX + (destinationX + 5.5625)
        leftDir = playerX - destinationX
    elif destinationX > playerX + offset:
        rightDir = destinationX - playerX
        leftDir = playerX + 5.5625 + (5.5625 - destinationX)
    else:
        absolute_y = absolute_y
        text = '0 ' + str(destinationX) + ' ' + str(absolute_y)
        if debug:
            text += " | "+q_dict_str_debug
        # input(text)
        return text

    absolute_y = absolute_y
    # input("absolute_y = %s" % str(absolute_y))
    if rightDir <= leftDir:
        text = '1 ' + str(destinationX) + ' ' + str(absolute_y)
    else:
        text = '-1 ' + str(destinationX) + ' ' + str(absolute_y)
    if debug:
        text += " | "+q_dict_str_debug
    # input(text)
    return text
