#import libraries from pygame extension
import pygame

#import classes PlayerCar and BotCar from cars.py
from cars import PlayerCar, BotCar

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

#set level_state to False to control level select screen portion of game loop
level_state = False

#define and initialize score
score = 0

#set amount of levels
level_count = 10
level_choice = 0

#for screen width and heigth, defined and initialized here to make changing easy
resW = 1080
resH = 720

#set the screen using resW and resH as arguments
screen = pygame.display.set_mode((resW, resH))
background = pygame.image.load('assets/standard-road.png').convert()
background = pygame.transform.smoothscale(background,(resW,resH))
screen.blit(background, (0,0))
pygame.display.flip()

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
    level_rect_list.append(level_surf_list[i].get_rect(topleft = (50, 25 + (i * 55))))


#creates a surface for rendering the title menu options ('Play' and 'Quit')
play_surf = menu_font.render(play_game, False, 'sky blue')
play_rect = play_surf.get_rect(topright = (resW - 500, resH / 3))
quit_surf = menu_font.render(quit_game, False, 'sky blue')
quit_rect = quit_surf.get_rect(topright = (resW - 500, (resH / 2) + 50))

quit_surf = menu_font.render(quit_game, False, 'purple')
quit_rect = quit_surf.get_rect(topright = (resW - 500, (resH / 2) + 50))

BotCars = pygame.sprite.Group()
myCar = BotCar()
BotCars.add(myCar)
    
player = pygame.sprite.GroupSingle()
playerCar = PlayerCar()
player.add(playerCar)
    
playerCar.setCollide(BotCars)
myCar.setCollide(player)

#game loop runs until play_state is False
while play_state:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title_state = False
            level_state = False
            play_state = False
            pygame.quit()
            exit()
        
        if title_state:

            #get mouse position to check if mouse is over Play or Quit
            mouse_pos = pygame.mouse.get_pos()

            #checks if mouse is positioned over Play or Quit and if leck click is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_state = pygame.mouse.get_pressed()
                if mouse_state[0]:
                    if play_rect.collidepoint(mouse_pos):
                        title_state = False
                        level_state = True
                        screen.fill('black')
                    elif quit_rect.collidepoint(mouse_pos):
                        title_state = False
                        play_state = False
        
        if level_state:

            #get mouse position to check if mouse is over any of the levels
            mouse_pos = pygame.mouse.get_pos()

            #checks if mouse is positioned over a level and if leck click is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_state = pygame.mouse.get_pressed()
                if mouse_state[0]:
                    for i in range(level_count):
                        if level_rect_list[i].collidepoint(mouse_pos):
                            level_state = False
                            level_choice = i + 1
                            print(level_choice)
                            screen.fill('black')

    
    #if title_state True, shows the title menu
    if title_state:
        screen.blit(title_surf, title_rect)
        screen.blit(play_surf, play_rect)
        screen.blit(quit_surf, quit_rect)

    if level_state:
        for i in range(level_count):
            screen.blit(level_surf_list[i], level_rect_list[i])

    if not level_state:
        match level_choice:
            case 1:
                screen.fill((50, 200, 50))
                myCar.setTarget(pygame.mouse.get_pos())
                BotCars.update()
                player.update()
                BotCars.draw(screen)
                player.draw(screen)
            case 2:
                screen.fill((255, 255, 200))
            case 3:
                screen.fill((255, 200, 200))
            case 4:
                screen.fill((200, 200, 200))
            case 5:
                screen.fill((200, 200, 150))
            case 6:
                screen.fill((200, 150, 150))
            case 7:
                screen.fill((150, 150, 150))
            case 8:
                screen.fill((150, 150, 100))
            case 9:
                screen.fill((150, 100, 100))
            case 10:
                screen.fill((100, 100, 150))

    #update screen with a background
    pygame.display.update()
    clock.tick(60)

pygame.quit()