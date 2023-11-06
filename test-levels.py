import pygame
from levels import Level


# Initialize pygame
pygame.init()
540 
# Set screen
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

#create a level instance
level = Level(screen_width, screen_height)

#Create coordinates for the horizontal road
fh_start_x = 0  
fh_end_x = 432.5
fh_y = 360

sh_start_x = 647.5
sh_end_x = 1080
sh_y = 360

#Coordinates for vertical roads
#R1
v_st_1 = 467.5
v_end_1 = 720
x1 = 540
v_st_2 = 0
v_end_2 = 252.5
x2 = 540

# coordinates for intersection
inter_x = screen_width // 2
inter_y = screen_height // 2

#call functions to add roads, intersections, etc
level.add_4_way_light(inter_x, inter_y)

level.add_random_decorations(30)

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
