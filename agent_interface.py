import random
import numpy as np
from agent_base_classes import *
from math import ceil, exp, trunc
from utils import *
import time


class DoodleJumpQLearningAgent(QLA, EGA):
    def __init__(self, **kwargs):
        QLA.__init__(self, **kwargs)
        EGA.__init__(self, **kwargs)
        # self.Q = np.zeros((X+1, Y+1, T))
        self.Q = np.random.rand(X+1, Y+1, T) + 1000
        self.save_interval = 100
        self.save_counter = 0

    def get_Q(self, s, a):
        (x, y), t = a
        # if (y >= Y) or (x >= X):
            # return 0
        return self.Q[x, y, t]

    def update_Q(self, s, a, s_, R):
        (x, y), t = a
        Q_sample = R + self.gamma * self.get_V(s_)
        diff = Q_sample - self.Q[x, y, t]
        self.Q[x, y, t] += (self.alpha * diff)
        if not (self.save_counter % self.save_interval):
            np.save(f'./game/QQ/Q_{time.time()}.npy', self.Q)
            print("saved!")
        self.save_counter += 1

    def get_possible_actions(self, s):
        actions = list()
        for board in s['relative_boards']:
            p, t = board[:2]
            actions.append((p, t))
        return actions
