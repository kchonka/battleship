# Kat Chonka & Denysse Cunza

# Main Battleship game file
# This file contains the UI display code along with the game logic.
import pygame
import math
from board import Board, Cell
from player import Player
from AI import AI

pygame.init()

# Color definition:
BLUE = (45, 145, 233)
LIGHT_BLUE = (153, 153, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (232, 150, 19)
LIGHT_RED = (230, 90, 85)
DARK_RED = (235, 52, 79)
PURPLE = (147, 40, 173)
LIGHT_YELLOW = (255, 255, 153)
YELLOW = (247, 244, 25)
GREEN = (0, 128, 0)

# Sizes:
total_length = 660
total_width = 960
board_length = 660  # 'board' refers only to the section with the grid
board_width = 660   # 'board' refers only to the section with the grid

# Open a new window
size = (total_width, total_length)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Battleship")

# Create the 5 ships (rectangular objects):
# Rect(left, top, width, height)
carrier = pygame.rect.Rect(700, 210, 60, 300)
battleship = pygame.rect.Rect(780, 210, 60, 240)
cruiser = pygame.rect.Rect(860, 210, 60, 180)
submarine = pygame.rect.Rect(740, 550, 180, 60)
destroyer = pygame.rect.Rect(800, 470, 120, 60)

# Add ships to a list
ships = [carrier, battleship, cruiser, submarine, destroyer]

# Declare other rect objects:
message_box = pygame.Rect(680, 125, 260, 60)    # Section below the start button; displays whose turn it is
action_box = pygame.Rect(680, 200, 260, 440)    # Section below the message box; holds ships at the start

last_AI_attack = None       # The result of the last AI attack (hit, miss, etc.)
last_player_attack = None   # The result of the last player attack (hit, miss, etc.)

player_moves = []           # List of all the moves the player has already taken


# Realigns the ships to the boxes so they are aligned to the rows & cols
# Takes in a ship (Rect) object
def realign(ship):
    x = ship.x
    y = ship.y
    new_x = 60 * round(x / 60)
    new_y = 60 * round(y / 60)
    ship.x = new_x
    ship.y = new_y
    # Add logic to make sure the ships do not overlap **
    # Add logic to make sure the ships do not go outside the board boundaries


# Checks to make sure that all the ships are in the right spaces on the grid to start the game
def check_setup(ships):
    for ship in ships:
        if ship.left < 60:
            return False
        if ship.left + ship.width > 660:
            return False
        if ship.top < 60:
            return False
        if ship.top + ship.height > 660:
            return False

    return True


# Function that converts a ship's x/y coordinates to the row/col coordinates
# RETURNS A LIST OF ALL THE BOARD BLOCKS THAT CONTAIN THE GIVEN SHIP
# RETURNS A LIST OF ALL THE BOARD BLOCKS THAT CONTAIN THE GIVEN SHIP
def get_ship_coordinates(ship):
    coordinates = []

    x = ship.x
    y = ship.y
    width = ship.width
    height = ship.height

    new_x = int(60 * round(x / 60))
    new_y = int(60 * round(y / 60))
    start_row = int(new_y / 60)
    start_col = int(new_x / 60)

    grid_width = int(width / 60)
    grid_height = int(height / 60)

    # Ship is horizontal
    if grid_height == 1:
        for i in range(grid_width):
            row = start_row
            col = start_col + i
            new_pair = [col, row]  # Has to be in the reverse, x denotes cols, y denotes rows
            coordinates.append(new_pair)
    else:  # Ship is vertical (grid_width == 1)
        for i in range(grid_height):
            row = start_row + i
            col = start_col
            new_pair = [col, row]
            coordinates.append(new_pair)

    return coordinates


# Converts the pixel coordinates to the equivalent Battleship grid coordinates
# Used when a user clicks on a certain space --> to get the grid coordinates of the space pressed
# Returns a list [row, col]
def convert_pixel_coordinates(pixel_x, pixel_y):
    board_coordinates = []

    rounded_x = int(60 * math.floor(pixel_x / 60))
    rounded_y = int(60 * math.floor(pixel_y / 60))
    row = int(rounded_x / 60)
    col = int(rounded_y / 60)

    board_coordinates.append(row)
    board_coordinates.append(col)

    return board_coordinates


# Converts a row / col on the grid to the corresponding pixel rectangle and returns it
def convert_grid_coordinates(row, col):
    row = row * 60
    col = col * 60

    square = pygame.rect.Rect(row, col, 60, 60)
    return square


# Takes a list pair of grid coordinates and a state
# Converts grid coordinates to pixel coordinates, colors the space with the new state
def color_board(coordinates, state):
    row = coordinates[0] * 60
    col = coordinates[1] * 60

    square = pygame.rect.Rect(row, col, 60, 60)
    if state == Cell.MISS:
        pygame.draw.rect(screen, GREEN, square)
    elif state == Cell.HIT:
        pygame.draw.rect(screen, DARK_RED, square)


def draw_grid_labels():
    # Horizontal & Vertical X and Y axis
    x_axis = pygame.Rect(0, 0, board_width, 60)
    y_axis = pygame.Rect(0, 0, 60, board_length)
    screen.fill(LIGHT_BLUE, x_axis)
    screen.fill(LIGHT_BLUE, y_axis)

    # Draw vertical & horizontal lines: (Battleship rows
    for x in range(11):
        pos = (x + 1) * 60
        pygame.draw.line(screen, WHITE, [pos, 0], [pos, board_length], 2)
        pygame.draw.line(screen, WHITE, [0, pos], [board_width, pos], 2)

    # Labels for x & y axis:
    pygame.font.init()
    label_font = pygame.font.Font('freesansbold.ttf', 30)
    # Vertical labels (Rows 1-10):
    label1 = label_font.render('1', True, BLACK)
    label2 = label_font.render('2', True, BLACK)
    label3 = label_font.render('3', True, BLACK)
    label4 = label_font.render('4', True, BLACK)
    label5 = label_font.render('5', True, BLACK)
    label6 = label_font.render('6', True, BLACK)
    label7 = label_font.render('7', True, BLACK)
    label8 = label_font.render('8', True, BLACK)
    label9 = label_font.render('9', True, BLACK)
    label10 = label_font.render('10', True, BLACK)
    screen.blit(label1, (20, 75))
    screen.blit(label2, (20, 140))
    screen.blit(label3, (20, 200))
    screen.blit(label4, (20, 260))
    screen.blit(label5, (20, 320))
    screen.blit(label6, (20, 380))
    screen.blit(label7, (20, 440))
    screen.blit(label8, (20, 500))
    screen.blit(label9, (20, 560))
    screen.blit(label10, (15, 620))
    # Horizontal labels (Cols A-J)
    labelA = label_font.render('A', True, BLACK)
    labelB = label_font.render('B', True, BLACK)
    labelC = label_font.render('C', True, BLACK)
    labelD = label_font.render('D', True, BLACK)
    labelE = label_font.render('E', True, BLACK)
    labelF = label_font.render('F', True, BLACK)
    labelG = label_font.render('G', True, BLACK)
    labelH = label_font.render('H', True, BLACK)
    labelI = label_font.render('I', True, BLACK)
    labelJ = label_font.render('J', True, BLACK)
    screen.blit(labelA, (80, 20))
    screen.blit(labelB, (140, 20))
    screen.blit(labelC, (200, 20))
    screen.blit(labelD, (260, 20))
    screen.blit(labelE, (320, 20))
    screen.blit(labelF, (380, 20))
    screen.blit(labelG, (440, 20))
    screen.blit(labelH, (500, 20))
    screen.blit(labelI, (560, 20))
    screen.blit(labelJ, (620, 20))


# Colors the part of the UI below the start button to display whose turn it is
def color_message_box():
    screen.fill(LIGHT_BLUE, message_box)
    pygame.draw.line(screen, BLACK, [680, 125], [680, 185], 2)
    pygame.draw.line(screen, BLACK, [680, 125], [940, 125], 2)
    pygame.draw.line(screen, BLACK, [680, 185], [940, 185], 2)
    pygame.draw.line(screen, BLACK, [940, 125], [940, 185], 2)


def update_message_box(message):
    message_font = pygame.font.Font('freesansbold.ttf', 20)
    message_text = message_font.render(message, True, BLACK)
    message_rect = message_text.get_rect(center=message_box.center)
    screen.blit(message_text, message_rect)


# Colors the section below the message box that holds the ships at the start
def color_action_box():
    screen.fill(LIGHT_BLUE, action_box)
    pygame.draw.line(screen, BLACK, [680, 200], [680, 640], 2)
    pygame.draw.line(screen, BLACK, [680, 200], [940, 200], 2)
    pygame.draw.line(screen, BLACK, [940, 200], [940, 640], 2)
    pygame.draw.line(screen, BLACK, [680, 640], [940, 640], 2)


# Update the grid display for when it's the player's turn
def update_player_grid(board_array):
    for row in range(1, 11):
        for col in range(1, 11):
            grid_cell = convert_grid_coordinates(row, col)

            if board_array[row][col] == Cell.EMPTY or board_array[row][col] == Cell.HIDDEN:
                pygame.draw.rect(screen, BLUE, grid_cell)
            elif board_array[row][col] == Cell.MISS:
                pygame.draw.rect(screen, GREEN, grid_cell)
            elif board_array[row][col] == Cell.HIT:
                pygame.draw.rect(screen, ORANGE, grid_cell)
            elif board_array[row][col] == Cell.SUNK:
                pygame.draw.rect(screen, DARK_RED, grid_cell)
    draw_grid_labels()


# Update the grid display for when it's the AI's turn:
def update_AI_grid(board_array):
    for row in range(1, 11):
        for col in range(1, 11):
            grid_cell = convert_grid_coordinates(row, col)

            if board_array[row][col] == Cell.EMPTY:
                pygame.draw.rect(screen, BLUE, grid_cell)
            elif board_array[row][col] == Cell.HIDDEN:  # When it's the AI's turn, the player sees their hidden ships
                pygame.draw.rect(screen, YELLOW, grid_cell)
            elif board_array[row][col] == Cell.MISS:
                pygame.draw.rect(screen, GREEN, grid_cell)
            elif board_array[row][col] == Cell.HIT:
                pygame.draw.rect(screen, ORANGE, grid_cell)
            elif board_array[row][col] == Cell.SUNK:
                pygame.draw.rect(screen, DARK_RED, grid_cell)

    draw_grid_labels()


# Pauses the screen time for wait_time milliseconds
def wait_for(wait_time):
    screen_copy = screen.copy()
    count = 0
    while count < wait_time:
        dt = clock.tick(60)
        count += dt
        pygame.event.pump()
        screen.blit(screen_copy, (0, 0))
        pygame.display.flip()


rectangle_dragging = False
selected = None

# The loop will carry on until the user exit the game/clicks the close button
carryOn = True

# Boolean variable to denote that the game is in the setup portion:
setup = True

# Boolean variables to denote who's turn it is:
player_turn = True
AI_turn = False

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# For double click timing:
last_click = pygame.time.get_ticks()

# Global variables:
player = Player()
AI = AI()
player_win = False
AI_win = False

# -------- Main Program Loop -----------
while carryOn:
    if setup:
        # --- Setup event loop: These events
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                carryOn = False  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # IF 'START' BUTTON IS PRESSED:
                if event.button == 1 and 680 < event.pos[0] < 940 and 70 < event.pos[1] < 110:

                    # Verify that the all the ships are on the board
                    # Then setup = False to switch to a new set of events
                    # If nothing is wrong with the setup, proceed to the AI turn
                    if check_setup(ships):
                        setup = False
                        AI_turn = True
                        player_turn = False
                        # Return all the coordinates of the user's ships - save to object
                        for ship in ships:
                            ship_coordinates = get_ship_coordinates(ship)
                            ship_name = ""
                            if ship == carrier:
                                ship_name = "carrier"
                            elif ship == battleship:
                                ship_name = "battleship"
                            elif ship == cruiser:
                                ship_name = "cruiser"
                            elif ship == submarine:
                                ship_name = "submarine"
                            elif ship == destroyer:
                                ship_name = "destroyer"
                            player.add_ship(ship_name, ship_coordinates)

                        # Place the AI's ships:
                        AI.random_placement()

                # SINGLE CLICK
                now = pygame.time.get_ticks()
                if event.button == 1 and now-last_click > 500:
                    for i, r in enumerate(ships):
                        if r.collidepoint(event.pos):
                            selected = i
                            selected_offset_x = r.x - event.pos[0]
                            selected_offset_y = r.y - event.pos[1]
                if event.button == 1 and now - last_click <= 500:
                    # DOUBLE CLICK:
                    # Rotate the double-clicked on ship
                    x = event.pos[0]    # current mouse x coordinate
                    y = event.pos[1]    # current mouse y coordinate
                    for ship in ships:
                        width = ship.width
                        height = ship.height
                        left = ship.left
                        top = ship.top
                        # If the current mouse position is within a ships's coordinates, rotate it
                        if left < x < left+width and top < y < top+height:
                            # Rotating the ship by switching the width and height
                            ship.height = width
                            ship.width = height
                last_click = pygame.time.get_ticks()    # Store the time of the last click
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = None
            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:  # selected can be 0 so not None is needed
                    # move object
                    ships[selected].x = event.pos[0] + selected_offset_x
                    ships[selected].y = event.pos[1] + selected_offset_y
                    realign(ships[selected])
    # Game in progress (after user presses start):
    elif not setup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                carryOn = False  # Flag that we are done so we exit this loop

            # If it's the player's turn and they press on a square that hasn't been pressed before: take a shot
            elif player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and event.pos[0] < 660:
                    coordinates = convert_pixel_coordinates(event.pos[0], event.pos[1])
                    # Take a shot
                    last_player_attack = AI.suffer_attack(coordinates)
                    # Check for sunken ships:
                    AI.check_sunken_ships()
                    # Update display
                    board_array = AI.get_board()
                    update_player_grid(board_array)
                    wait_for(800)

                    # Check if player wins:
                    if AI.check_loss():
                        player_win = True
                        carryOn = False

                    # Update turn: If last turn was a hit or sink, go again
                    if last_player_attack == Cell.HIT or last_player_attack == Cell.SUNK:
                        player_turn = True
                        AI_turn = False
                    else:
                        player_turn = False
                        AI_turn = True

    # --- Game logic should go here
    # If user presses start - make sure that all the board pieces are in the correct place, then start game
    if not setup:
        if AI_turn:

            # Q LEARNING AI:
            # Update message box:
            message = "AI's turn"
            color_message_box()
            update_message_box(message)
            sunken_ships = player.get_sunken_ships()
            row, col = AI.Q_Learning_AI(last_AI_attack, sunken_ships)
            player.suffer_attack(row, col)
            # Check for sunken ships:
            player.check_sunken_ships()
            last_AI_attack = player.get_state(row, col)
            # Update display:
            board_array = player.get_board()
            update_AI_grid(board_array)

            # Check if AI wins:
            if player.check_loss():
                AI_win = True
                carryOn = False

            # Update turn: If last turn was a hit or sink, go again
            if last_AI_attack == Cell.HIT or last_AI_attack == Cell.SUNK:
                AI_turn = True
                player_turn = False
            else:
                player_turn = True
                AI_turn = False

            wait_for(1500)

            '''
            # RANDOM AI:
            # Update message box:
            message = "AI's turn"
            color_message_box()
            update_message_box(message)
            sunken_ships = player.get_sunken_ships()

            board_array = player.get_board()
            update_AI_grid(board_array)
            # Shoot:
            row, col = AI.random_attack(last_AI_attack, sunken_ships)
            player.suffer_attack(row, col)
            # Check for sunken ships:
            player.check_sunken_ships()
            last_AI_attack = player.get_state(row, col)
            # Update display:
            board_array = player.get_board()
            update_AI_grid(board_array)

            # Check if AI wins:
            if player.check_loss():
                AI_win = True
                carryOn = False

            # Update turn: If last turn was a hit or sink, go again
            if last_AI_attack == Cell.HIT or last_AI_attack == Cell.SUNK:
                AI_turn = True
                player_turn = False
            else:
                player_turn = True
                AI_turn = False

            wait_for(1500)
            '''
        else:
            # Update message box:
            color_message_box()
            message_font = pygame.font.Font('freesansbold.ttf', 20)
            message = "Your turn"
            message_text = message_font.render(message, True, BLACK)
            message_rect = message_text.get_rect(center=message_box.center)
            screen.blit(message_text, message_rect)

            board_array = AI.get_board()
            update_player_grid(board_array)

            if last_player_attack == Cell.HIT or last_player_attack == Cell.SUNK:
                player_turn = True
                AI_turn = False

    # Draws & fills (without updates):
    grid_space = pygame.Rect(60, 60, 660, 660)
    if setup:
        pygame.draw.rect(screen, BLUE, grid_space)

    side_bar = pygame.Rect(662, 0, 300, total_length)
    screen.fill(PURPLE, side_bar)
    pygame.draw.line(screen, BLACK, [662, 0], [662, board_length], 5)

    # Horizontal & Vertical X and Y axis
    x_axis = pygame.Rect(0, 0, board_width, 60)
    y_axis = pygame.Rect(0, 0, 60, board_length)
    screen.fill(LIGHT_BLUE, x_axis)
    screen.fill(LIGHT_BLUE, y_axis)

    # START BUTTON:
    start_button = pygame.Rect(680, 70, 260, 40)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # Add colors (inactive color & hover color):
    if 680 + 260 > mouse[0] > 680 and 70 + 40 > mouse[1] > 70:
        pygame.draw.rect(screen, LIGHT_RED, (680, 70, 260, 40))
    else:
        pygame.draw.rect(screen, LIGHT_YELLOW, (680, 70, 260, 40))
    pygame.draw.line(screen, BLACK, [680, 70], [680, 110], 2)
    pygame.draw.line(screen, BLACK, [680, 70], [940, 70], 2)
    pygame.draw.line(screen, BLACK, [680, 110], [940, 110], 2)
    pygame.draw.line(screen, BLACK, [940, 70], [940, 110], 2)

    # Add start button logo
    start_logo_font = pygame.font.Font('freesansbold.ttf', 20)
    start_logo = start_logo_font.render('Start', True, BLACK)
    screen.blit(start_logo, (780, 85))

    color_message_box()
    color_action_box()
    draw_grid_labels()

    if setup or AI_turn:
        pygame.draw.rect(screen, YELLOW, carrier)
        pygame.draw.rect(screen, YELLOW, battleship)
        pygame.draw.rect(screen, YELLOW, cruiser)
        pygame.draw.rect(screen, YELLOW, submarine)
        pygame.draw.rect(screen, YELLOW, destroyer)

    # Add Battleship Text to the top
    logo_font = pygame.font.SysFont('Raleway', 50, bold=True)
    logo = logo_font.render('Battleship', True, WHITE)
    screen.blit(logo, (710, 20))

    # Display start message:
    if setup:
        message_font = pygame.font.Font('freesansbold.ttf', 17)
        message = "Hide your ships & press start."
        message_text = message_font.render(message, True, BLACK)
        message_rect = message_text.get_rect(center=message_box.center)
        screen.blit(message_text, message_rect)
    elif player_turn:
        message = "Your turn"
        color_message_box()
        update_message_box(message)

    # Update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Display winner:
if player_win:
    screen.fill(BLUE)
    winner_font = pygame.font.Font('freesansbold.ttf', 40)
    winner_box = pygame.rect.Rect(0, 0, total_width, total_length)
    winner_message = "You win!"
    winner_text = winner_font.render(winner_message, True, BLACK)
    winner_rect = winner_text.get_rect(center=winner_box.center)
    screen.blit(winner_text, winner_rect)
    wait_for(6000)
elif AI_win:
    screen.fill(BLUE)
    winner_font = pygame.font.Font('freesansbold.ttf', 40)
    winner_box = pygame.rect.Rect(0, 0, total_width, total_length)
    winner_message = "AI wins!"
    winner_text = winner_font.render(winner_message, True, BLACK)
    winner_rect = winner_text.get_rect(center=winner_box.center)
    screen.blit(winner_text, winner_rect)
    wait_for(6000)

# End the game
pygame.quit()
