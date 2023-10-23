import pygame
from levels import Level


# Initialize pygame
pygame.init()

# Set screen
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

#create a level instance
level = Level(screen_width, screen_height)

#call functions to add roads, intersections, etc

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(Level.BG_COLOR)

    # Draw the level
    level.draw(screen, 0, 0)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
