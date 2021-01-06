import random, re, datetime, time, math
from MaX import *


class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        time1 = time.time()
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)
        time2 = time.time()
        print('time[%.6f]|' % (time2 - time1), 'action:', self.action, "totnums:", len(legal_actions),
              "avg time per action:%.6f" % ((time2 - time1) / len(legal_actions)))


class TeamNameMinimaxAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        ### START CODE HERE ###

        ### END CODE HERE ###


class OurSimpleGreedyAgent3(Agent):
    def __init__(self, game):
        self.target1 = [(1, 1), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.target2 = [(19, 1), (17, 1), (17, 3), (16, 1), (16, 2), (16, 3), (16, 4)]
        self.target3 = [(2, 1), (2, 2)]
        self.target4 = [(18, 1), (18, 2)]
        self.game = game
        self.totnums = 0

    def cubDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return math.sqrt(abs(pos_x - target_x)**2 + abs(pos_y - target_y)**2 + abs(pos_z - target_z)**2)

    def hexDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return max([abs(pos_x - target_x), abs(pos_y - target_y), abs(pos_z - target_z)])

    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getTarget(self, board, player):
        target = {}
        if player == 1:
            for row in range(1, board.piece_rows + 1):
                if row == 4 and 1 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 3 and col == 2:
                        if board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif row == 2:
                        if 3 not in target and board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 1:
                        target[1] = target[1] + [(row, col)] if 1 in target else [(row, col)]
        else:
            for row in range(2 * board.size - 1, 2 * board.size - board.piece_rows - 1, -1):
                if row == 2 * board.size - board.piece_rows and 2 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 17 and col == 2:
                        if board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif row == 18:
                        if 4 not in target and board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 2:
                        target[2] = target[2] + [(row, col)] if 2 in target else [(row, col)]

        return target

    def starting(self, state) -> bool:
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        if (player == 1 and max([row for row, col in player_piece_pos_list]) > 9) or (
                player == 2 and min([row for row, col in player_piece_pos_list]) < 11):
            return True
        else:
            return False

    def getAction(self, state):
        time1 = time.time()
        legal_actions = self.game.actions(state)  # player = state[0], board = state[1]
        self.totnums = len(legal_actions)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        board = state[1]
        target = self.getTarget(board=board, player=player)
        a = 1.5 if self.starting(state) else 1
        if player == 1:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 1 and 1 in target:
                    if action[1] == (1, 1):
                        self.action = action
                        return
                    if action[0] in self.target1:
                        continue
                    if action[0][0] > 2 and action[1][0] < 3 and (
                            board.board_status[(1, 1)] == 1 or board.board_status[(2, 1)] == 1 or board.board_status[
                        (2, 2)] == 1):
                        continue
                    max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[1]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    if target[1][0][0] > 3:
                        max_toward_target[action] += 1
                    elif target[1][0][0] > 2:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
                    if action[1] == (3, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (3, 2):
                        max_toward_target[action] += 5


                elif board.board_status[action[0]] == 3 and 3 in target:
                    if action[0] in self.target3 or (
                            action[1][0] == 1 and board.board_status[(2, 1)] == 3 and board.board_status[(2, 2)] == 3):
                        continue
                    elif action[0][0] == 1 and action[1][0] == 2:
                        self.action = action
                        return
                    max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[3]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    max_toward_target[action] += 6 if target[3][0][0] > 2 else 4
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        else:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 2 and 2 in target:
                    if action[1] == (19, 1):
                        self.action = action
                        return
                    if action[0] in self.target2:
                        continue
                    if action[0][0] < 18 and action[1][0] > 17 and (
                            board.board_status[(19, 1)] == 2 or board.board_status[(18, 1)] == 2 or board.board_status[
                        (18, 2)] == 2):
                        continue
                    max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[2]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    if target[2][0][0] < 17:
                        max_toward_target[action] += 1
                    elif target[2][0][0] < 18:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
                    if action[1] == (17, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (17, 2):
                        max_toward_target[action] += 5

                elif board.board_status[action[0]] == 4 and 4 in target:
                    if action[0] in self.target4 or (
                            action[1][0] == 19 and board.board_status[(18, 1)] == 4 and board.board_status[
                        (18, 2)] == 4):
                        continue
                    elif action[0][0] == 19 and action[1][0] == 18:
                        self.action = action
                        return
                    max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[4]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    max_toward_target[action] += 6 if target[4][0][0] < 18 else 4
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        self.action = random.choice(max_actions) if max_actions else random.choice(legal_actions)
        time2 = time.time()
        print('time[%.6f]|' % (time2 - time1), 'action:', self.action, "totnums:", self.totnums,
              "avg time per action:%.6f" % ((time2 - time1) / self.totnums))


class OurSimpleGreedyAgent4(Agent):
    def __init__(self, game):
        self.target1 = [(1, 1), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.target2 = [(19, 1), (17, 1), (17, 3), (16, 1), (16, 2), (16, 3), (16, 4)]
        self.target3 = [(2, 1), (2, 2)]
        self.target4 = [(18, 1), (18, 2)]
        self.game = game
        self.totnums = 0

    def cubDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return math.sqrt(abs(pos_x - target_x)**2 + abs(pos_y - target_y)**2 + abs(pos_z - target_z)**2)

    def hexDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return max([abs(pos_x - target_x), abs(pos_y - target_y), abs(pos_z - target_z)])

    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getTarget(self, board, player):
        target = {}
        if player == 1:
            for row in range(1, board.piece_rows + 1):
                if row == 4 and 1 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 3 and col == 2:
                        if board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif row == 2:
                        if 3 not in target and board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 1:
                        target[1] = target[1] + [(row, col)] if 1 in target else [(row, col)]
        else:
            for row in range(2 * board.size - 1, 2 * board.size - board.piece_rows - 1, -1):
                if row == 2 * board.size - board.piece_rows and 2 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 17 and col == 2:
                        if board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif row == 18:
                        if 4 not in target and board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 2:
                        target[2] = target[2] + [(row, col)] if 2 in target else [(row, col)]

        return target

    def starting(self, state) -> bool:
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        if (player == 1 and max([row for row, col in player_piece_pos_list]) > 9) or (
                player == 2 and min([row for row, col in player_piece_pos_list]) < 11):
            return True
        else:
            return False

    def getAction(self, state):
        time1 = time.time()
        legal_actions = self.game.actions(state)  # player = state[0], board = state[1]
        self.totnums = len(legal_actions)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        board = state[1]
        target = self.getTarget(board=board, player=player)
        a = 1.5 if self.starting(state) else 1
        if player == 1:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 1 and 1 in target:
                    if action[1] == (1, 1):
                        self.action = action
                        return
                    if action[0] in self.target1:
                        continue
                    if action[0][0] > 2 and action[1][0] < 3 and (
                            board.board_status[(1, 1)] == 1 or board.board_status[(2, 1)] == 1 or board.board_status[
                        (2, 2)] == 1):
                        continue
                    max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[1]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    if target[1][0][0] > 3:
                        max_toward_target[action] += 1
                    elif target[1][0][0] > 2:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
                    if action[1] == (3, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (3, 2):
                        max_toward_target[action] += 5


                elif board.board_status[action[0]] == 3 and 3 in target:
                    if action[0] in self.target3 or (
                            action[1][0] == 1 and board.board_status[(2, 1)] == 3 and board.board_status[(2, 2)] == 3):
                        continue
                    elif action[0][0] == 1 and action[1][0] == 2:
                        self.action = action
                        return
                    max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[3]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    max_toward_target[action] += 6 if target[3][0][0] > 2 else 4
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        else:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 2 and 2 in target:
                    if action[1] == (19, 1):
                        self.action = action
                        return
                    if action[0] in self.target2:
                        continue
                    if action[0][0] < 18 and action[1][0] > 17 and (
                            board.board_status[(19, 1)] == 2 or board.board_status[(18, 1)] == 2 or board.board_status[
                        (18, 2)] == 2):
                        continue
                    max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[2]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    if target[2][0][0] < 17:
                        max_toward_target[action] += 1
                    elif target[2][0][0] < 18:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
                    if action[1] == (17, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (17, 2):
                        max_toward_target[action] += 5

                elif board.board_status[action[0]] == 4 and 4 in target:
                    if action[0] in self.target4 or (
                            action[1][0] == 19 and board.board_status[(18, 1)] == 4 and board.board_status[
                        (18, 2)] == 4):
                        continue
                    elif action[0][0] == 19 and action[1][0] == 18:
                        self.action = action
                        return
                    max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[4]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    max_toward_target[action] += 6 if target[4][0][0] < 18 else 4
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        self.action = random.choice(max_actions) if max_actions else random.choice(legal_actions)
        time2 = time.time()
        print('time[%.6f]|' % (time2 - time1), 'action:', self.action, "totnums:", self.totnums,
              "avg time per action:%.6f" % ((time2 - time1) / self.totnums))


class OurSimpleGreedyAgent5(Agent):
    def __init__(self, game):
        self.target1 = [(1, 1), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.target2 = [(19, 1), (17, 1), (17, 3), (16, 1), (16, 2), (16, 3), (16, 4)]
        self.target3 = [(2, 1), (2, 2)]
        self.target4 = [(18, 1), (18, 2)]
        self.game = game
        self.totnums = 0

    def cubDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return math.sqrt(abs(pos_x - target_x) ** 2 + abs(pos_y - target_y) ** 2 + abs(pos_z - target_z) ** 2)

    def hexDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return max([abs(pos_x - target_x), abs(pos_y - target_y), abs(pos_z - target_z)])

    def getOneEvaluate(self, state):
        player, board = state[0], state[1]
        myScore = 0
        my_piece_pos_list = board.getPlayerPiecePositions(player)
        for pos in my_piece_pos_list:
            myScore += field1[pos]

        return myScore if player == 1 else -myScore

    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getTarget(self, board, player):
        target = {}
        if player == 1:
            for row in range(1, board.piece_rows + 1):
                if row == 4 and 1 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 3 and col == 2:
                        if board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif row == 2:
                        if 3 not in target and board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 1:
                        target[1] = target[1] + [(row, col)] if 1 in target else [(row, col)]
        else:
            for row in range(2 * board.size - 1, 2 * board.size - board.piece_rows - 1, -1):
                if row == 2 * board.size - board.piece_rows and 2 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 17 and col == 2:
                        if board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif row == 18:
                        if 4 not in target and board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 2:
                        target[2] = target[2] + [(row, col)] if 2 in target else [(row, col)]

        return target

    def starting(self, state) -> bool:
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        if (player == 1 and max([row for row, col in player_piece_pos_list]) > 9) or (
                player == 2 and max([row for row, col in player_piece_pos_list]) < 11):
            return True
        else:
            return False

    def getAction(self, state):
        time1 = time.time()
        legal_actions = self.game.actions(state)  # player = state[0], board = state[1]
        self.totnums = len(legal_actions)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        board = state[1]
        target = self.getTarget(board=board, player=player)
        a = 1.5 if self.starting(state) else 1
        if player == 1:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 1 and 1 in target:
                    if action[1] == (1, 1):
                        self.action = action
                        return
                    if action[0] in self.target1:
                        continue
                    if action[0][0] > 2 and action[1][0] < 3 and (
                            board.board_status[(1, 1)] == 1 or board.board_status[(2, 1)] == 1 or board.board_status[
                        (2, 2)] == 1):
                        continue
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[1]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[1]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    if target[1][0][0] > 3:
                        max_toward_target[action] += 1
                    elif target[1][0][0] > 2:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
                    if action[1] == (3, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (3, 2):
                        max_toward_target[action] += 5


                elif board.board_status[action[0]] == 3 and 3 in target:
                    if action[0] in self.target3 or (
                            action[1][0] == 1 and board.board_status[(2, 1)] == 3 and board.board_status[(2, 2)] == 3):
                        continue
                    elif action[0][0] == 1 and action[1][0] == 2:
                        self.action = action
                        return
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[3]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[3]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    max_toward_target[action] += 6 if target[3][0][0] > 2 else 4
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        else:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 2 and 2 in target:
                    if action[1] == (19, 1):
                        self.action = action
                        return
                    if action[0] in self.target2:
                        continue
                    if action[0][0] < 18 and action[1][0] > 17 and (
                            board.board_status[(19, 1)] == 2 or board.board_status[(18, 1)] == 2 or board.board_status[
                        (18, 2)] == 2):
                        continue
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[2]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[2]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    if target[2][0][0] < 17:
                        max_toward_target[action] += 1
                    elif target[2][0][0] < 18:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
                    if action[1] == (17, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (17, 2):
                        max_toward_target[action] += 5

                elif board.board_status[action[0]] == 4 and 4 in target:
                    if action[0] in self.target4 or (
                            action[1][0] == 19 and board.board_status[(18, 1)] == 4 and board.board_status[
                        (18, 2)] == 4):
                        continue
                    elif action[0][0] == 19 and action[1][0] == 18:
                        self.action = action
                        return
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[4]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[4]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    max_toward_target[action] += 6 if target[4][0][0] < 18 else 4
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        self.action = random.choice(max_actions) if max_actions else random.choice(legal_actions)
        time2 = time.time()
        print('time[%.6f]|' % (time2 - time1), 'action:', self.action, "totnums:", self.totnums,
              "avg time per action:%.6f" % ((time2 - time1) / self.totnums))


class OurSimpleGreedyAgent6(Agent):
    def __init__(self, game):
        self.target1 = [(1, 1), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.target2 = [(19, 1), (17, 1), (17, 3), (16, 1), (16, 2), (16, 3), (16, 4)]
        self.target3 = [(2, 1), (2, 2)]
        self.target4 = [(18, 1), (18, 2)]
        self.game = game
        self.totnums = 0

    def cubDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return math.sqrt(abs(pos_x - target_x) ** 2 + abs(pos_y - target_y) ** 2 + abs(pos_z - target_z) ** 2)

    def hexDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return max([abs(pos_x - target_x), abs(pos_y - target_y), abs(pos_z - target_z)])

    def getOneEvaluate(self, state):
        player, board = state[0], state[1]
        myScore = 0
        my_piece_pos_list = board.getPlayerPiecePositions(player)
        for pos in my_piece_pos_list:
            myScore += field1[pos]

        return myScore if player == 1 else -myScore

    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getTarget(self, board, player):
        target = {}
        if player == 1:
            for row in range(1, board.piece_rows + 1):
                if row == 4 and 1 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 3 and col == 2:
                        if board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif row == 2:
                        if 3 not in target and board.board_status[(row, col)] != 3:
                            target[3] = target[3] + [(row, col)] if 3 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 1:
                        target[1] = target[1] + [(row, col)] if 1 in target else [(row, col)]
        else:
            for row in range(2 * board.size - 1, 2 * board.size - board.piece_rows - 1, -1):
                if row == 2 * board.size - board.piece_rows and 2 in target:
                    break
                for col in range(1, board.getColNum(row) + 1):
                    if row == 17 and col == 2:
                        if board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif row == 18:
                        if 4 not in target and board.board_status[(row, col)] != 4:
                            target[4] = target[4] + [(row, col)] if 4 in target else [(row, col)]
                    elif board.board_status[(row, col)] != 2:
                        target[2] = target[2] + [(row, col)] if 2 in target else [(row, col)]

        return target

    def starting(self, state) -> bool:
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        if (player == 1 and max([row for row, col in player_piece_pos_list]) > 9) or (
                player == 2 and max([row for row, col in player_piece_pos_list]) < 11):
            return True
        else:
            return False

    def getAction(self, state):
        time1 = time.time()
        legal_actions = self.game.actions(state)  # player = state[0], board = state[1]
        self.totnums = len(legal_actions)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        board = state[1]
        target = self.getTarget(board=board, player=player)
        a = 1.5 if self.starting(state) else 1
        if player == 1:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 1 and 1 in target:
                    if action[1] == (1, 1):
                        self.action = action
                        return
                    if action[0] in self.target1:
                        continue
                    if action[0][0] > 2 and action[1][0] < 3 and (
                            board.board_status[(1, 1)] == 1 or board.board_status[(2, 1)] == 1 or board.board_status[
                        (2, 2)] == 1):
                        continue
                    if self.getOneEvaluate(state) < 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[1]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[1]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    if target[1][0][0] > 3:
                        max_toward_target[action] += 1
                    elif target[1][0][0] > 2:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
                    if action[1] == (3, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (3, 2):
                        max_toward_target[action] += 5


                elif board.board_status[action[0]] == 3 and 3 in target:
                    if action[0] in self.target3 or (
                            action[1][0] == 1 and board.board_status[(2, 1)] == 3 and board.board_status[(2, 2)] == 3):
                        continue
                    elif action[0][0] == 1 and action[1][0] == 2:
                        self.action = action
                        return
                    if self.getOneEvaluate(state) < 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[3]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[3]])
                    max_toward_target[action] += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                        0] > 3 else a * (action[0][0] - action[1][0])
                    max_toward_target[action] += 6 if target[3][0][0] > 2 else 4
                    if action[0][0] > board.size:
                        max_toward_target[action] += action[0][0] - board.size
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        else:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 2 and 2 in target:
                    if action[1] == (19, 1):
                        self.action = action
                        return
                    if action[0] in self.target2:
                        continue
                    if action[0][0] < 18 and action[1][0] > 17 and (
                            board.board_status[(19, 1)] == 2 or board.board_status[(18, 1)] == 2 or board.board_status[
                        (18, 2)] == 2):
                        continue
                    if self.getOneEvaluate(state) < 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[2]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[2]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    if target[2][0][0] < 17:
                        max_toward_target[action] += 1
                    elif target[2][0][0] < 18:
                        max_toward_target[action] += 5
                    else:
                        max_toward_target[action] += 2
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
                    if action[1] == (17, 2):
                        max_toward_target[action] -= 3
                    elif action[0] == (17, 2):
                        max_toward_target[action] += 5

                elif board.board_status[action[0]] == 4 and 4 in target:
                    if action[0] in self.target4 or (
                            action[1][0] == 19 and board.board_status[(18, 1)] == 4 and board.board_status[
                        (18, 2)] == 4):
                        continue
                    elif action[0][0] == 19 and action[1][0] == 18:
                        self.action = action
                        return
                    if self.getOneEvaluate(state) < 0:
                        max_toward_target[action] = -min([self.hexDistance(action[1], t) for t in target[4]])
                    else:
                        max_toward_target[action] = -min([self.cubDistance(action[1], t) for t in target[4]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    max_toward_target[action] += 6 if target[4][0][0] < 18 else 4
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]

        self.action = random.choice(max_actions) if max_actions else random.choice(legal_actions)
        time2 = time.time()
        print('time[%.6f]|' % (time2 - time1), 'action:', self.action, "totnums:", self.totnums,
              "avg time per action:%.6f" % ((time2 - time1) / self.totnums))
