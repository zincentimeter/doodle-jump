import os
import utils
import numpy as np
import ast
import game_logic
from utils import *

##############################################################
# Game -> Model Processing

def getGameState(game : game_logic.DoodleJump):
    received_dict = game.gameState
    
    # print("received_dict : %s." % str(received_dict))
    raw_boards = list()
    relative_boards = list()
    agent_pos = received_dict['agent_pos']
    num_boards = 0
    for raw_board in received_dict['raw_boards']:
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

    return received_dict

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

# return ( direction, destination_absolute(x, y) )
def getAction(gameState: dict, target_absolute: tuple):

    player_absolute = gameState['agent_pos']
    player_x_absolute = player_absolute[0]
    
    target_x_absolute = target_absolute[0]
    target_y_absolute = target_absolute[1]
    target_offset = 5
    return lrdecide( player_x_absolute, target_x_absolute, target_offset, target_y_absolute)

def lrdecide(player_x_absolute, target_x_absolute, target_offset, target_y_absolute):
    """
    docstring
    """
    # input("%d %d %d %d" %  (player_x_absolute, target_x_absolute, target_offset, target_y_absolute))
    # 物体在玩家左边
    if (player_x_absolute > target_x_absolute + target_offset):
        right_direction_absolute = (W - player_x_absolute) + (target_x_absolute + W)
        left_direction_absolute = player_x_absolute - target_x_absolute
    # 物体在玩家右边
    elif (target_x_absolute > player_x_absolute + target_offset):
        right_direction_absolute = target_x_absolute - player_x_absolute
        left_direction_absolute = (player_x_absolute + W) + (W - target_x_absolute)
    # 物体在玩家可碰到的地方
    else:
        direction = 0
        return direction, (target_x_absolute, target_y_absolute)
    
    direction = 1 if (right_direction_absolute <= left_direction_absolute) \
        else -1
    return direction, (target_x_absolute, target_y_absolute)

