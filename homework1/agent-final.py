import random, re, datetime, time, copy, math

MAXDEPTH = 3
MAXEXPAND = 4

SCORE_MAX = 1000000
SCORE_MIN = -1 * SCORE_MAX
SCORE_WIN = 0


def getColNum(row):  # (maxRow, maxCol), (1, 1), (2, 2), ..., (10, 10), (11, 9), (12, 8), ..., (19, 1)
    if row in range(1, 10 + 1):
        return row
    else:
        return 20 - row

# create a field with different scores
#                                       (1, 1): 10
#                                 (2, 1): 10, (2, 2): 10
#                           (3, 1): 10, (3, 2): 10, (3, 3): 10
#                       (4, 1): 10, (4, 2): 10, (4, 3): 10, (4, 4): 10
#                   (5, 1): 8, (5, 2): 8, (5, 3): 8, (5, 4): 8, (5, 5): 8
#               (6, 1): 8, (6, 2): 7, (6, 3): 7, (6, 4): 7, (6, 5): 7, (6, 6): 8
#           (7, 1): 6, (7, 2): 5, (7, 3): 5, (7, 4): 5, (7, 5): 5, (7, 6): 5, (7, 7): 6
#       (8, 1): 4, (8, 2): 3, (8, 3): 3, (8, 4): 3, (8, 5): 3, (8, 6): 3, (8, 7): 3, (8, 8): 4
#   (9, 1): 2, (9, 2): 2, (9, 3): 0, (9, 4): 0, (9, 5): 0, (9, 6): 0, (9, 7): 0, (9, 8): 2, (9, 9):
# (10, 1): 0, (10, 2): 0, (10, 3): 0, (10, 4): 0, (10, 5): 0, (10, 6): 0,(10, 7): 0, (10, 8): 0, (10, 9): 0, (10, 10): 0
#   (11, 1): -2, (11, 2): -2, (11, 3): 0, (11, 4): 0, (11, 5): 0, (11, 6): 0, (11, 7): 0, (11, 8): -2, (11, 9): -2
#       (12, 1): -4, (12, 2): -3, (12, 3): -3, (12, 4): -3, (12, 5): -3, (12, 6): -3, (12, 7): -3, (12, 8): -4
#           (13, 1): -6, (13, 2): -5, (13, 3): -5, (13, 4): -5, (13, 5): -5, (13, 6): -5, (13, 7): -6
#               (14, 1): -8, (14, 2): -7, (14, 3): -7, (14, 4): -7, (14, 5): -7, (14, 6): -8
#                   (15, 1): -8, (15, 2): -8, (15, 3): -8, (15, 4): -8, (15, 5): -8
#                       (16, 1): -10, (16, 2): -10, (16, 3): -10, (16, 4): -10
#                           (17, 1): -10, (17, 2): -10, (17, 3): -10
#                                   (18, 1): -10, (18, 2): -10
#                                           (19, 1): -10

field1 = {}
for row in range(1, 10):
    for col in range(1, row + 1):
        if row < 5:
            field1[(row, col)] = 10
        elif row == 5:
            field1[(row, col)] = 8
        elif row == 9:
            if col < 3 or col > 7:
                field1[(row, col)] = 2
            else:
                field1[(row, col)] = 0
        else:
            if col == 1 or col == row:
                field1[(row, col)] = 20 - 2 * row
            else:
                field1[(row, col)] = 19 - 2 * row
for col in range(1, 11):
    field1[(10, col)] = 0
for row in range(11, 20):
    for col in range(1, getColNum(row) + 1):
        field1[(row, col)] = -field1[(20 - row, col)]


class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class BIEJUANLE(Agent):
    def __init__(self, game):
        self.target1 = [(1, 1), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        self.target2 = [(19, 1), (17, 3), (17, 1), (16, 4), (16, 3), (16, 2), (16, 1)]
        self.target3 = [(2, 1), (2, 2)]
        self.target4 = [(18, 2), (18, 1)]
        self.game = game
        self.action = None

    # distance calculation function
    def cubeEuclideanDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return math.sqrt(abs(pos_x - target_x) ** 2 + abs(pos_y - target_y) ** 2 + abs(pos_z - target_z) ** 2)

    # distance calculation function
    def cubeManhattanDistance(self, pos, target):
        pos_x = pos[0]
        pos_y = pos[1] - (pos_x - pos_x % 2) // 2
        pos_z = -pos_x - pos_y
        target_x = target[0]
        target_y = target[1] - (target_x - target_x % 2) // 2
        target_z = -target_x - target_y
        return max([abs(pos_x - target_x), abs(pos_y - target_y), abs(pos_z - target_z)])

    # evalute the state of pieces of both parts according to field1
    def getEvaluate(self, state) -> int:
        player, board = state[0], state[1]
        myScore = 0
        opScore = 0
        my_piece_pos_list = board.getPlayerPiecePositions(player)
        op_piece_pos_list = board.getPlayerPiecePositions(3 - player)
        for pos in my_piece_pos_list:
            myScore += field1[pos]
        for pos in op_piece_pos_list:
            opScore += field1[pos]

        return myScore - opScore if player == 1 else opScore - myScore

    # evalute the state of our pieces according to field1
    def getOneEvaluate(self, state) -> int:
        player, board = state[0], state[1]
        myScore = 0
        my_piece_pos_list = board.getPlayerPiecePositions(player)
        for pos in my_piece_pos_list:
            myScore += field1[pos]

        return myScore if player == 1 else -myScore

    # our top-level function to get action each turn
    def getAction(self, state):
        # time1 = time.time()
        # self.totalActions = 0
        self.boardScore = self.getEvaluate(state)        # evaluate current state according to the pieces of both parts
        self.oneScore = self.getOneEvaluate(state)       # evaluate current state according to our pieces
        if self.oneScore > 80 or -10 < self.boardScore < 10:  # if in the final term or in the quite interim term of the game
            score = self.search(state, 0)           # we make greedy search
        else:
            score = self.search(state, MAXDEPTH, MAXEXPAND)
        # time2 = time.time()
        # print('time[%.4f]|' % (time2 - time1), 'action:', self.action,
        #       'score[%d] tot[%d]' % (score, self.totalActions))

    def search(self, state, maxdepth=3, maxExpand=3):
        self.maxdepth = maxdepth
        self.maxExpand = maxExpand
        score = self.__search(state, maxdepth, 0)
        return score

    # our search function
    def __search(self, state, depth, pathScore=0):
        player, board = state[0], state[1]
        op_player = 3 - player
        # to get all legal actions and first assign a random action to self.action
        legal_actions = self.game.actions(state)
        self.action = [random.choice(legal_actions)]
        # if there are no actions, just return the score
        if len(legal_actions) == 0:
            return None
        # self.totalActions += len(legal_actions)
        # to check if the pieces of the opponent have nothing to do with our following steps
        if (player == 1 and (max([pos[0] for pos in board.getPlayerPiecePositions(player)]) < min(
                [pos[0] for pos in board.getPlayerPiecePositions(op_player)]))) or (
                player == 2 and (min([pos[0] for pos in board.getPlayerPiecePositions(player)]) > max(
            [pos[0] for pos in board.getPlayerPiecePositions(op_player)]))):

            split = True
        else:
            split = False

        # 1. in the case: maxdepth = 0 means we just pick the max scored action from the first layer of our search tree.
        #                 the same as the greedy search.
        if self.maxdepth == 0:
            max_toward_target = {}
            for action in legal_actions:
                max_toward_target[action] = self.getScore(state, action)
            max_toward_target_one_step = max(max_toward_target.values())
            max_actions = [action for action, value in max_toward_target.items() if value == max_toward_target_one_step]
            self.action = random.choice(max_actions)
            return max_toward_target_one_step
        # 2. in the case: current depth = 0 means we reach the leaves of our search tree, we return the max score of the
        #                 actions added to the score of the path
        elif depth <= 0:
            score = max([self.getScore(state, action) for action in legal_actions])
            return score + pathScore
        # 3. in the case: we are at the top level of our search tree, we need to first pick top-k scored actions to
        #                 expand, and after each iteration we need to assign the current max scored action to
        #                 self.action.
        elif depth == self.maxdepth:
            tot_action = {}
            max_toward_target = {}
            for action in legal_actions:
                tot_action[action] = self.getScore(state, action)
            # pick top-k actions
            max_expand_action = sorted(tot_action.items(), reverse=True, key=lambda x: x[1])[:self.maxExpand]
            for action, curScore in max_expand_action:
                # we need to change the board according to our selected action
                board.board_status[action[1]] = board.board_status[action[0]]
                board.board_status[action[0]] = 0
                # if we split up with the opponent, we don't need to consider the aciton of the opponent.
                if not split:
                    # we get the optimal action of the opponent and its score by self.getOpAction
                    opaction, opScore = self.getOpAction((op_player, board))
                    board.board_status[opaction[1]] = board.board_status[opaction[0]]
                    board.board_status[opaction[0]] = 0
                else:
                    opScore = 0
                # run the adversarial search recursively
                max_toward_target[action] = self.__search((player, board), depth - 1, curScore + pathScore - opScore)
                if not split:
                    board.board_status[opaction[0]] = board.board_status[opaction[1]]
                    board.board_status[opaction[1]] = 0
                # we need to change the board back to original state after each branch search
                board.board_status[action[0]] = board.board_status[action[1]]
                board.board_status[action[1]] = 0
                max_action = sorted(max_toward_target.items(), reverse=True, key=lambda x: x[1])[:1]
                self.action = max_action[0][0]
            return max(max_toward_target.values())
        # 4. in the case: we are not at the top or bottom level of the tree and we still expand the top-k scored actions
        #                 but we just return the highest score of these results.
        else:
            maxScore = SCORE_MIN
            tot_action = {}
            for action in legal_actions:
                tot_action[action] = self.getScore(state, action)
            max_expand_action = sorted(tot_action.items(), reverse=True, key=lambda x: x[1])[:self.maxExpand]
            for action, curScore in max_expand_action:
                curScore = self.getScore(state, action)
                # we need to change the board according to our selected action
                board.board_status[action[1]] = board.board_status[action[0]]
                board.board_status[action[0]] = 0
                # if we split up with the opponent, we don't need to consider the aciton of the opponent.
                if not split:
                    # we get the optimal action of the opponent and its score by self.getOpAction
                    opaction, opScore = self.getOpAction((op_player, board))
                    board.board_status[opaction[1]] = board.board_status[opaction[0]]
                    board.board_status[opaction[0]] = 0
                else:
                    opScore = 0
                # run the adversarial search recursively
                maxScore = max(maxScore, self.__search((player, board), depth - 1, curScore + pathScore - opScore))
                if not split:
                    board.board_status[opaction[0]] = board.board_status[opaction[1]]
                    board.board_status[opaction[1]] = 0
                # we need to change the board back to original state after each branch search
                board.board_status[action[0]] = board.board_status[action[1]]
                board.board_status[action[1]] = 0
            # since it's not the top level of the search tree, we actually don't need to know the real action in the
            # next few steps.
            return maxScore

    # we use getScore to evaluate our actions and return its score
    def getScore(self, state, action):
        player = self.game.player(state)
        board = state[1]
        target = self.getTarget(board=board, player=player)
        a = 1.5 if self.starting(state) else 1
        if player == 1:
            if board.board_status[action[0]] == 1 and 1 in target:
                if action[1] == (1, 1):
                    return SCORE_MAX
                if action[0] in self.target1:
                    return SCORE_MIN
                if action[0][0] > 2 and action[1][0] < 3 and (
                        board.board_status[(1, 1)] == 1 or board.board_status[(2, 1)] == 1 or board.board_status[
                    (2, 2)] == 1):
                    return SCORE_MIN
                # compute the distance between the new pos and target position.
                score = -min([self.cubeManhattanDistance(action[1], t) for t in target[1]])
                # compute the vertical displacement and reward if it makes big advance.
                score += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                    0] > 3 else a * (action[0][0] - action[1][0])
                # add to score according to different target
                if target[1][0][0] > 3:
                    score += 1
                elif target[1][0][0] > 2:
                    score += 5
                else:
                    score += 2
                # if the pieces are on the lower half plane, we want them to go forward.
                if action[0][0] > board.size:
                    score += action[0][0] - board.size
                # we don't want to see blue pieces occupy (3,2)
                if action[1] == (3, 2):
                    score -= 5
                elif action[0] == (3, 2):
                    score += 5

            elif board.board_status[action[0]] == 3 and 3 in target:
                if action[0] in self.target3 or (
                        action[1][0] == 1 and board.board_status[(2, 1)] == 3 and board.board_status[(2, 2)] == 3):
                    return SCORE_MIN
                elif action[0][0] == 1 and action[1][0] == 2:
                    return SCORE_MAX
                # compute the distance between the new pos and target position.
                score = -min([self.cubeManhattanDistance(action[1], t) for t in target[3]])
                # add to score according to different target
                score += 6 if target[3][0][0] > 2 else 4

                score += a * 2 * (action[0][0] - action[1][0]) if action[0][0] - action[1][
                    0] > 3 else a * (action[0][0] - action[1][0])
                # if the pieces are on the lower half plane, we want them to go forward.
                if action[0][0] > board.size:
                    score += action[0][0] - board.size
            else:
                return SCORE_MIN
        # the situation of player2 is the similar to player1
        else:
            if board.board_status[action[0]] == 2 and 2 in target:
                if action[1] == (19, 1):
                    return SCORE_MAX
                if action[0] in self.target2:
                    return SCORE_MIN
                if action[0][0] < 18 and action[1][0] > 17 and (
                        board.board_status[(19, 1)] == 2 or board.board_status[(18, 1)] == 2 or board.board_status[
                    (18, 2)] == 2):
                    return SCORE_MIN
                score = -min([self.cubeManhattanDistance(action[1], t) for t in target[2]])
                score += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                    0] > 3 else a * (action[1][0] - action[0][0])
                if target[2][0][0] < 17:
                    score += 1
                elif target[2][0][0] < 18:
                    score += 5
                else:
                    score += 2
                if action[0][0] < board.size:
                    score += board.size - action[0][0]
                if action[1] == (17, 2):
                    score -= 5
                elif action[0] == (17, 2):
                    score += 5

            elif board.board_status[action[0]] == 4 and 4 in target:
                if action[0] in self.target4 or (
                        action[1][0] == 19 and board.board_status[(18, 1)] == 4 and board.board_status[(18, 2)] == 4):
                    return SCORE_MIN
                elif action[0][0] == 19 and action[1][0] == 18:
                    return SCORE_MAX
                score = -min([self.cubeManhattanDistance(action[1], t) for t in target[4]])
                score += 6 if target[4][0][0] < 18 else 4
                score += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                    0] > 3 else a * (action[1][0] - action[0][0])
                if action[0][0] < board.size:
                    score += board.size - action[0][0]
            else:
                return SCORE_MIN
        return score

    # get the position of the target points
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

    # to judge if it's the early time of game by where our last piece is on.
    def starting(self, state) -> bool:
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        if (player == 1 and max([row for row, col in player_piece_pos_list]) > 9) or (
                player == 2 and min([row for row, col in player_piece_pos_list]) < 11):
            return True
        else:
            return False

    # to simulate the optimal action of the opponent according to the current state by using greedy search
    def getOpAction(self, state):
        legal_actions = self.game.actions(state)  # player = state[0], board = state[1]
        player = self.game.player(state)
        board = state[1]
        target = self.getTarget(board=board, player=player)
        a = 1.5 if self.starting(state) else 1
        max_toward_target_one_step = 0
        if player == 1:
            max_toward_target = {}
            max_actions = []
            for action in legal_actions:
                if board.board_status[action[0]] == 1 and 1 in target:
                    if action[1] == (1, 1):
                        return action, 1
                    if action[0] in self.target1:
                        continue
                    if action[0][0] > 2 and action[1][0] < 3 and (
                            board.board_status[(1, 1)] == 1 or board.board_status[(2, 1)] == 1 or board.board_status[
                        (2, 2)] == 1):
                        continue
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.cubeManhattanDistance(action[1], t) for t in target[1]])
                    else:
                        max_toward_target[action] = -min([self.cubeEuclideanDistance(action[1], t) for t in target[1]])
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
                        return action, 1
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.cubeManhattanDistance(action[1], t) for t in target[3]])
                    else:
                        max_toward_target[action] = -min([self.cubeEuclideanDistance(action[1], t) for t in target[3]])
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
                        return action, 1
                    if action[0] in self.target2:
                        continue
                    if action[0][0] < 18 and action[1][0] > 17 and (
                            board.board_status[(19, 1)] == 2 or board.board_status[(18, 1)] == 2 or board.board_status[
                        (18, 2)] == 2):
                        continue
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.cubeManhattanDistance(action[1], t) for t in target[2]])
                    else:
                        max_toward_target[action] = -min([self.cubeEuclideanDistance(action[1], t) for t in target[2]])
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
                            action[1][0] == 19 and board.board_status[(18, 1)] == 4 and board.board_status[(18, 2)] == 4):
                        continue
                    elif action[0][0] == 19 and action[1][0] == 18:
                        return action, 1
                    if self.getOneEvaluate(state) > 0:
                        max_toward_target[action] = -min([self.cubeManhattanDistance(action[1], t) for t in target[4]])
                    else:
                        max_toward_target[action] = -min([self.cubeEuclideanDistance(action[1], t) for t in target[4]])
                    max_toward_target[action] += a * 2 * (action[1][0] - action[0][0]) if action[1][0] - action[0][
                        0] > 3 else a * (action[1][0] - action[0][0])
                    max_toward_target[action] += 6 if target[4][0][0] < 18 else 4
                    if action[0][0] < board.size:
                        max_toward_target[action] += board.size - action[0][0]
            if len(max_toward_target):
                max_toward_target_one_step = max(max_toward_target.values())
                max_actions = [action for action, value in max_toward_target.items() if
                               value == max_toward_target_one_step]
        # we return the action of the opponent and its score
        return (random.choice(max_actions), max_toward_target_one_step // 5) if len(max_actions) else (
            random.choice(legal_actions), 0)
