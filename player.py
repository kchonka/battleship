# Class that represents the user player

from board import Board, Cell
from random import seed, randint


class Player:
    def __init__(self):
        self.board = Board()

    # Returns the board array list (not a Board object) --> calls Board's get_board
    def get_board(self):
        return self.board.get_board()

    # Returns a copy of the player's board object:
    def get_board_copy(self):
        return self.board

    def get_sunken_ships(self):
        return self.board.get_sunken_ships()

    # Returns the state of the board (Empty, hidden, missed, hit, sunk)
    def get_state(self, row, col):
        return self.board.get_state(row, col)

    # Checks for sunken ships and updates the board
    def check_sunken_ships(self):
        self.board.check_sunken_ships()

    # Check if lost: (the player is still in the game if all five of its ships are NOT sunk)
    def check_loss(self):
        sunken_ships = self.board.get_number_sunken_ships()
        if sunken_ships < 5:
            return False
        else:
            return True

    def add_ship(self, name, coordinates):
        self.board.add_ship(name, coordinates)

    # Get attacked by the opponent
    # Returns the new state of the grid at board[row][col]
    def suffer_attack(self, row, col):
        return self.board.shoot(row, col)
