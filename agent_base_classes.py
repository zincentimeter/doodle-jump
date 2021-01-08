import random
import numpy as np
from math import ceil, exp, trunc
from utils import *


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
        dist = [(exp(self.get_Q(s, a)/100), a) for a in actions]
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
        return self.Q

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
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class DeepQNetwork(nn.Module):
    # def __init__(self, h, w, outputs):
    #     super(DQN, self).__init__()
    #     self.conv1 = nn.Conv2d(3, 16, kernel_size=5, stride=2)
    #     self.bn1 = nn.BatchNorm2d(16)
    #     self.conv2 = nn.Conv2d(16, 32, kernel_size=5, stride=2)
    #     self.bn2 = nn.BatchNorm2d(32)
    #     self.conv3 = nn.Conv2d(32, 32, kernel_size=5, stride=2)
    #     self.bn3 = nn.BatchNorm2d(32)
    #     # Linear
    # def forward(self, x):
    #     x = F.relu(self.bn1(self.conv1(x)))
    #     x = F.relu(self.bn2(self.conv2(x)))
    #     x = F.relu(self.bn3(self.conv3(x)))
    #     return self.head(x.view(x.size(0), -1))
    def __init__(self, dim_state=4*30, dim_action=2):
        super(DeepQNetwork, self).__init__()
        self.fc1 = nn.Linear(dim_state, 50)
        self.fc1.weight.data.normal_(0, 0.1)
        # self.fc2 = nn.Linear(50, 50)
        # self.fc2.weight.data.normal_(0, 0.1)
        self.out = nn.Linear(50, dim_action)
        self.out.weight.data.normal_(0, 0.1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = F.relu(self.out(x))
        return x



class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = list()
        self.head = 0

    def push(self, transition):
        if len(self.memory) < self.capacity:
            self.memory.append(transition)
        else:
            self.memory[self.head] = transition
        self.head = (self.head + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def is_full(self):
        return len(self.memory) == self.capacity


class DeepQLearningAgent(MFRLA):
    def __init__(self, alpha, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = DeepQNetwork().to(DEVICE)

    def learn(self):
        abstract

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
        self.exp = self.ReplayMemory(10000)

    def observe(self, s, a, s_, R):
        transition = (s, a, s_, R)
        self.exp.push(transition)

    def learn(self):
        not_defined  # TODO: not_defined
        
    def update_Q(self, s, a, s_, R):
        not_defined  # TODO: not_defined
        
ERA = ExperienceReplayAgent
    
class FixedQTargetsAgent(DQLA):
    def __init__(self, C, **kwargs):
        super().__init__(**kwargs)
        self.C = C  # Every C step, set Q_target = Q
        self.step_counter = 0  
        self.Q_target = DeepQNetwork().to(DEVICE)
        self.Q_target.load_state_dict(self.Q.state_dict()).eval()

    def observe(self, s, a, s_, R):  # save experience
        not_defined  # TODO: not_defined
    
    def learn(self):
        not_defined  # TODO: not_defined

    def update_Q(self, s, a, s_, R):
        not_defined  # TODO: not_defined

FQTA = FixedQTargetsAgent