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
        self.q_table = np.zeros([100,5])            #[[0 for x in range(9)] for y in range(100)]
        '''self. move_simulation = []               # This is the number of moves that it has to simulate
        self.priority = 5                           # This is the priority given to simulations that intersect hits'''

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

    '''# This is the implementation of the Monte Carlo Algorithm
    def monte_carlo(self, out_path)
        simulations = []

        for i in range(self.move_simulation):
            self.board.simulate_board.update(self.board.get_state())
            brd, intersection = self.board.simulate_board.simulate_ship()

            # If we intersect a hit take account priority and overlap
            if intersection:
                for i in range(self.priority):
                    for i in range(intersection):
                        self.simulations.append(brd)
            self.simulations.append(brd)

        # Mean the ship simulations down the stacked axis to calculate percentages
        simulations = np.array(simulations)
        percentages = np.mean(simulations, axis=0)

        return percentages
        
    # This allows for the AI to run the game for testing
    def run_testing(self):
        res = self.board.attack_board()
        done_testing = False
        count = 0
        while not done:
            count += 1
            s, done = .monte_carlo(res)
        return np.count_nonzero(s.get_board() == 0)
        
    # Uses the MC algorithm to predict move against the player and moves
    def make_move(self)
        return self.monte_carlo(self.board.attack_board)'''

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
    def random_attack(self, last_move_state, sunken_ships):
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

        if action == Action.UP:
            action_index = 0
        elif action == Action.DOWN:
            action_index = 1
        elif action == Action.LEFT:
            action_index = 2
        elif action == Action.RIGHT:
            action_index = 3
        elif action == Action.HUNT:
            action_index = 4

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
    def get_actions(self, cur_pos):
        x = cur_pos[0]
        y = cur_pos[1]

        possible_actions = [] # List of all possible actions/movable directions

        if y - 1 > 0:
            new_coordinates = [x, y-1]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.UP)

        if y + 1 < 11:
            new_coordinates = [x, y+1]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.DOWN)

        if x - 1 > 0:
            new_coordinates = [x-1, y]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.LEFT)

        if x + 1 < 11:
            new_coordinates = [x+1, y]
            if new_coordinates not in self.moves:
                possible_actions.append(Action.RIGHT)

        if not possible_actions:
            possible_actions.append(Action.HUNT)

        return possible_actions


    # Helper method used by Q_Learned_AI
    # Takes in a list of possible actions
    def exploit_environment(self, last_pos, possible_actions, last_move_state):
        rewards = []
        actions = []

        for action in possible_actions:
            # Find the next pos as a result of taking the above action:
            next_pos = self.move_by_one(last_pos, action)
            next_index = self.get_qtable_pos(next_pos[0], next_pos[1])
            action_index = self.get_action_index(action)

            reward = self.q_table[next_index][action_index]
            actions.append(action)
            rewards.append(reward)

        # Choose the max reward
        maximum = max(rewards)

        if maximum == 0 and last_move_state == Cell.HIT and self.actions[-1] != Action.HUNT:
            action = self.actions[-1]
        else:
            max_index = rewards.index(maximum)
            action = actions[max_index]

        next_pos = self.move_by_one(last_pos, action)

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
                last_coordinates = [last_pos[0], last_pos[1]]
                # Add last_pos to active hits:
                self.active_hits.append(last_coordinates)
                # Get all possible actions after a hit
                possible_actions = self.get_actions(last_pos)
                # Return the row & col that correspond to the greatest reward
                return self.exploit_environment(last_pos, possible_actions, last_move_state)

            elif last_move_state == Cell.SUNK:
                # Remove from active hits
                for coordinates in sunken_ships:
                    if coordinates in self.active_hits:
                        self.active_hits.remove(coordinates)

                # Check if active hits is still not empty:
                if self.active_hits:
                    i = 0
                    last_pos = self.active_hits[0] # use the first active hit to work with
                    possible_actions = self.get_actions(last_pos)

                    # If the only action available is to hunt/shoot elsewhere,
                    # choose the next active position
                    while Action.HUNT in possible_actions and len(self.active_hits) > i+1:
                        i += 1
                        last_pos = self.active_hits[i] # use the first active hit to work with
                        possible_actions = self.get_actions(last_pos)

                    return self.exploit_environment(last_pos, possible_actions, last_move_state)

            # Last move resulted in a miss but there are other active hits
            elif last_move_state == Cell.MISS and self.active_hits:
                i = 0
                last_pos = self.active_hits[i] # use the first active hit to work with
                possible_actions = self.get_actions(last_pos)

                # If the only action available is to hunt/shoot elsewhere,
                # choose the next active position
                while Action.HUNT in possible_actions and len(self.active_hits) > i+1:
                    i += 1
                    last_pos = self.active_hits[i] # use the first active hit to work with
                    possible_actions = self.get_actions(last_pos)

                return self.exploit_environment(last_pos, possible_actions, last_move_state)


            # else, explore environment
            # This code gets executed if there was a previous MISS
            possible_actions = self.get_actions(last_pos)
            # explore
            action = random.choice(possible_actions)

            # Find the next pos as a result of taking the above action:
            next_pos = self.move_in_direction(action)
            self.actions.append(action)
            self.moves.append(next_pos)

            return next_pos[0], next_pos[1]

    # Move by one with the 'action' (up, dowm left, right)
    # Returns the next coordinates as a result of moving by 1 with the action
    def move_by_one(self, cur_pos, action):
        x = cur_pos[0]
        y = cur_pos[1]

        if action == Action.UP:
            return [x, y-1]
        elif action == Action.DOWN:
            return [x, y+1]
        elif action == Action.LEFT:
            return [x-1, y]
        elif action == Action.RIGHT:
            return [x+1, y]
        elif action == Action.HUNT:
            seed(time.time())
            x = randint(1, 10)
            y = randint(1, 10)
            return [x, y]

    def move_in_direction(self, action):
        coordinates = self.moves[-1]
        x = coordinates[0]
        y = coordinates[1]

        # Move anywhere up
        if action == Action.UP:
            room_to_move = y -1

            while coordinates in self.moves:
                seed(time.time())
                y = randint(1, room_to_move)
                coordinates = [x,y]
                if coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return coordinates[0], coordinates[1]

        # Move anywhere down:
        elif action == Action.DOWN:
            room_to_move = 10 - y

            while coordinates in self.moves:
                seed(time.time())
                y = randint(1, room_to_move)
                coordinates = [x,y]
                if coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return coordinates[0], coordinates[1]

        # Move anywhere left:
        elif action == Action.LEFT:
            room_to_move = x - 1

            while coordinates in self.moves:
                seed(time.time())
                x = randint(1, room_to_move)
                coordinates = [x,y]
                if coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return coordinates[0], coordinates[1]

        # Move anywhere right:
        elif action == Action.RIGHT:
            room_to_move = 10 - x

            while coordinates in self.moves:
                seed(time.time())
                x = randint(1, room_to_move)
                coordinates = [x,y]
                if coordinates not in self.moves:
                    self.moves.append(coordinates)
                    return coordinates[0], coordinates[1]

        elif action == Action.HUNT:
            seed(time.time())
            x = randint(1, 10)
            y = randint(1, 10)

            return [x, y]
