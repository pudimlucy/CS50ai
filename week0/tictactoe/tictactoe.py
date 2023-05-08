"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    
    cempty = 0
    for i in board:
        for j in i:
            if j == EMPTY:
                cempty += 1
    
    if cempty % 2 == 0:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i, oi in enumerate(board):
        for j, cj in enumerate(oi):
            if cj == EMPTY:
                moves.add((i, j))

    if moves == set():
        return None
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid Action.")
    
    bcopy = copy.deepcopy(board)
    bcopy[action[0]][action[1]] = player(board)

    return bcopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontals
    for row in board:
        if all(cell == row[0] for cell in row):
            if row[0] == X:
                return X
            if row[0] == O:
                return O
    
    # Verticals
    flipped = [[], [], []]
    for row in board:
        for j, cell in enumerate(row):
            flipped[j].append(cell)
    for row in flipped:
        if all(cell == row[0] for cell in row):
            if row[0] == X:
                return X
            if row[0] == O:
                return O

    # Diagonals
    diagonals = [[], []]
    for i, row in enumerate(board):
        diagonals[0].append(row[i])
        diagonals[1].append(row[2 - i])
    for diagonal in diagonals:
        if all(cell == diagonal[0] for cell in diagonal):
            if diagonal[0] == X:
                return X
            if diagonal[0] == O:
                return O

    # No current winners
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return (winner(board) or not actions(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    def maxplayer(board, beta=2):
        """
        Returns the maximum value out of all minimum values
        """
        if terminal(board):
            return (utility(board), None)
        
        score = -2
        opt_action = None
        
        for action in actions(board):
            if beta <= score:
                break

            minplayer_result = minplayer(result(board, action), score)
            if minplayer_result[0] > score:
                score = minplayer_result[0]
                opt_action = action

        return (score, opt_action)

    
    def minplayer(board, alpha=-2):
        """
        Returns the minimum value out of all maximum values
        """
        if terminal(board):
            return (utility(board), None)
        
        score = 2
        opt_action = None
        
        for action in actions(board):
            if alpha >= score:
                break
            
            maxplayer_result = maxplayer(result(board, action), score)
            if maxplayer_result[0] < score:
                score = maxplayer_result[0]
                opt_action = action

        return (score, opt_action)
    
    
    if player(board) == X:
        opt_action = maxplayer(board)[1]     
        return opt_action
    
    elif player(board) == O:
        opt_action = minplayer(board)[1]     
        return opt_action
    