import pygame
import math
from cars import PlayerCar, BotCar
from levels import Level

class levelthree(Level):
    
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        #Declarations
        levelNum = "Level 3"
        
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

        #font type
        fontType = "fonts/Get Now.ttf"
        levelFont = pygame.font.Font(fontType, 40)
        self.level_surf = levelFont.render(levelNum, True, "red")
        self.level_rect = self.level_surf.get_rect(topright = (screen_width - 20, 20))
        
        self.topLaneY = screen_height / 2 - 110
        self.botLaneY = screen_height / 2 + 10
        
        self.playerCar = PlayerCar((80, 600))
        self.playerGroup = pygame.sprite.GroupSingle()
        self.playerGroup.add(self.playerCar)
        
        self.botCar = BotCar((screen_width, self.topLaneY + 50), 180)
        self.botCar2 = BotCar((x1 - 50, 50), 90)
        self.botCar3 = BotCar((x2 + 50, screen_height - 50), 270)
        
        self.botGroup = pygame.sprite.Group()
        
        self.botGroup.add(self.botCar)
        self.botGroup.add(self.botCar2)
        self.botGroup.add(self.botCar3)
        
        self.botCar.setTarget(((1150, self.topLaneY + 50), True))
        self.botCar2.setTarget(((900, self.topLaneY - 60), True))
        self.botCar3.setTarget(((1000, self.topLaneY + 270), True))
        
        self.playerCar.setCollide([self.botGroup])
        self.botCar.setCollide([self.playerGroup])
        self.botCar2.setCollide([self.playerGroup])
        self.botCar3.setCollide([self.playerGroup])

        #displays level 6 on screen
        pygame.display.set_caption(levelNum)
              
        
        #call functions to add roads, intersections, etc
        self.add_horizontal_road(fh_start_x, fh_end_x, fh_y)
        self.add_horizontal_road(sh_start_x, sh_end_x, sh_y)
        self.add_vertical_road(x1, v_st_1, v_end_1)
        self.add_vertical_road(x2, v_st_2, v_end_2)
        self.add_intersection(inter_x, inter_y)
        self.add_random_decorations(30)
        
        
        #Adds stop sign
        self.stopSign= pygame.image.load('assets/stop-sign.png')
        self.stopSign = pygame.transform.smoothscale(self.stopSign,(60, 60)).convert_alpha()
        self.stopSignCoords = [(760, 670), (1090, 670), (1090, 350), (760,350)]
        
        #variables for timer
        self.carsGone = 0
        self.timer = None

    def update(self,screen):
        # Clear the screen
        screen.fill(self.BG_COLOR) 

        # Draw the level
        self.draw(screen, 0, 0)
        

        screen.blit(self.level_surf, self.level_rect)
        screen.blit(self.stopSign, (760, 670))
        screen.blit(self.stopSign, (1090, 670))
        screen.blit(self.stopSign, (1090, 350))
        screen.blit(self.stopSign, (760, 350))
        
        # Initialize timer
        if self.timer == None:
            self.timer = pygame.time.get_ticks()
            
        if self.carsGone == 0 and self.botCar.newTarget() and (pygame.time.get_ticks() - self.timer()) / 1000 > 2:
            self.timer = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - self.timer) / 1000 > 2:
            self.timer = pygame.time.get_ticks()
            if self.carsGone == 0:
                self.botCar3.setTarget(((1000, -200), True))
            elif self.carsGone == 1:   
                self.botCar2.setTarget(((900, self.height + 200), True))
            elif self.carsGone == 2:
                self.botCar.setTarget(((-200, self.topLaneY + 50), True))
            self.carsGone += 1

        
            
            

        playerPos, botPos = self.playerCar.getPos(), self.botCar.getPos()
        playerX, playerY = playerPos
        botX, botY = botPos
        
        self.playerGroup.update()
        self.botGroup.update()
        self.playerGroup.draw(screen)
        self.botGroup.draw(screen)
#Road Rules
        roads = self.get_targets(self.playerCar)#Checks if player is on the road
        
        timer = pygame.time.get_ticks()
        if self.playerCar.isStopped():
            #waits 3 seconds before failing so player can see the explosion
            if (pygame.time.get_ticks() - timer) > 3000:
                return "Fail"
        
        #if player is offroad or between roads for more than a second, fail
        if len(roads) != 1:
            if bool(self.playerCar.isOffRoad()) == False:
                self.playerCar.offRoad = True
                self.offRoadTimer = pygame.time.get_ticks()
                
            else:
                if pygame.time.get_ticks() - self.offRoadTimer >= 1000:
                    return "Fail"
            
        else:
            self.playerCar.offRoad = False
            
        #if player goes past the median, fail
        if self.playerCar.rect.y < (self.height/3):
            return "Fail"
            
        #If player successfully merges and continues to the right, pass
        if self.playerCar.rect.x > self.width + 50:
            return "Pass"
        
        else:
            return "NA"

    def pause(self):
        self.pauseTime = pygame.time.get_ticks()
        
    def resume(self):
        self.timer += pygame.time.get_ticks() - self.pauseTime

"""
def level_Three(screen, screen_width, screen_height):
    #Declarations
    levelNum = "Level 3"

    #Initialize font
    pygame.font.init()
    
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

    #font type
    fontType = "fonts/Get Now.ttf"
    levelFont = pygame.font.Font(fontType, 40)
    level_surf = levelFont.render(levelNum, True, "red")
    level_rect = level_surf.get_rect(topright = (screen_width - 20, 20))
    
    topLaneY = screen_height / 2 - 110
    botLaneY = screen_height / 2 + 10
    
    playerCar = PlayerCar((80, 600))
    playerGroup = pygame.sprite.GroupSingle()
    playerGroup.add(playerCar)
    
    botCar = BotCar((screen_width, topLaneY + 50), 180)
    botCar2 = BotCar((x1 - 50, 50), 90)
    botCar3 = BotCar((x2 + 50, screen_height - 50), 270)
    
    botGroup = pygame.sprite.Group()
    
    botGroup.add(botCar)
    botGroup.add(botCar2)
    botGroup.add(botCar3)
    
    botCar.setTarget(((1150, topLaneY + 50), True))
    botCar2.setTarget(((900, topLaneY - 60), True))
    botCar3.setTarget(((1000, topLaneY + 270), True))
    
    playerCar.setCollide([botGroup])
    botCar.setCollide([playerGroup])
    botCar2.setCollide([playerGroup])
    botCar3.setCollide([playerGroup])

    #displays level 6 on screen
    pygame.display.set_caption(levelNum)
    
    #create a level instance
    level = Level(screen_width, screen_height)
    
    
    
    #call functions to add roads, intersections, etc
    level.add_horizontal_road(fh_start_x, fh_end_x, fh_y)
    level.add_horizontal_road(sh_start_x, sh_end_x, sh_y)
    level.add_vertical_road(x1, v_st_1, v_end_1)
    level.add_vertical_road(x2, v_st_2, v_end_2)
    level.add_intersection(inter_x, inter_y)
    level.add_random_decorations(30)
    
    
    #Adds stop sign
    stopSign= pygame.image.load('assets/stop-sign.png')
    stopSign = pygame.transform.smoothscale(stopSign,(60, 60)).convert_alpha()
    stopSignCoords = [(760, 670), (1090, 670), (1090, 350), (760,350)]
    
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
        
        playerGroup.update()
        botGroup.update()
        playerGroup.draw(screen)
        botGroup.draw(screen)
        

        playerPos, botPos = playerCar.getPos(), botCar.getPos()
        botCar.update()
        playerX, playerY = playerPos
        botX, botY = botPos

        # Update the display
        pygame.display.flip()
    
     
  """  

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    540
    # Set screen
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN | pygame.SCALED)
    
    #calls the level_Three() Funcntion
    clock = pygame.time.Clock()
    run = True
    myLevel = levelthree(screen, screen_width, screen_height)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        status = myLevel.update(screen)
        
        if status == "Pass" or status == "Fail":
            run = False
            print(status)
                
        pygame.display.flip()
    
    pygame.quit()
        

