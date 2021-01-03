import numpy as np
from math import ceil


dx, dy = 50, 50
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)
T = 10


def relative_pos(a, b):
    return (a[0]-b[0], a[1]-b[1])

class ModelFreeReinforcementLearningAgent:
    def __init__(self, gamma, **kwargs):
        self.gamma = kwargs['gamma']
        
    def decide(self, s):
        abstract

    def get_Q(self, s, a):
        abstract

    def update_Q(self, s, a, s_, R):
        abstract

    def get_possible_actions(self, s):
        p0 = s['agent_pos']
        actions = list()
        for board in s['boards']:
            p, t = board[:2]
            actions.append((trunc(relative_pos(p,p0)), t))
            # TODO: Truncate position to integer
        return actions

    def get_V_opt_a(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            input('Warning! No possible action!')
        return max([(self.get_Q(s,a),a) for a in actions])

    def get_V(self, s):
        return get_V_opt_a(self, s)[0]

    def __get_optimal_action(self, s):
        return get_V_opt_a(self, s)[1]
    

class EpsilonGreedyAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.epsilon = kwargs['epsilon']

    def decide(self, s):
        pass

class SoftmaxAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, epsilon, **kwargs):
        super().__init__(**kwargs)

    def decide(self, s):
        pass


class ClassicalQLearningAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = kwargs['alpha']
        self.Q = np.zeros((X,Y,T))
   
    def get_Q(self, s, a):
        (x, y), t = a
        return self.Q[x, y, t]

    def update_Q(self, s, a, s_, R):
        (x, y), t = a
        Q_ = R + self.gamma * self.get_V(s_)
        diff = Q_ - self.self.Q[x, y, t]
        self.Q[x, y, t] += (self.alpha * diff)


class DeepQlearningAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = kwargs['alpha']
        self.Q = None

    def get_Q(self, s, a):
        pass

    def update_Q(self, s, a, s_, R):
        pass


class MyAgent(EpsilonGreedyAgent, ClassicalQLearningAgent):
    def __init__(self, alpha=2345, gamma=2134):
        pass
