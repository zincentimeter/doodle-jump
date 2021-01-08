from math import ceil, trunc
import socket
import game_logic
# Used for Q matrix size : 100800
SCREEN_SIZE = (800, 600)
dx, dy = 8*2, 6*2
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)  # = (90, 160)
T = 4

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

def bias(unbiased_absolutes: tuple):
    return unbiased_absolutes[0]+40, unbiased_absolutes[1]

def unbias(biased_absolutes: tuple):
    return biased_absolutes[0]-40, biased_absolutes[1]

# absolutes and its ref [0,W], [0,H]
# unbiased relative pos [-W, W], [-H, H]
# return biased relative pos [0, X], [0, Y]
def absoluteToRelative(absolultes: tuple, absolute_reference: tuple):
    absolute_x, absolute_y = difference(absolultes, absolute_reference)

    relative_x = (absolute_x + W) * X / (2 * W)
    relative_y = (absolute_y + H) * Y / (2 * H)
    relatives = (relative_x, relative_y)
    return truncate(relatives)

# biased relative pos [0, X], [0, Y]
# unbiased relative pos [-W, W], [-H, H]
# absolutes ref [0, W], [0, H]
# return absolutes [0, W], [0, H]
def relativeToAbsolute(relatives: tuple, absolute_reference: tuple):
    relative_x, relative_y = relatives

    absolute_x = (relative_x * (2 * W)) / X - W
    absolute_y = (relative_y * (2 * H)) / Y - H
    absolutes = (absolute_x, absolute_y)
    return add(absolutes, absolute_reference)


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
