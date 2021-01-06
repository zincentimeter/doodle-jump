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

try:
    del abstract, not_defined
except:
    pass

class ModelFreeReinforcementLearningAgent:
    def __init__(self, gamma, **kwargs):
        self.gamma = gamma

    def decide(self, s):
        abstract

    def observe(self, s, a, s_, R):
        abstract

    def get_Q(self, s, a):
        abstract

    def update_Q(self, s, a, s_, R):
        abstract

    def get_possible_actions(self, s):  # inplemented in Interface
        abstract

    def raise_no_possible_actions_error(self):
        input('Warning! No possible action!\nPress ENTER to continue...')
        # TODO: Need to do something when nothing is given.

    def get_V_opt_a(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            self.raise_no_possible_actions_error()
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
            self.raise_no_possible_actions_error()
        return random.choice(actions)

EGA = EpsilonGreedyAgent

class SoftmaxAgent(MFRLA):
    def decide(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            self.raise_no_possible_actions_error()
        dist = [(exp(self.get_Q(s, a)), a) for a in actions]
        return self.__choose_by_weight(dist)

    def __choose_by_weight(self, dist):
        '''
        dist: list of (weight, key), key without repetition
        '''
        choice = random.random() * sum([w for w, k in dist])
        best = max(dist)
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

    def observe(self, s, a, s_, R):
        self.update_Q(s, a, s_, R)

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

########################
# Deep Q Learning Part #
########################

class DeepQNetwork:
    pass

class DeepQLearningAgent(MFRLA):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = DeepQNetwork()

    def get_Q(self, s, a):
        return self.Q.query(s, a)
        
DQLA = DeepQLearningAgent

class NaiveDeepQLearningAgent(DQLA):
    def observe(self, s, a, s_, R):
        self.update_Q(s, a, s_, R)

    def update_Q(self, s, a, s_, R):
        self.Q.update(s, a, s_, R)

NDQLA = NaiveDeepQLearningAgent

class ExperienceReplayAgent(DQLA):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.experience = list()

    def observe(self, s, a, s_, R):
        not_defined  # TODO: not_defined
        
    def update_Q(self, s, a, s_, R):
        not_defined  # TODO: not_defined
        
ERA = ExperienceReplayAgent
    
class FixedQTargetsAgent(DQLA):
    def __init__(self, C, **kwargs):
        super().__init__(**kwargs)
        self.Q_target = self.Q.deepcopy()
        self.C = C
        self.step_counter = 0  # Every C step, set Q_target = Q

    def observe(self, s, a, s_, R):  # save experience
        not_defined  # TODO: not_defined
    
    def learn(self):
        not_defined  # TODO: not_defined

    def update_Q(self, s, a, s_, R):
        not_defined  # TODO: not_defined

FQTA = FixedQTargetsAgent

