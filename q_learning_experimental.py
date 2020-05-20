## *** NOT USED IN THE GAME *****
## Use to attempt to pre-train the agent for Q-Learning. 

from board import Board, Cell, Action
import random
import numpy as np
from random import seed, randint
import time
import math
import copy

def get_q_table_pos(x, y):
    return ((y - 1) * 10) + x - 1

def get_reward(state):
    reward = None
    if state == Cell.HIT or state == Cell.HIDDEN:
        reward = 1
    elif state == Cell.MISS or state == Cell.EMPTY:
        reward = -1
    elif state == Cell.SUNK:
        reward = 5

    return reward

def get_action_index(action):
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

def get_actions(cur_pos, explored):
    x = cur_pos[0]
    y = cur_pos[1]

    possible_actions = [] # List of all possible actions/movable directions

    if y - 1 > 0:
        new_coordinates = [x, y-1]
        if new_coordinates not in explored:
            possible_actions.append(Action.UP)

    if y + 1 < 11:
        new_coordinates = [x, y+1]
        if new_coordinates not in explored:
            possible_actions.append(Action.DOWN)

    if x - 1 > 0:
        new_coordinates = [x-1, y]
        if new_coordinates not in explored:
            possible_actions.append(Action.LEFT)

    if x + 1 < 11:
        new_coordinates = [x+1, y]
        if new_coordinates not in explored:
            possible_actions.append(Action.RIGHT)

    possible_actions.append(Action.HUNT)

    return possible_actions

# Move by one with the 'action' (up, dowm left, right)
# Returns the next coordinates as a result of moving by 1 with the action
def move_by_one(cur_pos, action, explored):
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

def move_in_direction(action):
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

# ------------------------------------------
# Define the player board:
player_board = Board()
player_board.add_ship("battleship", [[5,2], [6,2], [7,2], [8,2], [9,2]])
player_board.add_ship("carrier", [[2,7], [2,8], [2,9], [2,10]])
player_board.add_ship("cruiser", [[1,4], [2,4], [3,4]])
player_board.add_ship("submarine", [[6,7], [7,7], [7,8]])
player_board.add_ship("destroyer", [[9,4], [9,5]])

# state = [x, y] (100 of them)
# 4 actions --> Up, Down, Left, Right
# q_table = np.zeros([observation space, action space)
q_table = np.zeros([100,5])

# epsilon percent we want to explore:
epsilon = 0.5

learning_rate = 0.1
discount_rate = .99

max_steps_per_episode = 100 # Only 100 moves possible on the grid

for episode in range(100):
    # Get starting position: (choose random spot on the board)
    # Choose random staring position:
    seed(time.time())
    x = randint(1, 10)
    y = randint(1, 10)

    cur_pos = [x, y]
    cur_state = player_board.shoot(cur_pos[0], cur_pos[1])

    explored = [cur_pos]

    for step in range(max_steps_per_episode):   # while the game is not over

        # Get all possible next positions from the current pos:
        possible_actions = get_actions(cur_pos, explored)

        # Convert the coordinates to a number representing the state on the board:
        index = get_q_table_pos(cur_pos[0], cur_pos[1])

        # Exploration-exploitation trade-off:
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > epsilon:   #exploit, check learned values

            values = []
            actions = []

            # Select the action with the greatest q value
            for action in possible_actions:
                action_index = get_action_index(action)
                value = q_table[index][action_index]
                values.append(value)
                actions.append(action)

            # Choose the max reward
            maximum = max(values)
            max_index = values.index(maximum)
            action = actions[max_index]

        else:
            # explore, sample an action randomly
            # Select any one action randomly:
            action = random.choice(possible_actions)

        # Find the next pos as a result of taking the above action:
        next_pos = move_by_one(cur_pos, action, explored)
        # Convert next_pos for indexing:
        next_index = get_q_table_pos(next_pos[0], next_pos[1])

        # Convert 'action' to an int for indexing
        action_index = get_action_index(action)

        status = player_board.get_state(next_pos[0], next_pos[1])
        reward = get_reward(status)

        old_value = q_table[index][action_index]
        next_max = np.max(q_table[next_index])
        new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_rate * next_max)

        # Update q_table:
        q_table[index][action_index] = new_value

        cur_pos = next_pos
        explored.append(next_pos)

for i in range(100):
    print(i), print(q_table[i])
