from agent import *
from MaX import *
from game import ChineseChecker
import datetime
import tkinter as tk
from UI import GameBoard
import time


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
        return state[1].isEnd(iter)[1], iter  # return winner
    else:  # stuck situation
        print('stuck!')
        return 0, max_iter


def simulateMultipleGames(agents_dict, simulation_times, ccgame):
    win_times_P1 = 0
    avg_iter_P1 = []
    win_times_P2 = 0
    avg_iter_P2 = []
    tie_times = 0
    utility_sum = 0
    for i in range(simulation_times):
        run_result, Oneiter = runGame(ccgame, agents_dict)
        print(run_result)
        if run_result == 1:
            win_times_P1 += 1
            avg_iter_P1.append(Oneiter)
        elif run_result == 2:
            win_times_P2 += 1
            avg_iter_P2.append(Oneiter)
        elif run_result == 0:
            tie_times += 1
        print('game', i + 1, 'finished', 'winner is player ', run_result)
    print('In', simulation_times, 'simulations:')  # 模拟的次数
    print('winning times: for player 1 is ', win_times_P1,
          ('in avg iter[%d]' % (sum(avg_iter_P1) / win_times_P1)) if win_times_P1 else '')  # player 1 赢的次数
    print('winning times: for player 2 is ', win_times_P2,
          ('in avg iter[%d]' % (sum(avg_iter_P2) / win_times_P2)) if win_times_P2 else '')  # player 2 赢的次数
    print('Tie times:', tie_times)  # 平局的次数


def callback(ccgame):
    B.destroy()
    Agent1 = SimpleGreedyAgent(ccgame)
    Agent2 = OurSimpleGreedyAgent5(ccgame)
    Agent3 = OurSimpleGreedyAgent6(ccgame)
    our = BIEJUANLE(ccgame)
    simulateMultipleGames({1: Agent2, 2: our}, 100, ccgame)


if __name__ == '__main__':
    ccgame = ChineseChecker(10, 4)
    root = tk.Tk()
    board = GameBoard(root, ccgame.size, ccgame.size * 2 - 1, ccgame.board)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    B = tk.Button(board, text="Start", command=lambda: callback(ccgame=ccgame))
    B.pack()
    root.mainloop()
