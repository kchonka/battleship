# Class representing an AI object

from ship import Ship, Direction
from board import Board, Cell, Action
from random import seed, randint
import random
import time
import numpy as np
import math


class AI:
    def __init__(self):
        self.board = Board()                        # AI's board
        self.moves = []                             # List of all previous moves the AI has made (coordinates)
        self.actions = []                           # List of all previous actions the AI made (U, D, L, R)
        self.ship = Ship()                          # Memory object
        self.active_hits = []                       # Ships that have been hit but not sunk yet
        self.q_table = np.zeros([100,9])            #[[0 for x in range(9)] for y in range(100)]

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
        sunken_ships = self.board.get_number_sunken_ships()
        if sunken_ships < 5:
            return False
        else:
            return True

    def random_placement(self):
        carrier = []
        cruiser = []
        battleship = []
        submarine = []
        destroyer = []

        all_positions = []  # Used to keep track of no longer valid positions

        # ADD CARRIER - Length 5
        # Randomly choose orientation
        orientation = ['h', 'v'][randint(0, 1)]
        if orientation == 'h':
            # Generate the start point:
            x = randint(1, 6)
            y = randint(1, 6)
            for i in range(5):
                coordinates = [x+i,y]
                carrier.append(coordinates)
                all_positions.append(coordinates)
        elif orientation == 'v':
            x = randint(1, 6)
            y = randint(1, 6)
            for i in range(5):
                coordinates = [x,y+i]
                carrier.append(coordinates)
                all_positions.append(coordinates)

        # ADD BATTLESHIP - Length 4
        # Randomly choose orientation
        orientation = ['h', 'v'][randint(0, 1)]
        invalid = True # boolean to keep track of validity
        while invalid:
            if orientation == 'h':
                # Generate the start point:
                x = randint(1, 7)
                y = randint(1, 7)
                for i in range(4):
                    coordinates = [x+i,y]
                    if coordinates in all_positions:
                        battleship.clear()
                        invalid = True
                        break
                    else:
                        battleship.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

            elif orientation == 'v':
                # Generate the start point:
                x = randint(1, 7)
                y = randint(1, 7)
                for i in range(4):
                    coordinates = [x,y+i]
                    if coordinates in all_positions:
                        battleship.clear()
                        invalid = True
                        break
                    else:
                        battleship.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)


        # ADD CRUISER - Length 3
        # Randomly choose orientation
        orientation = ['h', 'v'][randint(0, 1)]
        invalid = True # boolean to keep track of validity
        while invalid:
            if orientation == 'h':
                # Generate the start point:
                x = randint(1, 8)
                y = randint(1, 8)
                for i in range(3):
                    coordinates = [x+i,y]
                    if coordinates in all_positions:
                        cruiser.clear()
                        invalid = True
                        break
                    else:
                        cruiser.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

            elif orientation == 'v':
                # Generate the start point:
                x = randint(1, 8)
                y = randint(1, 8)
                for i in range(3):
                    coordinates = [x,y+i]
                    if coordinates in all_positions:
                        cruiser.clear()
                        invalid = True
                        break
                    else:
                        cruiser.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

        # ADD SUBMARINE - Length 3
        # Randomly choose orientation
        orientation = ['h', 'v'][randint(0, 1)]
        invalid = True # boolean to keep track of validity
        while invalid:
            if orientation == 'h':
                # Generate the start point:
                x = randint(1, 8)
                y = randint(1, 8)
                for i in range(3):
                    coordinates = [x+i,y]

                    if coordinates in all_positions:
                        submarine.clear()
                        invalid = True
                        break
                    else:
                        submarine.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

            elif orientation == 'v':
                # Generate the start point:
                x = randint(1, 8)
                y = randint(1, 8)
                for i in range(3):
                    coordinates = [x,y+i]

                    if coordinates in all_positions:
                        submarine.clear()
                        invalid = True
                        break
                    else:
                        submarine.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

        # ADD DESTROYER - Length 2
        # Randomly choose orientation
        orientation = ['h', 'v'][randint(0, 1)]
        invalid = True # boolean to keep track of validity
        while invalid:
            if orientation == 'h':
                # Generate the start point:
                x = randint(1, 9)
                y = randint(1, 9)
                for i in range(2):
                    coordinates = [x+i,y]

                    if coordinates in all_positions:
                        destroyer.clear()
                        invalid = True
                        break
                    else:
                        destroyer.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

            elif orientation == 'v':
                # Generate the start point:
                x = randint(1, 8)
                y = randint(1, 8)
                for i in range(2):
                    coordinates = [x,y+i]

                    if coordinates in all_positions:
                        destroyer.clear()
                        invalid = True
                        break
                    else:
                        destroyer.append(coordinates)
                        invalid = False

                if invalid is False:
                    for pair in battleship:
                        all_positions.append(pair)

        self.board.add_ship("carrier", carrier)
        self.board.add_ship("battleship", battleship)
        self.board.add_ship("cruiser", cruiser)
        self.board.add_ship("submarine", submarine)
        self.board.add_ship("destroyer", destroyer)

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


    # Returns a numerical position on the qtable grid corresponding to the row & col
    def get_qtable_pos(self, x, y):
        return ((y - 1) * 10) + x - 1

    def get_action_index(self, action):
        action_index = None

        if action == Action.UP1:
            action_index = 0
        elif action == Action.DOWN1:
            action_index = 1
        elif action == Action.LEFT1:
            action_index = 2
        elif action == Action.RIGHT1:
            action_index = 3
        elif action == Action.UP2:
            action_index = 4
        elif action == Action.DOWN2:
            action_index = 5
        elif action == Action.LEFT2:
            action_index = 6
        elif action == Action.RIGHT2:
            action_index = 7
        elif action == Action.HUNT:
            action_index = 8

        return action_index

    def get_reward(self, state):
        if state == Cell.HIT:
            reward = 1
        elif state == Cell.MISS:
            reward = -1
        elif state == Cell.SUNK:
            reward = 5

        return reward

    # These are only actions to do when the AI makes an active hit:
    # Searchs up, down, left, and right one space
    def get_hit_actions(self, cur_pos):
        x = cur_pos[0]
        y = cur_pos[1]

        possible_actions = [] # List of all possible actions/movable directions

        if y - 1 > 0:
            new_coordinates = [x, y-1]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.UP1)

        if y + 1 < 11:
            new_coordinates = [x, y+1]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.DOWN1)

        if x - 1 > 0:
            new_coordinates = [x-1, y]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.LEFT1)

        if x + 1 < 11:
            new_coordinates = [x+1, y]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.RIGHT1)

        return possible_actions

    # Takes a pair of coordinates representing a state/cell on the board
    # Returns a list of all the possible moves: Up, down, left, right
    def get_explore_actions(self, cur_pos):
        x = cur_pos[0]
        y = cur_pos[1]

        possible_actions = [] # List of all possible actions/movable directions

        if y - 2 > 0:
            new_coordinates = [x, y-2]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.UP2)

        if y + 2 < 11:
            new_coordinates = [x, y+2]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.DOWN2)

        if x - 2 > 0:
            new_coordinates = [x-2, y]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.LEFT2)

        if x + 2 < 11:
            new_coordinates = [x+2, y]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.RIGHT2)

        if not possible_actions:
            possible_actions.append(Action.HUNT)

        return possible_actions

    # Helper method used by Q_Learned_AI
    # Takes in a list of possible actions
    def exploit_environment(self, last_pos, possible_actions):
        rewards = []
        actions = []

        for action in possible_actions:
            # Find the next pos as a result of taking the above action:
            next_pos = self.board.get_next_position(last_pos, action)
            next_index = self.get_qtable_pos(next_pos[0], next_pos[1])
            action_index = self.get_action_index(action)

            reward = self.q_table[next_index][action_index]
            actions.append(action)
            rewards.append(reward)

        # Choose the max reward
        maximum = max(rewards)
        max_index = rewards.index(maximum)
        action = actions[max_index]

        next_pos = self.board.get_next_position(last_pos, action)

        self.moves.append(next_pos)
        self.actions.append(action)
        return next_pos[0], next_pos[1]

    # Main method for the Q Learning AI
    # Returns a row & col for the next strike
    def Q_Learning_AI(self, last_move_state, sunken_ships):

        learning_rate = 0.1
        discount_rate = .99

        # If this is the first move:
        if not self.moves:
            # Make a random move:
            seed(time.time())
            row = randint(1, 10)
            col = randint(1, 10)

            coordinates = [row, col]
            self.moves.append(coordinates)
            self.actions.append(Action.HUNT)
            return row, col
        # This is not the first move
        else:
            # UPDATE THE QTABLE FOR THE LAST MOVE
            last_pos = self.moves[-1]
            last_action = self.actions[-1]

            reward = self.get_reward(last_move_state)

            last_pos_index = self.get_qtable_pos(last_pos[0], last_pos[1])
            last_action_index = self.get_action_index(last_action)

            old_value = self.q_table[last_pos_index][last_action_index]
            next_max = np.max(self.q_table[last_pos_index])

            # Compute the next value
            new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_rate * next_max)

            # Update the q_table:
            self.q_table[last_pos_index][last_action_index] = new_value

            # -------------
            # CHOOSE THE NEXT MOVE:

            if last_move_state == Cell.HIT:
                # Add last_pos to active hits:
                self.active_hits.append(last_pos)
                # Get all possible actions after a hit
                possible_actions = self.get_hit_actions(last_pos)
                # Return the row & col that correspond to the greatest reward
                return self.exploit_environment(last_pos, possible_actions)

            # Last move resulted in a miss but there are other active hits
            elif last_move_state == Cell.MISS and self.active_hits:
                last_pos = self.active_hits[0] # use the first active hit to work with
                possible_actions = self.get_hit_actions(last_pos)
                return self.exploit_environment(last_pos, possible_actions)

            elif last_move_state == Cell.SUNK:

                # Remove from active hits
                for coordinates in sunken_ships:
                    if coordinates in self.active_hits:
                        self.active_hits.remove(coordinates)

                # Check if active hits is still not empty:
                if self.active_hits:
                    last_pos = self.active_hits[0] # use the first active hit to work with
                    possible_actions = self.get_hit_actions(last_pos)

                    return self.exploit_environment(last_pos, possible_actions)


            # else, explore environment
            # This code gets executed if there was a previous MISS
            possible_actions = self.get_explore_actions(last_pos)
            action = random.choice(possible_actions)

            # Find the next pos as a result of taking the above action:
            next_pos = self.board.get_next_position(last_pos, action)
            self.actions.append(action)
            self.moves.append(next_pos)

            return next_pos[0], next_pos[1]
