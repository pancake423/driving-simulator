import pygame
from random import randint
from levels import Level
from cars import *

def levelFive(screen, screen_width, screen_height):
    level_title = "Urge to Merge"
    level_overview = "You start this level at the beginning of a highway on-ramp. While going down the ramp, match speed with highway traffic and safely merge. Avoid stopping on the on-ramp"

    #Level Elements
    level = Level(screen_width, screen_height)
    level.add_horizontal_road(0,screen_width,screen_height/3)
    #level.add_diagonal_road(0,screen_height,screen_width/2,screen_height/3)
    level.add_random_decorations(20)
    
    #Player
    player = pygame.sprite.GroupSingle()
    playerCar = PlayerCar((30,screen_height-30),)
    player.add(playerCar)
    
    #Bots
    bots = pygame.sprite.Group()
    botCar1 = BotCar((20,screen_height/3 + 50))
    botCar2 = BotCar((20,screen_height/4 + 20))
    bots.add(botCar1)
    bots.add(botCar2)
    botList = [botCar1, botCar2]
    botCar1.setTarget((screen_width + 100,screen_height/3 + 50))
    botCar2.setTarget((screen_width + 100,screen_height/4 + 20))
    
    #Collisions
    playerCar.setCollide([bots])
    botCar1.setCollide([player])
    botCar2.setCollide([player])
    
    clock = pygame.time.Clock()
    last_spawned = pygame.time.get_ticks() #initializing this for later
    run = True
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        #If there's less than 5 bot cars, create a new one
        if len(bots.sprites()) < 5:
            #wait 1 second between spawning cars so they do't spawn on top of each other
            if (pygame.time.get_ticks() - last_spawned) > 1000:
                #Divides the cars between both lanes of the road
                if randint(0,1) == 1:
                    botCarNum = BotCar((-50,screen_height/3 + 50))
                    botCarNum.setTarget((screen_width + 100,screen_height/3 + 50))
                else:
                    botCarNum = BotCar((-50,screen_height/4 + 20))
                    botCarNum.setTarget((screen_width + 100,screen_height/4 + 20))
                
                last_spawned = pygame.time.get_ticks()
                
                bots.add(botCarNum)
                botList.append(botCarNum)
                botCarNum.setCollide([player])
            
        else:    
            #Deletes bots once they get to the right and recreates them on the left
            for botCar in botList:
                if botCar.rect.x > screen_width + 50:
                   botList.remove(botCar)
                   botCar.kill()
            
        screen.fill(level.BG_COLOR)
        level.draw(screen, 0, 0)
        
        bots.draw(screen)
        bots.update()
        player.draw(screen)
        player.update()
        
        pygame.display.flip()
        
if __name__ == "__main__":
    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    
    levelFive(screen, screen_width, screen_height)
    pygame.quit()
    