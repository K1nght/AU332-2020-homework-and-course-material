import numpy as np
import pandas as pd

class Agent:

    def __init__(self, actions):
        self.actions = actions
        self.epsilon = 1

    def choose_action(self, observation):
        action = np.random.choice(self.actions)
        return action

    ### END CODE HERE ###