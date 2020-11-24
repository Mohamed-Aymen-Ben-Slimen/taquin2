from queue import PriorityQueue
from board import Board
import numpy as np
from graphics import *
import pprint
import time
from utils import Node, PriorityQueue

pp = pprint.PrettyPrinter(indent=4)

end_puzzle = [[0, 1, 2, 3],[4, 6, 5, 7], [8, 9, 10, 11],[12, 13, 14, 15]]





def a_star(board, heuristic):
    """
    solves the board using the A* approach accompanied by the heuristic function

    :param board: board to solve
    :param heuristic: heuristic function
    :return: path to solution, and number of explored nodes
    """

    frontier = PriorityQueue()
    node = Node(board)
    frontier.add(node, heuristic(node.data) + len(node.path()) - 1)

    explored = []

    while frontier.has_next():
        node = frontier.pop()
        print(node.data)

        # check if solved
        if node.data.is_solved():
            return node.path(), len(explored) + 1

        # add children to frontier
        for move in node.data.legal_moves():
            child = Node(node.data.forecast(move), node)
            # child must not have already been explored
            if (not frontier.has(child)) and (child.data not in explored):
                frontier.add(child, heuristic(child.data) + len(child.path()) - 1)
            # if the child is already in the frontier, it can be added only if it's better
            elif frontier.has(child):
                child_value = heuristic(child.data) + len(child.path()) - 1
                if child_value < frontier.get_value(child):
                    frontier.remove(child)
                    frontier.add(child, child_value)

        explored.append(node.data)
    return None, len(explored)


def n_wrong_heuristic(board):
    """
    counts the number of tiles incorrectly placed

    excludes the 0 tile
    """

    state = board.get_board()
    indices = np.array([np.argwhere(state == i)[0] for i in range(1, 16)])
    correct_indices = np.array([[i, j] for i in range(4) for j in range(4)])[:-1]
    n_wrong = 0
    for i,pair in enumerate(indices):
        if (pair != correct_indices[i]).any():
            n_wrong += 1

    return n_wrong




def manhattan_heuristic(board):
    """
    this sums up the manhattan distances between the board's state and the solution's state.

    excludes the 0 tile
    """
    state = board.get_board()
    indices = np.array([np.argwhere(state == i)[0] for i in range(1,16)])
    correct_indices = np.array([[i, j] for i in range(4) for j in range(4)])[:-1]

    return np.abs(indices - correct_indices).sum()






def initialize_board(filename):
    infile = open(filename, "r")
    board = []
    for i in range(4):
        board.append([])
    for row in range(4):
        for col in range(4):
            columnvalue = eval(infile.readline())
            board[row].append(columnvalue)
    return board

def display_numbers(window, board):
    if isinstance(board, int):
        return 0
    for row in range(4):
        for col in range(4):
            square = Rectangle(Point(col * 100, row * 100), Point((col + 1) * 100, (row + 1) * 100))
            square.setFill("white")
            square.draw(window)
            if board[row][col] != 0:
                center = Point(col * 100 + 50, row * 100 + 50)
                number = Text(center, board[row][col])
                number.setSize(24)
                number.setTextColor("purple")
                number.draw(window)



def main():
    filename = ("taquin.txt")
    board = Board(np.array(initialize_board(filename)))
    window = GraphWin("Jeux de Taquin", 400, 400)
    display_numbers(window, board.get_board())
    path, path_length = a_star(board, manhattan_heuristic)
    if path == 0:
        message = Text(Point(200, 200), "NO POSSIBLE SOLUTION")
        message.setSize(24)
        message.setTextColor("orange")
        message.draw(window)
    else:
        for pa in path:
            display_numbers(window, pa.get_board())
            time.sleep(0.3)
        message = Text(Point(200, 200), "SOLUTION FOUND")
        message.setSize(24)
        message.setTextColor("orange")
        message.draw(window)

    print("Press <ENTER> to quit.")
    input()
    window.close()

main()
