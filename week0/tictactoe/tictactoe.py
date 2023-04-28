"""
Tic Tac Toe Player
"""

import math
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
    # Horizontal
    for i, oi in enumerate(board):
        if all(x == oi[0] for x in oi):
            return oi[0]
    
    # Vertical
    ...

    # Diagonal
    ...
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
