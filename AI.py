# Class representing an AI object

from board import Board, Cell
from random import seed, randint
import time

class AI:
    def __init__(self):
        self.board = Board()
        self.moves = []

    # Returns the board array list (not a Board object) --> calls Board's get_board
    def get_board(self):
        return self.board.get_board()

    # Checks for sunken ships and updates the board
    def check_sunken_ships(self):
        self.board.check_sunken_ships()

    def random_placement(self):
        # ** must implement random placement on any given turn**
        # Sample example:
        carrier = [[10, 4], [10, 5], [10, 6], [10, 7], [10, 8]]
        battleship = [[2, 2], [2, 3], [2, 4], [2, 5]]
        cruiser = [[7, 2], [8, 2], [9, 2]]
        submarine = [[3, 9], [4, 9], [5, 9]]
        destroyer = [[5, 5], [6, 5]]

        self.board.add_ship("carrier", carrier)
        self.board.add_ship("battleship", battleship)
        self.board.add_ship("cruiser", cruiser)
        self.board.add_ship("submarine", submarine)
        self.board.add_ship("destroyer", destroyer)

    def monte_carlo_placement(self):
        pass

    # Get attacked BY the player opponent
    # Returns the new state at board[row][col]
    # Coordinates is a list pair of Board coordinates that the player fired at
    def suffer_attack(self, coordinates):
        row = coordinates[0]
        col = coordinates[1]
        return self.board.shoot(row, col)

    # Takes in one argument: The state of the last attack
    def random_attack(self, last_move_state):

        # If this is the first move:
        if not self.moves:
            seed(time.time())
            row = randint(1, 10)
            col = randint(1, 10)

            coordinates = [row, col]
            self.moves.append(coordinates)

            return row, col
        # Else:
        else:
            coordinates = self.moves[-1]

            if last_move_state == Cell.HIT:
                # If there was a hit: attack up, down, left, right
                last_row = coordinates[0]
                last_col = coordinates[1]

                print("last coordinates: " + str(coordinates))

                # UP:
                new_coordinates = [last_row, last_col - 1]
                print("UP" + str(new_coordinates))
                if new_coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return new_coordinates[0], new_coordinates[1]

                # DOWN:
                new_coordinates = [last_row, last_col + 1]
                print("DOWN" + str(new_coordinates))
                if new_coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return new_coordinates[0], new_coordinates[1]

                # LEFT:
                new_coordinates = [last_row - 1, last_col]
                print("LEFT" + str(new_coordinates))
                if new_coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return new_coordinates[0], new_coordinates[1]

                # RIGHT:
                new_coordinates = [last_row + 1, last_col]
                print("RIGHT" + str(new_coordinates))
                if new_coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return new_coordinates[0], new_coordinates[1]

            else:
                while coordinates in self.moves:
                    seed(time.time())
                    row = randint(1, 10)
                    col = randint(1, 10)

                    coordinates = [row, col]

                    if coordinates not in self.moves:
                        self.moves.append(coordinates)
                        return coordinates[0], coordinates[1]

