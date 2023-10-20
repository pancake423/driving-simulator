#import libraries from pygame extension
import pygame
from cars import AbstractCar
from cars import PlayerCar
from cars import BotCar

#initialize pygame
pygame.init()

#define and set title of pygame that will display on the window border
game_title = "2-D Driving Simulator"
pygame.display.set_caption(game_title)

#define and set title menu options
play_game = "Play"
quit_game = "Quit"

#define and set font type(s)
menu_font_type = 'fonts/Get Now.ttf'

#set play_state to True to control game loop
play_state = True

#set title_state to True to control title screen portion of game loop
title_state = True

#set level_state to True to control level select screen portion of game loop
level_state = True

#define and initialize score
score = 0

#set amount of levels
level_count = 10

#for screen width and heigth, defined and initialized here to make changing easy
resW = 800
resH = 600

#set the screen using resW and resH as arguments
screen = pygame.display.set_mode((resW, resH))

#initailize clock for the game
clock = pygame.time.Clock()

#initialize pygame fonts
pygame.font.init()

#set title menu fonts to Fixedsys regular, whose file name is '8514fix.fon'
title_font = pygame.font.Font(menu_font_type, 50)
menu_font = pygame.font.Font(menu_font_type, 50)

#creates a surface for rendering the title in the pygame window
title_surf = title_font.render(game_title, False, 'yellow')
title_rect = title_surf.get_rect(midtop = (resW / 2, 50))

#creates a surface for rendering the levels of the level select menu in the pygame window
level_surf_list = []
level_rect_list = []
for i in range(level_count):
    level_surf_list.append(menu_font.render("Level " + str(i + 1), False, 'purple'))
    level_rect_list.append(level_surf_list[i].get_rect(topleft = (50, 50 + (i * 50))))


#creates a surface for rendering the title menu options ('Play' and 'Quit')
play_surf = menu_font.render(play_game, False, 'sky blue')
play_rect = play_surf.get_rect(topright = (resW - 350, resH / 3))
quit_surf = menu_font.render(quit_game, False, 'purple')
quit_rect = quit_surf.get_rect(topright = (resW - 350, (resH / 2) + 50))

#game loop runs until play_state is False
while play_state:
    
    #if title_state True, shows the title menu
    if title_state == True:
        screen.blit(title_surf, title_rect)
        screen.blit(play_surf, play_rect)
        screen.blit(quit_surf, quit_rect)

        #get mouse position to check if mouse is over Play or Quit
        mouse_pos = pygame.mouse.get_pos()

        #checks if mouse is positioned over Play or Quit and if leck click is pressed
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_state = pygame.mouse.get_pressed()
                if mouse_state[0]:
                    if play_rect.collidepoint(mouse_pos):
                        title_state = False
                        screen.fill('black')
                    elif quit_rect.collidepoint(mouse_pos):
                        title_state = False
                        play_state = False
            elif event.type == pygame.QUIT:
                title_state = False
                level_state = False
                play_state = False

    if title_state == False and level_state == True:
        for i in range(level_count):
            screen.blit(level_surf_list[i], level_rect_list[i])

        #get mouse position to check if mouse is over any of the levels
        mouse_pos = pygame.mouse.get_pos()

        #checks if mouse is positioned over a level and if leck click is pressed
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_state = pygame.mouse.get_pressed()
                if mouse_state[0]:
                    for i in range(level_count):
                        if level_rect_list[i].collidepoint(mouse_pos):
                            level_state = False
                            screen.fill('black')
            elif event.type == pygame.QUIT:
                title_state = False
                level_state = False
                play_state = False

    #checks the most recent event to see if the player clicked the X button
    #at the top right of the window border
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title_state = False
            level_state = False
            play_state = False

    #update screen with a background
    pygame.display.update()
    clock.tick(60)

pygame.quit()