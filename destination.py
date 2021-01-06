#!!!!!!!!!!!!!!!!! DEPRECATED.
lastX = 0
lastY = 0
tf = False
tfY = 0
def output(dict, destinationY):
    """

    :param dict:
    :param destinationY:
    :return:
    """
    boards = dict['raw_boards']
    # input("boards %s " % str(boards))
    list = []
    for board in boards:
        list.append(abs(destinationY - board[0][1]))
    destinationX = boards[list.index(min(list))][0][0]
    destinationY = boards[list.index(min(list))][0][1]
    rightDir = 0
    leftDir = 0
    playerX = dict['agent_pos'][0]

    if playerX > destinationX + 0.1:
        rightDir = 5.5625 - playerX + (destinationX + 5.5625)
        leftDir = playerX - destinationX
    elif destinationX > playerX + 0.1:
        rightDir = destinationX - playerX
        leftDir = playerX + 5.5625 + (5.5625 - destinationX)
    else:
        destinationY = destinationY + dict['camera_y']
        text = '0 ' + str(destinationX) + ' ' + str(destinationY)
        print(text)
        try:
            file_handle = open('game/login.txt', mode='w')
            file_handle.write(text)
            file_handle.close()
        except:
            print("error")
        return

    destinationY = destinationY + dict['camera_y']
    # input("destinationY = %s" % str(destinationY))
    if rightDir <= leftDir:
        text = '1 ' + str(destinationX) + ' ' + str(destinationY)
    else:
        text = '-1 ' + str(destinationX) + ' ' + str(destinationY)
    print(text)
    try:
        file_handle = open('game/login.txt',mode='w')
        file_handle.write(text)
        file_handle.close()
    except:
        print("error")



def pusu(dict):
    speed = dict["agent_speed"]
    global lastX, lastY, tf
    destinationX = 0
    if abs(speed) > 13.5:
        pos = dict["agent_pos"]
        for board in dict["raw_boards"]:
            if pos[1] < board[0][1]:
                if board[1] == 1:
                    print("do")
                    pass
                else:
                    destinationY = board[0][1]
                    break
    else:
        destinationY = lastY
    for board in dict["raw_boards"]:
        if board[1] == 1:
            print("do")
            pass
        if destinationY == board[0][1]:
            destinationX = board[0][0]
            lastX = destinationX
            lastY = destinationY
            break


    rightDir = 0
    leftDir = 0
    playerX = dict['agent_pos'][0]
    if playerX > destinationX + 0.3:
        rightDir = 5.5625 - playerX + (destinationX + 5.5625)
        leftDir = playerX - destinationX
    elif destinationX > playerX + 0.3:
        rightDir = destinationX - playerX
        leftDir = playerX + 5.5625 + (5.5625 - destinationX)
    else:
        text = '0 ' + str(destinationX) + ' ' + str(destinationY)
        try:
            file_handle = open('game/login.txt', mode='w')
            file_handle.write(text)
            file_handle.close()
        except:
            a=1
        return
    if rightDir <= leftDir:
        text = '1 ' + str(destinationX) + ' ' + str(destinationY)
    else:
        text = '-1 ' + str(destinationX) + ' ' + str(destinationY)
    try:
        file_handle = open('game/login.txt', mode='w')
        file_handle.write(text)
        file_handle.close()
    except:
        a=1



