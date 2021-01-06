# uncompyle6 version 3.4.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.6 |Anaconda, Inc.| (default, Aug 26 2018, 21:41:56) 
# [GCC 7.3.0]
# Embedded file name: /Users/yuegao/Downloads/code_new-1/code_new/game.py
# Compiled at: 2018-09-29 21:37:24
# Size of source mod 2**32: 1766 bytes
from board import Board
import copy

class ChineseChecker(object):

    def __init__(self, size, piece_rows):  # size = 10, piece_rows = 4
        self.size = size
        self.piece_rows = piece_rows
        self.board = Board(self.size, self.piece_rows)

    def startState(self, resBoard=None, res=False):
        self.board = Board(self.size, self.piece_rows, resBoard, res)
        return (
         1, self.board)  # represent (current player, current board)

    def resState(self, resBoard):
        self.board = self.board.makeBoard(resBoard)
        return 1, self.board

    def isEnd(self, state, iter):
        return state[1].isEnd(iter)[0]  # state[1] represents self.board, .isEnd(iter)[0] return True or False

    def actions(self, state):
        action_list = []
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)  # get a list of pos that player's pieces occur
        for pos in player_piece_pos_list:
            for adj_pos in board.adjacentPositions(pos):
                if board.isEmptyPosition(adj_pos):
                    action_list.append((pos, adj_pos))

        for pos in player_piece_pos_list:
            boardCopy = copy.deepcopy(board)
            boardCopy.board_status[pos] = 0
            for new_pos in boardCopy.getAllHopPositions(pos):
                if (
                 pos, new_pos) not in action_list:
                    action_list.append((pos, new_pos))

        return action_list

    def player(self, state):
        return state[0]

    def succ(self, state, action):
        player = state[0]
        board = copy.deepcopy(state[1])
        #assert board.board_status[action[0]] == player
        #assert board.board_status[action[1]] == 0
        board.board_status[action[1]] = board.board_status[action[0]]
        board.board_status[action[0]] = 0
        return (
         3 - player, board)  # players take turns by 3 - 1 = 2 or 3 - 2 = 1
# okay decompiling game.pyc
