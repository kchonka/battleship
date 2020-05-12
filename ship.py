from enum import Enum


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# Small memory class for the AI to store coordinates of the last known ship
class Ship:
    def __init__(self):
        self.origin = []                   # The first / original hit: the "origin" hit
        self.coordinates = []              # List of all the coordinates of the ship
        self.empty = True                  # This object has nothing in it
        self.direction = Direction.UP      # Default to the first direction 'up'

    def clear(self):
        self.origin = []
        self.coordinates = []
        self.direction = Direction.UP
        self.empty = True

    def add_coordinates(self, coordinates):
        self.coordinates.append(coordinates)
        self.origin = self.coordinates[0]
        self.empty = False

    def is_empty(self):
        return self.empty

    def get_coordinates(self):
        return self.coordinates

    # Returns empty list if the origin hit is empty
    def get_origin(self):
        return self.origin

    def get_direction(self):
        return self.direction

    def increment_direction(self):
        if self.direction == Direction.UP:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.RIGHT
