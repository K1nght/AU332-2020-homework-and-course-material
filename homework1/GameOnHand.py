from agent import *
from MaX import *
from hyperparamSelect import *
from game import ChineseChecker
import datetime
import tkinter as tk
from UI import GameBoard
import time


def runGame(ccgame, agent, max_iter):
    global continue_to_play, iter, state

    iter += 1
    board.board = state[1]
    board.draw()
    board.update_idletasks()
    board.update()

    pos = (int(PosRowvar.get()), int(PosColvar.get()))
    new_pos = (int(NewPosRowvar.get()), int(NewPosColvar.get()))
    playerAction = (pos, new_pos)
    legal_actions = ccgame.actions(state)
    if playerAction in legal_actions:
        state = ccgame.succ(state, playerAction)
    else:
        messagevar.set("Your action:" + str(playerAction[0]) + "->" + str(playerAction[1]) + "is illegal!")
        return
    board.board = state[1]
    board.draw()
    board.update_idletasks()
    board.update()
    time.sleep(0.1)

    agent.getAction(state)
    legal_actions = ccgame.actions(state)
    if agent.action not in legal_actions:  # check if the action of agent is legal
        agent.action = random.choice(legal_actions)
    state = ccgame.succ(state, agent.action)
    messagevar.set("iter: %d, the computer goes " % iter + str(agent.action[0]) + "->" + str(agent.action[1]))
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


if __name__ == '__main__':
    ccgame = ChineseChecker(10, 4)
    root = tk.Tk()
    board = GameBoard(root, ccgame.size, ccgame.size * 2 - 1, ccgame.board)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    messagevar = tk.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
    messagevar.set("")
    l = tk.Label(board, textvariable=messagevar, bg='green', fg='white', font=('Arial', 15), width=40, height=2)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    l.place(x=470, y=100)

    continue_to_play = False
    state = ccgame.startState()
    print(state)
    max_iter = 100  # deal with some stuck situations
    iter = 0

    simpleGreedyAgent1 = OurSimpleGreedyAgent7(ccgame)
    simpleGreedyAgent2 = OurSimpleGreedyAgent3(ccgame)
    simpleGreedyAgent3 = OurSimpleGreedyAgent9(ccgame, [4.592610285885809,4.571414918394476,4.1524472708189855,3.887514780700033])
    randomAgent = RandomAgent(ccgame)
    teamAgent = TeamNameMinimaxAgent(ccgame)

    PosRowvar = tk.StringVar()
    PosColvar = tk.StringVar()
    NewPosRowvar = tk.StringVar()
    NewPosColvar = tk.StringVar()
    entryPosRow = tk.Entry(board, textvariable=PosRowvar, font=('Arial', 15), width=3)
    entryPosCol = tk.Entry(board, textvariable=PosColvar, font=('Arial', 15), width=3)
    entryNewPosRow = tk.Entry(board, textvariable=NewPosRowvar, font=('Arial', 15), width=3)
    entryNewPosCol = tk.Entry(board, textvariable=NewPosColvar, font=('Arial', 15), width=3)
    entryPosRow.place(x=670, y=185)
    entryPosCol.place(x=800, y=185)
    entryNewPosRow.place(x=670, y=250)
    entryNewPosCol.place(x=800, y=250)

    PosRowL = tk.Label(board, text="Pos: Row", font=('Arial', 12), width=13, height=2)
    PosColL = tk.Label(board, text="Col", font=('Arial', 12), width=5, height=2)
    NewPosRowL = tk.Label(board, text="New Pos: Row", font=('Arial', 12), width=13, height=2)
    NewPosColL = tk.Label(board, text="Col", font=('Arial', 12), width=5, height=2)
    PosRowL.place(x=510, y=180)
    PosColL.place(x=740, y=180)
    NewPosRowL.place(x=510, y=240)
    NewPosColL.place(x=740, y=240)

    S = tk.Button(board, text="go",
                  command=lambda: runGame(ccgame=ccgame, agent=simpleGreedyAgent3,
                                          max_iter=max_iter), font=('Arial', 15), width=8, height=2)
    S.place(x=630, y=300)
    root.mainloop()
