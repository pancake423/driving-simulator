import pygame
from levels import Level

def level_One(screen, screen_width, screen_height):
    #pygame.init()

    # Create a level instance

    level = Level(screen_width, screen_height)

    # Define coordinates for the horizontal roads
    fh_start_x = 0
    fh_end_x = 432.5
    fh_y = 360

    sh_start_x = 647.5
    sh_end_x = 1080
    sh_y = 360

    # Coordinates for vertical roads
    v_st_1 = 467.5
    v_end_1 = 720
    x1 = 540
    v_st_2 = 0
    v_end_2 = 252.5
    x2 = 540

    # Coordinates for the intersection
    inter_x = screen_width // 2
    inter_y = screen_height // 2

    # Call functions to add roads, intersections, etc
    level.add_horizontal_road(fh_start_x, fh_end_x, fh_y)
    level.add_horizontal_road(sh_start_x, sh_end_x, sh_y)
    # Add vertical roads and intersection as needed
    level.add_vertical_road(x1, v_st_1, v_end_1)
    level.add_vertical_road(x2, v_st_2, v_end_2)
    level.add_intersection(inter_x, inter_y)

    return level

# Entry point for your program
if __name__ == "__main__":
    screen_width = 1080
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    while level_One(screen, screen_width, screen_height):
        pass  # The game loop will keep running until the game is closed
