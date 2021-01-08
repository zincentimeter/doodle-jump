from math import ceil, trunc
import socket
import doodlejump
# Used for Q matrix size : 100800
SCREEN_SIZE = (800, 600)
dx, dy = 8, 6
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)  # = (90, 160)
T = 7

# The maxmimal value of original coordinate system in game
raw_x = 5.5625  # [-raw_x , raw_x]
raw_y = 10  # [-raw_y, raw_y]


def init_globals():
    # Record the last game state
    global last_gameState
    global text
    global recv_bytes
    global connection
    last_gameState = {}
    text = ''
    

    # recv_bytes = 8192
    # try:
    #     global s
    #     s = socket.socket()
    #     socket.setdefaulttimeout(None)
    #     print('socket created.')
    #     port = 60001
    #     s.bind(('127.0.0.1', port)) #local host
    #     s.listen(30) #listening for connection for 30 sec?
    #     print('socket listening ... ')
    # except KeyboardInterrupt:
    #     print("manually terminated while receiving.")
    #     exit()


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
    # relative_x = (absolute_x + 2 * raw_x) * X / (4 * raw_x)
    # relative_y = (absolute_y + 2 * raw_y) * Y / (4 * raw_y)
    relative_x = (absolute_x) * X / raw_x
    relative_y = (absolute_y) * Y / raw_y
    return truncate((relative_x, relative_y))


def relativeToAbsolute(relatives: tuple, absolute_reference: tuple):
    relative_x, relative_y = relatives
    # absolute_x = (relative_x * 4 * raw_x) / X - 2 * raw_x
    # absolute_y = (relative_y * 4 * raw_y) / Y - 2 * raw_y
    absolute_x = relative_x * raw_x / X
    absolute_y = relative_y * raw_y / Y
    return add((absolute_x, absolute_y), absolute_reference)


def getTypeValue(board_typename: str):
    if (board_typename == 'Platform_Green'):
        return 0
    elif (board_typename == 'Platform_Brown'):
        return 1
    elif (board_typename == 'Platform_Blue'):
        return 2
    elif (board_typename == 'Platform_White'):
        return 3
    elif (board_typename == 'Propeller'):
        return 4
    elif (board_typename == 'Trampoline'):
        return 5
    elif (board_typename == 'Spring'):
        return 6
