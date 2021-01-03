class QLearningAgent(ModelFreeReinforcementLearningAgent):
    pass

class DeepQlearningAgent(ModelFreeReinforcementLearningAgent):
    pass

class ModelFreeReinforcementLearningAgent:

    def __init__(self):
        pass

    def decide(self, s):
        pass

    def get_Q(self, s, a):
        pass

    def get_V(self, s):
        pass

    def update_Q(self, s, a, s_, R):
        pass

    def __get_argmax_action_wrt_Q():
        pass
    