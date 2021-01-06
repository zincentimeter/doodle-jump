import random
import numpy as np
from agent_base_classes import *
from math import ceil, exp, trunc

SCREEN_SIZE = (720, 1280)
dx, dy = 50, 50
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)
T = 10
last_D = 0

def relative_pos(a, b):
    return (a[0] - b[0], a[1] - b[1])

def trunc_tuple(a: tuple, dx=1, dy=1):
    x, y = a
    x = round(x / dx)
    y = round(y / dy)
    return x, y

class DoodleJumpQLearningAgent(QLA, EGA):
    def __init__(self, **kwargs):
        QLA.__init__(self, **kwargs)
        EGA.__init__(self, **kwargs)
        self.Q = np.zeros((X, Y, 20))

    def get_Q(self, s, a):
        (x, y), t = a
        return self.Q[x, y, t]

    def update_Q(self, s, a, s_, R):
        (x, y), t = a
        Q_sample = R + self.gamma * self.get_V(s_)
        diff = Q_sample - self.Q[x, y, t]
        self.Q[x, y, t] += (self.alpha * diff)

    def get_possible_actions(self, s):
        p0 = s['agent_pos']
        actions = list()
        for board in s['boards']:
            p, t = board[:2]
            actions.append((trunc_tuple(relative_pos(p, p0)), t))
            # TODO: Truncate position to integer
        return actions

if __name__ == "__main__":
    from game_interface import *

    agent = DoodleJumpQLearningAgent(alpha=0.02, gamma=0.02)
    
    gameState = logToDict()
    input(gameState)
    action = agent.get_optimal_action(gameState)
    writeBack(getFormated(gameState, action))
    lastState = gameState
    lastAction = action
    while (True):
        gameState = logToDict()
        reward = gameState['score'] - lastState['score']
        agent.observe(lastState, lastAction, gameState, reward)
        action = agent.decide(gameState)
        # input(gameState['agent_pos'])
        writeBack(getFormated(gameState, action))
        lastState = gameState
        lastAction = action
        os.system("cls")