#import libraries from pygame extension
import pygame

#import classes PlayerCar and BotCar from cars.py
from cars import PlayerCar, BotCar

#import classes Level, RectSprite, ImageSprite, & RoadLane
from levels import Level, RectSprite, ImageSprite, RoadLane, Level

#import level_Tut function
from levelTut import level_Tutorial

#import level_Four function
from Level4 import level_Four

def display_score(x_axis = 25, y_axis = 25):
    current_time = "Score: " + str((pygame.time.get_ticks() - start_time - paused_time) / 1000)
    score_surf = menu_font.render(current_time, False, (221, 73, 73))
    score_rect = score_surf.get_rect(topleft = (x_axis, y_axis))
    screen.blit(score_surf, score_rect)

def display_speed(player_car, is_x_flipped):
    if is_x_flipped:
        player_speed = "Speed: {0:.2g}".format((-1) * playerCar.getSpeed())
    else:
        player_speed = "Speed: {0:.2g}".format(playerCar.getSpeed())
    speed_surf = menu_font.render(player_speed, False, (221, 73, 73))
    speed_rect = speed_surf.get_rect(bottomleft = (25, resH - 25))
    screen.blit(speed_surf, speed_rect)

def refresh_cars(player_car, bot_car):
    BotCars.add(bot_car)
    player.add(player_car)
    player_car.setCollide([BotCars])
    bot_car.setCollide([player])  
    return player_car, bot_car



#initailize clock for the game
clock = pygame.time.Clock()

#initialize pygame fonts
pygame.font.init()

start_time = 0
time_at_pause = 0
paused_time = 0

#define and set title of pygame that will display on the window border
game_title = "2-D Driving Simulator"
pygame.display.set_caption(game_title)

#define and set title menu options
play_game = "Play"
quit_game = "Quit"

#define and set start play screen
start_playing = "Press 'Spacebar' to begin the level"

#define and set pause menu options
continue_game = "Continue"
quit_to_desktop = "Quit to Desktop"
quit_to_title = "Quit to Title Screen"

#define game over
game_fail = "Game Over"

#define restart or quit message
ask_retry = "Press 'spacebar' to retry the level"
ask_quit = "Press 'q' to return to level select"

#define and set font type(s)
font_type = 'fonts/Get Now.ttf'

#set title_state to True to control title screen portion of game loop
title_state = True

#set level_state to False to control level select screen portion of game loop
level_state = False

#start start_screen to False to control start screen of each level
start_screen = False

#set play_state and pause_state to False to control gameplay portion of game loop
play_state = False
pause_state = False
paused_level_screen = False

#set end_state to False to control level end screen portion of game loop
end_state = False

botTurned = False

cars_group = False

#set amount of levels
level_count = 5
level_choice = 0

#for screen width and heigth, defined and initialized here to make changing easy
resW = 1920
resH = 1080
resCH = 420

#set the screen using resW and resH as arguments
screen = pygame.display.set_mode((resW, resH))

#set background image for title menu
background = pygame.image.load('assets/standard-road.png')
#background_ratio = background.get_width()/background.get_height()
background = pygame.transform.smoothscale(background,(resW,resH)).convert_alpha()
background_rect = background.get_rect(midtop = (resW/2, 0))

#car background image for title menu
carBackground = pygame.image.load('assets/unicorn-car-blue.png')
car_ratio = carBackground.get_width()/carBackground.get_height()
carBackground = pygame.transform.smoothscale(carBackground,(resCH*car_ratio,resCH)).convert_alpha()
carBackground_rect_one = carBackground.get_rect(midbottom = (420, 900))
carBackground_rect_two = carBackground.get_rect(midbottom = (420, 750))

#AI car background image for title menu
AIcarBackground = pygame.image.load('assets/unicorn-car-red.png')
AICarBackground = pygame.transform.smoothscale(AIcarBackground,(resCH*car_ratio,resCH)).convert_alpha()
AICarBackground = pygame.transform.flip(AICarBackground, False, True)
AICarBackground_rect_one = AICarBackground.get_rect(midtop = (1340, 200))
AICarBackground_rect_two = AICarBackground.get_rect(midtop = (1340, 350))

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
level_list = [None for i in range(level_count)]
for i in range(level_count):
    level_surf_list.append(menu_font.render("Level " + str(i + 1), False, 'lawn green'))
    level_rect_list.append(level_surf_list[i].get_rect(topleft = (120, 50 + (i * 130))))

#creates surfaces for the game over screen and retry message
fail_surf = menu_font.render(game_fail, False, 'red')
fail_rect = fail_surf.get_rect(midtop = (resW / 2, 25))
retry_surf = menu_font.render(ask_retry, False, 'red')
retry_rect = retry_surf.get_rect(midtop = (resW / 2, 100))

return_title_surf = menu_font.render(ask_quit, False, 'red')
return_title_rect = return_title_surf.get_rect(midtop = (resW / 2, 175))

#creates surfaces for the pause screen
continue_surf = menu_font.render(continue_game, False, 'red')
continue_rect = continue_surf.get_rect(midtop = (resW / 2, 200))
quit_title_surf = menu_font.render(quit_to_title, False, 'red')
quit_title_rect = quit_title_surf.get_rect(midtop = (resW / 2, 275))
quit_desktop_surf = menu_font.render(quit_to_desktop, False, 'red')
quit_desktop_rect = quit_desktop_surf.get_rect(midtop = (resW / 2, 350))
pause_surf = pygame.Surface((resW - 200, resH - 100))
pause_surf.fill('black')
pause_rect = pause_surf.get_rect(midtop = (resW / 2, 50))

#creates a surface for the start playing screen
start_surf = menu_font.render(start_playing, False, 'red')
start_rect = start_surf.get_rect(midtop = (resW / 2, resH / 200))

BotCars = pygame.sprite.Group() 
player = pygame.sprite.GroupSingle()

if __name__ == "__main__":

    #initialize pygame
    pygame.init()

    #game loop runs unitl a quit condition is met
    while True:

        #game loop primarily responsible for display
        #if title_state True, shows the title menu
        if title_state:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(background, background_rect)
            screen.blit(carBackground, carBackground_rect_one)
            screen.blit(AICarBackground, AICarBackground_rect_one)
            screen.blit(title_surf, title_rect)
            screen.blit(play_surf, play_rect)
            screen.blit(quit_surf, quit_rect)

            if play_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, 'lawngreen', play_rect, 3)
            elif quit_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, 'lawngreen', quit_rect, 3)

        if level_state:
            screen.blit(background, background_rect)
            screen.blit(carBackground, carBackground_rect_two)
            screen.blit(AICarBackground, AICarBackground_rect_two)
            for i in range(level_count):
                screen.blit(level_surf_list[i], level_rect_list[i])
                if level_rect_list[i].collidepoint(mouse_pos):
                    pygame.draw.rect(screen, 'lawngreen', level_rect_list[i], 3)

        if start_screen:

            screen.fill(Level.BG_COLOR)
            screen.blit(start_surf, start_rect)

        if play_state:
            topLaneY = 0
            topLaneX = 80
            botLaneY = 0
            botLaneX = resW
            x_flip = False
            match level_choice:
                case 1:
                    topLaneY = (resH / 2) - 65
                    topLaneX = resW - 80
                    botLaneY = (resH / 2) + 65
                    botLaneX = 80
                    x_flip = True
                    if level_list[level_choice - 1] == None:
                        level_list[level_choice - 1] = level_Tutorial(screen, resW, resH)

                    if not cars_group:
                        playerCar = PlayerCar((topLaneX, topLaneY), 180)
                        myCar = BotCar((botLaneX, botLaneY))
                        BotCars.add(myCar)
                        player.add(playerCar)
                        playerCar.setCollide([BotCars])
                        myCar.setCollide([player])
                        cars_group = True
                        
                    screen.fill(Level.BG_COLOR)
                    myCar.setTarget(((resW / 2) - 107.5, botLaneY))
                case 2:
                    screen.fill((255, 200, 100))
                case 3:
                    screen.fill((100, 200, 255))
                case 4:
                    topLaneY = resH / 2 + 10
                    botLaneY = resH / 2 - 110
                    x_flip = False
                    if level_list[level_choice - 1] == None:
                        level_list[level_choice - 1] = level_Four(screen, resW, resH)

                    if not cars_group:
                        playerCar = PlayerCar((topLaneX, topLaneY))
                        myCar = BotCar((botLaneX, botLaneY), 180)
                        player.add(playerCar)
                        BotCars.add(myCar)
                        playerCar.setCollide([BotCars])
                        myCar.setCollide([player])
                        cars_group = True

                    myCar.setTarget((-1000, topLaneY))
                    screen.fill(Level.BG_COLOR)

                    playerPos, botPos = playerCar.getPos(), myCar.getPos()
                    playerX, playerY = playerPos
                    botX, botY = botPos
        
                    if not botTurned and botX - playerX < 450:
                        myCar.setTarget((playerX + 100, playerY), True)
                        botTurned = True

                case 5:
                    screen.fill((255, 100, 200))

            player.update() 
            BotCars.update()
            level_list[level_choice - 1].draw(screen, 0, 0)           
            BotCars.draw(screen)
            player.draw(screen)
            display_score()

            if playerCar.isStopped():
                play_state = False
                end_state = True

        if pause_state:
            screen.blit(pause_surf, pause_rect)
            screen.blit(continue_surf, continue_rect)
            screen.blit(quit_title_surf, quit_title_rect) 
            screen.blit(quit_desktop_surf, quit_desktop_rect)

            if continue_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, 'lawngreen', continue_rect, 3)
            elif quit_title_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, 'lawngreen', quit_title_rect, 3)   
            elif quit_desktop_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, 'lawngreen', quit_desktop_rect, 3) 

        if end_state:
            screen.blit(fail_surf, fail_rect)
            screen.blit(retry_surf, retry_rect)
            screen.blit(return_title_surf, return_title_rect)


        #----event loop checks for all possible events in the game----
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
                                start_screen = True
                                start_time = pygame.time.get_ticks()
                                level_choice = i + 1
                                screen.fill('black')

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause_state = True
                    level_state = False
                    paused_level_screen = True


            if start_screen:
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    play_state = True
                    start_screen = False

            if play_state:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    time_at_pause = pygame.time.get_ticks()
                    pause_state = True
                    play_state = False

            if pause_state:
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_state = pygame.mouse.get_pressed()
                    if mouse_state[0]:
                        if not paused_level_screen:
                            if continue_rect.collidepoint(mouse_pos):
                                paused_time += pygame.time.get_ticks() - time_at_pause
                                play_state = True
                                pause_state = False
                                
                            if quit_title_rect.collidepoint(mouse_pos):
                                pause_state = False
                                title_state = True
                                if cars_group:
                                    player.remove(playerCar)
                                    BotCars.remove(myCar)
                                    cars_group = False

                                #if not cars_group:
                                    #if (x_flip):
                                        #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY), 180), BotCar((botLaneX, botLaneY)))
                                    #else:
                                        #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY)), BotCar((botLaneX, botLaneY), 180))
                                paused_time = 0

                            if quit_desktop_rect.collidepoint(mouse_pos):
                                pause_state = False
                                pygame.quit()
                                exit()

                        else:
                            if continue_rect.collidepoint(mouse_pos):
                                paused_time += pygame.time.get_ticks() - time_at_pause
                                level_state = True
                                pause_state = False
                                paused_level_screen = False
                                
                            if quit_title_rect.collidepoint(mouse_pos):
                                pause_state = False
                                title_state = True
                                paused_level_screen = False
                                if cars_group:
                                    player.remove(playerCar)
                                    BotCars.remove(myCar)
                                    cars_group = False

                                #if not cars_group:
                                    #if (x_flip):
                                        #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY), 180), BotCar((botLaneX, botLaneY)))
                                    #else:
                                        #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY)), BotCar((botLaneX, botLaneY), 180))
                                paused_time = 0

                            if quit_desktop_rect.collidepoint(mouse_pos):
                                pause_state = False
                                paused_level_screen = False
                                pygame.quit()
                                exit()

            if end_state:

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    play_state = True
                    end_state = False
                    paused_time = 0
                    if cars_group:
                        player.remove(playerCar)
                        BotCars.remove(myCar)
                        cars_group = False
                    #if not cars_group:
                        #if (x_flip):
                            #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY), 180), BotCar((botLaneX, botLaneY)))
                        #else:
                            #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY)), BotCar((botLaneX, botLaneY), 180))
                    start_time = pygame.time.get_ticks()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    level_state = True
                    end_state = False
                    paused_time = 0
                    if cars_group:
                        player.remove(playerCar)
                        BotCars.remove(myCar)
                        cars_group = False
                    #if not cars_group:
                        #if (x_flip):
                            #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY), 180), BotCar((botLaneX, botLaneY)))
                        #else:
                            #playerCar, myCar = refresh_cars(PlayerCar((topLaneX, topLaneY)), BotCar((botLaneX, botLaneY), 180))

        #----end event loop----

        #update screen with a background
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()