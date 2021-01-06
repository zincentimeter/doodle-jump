import random
import numpy as np
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


class ModelFreeReinforcementLearningAgent:
    def __init__(self, gamma, **kwargs):
        self.gamma = gamma

    def decide(self, s):
        abstract

    def get_Q(self, s, a):
        abstract

    def update_Q(self, s, a, s_, R):
        abstract

    def get_possible_actions(self, s):
        # TODO: abstract
        p0 = s['agent_pos']
        actions = list()
        for board in s['boards']:
            p, t = board[:2]
            actions.append((trunc_tuple(relative_pos(p, p0)), t))
            # TODO: Truncate position to integer
        return actions

    def raise_no_actions_error(self):
        input('Warning! No possible action!\nPress ENTER to continue...')
        # TODO: Need to do something when nothing is given.

    def get_V_opt_a(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            self.raise_no_actions_error()
        return max([(self.get_Q(s, a), a) for a in actions])

    def get_V(self, s):
        return self.get_V_opt_a(s)[0]

    def get_optimal_action(self, s):
        return self.get_V_opt_a(s)[1]

MFRLA = ModelFreeReinforcementLearningAgent

class EpsilonGreedyAgent(MFRLA):
    def __init__(self, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.epsilon = epsilon

    def decide(self, s):
        if random.random() < self.epsilon:
            return self.__get_random_action(s)
        else:
            return self.get_optimal_action(s)

    def __get_random_action(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            self.raise_no_actions_error()
        return random.choice(actions)

EGA = EpsilonGreedyAgent

class SoftmaxAgent(MFRLA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def decide(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            self.raise_no_actions_error()
        dist = [(exp(self.get_Q(s, a)), a) for a in actions]
        return self.__choose_by_weight(dist)

    def __choose_by_weight(self, dist):
        '''
        dist: list of (weight, key), key without repetition
        '''
        best = max(dist)
        choice = random.random() * sum([w for w, k in dist])
        choice -= best[0]
        if choice < 0:
            return best[1]
        for w, k in dist:
            if k == best[1]:
                continue
            choice -= w
            if choice < 0:
                return k
        return k

SMA = SoftmaxAgent

class QLearningAgent(MFRLA):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = dict()

    def get_Q(self, s, a):
        try:
            return self.Q[s, a]
        except KeyError:
            default = 0  # or at random
            self.Q[s, a] = default
            return default

    def update_Q(self, s, a, s_, R):
        Q_sample = R + self.gamma * self.get_V(s_)
        diff = Q_sample - self.get_Q(s, a)
        self.Q[s, a] += (self.alpha * diff)

QLA = QLearningAgent

class NaiveDeepQLearningAgent(MFRLA):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = DeepQNetwork()

    def get_Q(self, s, a):
        return self.Q.query(s, a)

    def update_Q(self, s, a, s_, R):
        self.Q.update()
        
NDQLA = NaiveDeepQLearningAgent

class ExperienceReplayAgent:
    pass
