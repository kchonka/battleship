# Class representing a board object
# Both the player and AI classes will use this class as their board

HEIGHT = 10
WIDTH = 10

'''
0 = EMPTY CELL
1 = CELL WITH HIDDEN SHIP PIECE
2 = A MISS (CELL THAT WAS EMPTY AND HIT)
3 = A HIT (CELL WITH A SHIP THAT WAS ATTACKED)
'''

class Board:
    def __init__(self):
        self.board = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]

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

    def update(self, x, y, change):
        self.board[x][y] == change


new_board = Board()
print(new_board)

