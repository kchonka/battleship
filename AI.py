# Class representing an AI object

from board import Board, Cell


class AI:
    def __init__(self):
        self.board = Board()

    def random_placement(self):
        pass

    def monte_carlo_placement(self):
        pass

    # This function is used when recieveing a shot from the player opponent
    # Coordinates is a list pair of Board coordinates that the player fired at:
    def attack(self, coordinates):
        row = coordinates[0]
        col = coordinates[1]
        return self.board.shoot(row, col)

