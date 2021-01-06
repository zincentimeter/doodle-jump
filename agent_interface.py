import random
import numpy as np
import agent_base_classes
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



# # NOTE: Testing in Programming Assignment ONLY!!!!!!!!!!!!!!!!!
# class QLearningAgentDemo(ModelFreeReinforcementLearningAgent):
#     def __init__(self, alpha, **kwargs):
#         super().__init__(**kwargs)
#         self.alpha = alpha
#         # self.Q = util.Counter()
#         self.Q = np.zeros((X, Y, T))

#     def get_Q(self, s, a):
#         if not (s, a) in self.Q.keys():
#             self.Q[s, a] = 0
#         return self.Q[s, a]

#     def update_Q(self, s, a, s_, R):
#         Q_sample = R + self.gamma * self.get_V(s_)
#         diff = Q_sample - self.Q[s, a]
#         self.Q[s, a] += (self.alpha * diff)

#     def get_V_opt_a(self, s):
#         actions = self.get_possible_actions(s)
#         if 0 == len(actions):
#             return (0, None)
#         return max([(self.get_Q(s, a), a) for a in actions])

#     def get_possible_actions(self, s):
#         return ReinforcementAgent.getLegalActions(self, s)

#     def get_random_action(self, s):
#         actions = self.get_possible_actions(s)
#         if 0 == len(actions):
#             return None
#         return random.sample(actions, 1)

#     # NOTE: Testing in Programming Assignment ONLY!!!!!!!!!!!!!!!!!


# class MyAgent(EpsilonGreedyAgent, QLearningAgentDemo):
#     def __init__(self, **args):
#         EpsilonGreedyAgent.__init__(self, **args)
#         QLearningAgentDemo.__init__(self, **args)
#         # ReinforcementAgent.__init__(self, **args)

#     def getQValue(self, s, a):
#         return self.get_Q(s, a)

#     def computeValueFromQValues(self, s):
#         return self.get_V(s)

#     def computeActionFromQValues(self, s):
#         return self.get_optimal_action(s)

#     def getAction(self, s):
#         return self.decide(s)

#     def update(self, s, a, s_, R):
#         self.update_Q(s, a, s_, R)

#     def getPolicy(self, state):
#         return self.computeActionFromQValues(state)

#     def getValue(self, state):
#         return self.computeValueFromQValues(state)


# if __name__ == "__main__":
#     from Log2Dict import *
#     from destination import *

#     while (True):
#         input_dict = logToDict()
#         # input(input_dict)
#         agent = ClassicalQLearningAgent(alpha=0.02, gamma=0.02)
#         action = agent.get_optimal_action(input_dict)
#         destinationY = desample(action[0])[1]
#         output(input_dict, desample(action[0])[1])

