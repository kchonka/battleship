# Class representing an AI object

from ship import Ship, Direction
from board import Board, Cell
from random import seed, randint
import time


class AI:
    def __init__(self):
        self.board = Board()                        # AI's board
        self.moves = []                             # List of all previous moves the AI has made (coordinates)
        self.ship = Ship()                          # Memory object

    # Returns the board array list (not a Board object) --> calls Board's get_board
    def get_board(self):
        return self.board.get_board()

    # Returns the state of the board (Empty, hidden, missed, hit, sunk)
    def get_state(self, row, col):
        return self.board.get_state(row, col)

    # Checks for sunken ships and updates the board
    def check_sunken_ships(self):
        self.board.check_sunken_ships()

    # Check if loss: (the AI is still in the game if all five of its ships are NOT sunk)
    def check_loss(self):
        sunken_ships = self.board.get_sunken_ships()
        if sunken_ships < 5:
            return False
        else:
            return True

    def random_placement(self):
        # Randomly choose orientation
        orientation = ['h', 'v'][randint(0, 1)]
        '''
        if is empty position
            orientation of ship = h or v randomly
            if vertical, all starting pos y <= 6 == (6,0)
                place the carrier on the board
                update carrier location to add coordinates
            if horizontal, all starting  pos x<= 6 == (0,6)
                place the carrier on the board
                update carrier location to add coordinates
        else if not empty
            search for empty spot
        '''
        # Check if the spot on the grid is empty
        if self.ship.is_empty():
            if orientation == 'h':
                x = randint(0, 6)
                y = randint(0, 6)
                carrier = self.ship.add_coordinates([y, x])
                return self.board.add_ship("carrier", carrier)
            elif orientation == 'v':
                x = randint(0, 6)
                y = randint(0, 6)
                carrier = self.ship.add_coordinates([y, x])
                return self.board.add_ship("carrier", carrier)

        '''
        if is empty position
            orientation of ship = h or v randomly
            if vertical, all starting pos y <= 7 == (7,0)
                place the battleship on the board
                update battleship location to add coordinates
            if horizontal, all starting  pos x<= 7 == (0,7)
                place the battleship on the board
                update battleship location to add coordinates
        else if not empty
            search for empty spot
        '''

        # Check if the spot on the grid is empty
        if self.ship.is_empty():
            if orientation == 'h':
                x = randint(0, 7)
                y = randint(0, 7)
                battleship = self.ship.add_coordinates([y, x])
                return self.board.add_ship("battleship", battleship)
            elif orientation == 'v':
                x = randint(0, 6)
                y = randint(0, 6)
                battleship = self.ship.add_coordinates([y, x])
                return self.board.add_ship("battleship", battleship)

        '''
        if is empty position
            orientation of ship = h or v randomly
            if vertical, all starting pos y <= 8 == (8,0)
                place the cruiser on the board
                update cruiser location to add coordinates
            if horizontal, all starting  pos x<= 8 == (0,8)
                place the cruiser on the board
                update cruiser location to add coordinates
        else if not empty
            search for empty spot
        '''
        # Check if the spot on the grid is empty
        if self.ship.is_empty():
            if orientation == 'h':
                x = randint(0, 7)
                y = randint(0, 7)
                cruiser = self.ship.add_coordinates([y, x])
                return self.board.add_ship("cruiser", cruiser)
            elif orientation == 'v':
                x = randint(0, 6)
                y = randint(0, 6)
                cruiser = self.ship.add_coordinates([y, x])
                return self.board.add_ship("cruiser", cruiser)
        '''
        if is empty position
            orientation of ship = h or v randomly
            if vertical, all starting pos y <= 8 == (8,0)
                place the submarine on the board
                update ship location to add coordinates
            if horizontal, all starting  pos x<= 8 == (0,8)
                place the submarine on the board
                update submarine location to add coordinates
        else if not empty
            search for empty spot
        '''
        # Check if the spot on the grid is empty
        if self.ship.is_empty():
            if orientation == 'h':
                x = randint(0, 7)
                y = randint(0, 7)
                submarine = self.ship.add_coordinates([y, x])
                return self.board.add_ship("submarine", submarine)
            elif orientation == 'v':
                x = randint(0, 6)
                y = randint(0, 6)
                submarine = self.ship.add_coordinates([y, x])
                return self.board.add_ship("submarine", submarine)
        '''
        if is empty position
            orientation of ship = h or v randomly
            if vertical, all starting pos y <= 9 == (9,0)
                place the destroyer on the board
                update destroyer location to add coordinates
            if horizontal, all starting  pos x<= 9 == (0,9)
                place the destroyer on the board
                update destroyer location to add coordinates
        else if not empty
            search for empty spot
        '''
        # Check if the spot on the grid is empty
        if self.ship.is_empty():
            if orientation == 'h':
                x = randint(0, 7)
                y = randint(0, 7)
                destroyer = self.ship.add_coordinates([y, x])
                return self.board.add_ship("destroyer", destroyer)
            elif orientation == 'v':
                x = randint(0, 6)
                y = randint(0, 6)
                destroyer = self.ship.add_coordinates([y, x])
                return self.board.add_ship("destroyer", destroyer)

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
        x = coordinates[0]
        y = coordinates[1]

        if direction == Direction.UP:
            # Check if moving up is possible:
            if y - 1 > 0:
                new_coordinates = [x, y - 1]
                if new_coordinates not in self.moves:
                    self.moves.append(new_coordinates)
                    return new_coordinates[0], new_coordinates[1]
                else:
                    return self.attackUDLR(new_coordinates, direction)

            else:  # moving up not possible, increment direction
                self.ship.increment_direction()
                direction = self.ship.get_direction()
                return self.attackUDLR(coordinates, direction)

        if direction == Direction.DOWN:
            # Check if moving down is possible:
            if y + 1 < 11:
                new_coordinates = [x, y + 1]
                if new_coordinates not in self.moves:
                    self.moves.append(new_coordinates)
                    return new_coordinates[0], new_coordinates[1]
                else:
                    return self.attackUDLR(new_coordinates, direction)
            else:
                self.ship.increment_direction()
                direction = self.ship.get_direction()
                return self.attackUDLR(coordinates, direction)

        if direction == Direction.LEFT:
            # Check if moving left is possible:
            if x - 1 > 0:
                new_coordinates = [x - 1, y]
                if new_coordinates not in self.moves:
                    self.moves.append(new_coordinates)
                    return new_coordinates[0], new_coordinates[1]
                else:
                    return self.attackUDLR(new_coordinates, direction)
            else:
                self.ship.increment_direction()
                direction = self.ship.get_direction()
                return self.attackUDLR(coordinates, direction)

        if direction == Direction.RIGHT:
            new_coordinates = [x + 1, y]
            if new_coordinates not in self.moves:
                self.moves.append(new_coordinates)
                return new_coordinates[0], new_coordinates[1]
            else:
                return self.attackUDLR(new_coordinates, direction)

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
        else:  # Else if not first move:

            if last_move_state == Cell.HIT:
                self.ship.add_coordinates(self.moves[-1])
                direction = self.ship.get_direction()
                coordinates = self.moves[-1]
                return self.attackUDLR(coordinates, direction)

            elif last_move_state == Cell.SUNK:
                # Last move sunk the ship, so on this turn make a random shot
                self.ship.clear()
                return self.random_shot()

            else:  # last_move_state was a MISS
                if self.ship.is_empty() is False:  # Ship in progress, work from there
                    self.ship.increment_direction()
                    direction = self.ship.get_direction()
                    origin = self.ship.get_origin()

                    return self.attackUDLR(origin, direction)

                else:  # Random shot
                    return self.random_shot()
