def output(dict, destinationY):
    """

    :param dict:
    :param destinationY:
    :return:
    """
    boards = dict['boards']
    for board in boards:
        if destinationY == board[0][1]:
            destinationX = board[0][0]
            break

    playerX = dict['agentPos'][0]
    if playerX > destinationX + 0.1:
        rightDir = 5.5625 - playerX + (destinationX + 5.5625)
        leftDir = playerX - destinationX
    if destinationX > playerX + 0.1:
        rightDir = destinationX - playerX
        leftDir = playerX + 5.5625 + (5.5625 - destinationX)

    if rightDir <= leftDir:
        text = '1 ' + str(destinationX) + ' ' + str(destinationY)
    else:
        text = '-1 ' + str(destinationX) + ' ' + str(destinationY)

    with open('game/login.txt', 'w', encoding='utf-8') as f:
        f.write(text)




