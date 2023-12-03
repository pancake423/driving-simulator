import pygame
from levels import Level
from cars import *

class Tutorial(Level):
    level_title = "Stay on the Road!"
    level_overview = "Learn to control the vehicle, drive forward, back, stop, and turn."

    #initialize/build the level
    def __init__(self, screen, screen_w, screen_h):

        super().__init__(screen_w, screen_h)

        #add the level, a t-intersection, to the tutorial level
        self.add_t_intersection(screen_w / 2, screen_h / 2, entrance="left")
        self.add_horizontal_road(screen_w / 2 - 108, 0, screen_h / 2)
        self.add_vertical_road(screen_w / 2, screen_h / 2 - 108, 0)
        self.add_vertical_road(screen_w / 2, screen_h / 2 + 108, screen_h)
        self.add_random_decorations(20)
        self.timeOffroad = pygame.time.get_ticks() #tracks time player is off the road, used to fail player in certain cases

        #initialize the player car sprite
        self.player = pygame.sprite.GroupSingle()
        self.playerCar = PlayerCar((60, (screen_h / 2) + 65), 0)
        self.player.add(self.playerCar)

        #initialize the bot car sprite(s)
        self.bots = pygame.sprite.Group()
        self.botCar1 = BotCar((screen_w / 2 + 65, screen_h + 100), 270)
        self.botCar1.setTarget(((screen_w / 2 + 65, -100), False))
        self.botCar2 = BotCar((screen_w / 2 - 65, -100), 90)
        self.botCar2.setTarget(((screen_w / 2 - 65, screen_h + 100), False))
        self.bots.add(self.botCar1)
        self.bots.add(self.botCar2)

        #set collision(s) for the player and the bot car(s)
        self.playerCar.setCollide([self.bots])
        self.botCar1.setCollide([self.player])

    #update prints all the elements of the level to the screen as well as
    #checking pass/fail conditions of the level and returning pass/fail
    #if one of these conditions is met, depending on the condition
    def update(self, screen):
        self.draw(screen, 0, 0)
        self.bots.draw(screen)
        self.bots.update()
        self.player.draw(screen)
        self.player.update()
        

        #this checks that the player is on the road
        onRoad = self.get_targets(self.playerCar)

        #here be road rules

        #records time
        timer = pygame.time.get_ticks()
        if self.playerCar.isStopped():
            #wait 3 seconds to allow explosion visual and sound to play
            if (pygame.time.get_ticks() - timer) > 3000:
                print("Crashed fail")
                return "Fail"
            
        if len(onRoad) < 1:
            if not self.playerCar.isOffRoad():
                self.playerCar.offRoad = True
                self.timeOffroad = pygame.time.get_ticks()
            
            else:
                if pygame.time.get_ticks() - self.timeOffroad >= 1000:
                    print("Offroad fail")
                    return "Fail"
        
        else:
            self.playerCar.offRoad = False
            
        if self.playerCar.rect.x < self.width / 2 - 65:
            if (self.playerCar.rect.y < (self.height / 2) - 50) and (self.playerCar.getAngle() < 90 or self.playerCar.getAngle() > 270):
                print("Crossed median fail")
                return "Fail"
            
        if self.playerCar.getAngle() >= 90 and self.playerCar.getAngle() <= 270:
            if (self.playerCar.rect.x < (self.width / 2) - 50):
                print("Crossed median fail")
                return "Fail"
        
        if self.playerCar.rect.y > (self.width + 50):
            print("Passed")
            return "Pass"
        
        else: 
            return "NA"
        
if __name__ == "__main__":
    pygame.init()
    screen_w = 1920
    screen_h = 1080

    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN | pygame.SCALED)
    
    clock = pygame.time.Clock()
    level = Tutorial(screen, screen_w, screen_h)
    run = True
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                        
        status = level.update(screen)
        if status == "Pass" or status == "Fail":
            run = False
            print(status)

        pygame.display.flip()
    
    pygame.quit()



    """
    #pygame.init()

    # Create a level instance

    level = Level(screen_width, screen_height)
    
    #stopSign= pygame.image.load('assets/NewTempStop.png')
    #stopSign = pygame.transform.smoothscale(stopSign,(60, 60)).convert_alpha()

    # Coordinates for the intersection
    x = screen_width / 2
    y = screen_height / 2

    # Define coordinates for the horizontal roads
    fh_end_x = screen_width / 2 - 107.5

    sh_start_x = screen_width / 2 + 107.5

    # Coordinates for vertical roads
    v_end_2 = screen_height / 2 - 107.5

    # Call functions to add roads, intersections, etc
    level.add_horizontal_road(0, fh_end_x, y)
    level.add_horizontal_road(sh_start_x, screen_width, y)

    # Add vertical roads and intersection as needed
    level.add_vertical_road(x, 0, v_end_2)
    level.add_intersection(x, y)

    level.add_random_decorations(30)
    """
    #return level
