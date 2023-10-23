#import libraries from pygame extension
import pygame

#import classes PlayerCar and BotCar from cars.py
from cars import PlayerCar, BotCar

def display_score():
    current_time = str((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = menu_font.render(current_time, False, (221, 73, 73))
    score_rect = score_surf.get_rect(topleft = (25, 25))
    screen.blit(score_surf, score_rect)

#initialize pygame
pygame.init()

#initailize clock for the game
clock = pygame.time.Clock()

#initialize pygame fonts
pygame.font.init()

start_time = 0

#define and set title of pygame that will display on the window border
game_title = "2-D Driving Simulator"
pygame.display.set_caption(game_title)

#define and set title menu options
play_game = "Play"
quit_game = "Quit"

#define game over
game_fail = "Game Over"

#define and set font type(s)
font_type = 'fonts/Get Now.ttf'

#set title_state to True to control title screen portion of game loop
title_state = True

#set level_state to False to control level select screen portion of game loop
level_state = False

#set play_state to False to control gameplay portion of game loop
play_state = False

#set end_state to False to control level end screen portion of game loop
end_state = False

#set amount of levels
level_count = 10
level_choice = 0

#for screen width and heigth, defined and initialized here to make changing easy
resW = 1080
resH = 720
resCW = 480
resCH = 280

#set the screen using resW and resH as arguments
screen = pygame.display.set_mode((resW, resH))

#set background image for title menu
background = pygame.image.load('assets/standard-road.png').convert()
background = pygame.transform.smoothscale(background,(resW,resH))

#car background image for title menu
carBackground = pygame.image.load('assets/unicorn-car-blue.png')
carBackground = pygame.transform.smoothscale(carBackground,(resCW,resCH)).convert_alpha()

#AI car background image for title menu
AIcarBackground = pygame.image.load('assets/unicorn-car-red.png')
AICar = pygame.transform.smoothscale(AIcarBackground,(resCW,resCH)).convert_alpha()
redCar = pygame.transform.flip(AICar, False, True).convert_alpha()
#set menu font to 'Get Now.ttf'
menu_font = pygame.font.Font(font_type, 50)

#creates a surface for rendering the title in the pygame window
title_surf = menu_font.render(game_title, False, 'yellow')
title_rect = title_surf.get_rect(midtop = (resW / 2, 50))

#creates a surface for rendering the title menu options ('Play' and 'Quit')
play_surf = menu_font.render(play_game, False, 'sky blue')
play_rect = play_surf.get_rect(topright = (resW - 500, resH / 3))
quit_surf = menu_font.render(quit_game, False, 'sky blue')
quit_rect = quit_surf.get_rect(topright = (resW - 500, (resH / 2) + 50))

quit_surf = menu_font.render(quit_game, False, 'sky blue')
quit_rect = quit_surf.get_rect(topright = (resW - 500, (resH / 2) + 50))

#creates a surface for rendering the levels of the level select menu in the pygame window
level_surf_list = []
level_rect_list = []
for i in range(level_count):
    level_surf_list.append(menu_font.render("Level " + str(i + 1), False, 'lawn green'))
    level_rect_list.append(level_surf_list[i].get_rect(topleft = (65, 25 + (i * 55))))

#creates a surface for the game over screen
fail_surf = menu_font.render(game_fail, False, 'red')
fail_rect = fail_surf.get_rect(midtop = (resW / 2, 25))

BotCars = pygame.sprite.Group()
myCar = BotCar()
BotCars.add(myCar)
    
player = pygame.sprite.GroupSingle()
playerCar = PlayerCar()
player.add(playerCar)
    
playerCar.setCollide(BotCars)
myCar.setCollide(player)

#game loop runs unitl a quit condition is met
while True:

    #event loop checks for all possible events in the game
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
                        pygame.quit()
                        exit()
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
                            play_state = True
                            level_choice = i + 1
                            #print(level_choice)
                            screen.fill('black')

        if end_state:

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                play_state = True
                end_state = False
                playerCar.setImage()
                myCar.setImage()
                start_time = pygame.time.get_ticks()




    
    #if title_state True, shows the title menu
    if title_state:
        screen.blit(background, (0,0))
        screen.blit(carBackground, (40,400))
        screen.blit(redCar, (560,100))
        screen.blit(title_surf, title_rect)
        screen.blit(play_surf, play_rect)
        screen.blit(quit_surf, quit_rect)

    if level_state:
        screen.blit(background, (0,0))
        screen.blit(carBackground, (40,400))
        screen.blit(redCar, (560,100))
        for i in range(level_count):
            screen.blit(level_surf_list[i], level_rect_list[i])

    if play_state:
        match level_choice:
            case 1:
                screen.fill((50, 200, 50))
                myCar.setTarget(pygame.mouse.get_pos())
            case 2:
                screen.fill((255, 200, 100))
            case 3:
                screen.fill((100, 200, 255))
            case 4:
                screen.fill((200, 100, 255))
            case 5:
                screen.fill((255, 100, 200))
            case 6:
                screen.fill((200, 255, 100))
            case 7:
                screen.fill((100, 255, 200))
            case 8:
                screen.fill((200, 100, 100))
            case 9:
                screen.fill((100, 200, 100))
            case 10:
                screen.fill((100, 100, 200))

        display_score()
        player.update() 
        BotCars.update()           
        BotCars.draw(screen)
        player.draw(screen)
        
        if playerCar.isStopped():
            play_state = False
            end_state = True

    if end_state:
        screen.blit(fail_surf, fail_rect)

    #update screen with a background
    pygame.display.flip()
    clock.tick(60)

pygame.quit()