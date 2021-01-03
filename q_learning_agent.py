import random
import numpy as np
from math import ceil, exp

SCREEN_SIZE = (1920, 1080)
dx, dy = 50, 50
W, H = SCREEN_SIZE
X, Y = ceil(W / dx), ceil(H / dy)
T = 10


def relative_pos(a, b):
    return (a[0]-b[0], a[1]-b[1])

class ModelFreeReinforcementLearningAgent:
    def __init__(self, gamma, **kwargs):
        self.gamma = gamma
        if kwargs:
            input(f'Warning! Some arguments unused: {kwargs.keys()}\nPress ENTER to continue...')
        
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
            input('Warning! No possible action!\nPress ENTER to continue...')  
            # TODO: Need to do something when nothing is given.
        return max([(self.get_Q(s,a),a) for a in actions])

    def get_V(self, s):
        return self.get_V_opt_a(s)[0]

    def get_optimal_action(self, s):
        return self.get_V_opt_a(s)[1]
    

class EpsilonGreedyAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, epsilon, **kwargs):
        super().__init__(**kwargs)
        self.epsilon = epsilon

    def decide(self, s):
        if random.random() < self.epsilon:
            return self.get_random_action(s)
        else:
            return self.get_optimal_action(s)

    def get_random_action(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            input('Warning! No possible action!\nPress ENTER to continue...')
            # # TODO: Need to do something when nothing is given.
        return random.choice(actions)


class SoftmaxAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def decide(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            input('Warning! No possible action!\nPress ENTER to continue...')
            # # TODO: Need to do something when nothing is given.
        dist = [(exp(self.get_Q(s,a)),a) for a in actions]
        best = max(dist)
        choice = random.random() * sum([expQ for expQ,a in dist])
        choice -= best[0]
        if choice < 0:
            return best[1]
        for expQ,a in dist:
            if (expQ,a) == best:
                continue
            choice -= expQ
            if choice < 0:
                return a
        return dist[-1][1]


class ClassicalQLearningAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = np.zeros((X,Y,T))
   
    def get_Q(self, s, a):
        (x, y), t = a
        return self.Q[x, y, t]

    def update_Q(self, s, a, s_, R):
        (x, y), t = a
        Q_sample = R + self.gamma * self.get_V(s_)
        diff = Q_sample - self.Q[x, y, t]
        self.Q[x, y, t] += (self.alpha * diff)


class DeepQlearningAgent(ModelFreeReinforcementLearningAgent):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = None

    def get_Q(self, s, a):
        pass

    def update_Q(self, s, a, s_, R):
        pass


# NOTE: Testing in Programming Assignment ONLY!!!!!!!!!!!!!!!!!
class QLearningAgentDemo(ModelFreeReinforcementLearningAgent):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = util.Counter()
   
    def get_Q(self, s, a):
        if not (s,a) in self.Q.keys():
            self.Q[s, a] = 0
        return self.Q[s, a]

    def update_Q(self, s, a, s_, R):
        Q_sample = R + self.gamma * self.get_V(s_)
        diff = Q_sample - self.Q[s, a]
        self.Q[s, a] += (self.alpha * diff)
        
    def get_V_opt_a(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            return (0, None)
        return max([(self.get_Q(s,a),a) for a in actions])

    def get_possible_actions(self, s):
        return ReinforcementAgent.getLegalActions(self, s)
    
    def get_random_action(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            return None
        return random.sample(actions, 1)    
        

# NOTE: Testing in Programming Assignment ONLY!!!!!!!!!!!!!!!!!
class MyAgent(EpsilonGreedyAgent, QLearningAgentDemo, ReinforcementAgent):
    def __init__(self, **args):
        EpsilonGreedyAgent.__init__(self, **args)
        QLearningAgentDemo.__init__(self, **args)
        ReinforcementAgent.__init__(self, **args)

    def getQValue(self, s, a):
        return self.get_Q(s, a)

    def computeValueFromQValues(self, s):
        return self.get_V(s)

    def computeActionFromQValues(self, s):
        return self.get_optimal_action(s)

    def getAction(self, s):
        return self.decide(s)

    def update(self, s, a, s_, R):
        self.update_Q(s, a, s_, R)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    
