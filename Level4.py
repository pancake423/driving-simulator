import pygame
from levels import Level
from cars import PlayerCar, BotCar

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
    botCar.setTarget((-1000, topLaneY))
    
    
    playerCar.setCollide(botGroup)
    botCar.setCollide(playerGroup)
    
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
            botCar.setTarget((playerX + 100, playerY), True)
            botTurned = True
          
        pygame.display.flip()
        
    if playerCar.isStopped():
        return "Collided!"
    else:
        return "Didn't collide!"


if __name__ == "__main__":
    pygame.init()
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    
    print(level_Four(screen, screen_width, screen_height))
    pygame.quit()
    
    
    