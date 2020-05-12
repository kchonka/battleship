# Class that represents the user player

from board import Board, Cell
from random import seed, randint


class Player:
    def __init__(self):
        self.board = Board()
        self.all_ships = []

    # Returns the board array list (not a Board object) --> calls Board's get_board
    def get_board(self):
        return self.board.get_board()

    def add_ship(self, coordinates):
        self.board.add_ship(coordinates)
        self.all_ships.append(coordinates)

    # Get attacked by the opponent
    # Returns the new state of the grid at board[row][col]
    def suffer_attack(self, row, col):
        return self.board.shoot(row, col)

    def print_all_ship_coordinates(self):
        return self.all_ships