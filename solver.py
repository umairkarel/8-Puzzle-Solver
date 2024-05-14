""" 
    Created on Thu June 20 2021

    @author: umairkarel
"""

from constants import POSITIONS, GOAL_STATE


class Node:
    """Node for Board"""

    def __init__(self, data, level, f):
        self.data = data
        self.f = f
        self.level = level
        self.data_length = len(data)
        self.prev = None

    def neighbors(self):
        """
        Generates neighboring nodes by making valid moves on the CURRENTent node and returns them.
        """
        neighbors = []
        moves, (x, y) = self.find_moves()

        for i, j in moves:
            state = self.copy(self.data)
            state[x][y], state[i][j] = state[i][j], state[x][y]
            neighbors.append(Node(state, self.level + 1, 0))

        return neighbors

    def copy(self, data):
        """
        A function to copy a 2D list and return the copied list.

        Parameters:
            data (list): The 2D list to be copied.

        Returns:
            list: A copy of the input 2D list.
        """
        temp = []

        for i in data:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find_blank(self, data):
        """
        A function to find the position of the blank space (0) in a 2D list.

        Parameters:
            data (list): The 2D list to search for the blank space.

        Returns:
            tuple: The row and column index of the blank space.
        """

        for i in range(self.data_length):
            for j in range(self.data_length):
                if data[i][j] == 0:
                    return (i, j)

    def find_moves(self):
        """
        A function to find possible moves based on the blank space position in a 2D list.

        Returns:
            list: A list of possible moves represented as tuples.
        """
        x, y = self.find_blank(self.data)
        moves = []

        if x != 0:
            moves.append((x - 1, y))
        if y != 0:
            moves.append((x, y - 1))
        if y != 2:
            moves.append((x, y + 1))
        if x != 2:
            moves.append((x + 1, y))

        return moves, (x, y)


def heuristic(board, goal, heuristic_func):
    """
    A heuristic function to calculate the cost based on the given board state and goal state

    Parameters:
    - board: The CURRENTent state of the board.
    - goal: The goal state of the board.
    - heuristic_func: The type of heuristic function to be used ("hamming" or "manhattan").

    Returns:
    - count: The total cost calculated based on the heuristic function selected.
    """
    count = 0

    # Hamming Priority
    if heuristic_func == "hamming":
        for i in range(3):
            for j in range(3):
                if board[i][j] and board[i][j] != goal[i][j]:
                    count += 1

    # Manhattan Distance
    elif heuristic_func == "manhattan":
        for i in range(3):
            for j in range(3):
                if board[i][j]:
                    x, y = POSITIONS[board[i][j]]
                    manhattan = abs(x - i) + abs(y - j)
                    count += manhattan

    return count


def get_path():
    """
    A function that retrieves the path from the current node to the root node.
    """
    path = []
    temp = CURRENT
    path.insert(0, temp)

    while temp.prev:
        path.insert(0, temp.prev)
        temp = temp.prev

    return path


CURRENT = None


def solve(start, heuristic_func):
    """
    A* search algorithm to solve the puzzle using the given heuristic function.

    Parameters:
        start: The initial state of the puzzle.
        heuristic_func: The type of heuristic function to be used ("hamming" or "manhattan").

    Returns:
        The path to the goal state.
    """
    global CURRENT

    openSet = []
    closedSet = []

    start = Node(start, 0, 0)
    start.f = heuristic(start.data, GOAL_STATE, heuristic_func) + start.level
    openSet.append(start)

    while len(openSet) > 0:
        low = min(openSet, key=lambda x: x.f)
        CURRENT = openSet[low]

        if heuristic(CURRENT.data, GOAL_STATE, heuristic_func) == 0:
            break

        closedSet.append(CURRENT.data)
        openSet.remove(CURRENT)

        for neighbor in CURRENT.neighbors():
            if neighbor.data not in closedSet:
                neighbor.f = (
                    heuristic(neighbor.data, GOAL_STATE, heuristic_func)
                    + neighbor.level
                )
                openSet.append(neighbor)
                neighbor.prev = CURRENT

        # openSet.sort(key = lambda x:x.f,reverse=False)

    return get_path()
