from agent import *
from MaX import *
from MaxWithNp import *
from game import ChineseChecker
from hyperparamSelect import *
import datetime
import tkinter as tk
from UI import GameBoard
import time

resBoard = {(1, 1): 1,
            (2, 1): 3, (2, 2): 3,
            (3, 1): 1, (3, 2): 3, (3, 3): 1,
            (4, 1): 1, (4, 2): 0, (4, 3): 1, (4, 4): 0,
            (5, 1): 0, (5, 2): 0, (5, 3): 0, (5, 4): 0, (5, 5): 0,
            (6, 1): 0, (6, 2): 0, (6, 3): 0, (6, 4): 0, (6, 5): 0, (6, 6): 0,
            (7, 1): 0, (7, 2): 0, (7, 3): 0, (7, 4): 0, (7, 5): 0, (7, 6): 0, (7, 7): 0,
            (8, 1): 1, (8, 2): 0, (8, 3): 0, (8, 4): 0, (8, 5): 0, (8, 6): 0, (8, 7): 0, (8, 8): 0,
            (9, 1): 0, (9, 2): 0, (9, 3): 0, (9, 4): 0, (9, 5): 1, (9, 6): 0, (9, 7): 0, (9, 8): 0, (9, 9): 0,
            (10, 1): 0, (10, 2): 0, (10, 3): 0, (10, 4): 0, (10, 5): 0, (10, 6): 0, (10, 7): 0, (10, 8): 0, (10, 9): 0,
            (10, 10): 0,
            (11, 1): 0, (11, 2): 0, (11, 3): 0, (11, 4): 0, (11, 5): 0, (11, 6): 0, (11, 7): 0, (11, 8): 2, (11, 9): 0,
            (12, 1): 0, (12, 2): 0, (12, 3): 0, (12, 4): 0, (12, 5): 0, (12, 6): 0, (12, 7): 0, (12, 8): 0,
            (13, 1): 0, (13, 2): 0, (13, 3): 0, (13, 4): 0, (13, 5): 0, (13, 6): 0, (13, 7): 0,
            (14, 1): 0, (14, 2): 0, (14, 3): 0, (14, 4): 0, (14, 5): 0, (14, 6): 0,
            (15, 1): 0, (15, 2): 0, (15, 3): 0, (15, 4): 0, (15, 5): 0,
            (16, 1): 0, (16, 2): 2, (16, 3): 2, (16, 4): 2,
            (17, 1): 2, (17, 2): 4, (17, 3): 2,
            (18, 1): 4, (18, 2): 4,
            (19, 1): 2}


def continueGame(ccgame, agents, max_iter):
    global continue_to_play, iter, state
    if not continue_to_play:
        continue_to_play = True
        buttonStr.set("stop")
        while (not ccgame.isEnd(state, iter)) and iter < max_iter and continue_to_play:
            iter += 1
            messagevar.set("iter: %d" % iter)
            board.board = state[1]
            board.draw()
            board.update_idletasks()
            board.update()

            player = ccgame.player(state)
            agent = agents[player]
            # function agent.getAction() modify class member action
            agent.getAction(state)
            legal_actions = ccgame.actions(state)
            if agent.action not in legal_actions:  # check if the action of agent is legal
                agent.action = random.choice(legal_actions)
            state = ccgame.succ(state, agent.action)
        board.board = state[1]
        board.draw()
        board.update_idletasks()
        board.update()
        time.sleep(0.1)
        if ccgame.isEnd(state, iter):
            print("player%d win the game in iter[%d]" % (state[1].isEnd(iter)[1], iter))  # return winner
            messagevar.set("player%d win the game in iter[%d]" % (state[1].isEnd(iter)[1], iter))  # return winner
        elif iter >= max_iter:  # stuck situation
            print('stuck!')
            messagevar.set('stuck!')
            B.destroy()

    else:
        continue_to_play = False
        buttonStr.set("continue")


def runStepsGame(ccgame, agents, max_iter):
    global continue_to_play, iter, state
    steps = int(stepvar.get())
    step = 0
    if continue_to_play:
        continue_to_play = False
        buttonStr.set("continue")
    else:
        while (not ccgame.isEnd(state, iter)) and iter < max_iter and step < steps:
            iter += 1
            step += 1
            messagevar.set("iter: %d" % iter)
            board.board = state[1]
            board.draw()
            board.update_idletasks()
            board.update()

            player = ccgame.player(state)
            agent = agents[player]
            # function agent.getAction() modify class member action
            agent.getAction(state)
            legal_actions = ccgame.actions(state)
            if agent.action not in legal_actions:  # check if the action of agent is legal
                agent.action = random.choice(legal_actions)
            state = ccgame.succ(state, agent.action)
        board.board = state[1]
        board.draw()
        board.update_idletasks()
        board.update()
        time.sleep(0.1)
        if ccgame.isEnd(state, iter):
            print("player%d win the game in iter[%d]" % (state[1].isEnd(iter)[1], iter))  # return winner
            messagevar.set("player%d win the game in iter[%d]" % (state[1].isEnd(iter)[1], iter))  # return winner
        elif iter >= max_iter:  # stuck situation
            print('stuck!')
            messagevar.set('stuck!')
            B.destroy()


def runGame(ccgame, agents):
    state = ccgame.startState()
    print(state)
    max_iter = 100  # deal with some stuck situations
    iter = 0
    start = datetime.datetime.now()
    while (not ccgame.isEnd(state, iter)) and iter < max_iter:
        iter += 1
        board.board = state[1]
        board.draw()
        board.update_idletasks()
        board.update()

        player = ccgame.player(state)
        agent = agents[player]
        # function agent.getAction() modify class member action
        agent.getAction(state)
        legal_actions = ccgame.actions(state)
        if agent.action not in legal_actions:  # check if the action of agent is legal
            agent.action = random.choice(legal_actions)
        state = ccgame.succ(state, agent.action)
    board.board = state[1]
    board.draw()
    board.update_idletasks()
    board.update()
    time.sleep(0.1)

    end = datetime.datetime.now()
    if ccgame.isEnd(state, iter):
        return state[1].isEnd(iter)[1]  # return winner
    else:  # stuck situation
        print('stuck!')
        return 0


def simulateMultipleGames(agents_dict, simulation_times, ccgame):
    win_times_P1 = 0
    win_times_P2 = 0
    tie_times = 0
    utility_sum = 0
    for i in range(simulation_times):
        run_result = runGame(ccgame, agents_dict)
        print(run_result)
        if run_result == 1:
            win_times_P1 += 1
        elif run_result == 2:
            win_times_P2 += 1
        elif run_result == 0:
            tie_times += 1
        print('game', i + 1, 'finished', 'winner is player ', run_result)
    print('In', simulation_times, 'simulations:')  # 模拟的次数
    print('winning times: for player 1 is ', win_times_P1)  # player 1 赢的次数
    print('winning times: for player 2 is ', win_times_P2)  # player 2 赢的次数
    print('Tie times:', tie_times)  # 平局的次数


def callback(ccgame):
    B.destroy()
    simpleGreedyAgent1 = SimpleGreedyAgent(ccgame)
    simpleGreedyAgent2 = SimpleGreedyAgent(ccgame)
    randomAgent = RandomAgent(ccgame)
    teamAgent = TeamNameMinimaxAgent(ccgame)
    simulateMultipleGames({1: teamAgent, 2: simpleGreedyAgent2}, 1, ccgame)


if __name__ == '__main__':
    ccgame = ChineseChecker(10, 4)
    root = tk.Tk()
    board = GameBoard(root, ccgame.size, ccgame.size * 2 - 1, ccgame.board)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    messagevar = tk.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
    messagevar.set("")
    l = tk.Label(board, textvariable=messagevar, bg='green', fg='white', font=('Arial', 15), width=30, height=2)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    l.place(x=500, y=50)

    continue_to_play = False
    # state = ccgame.startState(resBoard, True)
    state = ccgame.startState()
    print(state)
    max_iter = 100  # deal with some stuck situations
    iter = 0
    buttonStr = tk.StringVar()
    buttonStr.set("Start")

    Agent0 = SimpleGreedyAgent(ccgame)
    Agent1 = OurSimpleGreedyAgent3(ccgame)
    Agent2 = OurSimpleGreedyAgent7(ccgame)
    Agent3 = OurSimpleGreedyAgent9(ccgame, [1, 1, 1, 1])
    Agent5 = OurSimpleGreedyAgentBO(ccgame)

    agents = {1: Agent0, 2: Agent2}

    B = tk.Button(board, textvariable=buttonStr,
                  command=lambda: continueGame(ccgame=ccgame, agents=agents,
                                               max_iter=max_iter))
    B.place(x=620, y=130)

    stepvar = tk.StringVar()
    entryStep = tk.Entry(board, textvariable=stepvar, font=('Arial', 15), width=3)
    entryStep.place(x=610, y=180)

    S = tk.Button(board, text="run steps",
                  command=lambda: runStepsGame(ccgame=ccgame, agents=agents,
                                               max_iter=max_iter))
    S.place(x=660, y=180)
    root.mainloop()
