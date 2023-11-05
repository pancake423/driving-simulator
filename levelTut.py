import pygame
from levels import Level

def level_Tutorial(screen, screen_width, screen_height):
    #pygame.init()

    # Create a level instance

    level = Level(screen_width, screen_height)
    
    #stopSign= pygame.image.load('assets/NewTempStop.png')
    #stopSign = pygame.transform.smoothscale(stopSign,(60, 60)).convert_alpha()

    # Coordinates for the intersection
    x = screen_width / 2
    y = screen_height / 2

    # Define coordinates for the horizontal roads
    fh_start_x = 0
    fh_end_x = screen_width / 2 - 107.5

    sh_start_x = screen_width / 2 + 107.5
    sh_end_x = screen_width

    # Coordinates for vertical roads
    v_st_1 = screen_height / 2 + 107.5
    v_end_1 = screen_height
    v_st_2 = 0
    v_end_2 = screen_height / 2 - 107.5

    # Call functions to add roads, intersections, etc
    level.add_horizontal_road(fh_start_x, fh_end_x, y)
    level.add_horizontal_road(sh_start_x, sh_end_x, y)

    # Add vertical roads and intersection as needed
    level.add_vertical_road(x, v_st_2, v_end_2)
    level.add_intersection(x, y)

    level.add_random_decorations(30)

    return level
