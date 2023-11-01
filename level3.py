import pygame
import math
from cars import PlayerCar, BotCar
from levels import Level



def level_Three(screen, screen_width, screen_height):
    #Declarations
    levelNum = "Level 3"

    #Initialize font
    pygame.font.init()

    #font type
    fontType = "fonts/Get Now.ttf"
    levelFont = pygame.font.Font(fontType, 40)
    level_surf = levelFont.render(levelNum, True, "red")
    level_rect = level_surf.get_rect(topright = (screen_width - 20, 20))
    
    topLaneY = screen_height / 2 - 110
    botLaneY = screen_height / 2 + 10
    
    playerCar = PlayerCar((80, botLaneY))
    playerGroup = pygame.sprite.GroupSingle()
    playerGroup.add(playerCar)
    
    botCar = BotCar((screen_width, topLaneY), 180)
    botGroup = pygame.sprite.Group()
    botGroup.add(botCar)
    botCar.setTarget((-1000, topLaneY))
    
    playerCar.setCollide([botGroup])
    botCar.setCollide([playerGroup])

    #displays level 6 on screen
    pygame.display.set_caption(levelNum)
    
    #create a level instance
    level = Level(screen_width, screen_height)
    
    
    #Create coordinates for the horizontal road
    fh_start_x = 0  
    fh_end_x = 842
    fh_y = 540

    sh_start_x = 1057
    sh_end_x = 2160
    sh_y = 540

    #Coordinates for vertical roads
    #R1 bottom road
    v_st_1 = 1485
    v_end_1 = 646 #650
    x1 = 955
    
    #top road
    v_st_2 = 0
    v_end_2 = 432 #430
    x2 = 955
    
    
    # coordinates for intersection
    inter_x = screen_width // 2.02
    inter_y = screen_height // 2
    
    #call functions to add roads, intersections, etc
    level.add_horizontal_road(fh_start_x, fh_end_x, fh_y)
    level.add_horizontal_road(sh_start_x, sh_end_x, sh_y)
    level.add_vertical_road(x1, v_st_1, v_end_1)
    level.add_vertical_road(x2, v_st_2, v_end_2)
    level.add_intersection(inter_x, inter_y)
    level.add_random_decorations(30)
    
    
    #Adds stop sign
    stopSign= pygame.image.load('assets/NewTempStop.png')
    stopSign = pygame.transform.smoothscale(stopSign,(60, 60)).convert_alpha()

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    botTurned = False
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(Level.BG_COLOR) 

        # Draw the level
        level.draw(screen, 0, 0)
        

        screen.blit(level_surf, level_rect)
        screen.blit(stopSign, (760, 670))
        screen.blit(stopSign, (1090, 670))
        screen.blit(stopSign, (1090, 350))
        screen.blit(stopSign, (760, 350))
        #display_score()

        
        playerGroup.update()
        botGroup.update()
        playerGroup.draw(screen)
        botGroup.draw(screen)
        
        playerPos, botPos = playerCar.getPos(), botCar.getPos()
        playerX, playerY = playerPos
        botX, botY = botPos

        # Update the display
        pygame.display.flip()
    
     
    
#displays the timer onto the screen
#def display_score(x_axis = 25, y_axis = 25):
    #Declarations
    #start_time = 0
    #time_at_pause = 0
    #paused_time = 0
    #font type & size
    #timerFont = pygame.font.Font(fontType, 40)
    #Puts the timer onto the screen
    #current_time = "Timer: " + str((pygame.time.get_ticks() - start_time - paused_time) / 1000)
    #score_surf = timerFont.render(current_time, False, "red")
    #score_rect = score_surf.get_rect(topleft = (x_axis, y_axis))
    #screen.blit(score_surf, score_rect)
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    540
    # Set screen
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN | pygame.SCALED)
    
    #calls the level_Three() Funcntion
    print(level_Three(screen, screen_width, screen_height))

    # Quit pygame
    pygame.quit()

