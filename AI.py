# Class representing an AI object

from ship import Ship, Direction
from board import Board, Cell
from random import seed, randint
import time


class AI:
    def __init__(self):
        self.board = Board()                        # AI's board
        self.moves = []                             # List of all previous moves the AI has made (coordinates)
        self.ship = Ship()                          # Small memory object to store hit info

    # Returns the board array list (not a Board object) --> calls Board's get_board
    def get_board(self):
        return self.board.get_board()

    # Returns the state of the board (Empty, hidden, missed, hit, sunk)
    def get_state(self, row, col):
        return self.board.get_state(row, col)

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

    # Helper method for random_attack
    # Selects a random cell for attack
    def random_shot(self):
        coordinates = self.moves[-1]
        while coordinates in self.moves:
            seed(time.time())
            row = randint(1, 10)
            col = randint(1, 10)

            coordinates = [row, col]

            if coordinates not in self.moves:
                self.moves.append(coordinates)
                return coordinates[0], coordinates[1]

    # Helper method for random_attack
    # Takes in a pair of coordinates and a direction
    # # Returns a new move following UDLR (Up, Down, Left, Right) order
    def attackUDLR(self, coordinates, direction):
        last_row = coordinates[0]
        last_col = coordinates[1]

        if direction == Direction.UP:
            new_coordinates = [last_row, last_col - 1]
            print("UP" + str(new_coordinates))
            if new_coordinates not in self.moves:
                self.moves.append(new_coordinates)
                return new_coordinates[0], new_coordinates[1]

        elif direction == Direction.DOWN:
            new_coordinates = [last_row, last_col + 1]
            print("DOWN" + str(new_coordinates))
            if new_coordinates not in self.moves:
                self.moves.append(new_coordinates)
                return new_coordinates[0], new_coordinates[1]

        elif direction == Direction.LEFT:
            new_coordinates = [last_row - 1, last_col]
            print("LEFT" + str(new_coordinates))
            if new_coordinates not in self.moves:
                self.moves.append(new_coordinates)
                return new_coordinates[0], new_coordinates[1]

        elif direction == Direction.RIGHT:
            new_coordinates = [last_row + 1, last_col]
            print("RIGHT" + str(new_coordinates))
            if new_coordinates not in self.moves:
                self.moves.append(new_coordinates)
                return new_coordinates[0], new_coordinates[1]

    # Takes in one argument: The state of the last attack
    def random_attack(self, last_move_state):

        # If this is the first move:
        if not self.moves:
            # Make random selection
            seed(time.time())
            row = randint(1, 10)
            col = randint(1, 10)

            coordinates = [row, col]
            self.moves.append(coordinates)
            return row, col
        else:   # Else if not first move:

            if last_move_state == Cell.HIT:
                self.ship.add_coordinates(self.moves[-1])
                direction = self.ship.get_direction()
                coordinates = self.moves[-1]
                return self.attackUDLR(coordinates, direction)

            elif last_move_state == Cell.SUNK:
                # Last move sunk the ship, so on this turn make a random shot
                self.ship.clear()
                return self.random_shot()

            else:   # last_move_state was a MISS
                if self.ship.is_empty() is False:   # Ship in progress, work from there
                    self.ship.increment_direction()
                    direction = self.ship.get_direction()
                    origin = self.ship.get_origin()

                    return self.attackUDLR(origin, direction)

                else:     # Random shot
                    return self.random_shot()


