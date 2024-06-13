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

    numX = 0
    numO = 0

    # counting amount of x and o in the board

    for list in board:
        for cell in list:
            if cell == X:
                numX += 1
            elif cell == O:
                numO += 1

    if numX > numO:
        return O
    else:
        return X
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possibleActions = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possibleActions.append((i, j))

    return set(possibleActions)

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    for num in action:
        if num < 0 or num > 2 :
            raise Exception

    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move")
    
    # might need to deep copy the board idk yet
    newBoard = copy.deepcopy(board)

    newBoard[action[0]][action[1]] = player(board)

    return newBoard

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # checking rows
    for row in board:
        if row[0] is not EMPTY:
            if row[0] == row[1] == row[2]:
                return row[0]
        
    # checking columns
    for i in range(3):
        if board[0][i] is not EMPTY:
            if board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]
        
    # checking diagonals
    if board[0][0] is not EMPTY and board[0][2] is not EMPTY:
        if board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        elif board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
    
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if board == initial_state():
        return False

    if winner(board) != None:
        return True

    for row in board:
        if EMPTY in row:
            return False
    
    
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        bestValue = -math.inf
        for action in actions(board):
            value = minimizer(result(board, action))
            if value > bestValue:
                bestValue = value
                bestAction = action
    else:
        bestValue = math.inf
        for action in actions(board):
            value = maximizer(result(board, action))
            if value < bestValue:
                bestValue = value
                bestAction = action
                
    return bestAction
    raise NotImplementedError




def maximizer(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, minimizer(result(board, action)))

    return v

    raise NotImplementedError



def minimizer(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, maximizer(result(board, action)))

    return v


    raise NotImplementedError