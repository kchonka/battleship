# Class representing an AI object

from board import Board, Cell
from random import seed, randint
import time

class AI:
    def __init__(self):
        self.board = Board()

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

    # This function is used when getting shot at BY the player opponent
    # Coordinates is a list pair of Board coordinates that the player fired at:
    def receive_attack(self, coordinates):
        row = coordinates[0]
        col = coordinates[1]
        return self.board.shoot(row, col)

    def random_attack(self, board):
        seed(time.time())
        row = randint(1, 10)
        col = randint(1, 10)

        new_state = board.shoot(row, col)

        return row, col, new_state
