# Kat Chonka & Denysse Cunza

# Class representing a board object
# Both the player and AI classes will use this class as their board

from enum import Enum
from random import seed, randint
import random
import time

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    HUNT = 4      # Take random shot elsewhere


class Cell(Enum):
    EMPTY = 0       # EMPTY CELL
    HIDDEN = 1      # CELL WITH A HIDDEN SHIP PIECE
    MISS = 2        # A MISS (CELL THAT WAS EMPTY AND HIT)
    HIT = 3         # A HIT (CELL WITH A SHIP THAT WAS HIT / SUCCESSFULLY ATTACKED)
    SUNK = 4        # A SHIP THAT WAS FULLY HIT / SUNK


class Board:
    def __init__(self):
        # 10 row x 10 cols for the game, but row 0 & col 0 are unused / off limits = 11 x 11
        self.board = [[Cell.EMPTY for x in range(11)] for y in range(11)]
        self.ships = {"battleship": None, "carrier": None, "cruiser": None, "submarine": None, "destroyer": None}
        self.ships_sunk = {"battleship": False, "carrier": False, "cruiser": False, "submarine": False, "destroyer": True}
        self.sunk = 0  # The number of sunken ships
        self.moves = 0 # The number of cells explored / moves taken
        self.sunken_ship_coordinates = [] # List of all the coordinates with "SUNK" status
        '''self.size = 0              # For Monte Carlo
        self.ship = []
        self.hits = []
        self.available_ships = []'''

    # Resets the board
    def reset(self):
        self.board = [[Cell.EMPTY for x in range(WIDTH)] for y in range(HEIGHT)]

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

    # Returns the amount of sunken ships on the board
    def get_number_sunken_ships(self):
        return self.sunk

    # Given a ship's name, checks to see whether the ship was sunk entirely
    # If sunk, updates the hits on the board to sunk (HIT --> SUNK)
    # Returns 'True' if the ship was sunk, 'False' if not
    def check_sunken_ships(self):
        for name in self.ships.keys():
            sunk = True
            coordinates = self.ships[name]
            if coordinates is not None:
                for pair in coordinates:
                    x = pair[0]
                    y = pair[1]
                    if self.board[x][y] != Cell.HIT:
                        sunk = False
                        break
                if sunk:
                    self.sunk += 1
                    # Update board if sunk
                    for pair in coordinates:
                        x = pair[0]
                        y = pair[1]
                        self.board[x][y] = Cell.SUNK
                        self.sunken_ship_coordinates.append([x,y])
        return sunk
    # Returns the state of the board (Empty, hidden, missed, hit, sunk)
    def get_state(self, row, col):
        return self.board[row][col]

    # Shoot at [x][y]
    # Checks the current state at those coordinates, updates, and returns the new state
    def shoot(self, x, y):
        status = self.board[x][y]

        # Checks the current state of the block:
        if status == Cell.EMPTY:
            self.board[x][y] = Cell.MISS    # If current state is EMPTY --> update to a MISS
        elif status == Cell.HIDDEN:
            self.board[x][y] = Cell.HIT     # If current state is HIDDEN SHIP --> update to a HIT

        return self.board[x][y]             # Return the updated board state


    def is_game_over(self):
        if self.moves >= 100 or self.sunk == 5:
            return True
        else:
            return False

    # Returns the ships sunk and their coordinates on the board
    def get_sunken_ships(self):
        return self.sunken_ship_coordinates

    '''# This is needed for Monte Carlo
    class BoardSimulation(Board):

    def __init__(self, attack_board):
        Board.__init__(self, attack_board.size)
        self.attack_board = attack_board
        self.board = self.attack_board.get_board()
        self.square_states = self.board.get_state()

    def simulate_ship(self):
        # Select a random ship length that hasnt been destroyed yet, and place it onto the board at a valid location
        ind = np.random.choice(np.nonzero(self.attack_board.ship_counts)[0])
        leng = self.attack_board.available_ships[ind]

        # Check if the ship intersects and existing hit, if it does then we want to emphasis it to the algorithm
        intersection = 0
        for coordin in self.ship[0]:
            if coordin in self.attack_board.hits:
                intersection += 1
        if intersection == len(self.ship[0]):
            intersection = 0

        # Make sure to remove all non ship squares to not mess with frequencies
        sim_board = self.get_board()
        # sim_board[sim_board != self.square_states[Cell.MISS]] == 0

        return sim_board, intersection

    # Resets the simulation
    def update_sim(self, attack_board):
        self.__init__(attack_board)'''
