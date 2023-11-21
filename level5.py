import pygame
from random import randint
from levels import Level
from cars import *

class LevelFive(Level):
    level_title = "Urge to Merge"
    level_overview = "You start this level at the beginning of a highway on-ramp. While going down the ramp, match speed with highway traffic and safely merge. Avoid stopping on the on-ramp"
    
    def __init__(self,screen, screen_width, screen_height):
        super().__init__(screen_width,screen_height)
        
        #Level Elements
        self.add_4_lane_with_on_ramp(0,screen_height/3,screen_width,screen_height/3,0,screen_height)
        self.add_random_decorations(20)
        self.offRoadTimer = pygame.time.get_ticks()
        
        #Player
        self.player = pygame.sprite.GroupSingle()
        self.playerCar = PlayerCar((150,screen_height-60),315)
        self.player.add(self.playerCar)
        
        #Bots
        self.bots = pygame.sprite.Group()
        self.botCar1 = BotCar((20,screen_height/3 + 90))
        self.botCar2 = BotCar((20,screen_height/3 + 180))
        self.bots.add(self.botCar1)
        self.bots.add(self.botCar2)
        self.botList = [self.botCar1, self.botCar2]
        self.botCar1.setTarget(((screen_width + 100,screen_height/3 + 100),False))
        self.botCar2.setTarget(((screen_width + 100,screen_height/3 + 180),False))
        self.last_spawned = pygame.time.get_ticks() #initializing this for later
        
        #Collisions
        self.playerCar.setCollide([self.bots])
        self.botCar1.setCollide([self.player])
        self.botCar2.setCollide([self.player])
    
    def update(self):
        self.draw(screen, 0, 0)
        self.bots.draw(screen)
        self.bots.update()
        self.player.draw(screen)
        self.player.update()

        #Creates Bot Traffic
        self.botCount = 10
        #If there's less than botCount bot cars, create a new one
        if len(self.bots.sprites()) < self.botCount:
            #wait 0.5 seconds between spawning cars so they don't spawn on top of each other
            if (pygame.time.get_ticks() - self.last_spawned) > 500:
                #Divides traffic between both sides of the divided highway
                if randint(0,1) == 1:
                    #Divides traffic between both lanes
                    if randint(0,1) == 1:
                        self.botCar = BotCar((-50,screen_height/3 + 90))
                        self.botCar.setTarget(((screen_width + 100,screen_height/3 + 90),False))
                    else:
                        self.botCar = BotCar((-50,screen_height/3 + 180))
                        self.botCar.setTarget(((screen_width + 100,screen_height/3 + 180),False))
                else:
                    if randint(0,1) == 1:
                        self.botCar = BotCar((screen_width + 50,screen_height/4),180)
                        self.botCar.setTarget(((-200,screen_height/4),False))
                    else:
                        self.botCar = BotCar((screen_width + 50,screen_height/4 - 90),180)
                        self.botCar.setTarget(((-200,screen_height/4 - 90),False))
                
                self.last_spawned = pygame.time.get_ticks()
                
                self.bots.add(self.botCar)
                self.botList.append(self.botCar)
                self.botCar.setCollide([self.player])
                
        else:    
            #Deletes bots once they go offscreen
            for botCar in self.botList:
                if botCar.rect.x > screen_width + 100 or botCar.rect.x < -100:
                   self.botList.remove(botCar)
                   botCar.kill()
                   
        #Road Rules
        roads = self.get_targets(self.playerCar)#Checks if player is on the road
        if self.playerCar.isStopped():
            return "Fail"
        
        #if player is offroad or between roads for more than a second, fail
        if len(roads) != 1:
            if bool(self.playerCar.isOffRoad()) == False:
                self.playerCar.offRoad = True
                self.offRoadTimer = pygame.time.get_ticks()
                
            else:
                print(f"Offroad for {pygame.time.get_ticks() - self.offRoadTimer} milliseconds")
                if pygame.time.get_ticks() - self.offRoadTimer >= 1000:
                    return "Fail"
            
        else:
            self.playerCar.offRoad = False
            
        #if player goes past the median, fail
        print(self.playerCar.rect.y)
        if self.playerCar.rect.y < (screen_height/3):
            return "Fail"
            
        #If player successfully merges and continues to the right, pass
        if self.playerCar.rect.x > screen_width + 50:
            return "Pass"
        
        else:
            return "NA"
        
if __name__ == "__main__":
    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    
    clock = pygame.time.Clock()
    level = LevelFive(screen,screen_width,screen_height)
    run = True
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        status = level.update()
        if status == "Pass" or status == "Fail":
            run = False
            print(status)
            
        pygame.display.flip()
    
    pygame.quit()
    