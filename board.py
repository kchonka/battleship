# Class representing a board object
# Both the player and AI classes will use this class as their board

from enum import Enum
HEIGHT = 11
WIDTH = 11

# 10 row x 10 cols for the game, but row 0 & col 0 are unused / off limits = 11 x 11


class Cell(Enum):
    EMPTY = 0       # EMPTY CELL
    HIDDEN = 1      # CELL WITH A HIDDEN SHIP PIECE
    MISS = 2        # A MISS (CELL THAT WAS EMPTY AND HIT)
    HIT = 3         # A HIT (CELL WITH A SHIP THAT WAS HIT / SUCCESSFULLY ATTACKED)
    SUNK = 4        # A SHIP THAT WAS FULLY HIT / SUNK


class Board:
    def __init__(self):
        self.board = [[Cell.EMPTY for x in range(WIDTH)] for y in range(HEIGHT)]
        self.ships = {"battleship": None, "carrier": None, "cruiser": None, "submarine": None, "destroyer": None}

    # Returns the array matrix with all the states:
    def get_board(self):
        return self.board

    # Updates the board for a hidden ship
    # Takes in a list of coordinates for a ship
    def add_ship(self, name, coordinates):
        # Update the coordinates on the board
        for pair in coordinates:
            x = pair[0]
            y = pair[1]
            self.board[x][y] = Cell.HIDDEN

        self.ships[name] = coordinates

    # Given a ship's name, checks to see whether the ship was sunk entirely
    # If sunk, updates the hits on the board to sunk (HIT --> SUNK)
    # Returns 'True' if the ship was sunk, 'False' if not
    def check_sunken_ships(self):
        for name in self.ships.keys():
            sunk = True
            coordinates = self.ships[name]
            if coordinates is not None:
                for pair in coordinates:
                    row = pair[0]
                    col = pair[1]
                    if self.board[row][col] != Cell.HIT:
                        sunk = False
                        break
                if sunk:    # Update board if sunk
                    for pair in coordinates:
                        row = pair[0]
                        col = pair[1]
                        self.board[row][col] = Cell.SUNK

    # Returns the state of the board (Empty, hidden, missed, hit, sunk)
    def get_state(self, row, col):
        return self.board[row][col]

    # Shoot at [row][col]
    # Checks the current state at those coordinates, updates, and returns the new state
    def shoot(self, row, col):
        state = self.board[row][col]

        # Checks the current state of the block:
        if state == Cell.EMPTY:
            self.board[row][col] = Cell.MISS    # If current state is EMPTY --> update to a MISS
        elif state == Cell.HIDDEN:
            self.board[row][col] = Cell.HIT     # If current state is HIDDEN SHIP --> update to a HIT

        return self.board[row][col]             # Return the updated board state

    '''
    # Outputs a board representation to the stdout console
    def print_board(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.board[x][y] == 0:
                    print("_")  # Empty cell
                elif self.board[x][y] == 1:
                    print("#")  # Cell with a ship piece
                elif self.board[x][y] == 2:
                    print("X")  # Miss
                elif self.board[x][y] == 3:
                    print("S")  # Hit
    '''

