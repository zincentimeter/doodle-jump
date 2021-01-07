import random
import numpy as np
from math import ceil, exp, trunc
from utils import *
from collections import namedtuple


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

    def get_Q_a_list(self, s):
        abstact

    def get_possible_actions(self, s):  # inplemented in Interface
        abstract

    def raise_no_possible_actions_error(self):
        input('Warning! No possible action!\nPress ENTER to continue...')
        # TODO: Need to do something when nothing is given.

    def get_V_opt_a(self, s):
        return max(self.get_Q_a_list(s))

    def get_V(self, s):
        return self.get_V_opt_a(s)[0]

    def get_optimal_action(self, s):
        return self.get_V_opt_a(s)[1]

MFRLA = ModelFreeReinforcementLearningAgent


class EpsilonGreedyAgent(MFRLA):
    def __init__(self, epsilon, eps_decay=None, eps_end=None, **kwargs):
        super().__init__(**kwargs)
        self.epsilon = epsilon
        if eps_decay:
            self.eps_decay = eps_decay
        if eps_end:
            self.eps_end = eps_end

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
        dist = self.get_Q_a_list(s)
        dist = [(exp(Q), a) for Q, a in dist]
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
        Q_sample = R + self.gamma * self.get_V(s_)
        diff = Q_sample - self.get_Q(s, a)
        self.Q[s, a] += (self.alpha * diff)

    def get_Q(self, s, a):
        try:
            return self.Q[s, a]
        except KeyError:
            default = 0  # or at random
            self.Q[s, a] = default
            return default

    def get_Q_a_list(self, s):
        actions = self.get_possible_actions(s)
        if 0 == len(actions):
            self.raise_no_possible_actions_error()
        return [(self.get_Q(s, a), a) for a in actions]

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
    def __init__(self, dim_state, dim_action):
        super(DeepQNetwork, self).__init__()
        self.fc1 = nn.Linear(dim_state, 60)
        self.fc1.weight.data.normal_(0, 0.1)
        self.fc2 = nn.Linear(60, 30)
        self.fc2.weight.data.normal_(0, 0.1)
        self.out = nn.Linear(30, dim_action)
        self.out.weight.data.normal_(0, 0.1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
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

    def __len__(self):
        return len(self.memory)


Transition = namedtuple('Transition', ('s', 'a', 's_', 'R'))


class ExperienceReplayAgent(DQLA):
    def __init__(self, alpha, C, batch_size, dim_state=4*10*3, dim_action=2, **kwargs):
        super().__init__(**kwargs)
        self.alpha = alpha
        self.Q = DeepQNetwork(dim_state, dim_action).to(DEVICE)
        self.step_counter = 0  
        self.C = C  # Every C step, set Q_target = Q
        self.batch_size = batch_size
        self.Q_target = DeepQNetwork(dim_state, dim_action).to(DEVICE)
        self.Q_target.load_state_dict(self.Q.state_dict())
        self.Q_target.eval()
        self.exp = ReplayMemory(10000)
        self.optimizer = optim.RMSprop(self.Q.parameters())

    def enter_new_episode(self):
        self.step_counter += 1
        if not (self.step_counter % self.C):
            self.Q_target.load_state_dict(self.Q.state_dict())
        
    def observe(self, s, a, s_, R):
        transition = Transition(s, a, s_, R)
        self.exp.push(transition)
        self.learn()

    def learn(self):
        if len(self.exp) < self.batch_size:
            return
        transitions = self.exp.sample(self.batch_size)
        minibatch = Transition(*zip(*transitions))
        s = torch.cat(minibatch.s)
        a = torch.cat(minibatch.a)
        s_ = torch.cat(minibatch.s_)
        R = torch.cat(minibatch.R)
        Q = self.Q(s).gather(1, a)
        V_s_ = self.Q_target(s_).max(1)[0].detach()
        Q_sample = (R + self.gamma * V_s_).unsqueezze(1)
        loss = F.smooth_l1_loss(Q_sample, Q)
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.Q.parameters():
            param.grad.data.clamp(-1,1)
        self.optimizer.step()

    def get_Q(self, s, a):
        return self.get_Q_a_list(s)[a][0]

    def get_Q_a_list(self, s):
        with torch.no_grad():
            y = self.Q(s)
        return [(q.item(), i) for i, q in enumerate(y[0])]

ERA = ExperienceReplayAgent