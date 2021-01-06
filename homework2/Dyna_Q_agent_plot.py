import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

UNIT = 40

# hyper-parameter of q table.
ALPHA = 1.0
ALPHA_MIN = 0.5
ALPHA_DECAY_STEP = 5
GAMMA = 0.9

# hyper-parameter of model.
EPSILON = 1.0
EPSILON_MIN = 0.1
EPSILON_DECAY_STEP = 5


class Q_tabel:

    def __init__(self, MAZE_H, MAZE_W, state_found, action_size):
        self.MAZE_H = MAZE_H  # MAZE的高
        self.MAZE_W = MAZE_W  # MAZE的宽
        self.action_size = action_size  # action的数量
        # initialize the Q-table
        # its dim is (state_found(2) x MAZE_H(6) x MAZE_W(6) x action_size(4))
        self.q = np.zeros((state_found, MAZE_H, MAZE_W, action_size))
        # Q-table hyper-parameter
        self.alpha = ALPHA
        self.alpha_min = ALPHA_MIN
        self.alpha_decay = (self.alpha - self.alpha_min) / ALPHA_DECAY_STEP
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = (self.epsilon - self.epsilon_min) / EPSILON_DECAY_STEP

    # update Q(s, a) by argmax(Q(s', a'))(a') and reward
    def update(self, state, action, state_, reward):
        cur_state_found = int(state[-1])
        cur_state_h = int(state[0] - 5) // UNIT
        cur_state_w = int(state[1] - 5) // UNIT
        next_state_found = int(state_[-1])
        next_state_h = int(state_[0] - 5) // UNIT
        next_state_w = int(state_[1] - 5) // UNIT
        cur_q = self.q[cur_state_found, cur_state_h, cur_state_w, action]
        # Q-learning
        RL_update = reward + self.gamma * np.amax(self.q[next_state_found, next_state_h, next_state_w, :] - cur_q)
        self.q[cur_state_found, cur_state_h, cur_state_w, action] = cur_q + self.alpha * RL_update

    # decay alpha by a step
    def decay_alhpa(self):
        if self.alpha > self.alpha_min:
            self.alpha -= self.alpha_decay

    # decay epsilon by a step
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_decay

    # epsilon-greedy method
    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            cur_state_found = int(state[-1])
            cur_state_h = int(state[0] - 5) // UNIT
            cur_state_w = int(state[1] - 5) // UNIT
            # print(state)
            # print(self.q[cur_state_found, cur_state_h, cur_state_w, :])
            # return np.argmax(self.q[cur_state_found, cur_state_h, cur_state_w, :])
            max_idx = np.argwhere(self.q[cur_state_found, cur_state_h, cur_state_w, :] == np.amax(
                self.q[cur_state_found, cur_state_h, cur_state_w, :]))
            # if there are more than one action sharing max Q-value, randomly select one of them
            return random.sample(max_idx.flatten().tolist(), 1)[0]

    # plot the policy table after finishing training
    def plot_Q(self):
        fig = plt.figure(figsize=(12,8))
        ax1, ax2 = fig.add_subplot(121, aspect='equal'), fig.add_subplot(122, aspect='equal')
        ax1.set_title("haven't found the treasure")
        ax2.set_title("have found the treasure")
        ax1.set_xlim(0, 6)
        ax1.set_ylim(0, 6)
        ax2.set_xlim(0, 6)
        ax2.set_ylim(0, 6)
        ax1.grid(True)
        ax2.grid(True)
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        for tic in ax1.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
        for tic in ax1.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
        for tic in ax2.xaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
        for tic in ax2.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
        for i in range(6):
            for j in range(6):
                q1 = self.q[0, i, 5-j, :]
                max_idx1 = np.argwhere(q1==np.amax(q1))
                action1 = random.sample(max_idx1.flatten().tolist(), 1)[0]
                q2 = self.q[1, i, 5 - j, :]
                max_idx2 = np.argwhere(q2==np.amax(q2))
                action2 = random.sample(max_idx2.flatten().tolist(), 1)[0]
                if action1 == 0:
                    ax1.add_patch(
                        patches.Arrow(i+0.5, j+0.2, 0, 0.6)
                    )
                elif action1 == 1:
                    ax1.add_patch(
                        patches.Arrow(i+0.5, j+0.8, 0, -0.6)
                    )
                elif action1 == 2:
                    ax1.add_patch(
                        patches.Arrow(i+0.2, j+0.5, 0.6, 0)
                    )
                elif action1 == 3:
                    ax1.add_patch(
                        patches.Arrow(i+0.8, j+0.5, -0.6, 0)
                    )
                if action2 == 0:
                    ax2.add_patch(
                        patches.Arrow(i+0.5, j+0.2, 0, 0.6)
                    )
                elif action2 == 1:
                    ax2.add_patch(
                        patches.Arrow(i+0.5, j+0.8, 0, -0.6)
                    )
                elif action2 == 2:
                    ax2.add_patch(
                        patches.Arrow(i+0.2, j+0.5, 0.6, 0)
                    )
                elif action2 == 3:
                    ax2.add_patch(
                        patches.Arrow(i+0.8, j+0.5, -0.6, 0)
                    )
        # for i in range(6):
        #     for j in range(6):
        #         ax1.annotate("(%d,%d)" % (i, 5-j), xy=(i+0.3, j+0.4), xytext=(i+0.3, j+0.4))
        #         ax2.annotate("(%d,%d)" % (i, 5-j), xy=(i+0.3, j+0.4), xytext=(i+0.3, j+0.4))
        plt.show()


class model:

    def __init__(self):
        # use dictionary to store the previously observed state and the action a previously taken in the state s
        # and the value is the next state s' and reward r
        self.memory = {}

    def store(self, state, action, state_, reward):
        # use tuple to store the pair (s, a):(s', r)
        self.memory[(tuple(state), action)] = (state_, reward)

    def sample(self):
        # randomly select previously observed state and action, also get their next state and reward
        s = random.sample(self.memory.items(), 1)
        state, action = s[0][0][0], s[0][0][1]
        state_, reward = s[0][1][0], s[0][1][1]
        return state, action, state_, reward

    def print_memory(self):
        # print stored pair of (s, a):(s', r)
        for s_and_a, s__and_r in self.memory.items():
            s, a = s_and_a[0], s_and_a[1]
            s_, r = s__and_r[0], s__and_r[1]
            print("(s_x: ", int(s[0] - 5) // UNIT, " s_y:", int(s[1] - 5) // UNIT, ") |(s'_x:", int(s_[0] - 5) // UNIT,
                  " s'_y:", int(s_[1] - 5) // UNIT, ") |s_found: ", int(s[-1]), " |reward:", r, " |action:", a)
