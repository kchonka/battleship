# Main Battleship game file
import pygame
pygame.init()


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
YELLOW =  (247, 244, 25)

# Sizes:
total_length = 660
total_width = 960
board_length = 660
board_width = 660

# Open a new window
size = (total_width, total_length)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Battleship")

# Create the 5 ships:
# Rect(left, top, width, height)
carrier = pygame.rect.Rect(700, 210, 60, 300)
battleship = pygame.rect.Rect(780, 210, 60, 240)
cruiser = pygame.rect.Rect(860, 210, 60, 180)
submarine = pygame.rect.Rect(740, 550, 180, 60)
destroyer = pygame.rect.Rect(800, 470, 120, 60)

# Add ships to a list
ships = [carrier, battleship, cruiser, submarine, destroyer]

rectangle_dragging = False
selected = None

# The loop will carry on until the user exit the game/clicks the close button
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

last_click = pygame.time.get_ticks()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        # --- global events --------
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                carryOn = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            now = pygame.time.get_ticks()
            # SINGLE CLICK
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
            if selected is not None:  # selected can be `0` so `is not None` is required
                # move object
                # event.pos[0] = x axis position
                # event.pos[1] = y axis position
                ships[selected].x = event.pos[0] + selected_offset_x
                ships[selected].y = event.pos[1] + selected_offset_y
                realign(ships[selected])

        # --- Game logic should go here
        # If user presses start - make sure that all the board pieces are in the correct place, then start game
        # Return all the coordinates of the user's ships - save to object
        # Have the AI place all of its ships
        # loop until


    # Draws (without updates)
    # Coloring the screen:
    screen.fill(BLUE)
    # Rect(left, top, width, height) -> Rect
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
    #if click[0] == 1:
        # action after clicking

    # Message box - section above the action box that tells you what to do
    message_box = pygame.Rect(680, 125, 260, 60)
    screen.fill(LIGHT_BLUE, message_box)
    pygame.draw.line(screen, BLACK, [680, 125], [680, 185], 2)
    pygame.draw.line(screen, BLACK, [680, 125], [940, 125], 2)
    pygame.draw.line(screen, BLACK, [680, 185], [940, 185], 2)
    pygame.draw.line(screen, BLACK, [940, 125], [940, 185], 2)

    # "Action box"
    action_box = pygame.Rect(680, 200, 260, 440)
    screen.fill(LIGHT_BLUE, action_box)
    pygame.draw.line(screen, BLACK, [680, 200], [680, 640], 2)
    pygame.draw.line(screen, BLACK, [680, 200], [940, 200], 2)
    pygame.draw.line(screen, BLACK, [940, 200], [940, 640], 2)
    pygame.draw.line(screen, BLACK, [680, 640], [940, 640], 2)

    # *** DRAW SHAPES, LINES, COLORS, ETC. HERE ***
    # Draw vertical & horizontal lines: (Battleship rows
    for x in range(11):
        pos = (x+1)*60
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

    # Add Battleship Text to the top
    logo_font = pygame.font.SysFont('Raleway', 50, bold=True)
    logo = logo_font.render('Battleship', True, WHITE)
    screen.blit(logo, (710, 20))

    pygame.draw.rect(screen, YELLOW, carrier)
    pygame.draw.rect(screen, YELLOW, battleship)
    pygame.draw.rect(screen, YELLOW, cruiser)
    pygame.draw.rect(screen, YELLOW, submarine)
    pygame.draw.rect(screen, YELLOW, destroyer)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# End the game
pygame.quit()


# Function that converts a ship's x/y coordinates to the row/col coordinates
# RETURNS A LIST OF ALL THE BOARD BLOCKS THAT CONTAIN THE GIVEN SHIP
def get_ship_coordinates(ship):

    coordinates = []

    x = ship.x
    y = ship.y
    width = ship.width
    height = ship.height

    new_x = int(60 * round(x/60))
    new_y = int(60 * round(y/60))
    start_row = int(new_x / 60)
    start_col = int(new_y / 60)
    width_in_boxes = int(width / 60)
    height_in_boxes = int(height / 60)

    # Ship is horizontal
    if height_in_boxes == 1:
        for i in range(height_in_boxes):
            row = start_row
            col = start_col + 1
            new_pair = [row, col]
            coordinates.append(new_pair)
    else:  # Ship is vertical (width_in_boxes == 1)
        for i in range(width_in_boxes):
            row = start_row + 1
            col = start_col
            new_pair = [row, col]
            coordinates.append(new_pair)

    return coordinates


# Converts the pixel coordinates to the equivalent Battleship board coordinates
# Returns a list [row, col]
def convert_coordinates(pixel_x, pixel_y):
    board_coordinates = []

    rounded_x = int(60 * round(pixel_x / 60))
    rounded_y = int(60 * round(pixel_y / 60))
    row = int(rounded_x / 60)
    col = int(rounded_y / 60)

    board_coordinates.append(row)
    board_coordinates.append(col)

    return board_coordinates




