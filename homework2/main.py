from maze_env import Maze
from RL_brain import Agent
from Dyna_Q_agent_plot import *
import time

# set random seed
i = 1
np.random.seed(i)
# python random lib
random.seed(i)

UNIT = 40
MAZE_H = 6  # MAZE的高
MAZE_W = 6  # MAZE的宽
STATE_FOUND = 2  # 一共有找到treasure和没有找到treasure两种状态

# hyper-parameter.
EPISODES = 50
SLEEP_TIME = 0.01
N = 1500

if __name__ == "__main__":

    env = Maze()
    state_size = 5
    action_size = env.n_actions
    # initialize Q-table and model
    Q = Q_tabel(MAZE_H, MAZE_W, STATE_FOUND, action_size)
    M = model()
    # start training
    for episode in range(EPISODES):
        s = env.reset()
        episode_reward = 0
        while True:
            env.render()  # You can comment all render() to turn off the graphical interface in training process to accelerate your code.
            time.sleep(SLEEP_TIME)
            # get action for the current state
            if len(s) < state_size:
                s.append(False)
            a = Q.get_action(s)
            # take the action in the env, obtain the next state
            s_, r, done = env.step(a)
            # print("(s_x: ", int(s[0] - 5) // UNIT, " s_y:", int(s[1] - 5) // UNIT, ") |(s'_x:", int(s_[0] - 5) // UNIT,
            #       " s'_y:", int(s_[1] - 5) // UNIT, ") |found: ", int(s[-1]), " |reward:", r, " |action:", a)
            # update score value
            episode_reward += r
            # update Q-table
            Q.update(state=s, action=a, state_=s_, reward=r)
            # store the (s', r) in Model(s, a)
            M.store(state=s, action=a, state_=s_, reward=r)
            # go to the next state
            s = s_
            # Repeat N times:
            for _ in range(N):
                # randomly select previously observed state, action and their corresponding next state and reward
                state, action, state_, reward = M.sample()
                # use the memory to update Q-table
                Q.update(state=state, action=action, state_=state_, reward=reward)

            if done:
                env.render()
                time.sleep(SLEEP_TIME)
                break
        # decay alpha and epsilon per episode
        Q.decay_alhpa()
        Q.decay_epsilon()
        print('episode:', episode, '  |episode_reward:', episode_reward)

    print('\ntraining over\n')
    Q.plot_Q()
