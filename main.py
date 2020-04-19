# Main Battleship game file
import pygame
pygame.init()

# Color definition:
BLUE = (45, 145, 233)       # Blue for the background (to look like water)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (233, 159, 79)
LIGHT_RED = (230, 90, 85)

# Sizes:
total_length = 660
total_width = 960
board_length = 660
board_width = 660
# Open a new window
size = (total_width, total_length)  # (width, length)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Battleship")    # Name of the window/game

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop

        # --- Game logic should go here

    # Coloring the screen:
    screen.fill(BLUE)
    # Rect(left, top, width, height) -> Rect
    bottom = pygame.Rect(660, 0, 300, total_length)
    screen.fill(LIGHT_RED, bottom)
    # Draw separation line:
    pygame.draw.line(screen, BLACK, [662, 0], [662, board_length], 5)

    # *** DRAW SHAPES, LINES, COLORS, ETC. HERE ***
    # Draw vertical & horizontal lines: (Battleship rows
    for x in range(11):
        pos = (x+1)*60
        pygame.draw.line(screen, WHITE, [pos, 0], [pos, board_length], 2)
        pygame.draw.line(screen, WHITE, [0, pos], [board_width, pos], 2)

    # Add labels:
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

    # Add Text on the side
    fleet = label_font.render('Your Fleet:', True, WHITE)
    screen.blit(fleet, (730, 20))




    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
