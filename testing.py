import pygame
import utils

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

red_screen = pygame.Surface(size)
blue_screen = pygame.Surface(size)

red = True

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                red = not red

    # --- Game logic should go here

    # --- Screen-clearing code goes here
    screen.fill(utils.colors["Black"])

    # --- Drawing code should go here

    red_screen.fill(utils.colors["Red"])
    blue_screen.fill(utils.colors["Blue"])

    if red:
        screen.blit(red_screen, (0, 0))
    else:
        screen.blit(blue_screen, (0, 0))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
