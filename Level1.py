import pygame
from levels import Level
from cars import PlayerCar

def level_One(screen, screen_width, screen_height):
    #pygame.init()

    # Create a level instance

    level = Level(screen_width, screen_height)

    # Define coordinates for the horizontal roads
    fh_start_x = 0  
    fh_end_x = 850
    fh_y = 540

    sh_start_x = 1068
    sh_end_x = 2160
    sh_y = 540

    #Coordinates for vertical roads
    #R1 bottom road
    v_st_1 = 1485
    v_end_1 = 648 #650
    x1 = 960
    
    #top road
    v_st_2 = 0
    v_end_2 = 432 #430
    x2 = 960

    # Coordinates for the intersection
    inter_x = screen_width // 2
    inter_y = screen_height // 2

    player = pygame.sprite.GroupSingle()
    playerCar = PlayerCar((200,590),)
    player.add(playerCar)

    #add traffic lights
    level.add_4_way_light(inter_x, inter_y)

    # Call functions to add roads, intersections, etc
    level.add_horizontal_road(fh_start_x, fh_end_x, fh_y)
    level.add_horizontal_road(sh_start_x, sh_end_x, sh_y)
    # Add vertical roads and intersection as needed
    level.add_vertical_road(x1, v_st_1, v_end_1)
    level.add_vertical_road(x2, v_st_2, v_end_2)
    level.add_intersection(inter_x, inter_y)
    

    

    level.add_random_decorations(30)

    level.draw(screen, 0, 0)

    player.draw(screen)
    player.update

    return level

# Entry point for your program
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen_width = 1920
    screen_height = 1080

    screen = pygame.display.set_mode((screen_width, screen_height))

    level = level_One(screen, screen_width, screen_height)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        
        pygame.display.flip()
        pass  # The game loop will keep running until the game is closed
