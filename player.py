# Class that represents the user player

from board import Board, Cell
from ship import Ship


class Player:
    def __init__(self):
        self.board = Board()

    def place_ship(self, coordinates):
        self.board.add_ship(coordinates)

    # When the AI attacks the player board, it'll make an attempt at board[row][col]
    def attack(self, row, col):
        self.board.update[row][col]

