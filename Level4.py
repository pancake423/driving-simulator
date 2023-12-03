import pygame
from levels import Level
from cars import PlayerCar, BotCar

class LevelFour(Level):
    
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.add_horizontal_road(0, screen_width, screen_height / 2 - 53)
        self.add_random_decorations(30)
        
        self.topLaneY = screen_height / 2 - 110
        self.botLaneY = screen_height / 2 + 10
        
        self.playerCar = PlayerCar((80, self.botLaneY))
        self.playerGroup = pygame.sprite.GroupSingle()
        self.playerGroup.add(self.playerCar)
    
        self.botCar = BotCar((screen_width, self.topLaneY), 180)
        self.botGroup = pygame.sprite.Group()
        self.botGroup.add(self.botCar)
        self.botCar.setTarget(((-1000, self.topLaneY), False))
        
        self.playerCar.setCollide([self.botGroup])
        self.botCar.setCollide([self.playerGroup])
        
        self.botTurned = False
        self.startTime = pygame.time.get_ticks()
        
    def update(self, screen):
        self.draw(screen, 0, 0)
        
        self.playerGroup.update()
        self.botGroup.update()
        self.playerGroup.draw(screen)
        self.botGroup.draw(screen)
        
        playerPos, botPos = self.playerCar.getPos(), self.botCar.getPos()
        playerAngle = self.playerCar.getAngle()
        playerSpeed = self.playerCar.getSpeed()
        playerX, playerY = playerPos
        botX, botY = botPos
        
        timePassed = (pygame.time.get_ticks() - self.startTime) / 1000
        
        roads = self.get_targets(self.playerCar)
        
        # Before AI car turns
        if not self.botTurned:
            
            # Road Rules (Other lane, off road, wrong way, or not up to speed)
            if (len(roads) != 1 or
                (playerAngle > 90 and playerAngle < 270) or
                (playerSpeed < 30 and timePassed > 3)):
                
                return "Fail"
            
            # Make AI turn when close
            if botX - playerX < 450:
                self.botCar.setTarget(((playerX + 100, playerY), True))
                self.botTurned = True
                self.startTime = pygame.time.get_ticks()
                
        # After AI car turns
        else:
            if len(roads) > 1 or (self.playerCar.isStopped() and timePassed > 3):
                return "Fail"
            elif timePassed > 3:
                return "Pass"
        
        return "NA"
    
    def pause(self):
        self.pauseTime = pygame.time.get_ticks()
        print(f"Paused at {self.pauseTime}")
        
    def resume(self):
        self.startTime += pygame.time.get_ticks() - self.pauseTime
        print(f"Resumed, adding {pygame.time.get_ticks() - self.pauseTime}ms")

"""
def level_Four(screen, screen_width, screen_height):
    level = Level(screen_width, screen_height)
    level.add_horizontal_road(0, screen_width, screen_height / 2 - 53)
    level.add_random_decorations(30)
    
    topLaneY = screen_height / 2 - 110
    botLaneY = screen_height / 2 + 10
    
    playerCar = PlayerCar((80, botLaneY))
    playerGroup = pygame.sprite.GroupSingle()
    playerGroup.add(playerCar)
    
    botCar = BotCar((screen_width, topLaneY), 180)
    botGroup = pygame.sprite.Group()
    botGroup.add(botCar)
    botCar.setTarget(((-1000, topLaneY), False))
    
    
    playerCar.setCollide([botGroup])
    botCar.setCollide([playerGroup])
    
    clock = pygame.time.Clock()
    run = True
    botTurned = False
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        level.draw(screen, 0, 0)
        
        playerGroup.update()
        botGroup.update()
        playerGroup.draw(screen)
        botGroup.draw(screen)
        
        playerPos, botPos = playerCar.getPos(), botCar.getPos()
        playerX, playerY = playerPos
        botX, botY = botPos
        
        if not botTurned and botX - playerX < 450:
            botCar.setTarget(((playerX + 100, playerY), True))
            botTurned = True
            
        print(level.get_targets(playerCar))
          
        pygame.display.flip()
        
    if playerCar.isStopped():
        return "Collided!"
    else:
        return "Didn't collide!"
"""


if __name__ == "__main__":
    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    
    clock = pygame.time.Clock()
    run = True
    myLevel = LevelFour(screen, screen_width, screen_height)
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