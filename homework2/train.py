from maze_env import Maze
from RL_brain import Agent
from Dyna_Q_agent import *
import time

UNIT = 40
MAZE_H = 6       # MAZE的高
MAZE_W = 6       # MAZE的宽
STATE_FOUND = 2  # 一共有找到treasure和没有找到treasure

# hyper-parameter.
EPISODES = 50
SLEEP_TIME = 0.01
N = 1500

if __name__ == "__main__":
    ### START CODE HERE ###
    # This is an agent with random policy. You can learn how to interact with the environment through the code below.
    # Then you can delete it and write your own code.

    for i in range(10):
        np.random.seed(i)
        # python random lib
        random.seed(i)

        env = Maze()
        state_size = 5
        action_size = env.n_actions

        Q = Q_tabel(MAZE_H, MAZE_W, STATE_FOUND, action_size)
        M = model()
        for episode in range(EPISODES):
            s = env.reset()
            episode_reward = 0
            while True:
                # env.render()  # You can comment all render() to turn off the graphical interface in training process to accelerate your code.
                # time.sleep(SLEEP_TIME)
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

                Q.update(state=s, action=a, state_=s_, reward=r)
                M.store(state=s, action=a, state_=s_, reward=r)
                # go to the next state
                s = s_
                for _ in range(N):
                    state, action, state_, reward = M.sample()
                    Q.update(state=state, action=action, state_=state_, reward=reward)

                if done:
                    # env.render()
                    # time.sleep(SLEEP_TIME)
                    break

            Q.decay_alhpa()
            Q.decay_epsilon()
            print('seed:', i, '  |episode:', episode, '  |episode_reward:', episode_reward)

    ### END CODE HERE ###

    print('\ntraining over\n')
