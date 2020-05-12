# Class representing an AI object

from board import Board, Cell
from random import seed, randint
import time

class AI:
    def __init__(self):
        self.board = Board()

    # Returns the board array list (not a Board object) --> calls Board's get_board
    def get_board(self):
        return self.board.get_board()

    def random_placement(self):
        # Sample example:
        carrier = [[10, 4], [10, 5], [10, 6], [10, 7], [10, 8]]
        battleship = [[2, 2], [2, 3], [2, 4], [2, 5]]
        cruiser = [[7, 2], [8, 2], [9, 2]]
        submarine = [[3, 9], [4, 9], [5, 9]]
        destroyer = [[5, 5], [6, 5]]

        self.board.add_ship(carrier)
        self.board.add_ship(battleship)
        self.board.add_ship(cruiser)
        self.board.add_ship(submarine)
        self.board.add_ship(destroyer)

    def monte_carlo_placement(self):
        pass

    # Get attacked BY the player opponent
    # Returns the new state at board[row][col]
    # Coordinates is a list pair of Board coordinates that the player fired at
    def suffer_attack(self, coordinates):
        row = coordinates[0]
        col = coordinates[1]
        return self.board.shoot(row, col)

    def random_attack(self):
        seed(time.time())
        row = randint(1, 10)
        col = randint(1, 10)
        return row, col
