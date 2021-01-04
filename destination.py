
def output(dict, destinationY):
    """

    :param dict:
    :param destinationY:
    :return:
    """
    boards = dict['raw_boards']
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
        text = '0 ' + str(destinationX) + ' ' + str(destinationY)
        print(text)
        try:
            file_handle = open('game/login.txt', mode='w')
            file_handle.write(text)
            file_handle.close()
        except:
            print("error")
        return
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




