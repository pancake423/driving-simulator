import pygame
import math
from cars import PlayerCar, BotCar
from levels import Level

# Initialize pygame
pygame.init()
540
#Declarations
levelNum = "Level 6"

#Initialize font
pygame.font.init()

# Set screen
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

#font type
fontType = "fonts/Get Now.ttf"
levelFont = pygame.font.Font(fontType, 40)
level_surf = levelFont.render(levelNum, True, "red")
level_rect = level_surf.get_rect(topright = (screen_width - 20, 20))

#displays the timer onto the screen
def display_score(x_axis = 25, y_axis = 25):
    #Declarations
    start_time = 0
    time_at_pause = 0
    paused_time = 0
    #font type & size
    timerFont = pygame.font.Font(fontType, 40)
    #Puts the timer onto the screen
    current_time = "Timer: " + str((pygame.time.get_ticks() - start_time - paused_time) / 1000)
    score_surf = timerFont.render(current_time, False, "red")
    score_rect = score_surf.get_rect(topleft = (x_axis, y_axis))
    screen.blit(score_surf, score_rect)


#displays level 6 on screen
pygame.display.set_caption(levelNum)

#create a level instance
level = Level(screen_width, screen_height)

#Adds stop sign

stopSign= pygame.image.load('assets/NewTempStop.png')
stopSign = pygame.transform.smoothscale(stopSign,(60, 60)).convert_alpha()

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
level.add_horizontal_road(fh_start_x, fh_end_x, fh_y)
level.add_horizontal_road(sh_start_x, sh_end_x, sh_y)
level.add_vertical_road(x1, v_st_1, v_end_1)
level.add_vertical_road(x2, v_st_2, v_end_2)
level.add_intersection(inter_x, inter_y)

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
    
    screen.blit(level_surf, level_rect)
    screen.blit(stopSign, (350, 490))
    screen.blit(stopSign, (670, 490))
    screen.blit(stopSign, (670, 167))
    screen.blit(stopSign, (350, 167))
    display_score()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()

