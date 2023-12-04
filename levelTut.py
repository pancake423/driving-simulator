import pygame
from levels import Level
from cars import *

class Tutorial(Level):
    level_title = "Stay on the Road!"
    level_overview = "Learn to control the vehicle, drive forward, back, stop, and turn."

    #initialize/build the level
    def __init__(self, screen, screen_w, screen_h):

        super().__init__(screen_w, screen_h)

        #set font to 'Get Now.ttf', a free font found online
        self.font = pygame.font.Font('fonts/Get Now.ttf', 25)
    
        #flags
        self.stopped_at_sign = False #used to check if player stopped at the stop sign
        self.play = False #used to allow the level to play after the player has read the instructions
        self.explain = True #used to pause the level and display explanation of controls until user input
        self.crashed = False
        self.stage_0_pass = False
        self.stage_1_pass = False
        self.stage_2_pass = False
        self.stage_3_pass = False
        self.needs_reset = False #used to reset the player car when a fail condition has been achieved

        #0 is stop at sign, 1 is reverse back off-screen, 2 is stop at sign then turn left, 3 is stop at sign and turn right
        #-1 denotes the end of the level
        self.stage = 0 #used to update the tutorial to the next stage after completing an objective

        #stage explanations 
        #(self.stage## - the first digit denotes the stage, the second digit denotes the line of text)
        self.stage00 = "Welcome to our 2D Driving Simulator (I'm still not sure has a proper name)."
        self.stage01 = "Hold either up arrow or 'w' to drive the car forward. Hold space to stop the car."
        self.stage02 = "Press the space bar to continue from this and other following screens."
        self.stage10 = "You actually stopped at the sign? Wow. That's rare. Thank you."
        self.stage11 = "Now, hold either down arrow or 'd' to reverse the car."
        self.stage12 = "It's like going forward, but backward!"
        self.stage20 = "That is illegal. Why did you listen to me? You didn't even check traffic behind you (probably)."
        self.stage21 = "I promise, this time, what I'm asking you to do is legal. In fact, it's required by law."
        self.stage22 = "Stop at the stop sign, then turn right (right arrow or 'd'). CHECK FOR TRAFFIC THIS TIME!"
        self.stage30 = "You did it? You did it, of course you did it, I never doubted you. I swear!"
        self.stage31 = "Now, the final test. Stop at the stop sign, then turn left (left arrow or 'a')."
        self.stage32 = "Do that, and I'll be reeaaalllly impressed."
        self.stage_retry = "Try again."

        #surfaces and rectangles for stage explanations
        self.stage_part_1_surf = None
        self.stage_part_1_rect = None
        self.stage_part_2_surf = None
        self.stage_part_2_rect = None
        self.stage_part_3_surf = None
        self.stage_part_3_rect = None

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
        self.botCar2.setCollide([self.player])

    def stage_instructions(self, screen, stage_part_1, stage_part_2, stage_part_3):
        self.stage_part_1_surf = self.font.render(stage_part_1, False, 'red')
        self.stage_part_1_rect = self.stage_part_1_surf.get_rect(midtop = (self.width / 2, 200))
        self.stage_part_2_surf = self.font.render(stage_part_2, False, 'red')
        self.stage_part_2_rect = self.stage_part_2_surf.get_rect(midtop = (self.width / 2, 275))
        self.stage_part_3_surf = self.font.render(stage_part_3, False, 'red')
        self.stage_part_3_rect = self.stage_part_3_surf.get_rect(midtop = (self.width / 2, 350))
        screen.blit(self.stage_part_1_surf, self.stage_part_1_rect)
        screen.blit(self.stage_part_2_surf, self.stage_part_2_rect)
        screen.blit(self.stage_part_3_surf, self.stage_part_3_rect)

    def check_bots(self):
        if self.botCar1.rect.y <= -100:
            self.bots.remove(self.botCar1)
            self.botCar1.kill()
            self.botCar1 = BotCar((self.width / 2 + 65, self.height + 100), 270)
            self.botCar1.setTarget(((self.width / 2 + 65, -100), False))
            self.bots.add(self.botCar1)
            self.botCar1.setCollide([self.player])
            self.playerCar.setCollide([self.bots])

        if self.botCar2.rect.y >= self.height + 100:
            self.bots.remove(self.botCar2)
            self.botCar2.kill()
            self.botCar2 = BotCar((self.width / 2 - 65, -100), 90)
            self.botCar2.setTarget(((self.width / 2 - 65, self.height + 100), False))
            self.bots.add(self.botCar2)
            self.botCar2.setCollide([self.player])
            self.playerCar.setCollide([self.bots])

    def reset_player(self):
        self.player.remove(self.playerCar)
        self.playerCar.kill()
        self.playerCar = PlayerCar((60, (self.height / 2) + 65), 0)
        self.player.add(self.playerCar)
        self.playerCar.setCollide([self.bots])
        self.botCar1.setCollide([self.player])
        self.botCar2.setCollide([self.player])


    #update prints all the elements of the level to the screen as well as
    #checking pass/fail conditions of the level and returning pass/fail
    #if one of these conditions is met, depending on the condition
    def update(self, screen):

        if self.explain:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print("Input detected.")
                    self.explain = False
                    self.play = True

            screen.fill(self.BG_COLOR)

            if self.stage == 0:
                self.stage_instructions(screen, self.stage00, self.stage01, self.stage02)

            if self.stage == 1:
                self.stopped_at_sign = False
                self.stage_instructions(screen, self.stage10, self.stage11, self.stage12)

            if self.stage == 2:
                if self.needs_reset:
                    self.reset_player()
                    self.needs_reset = False
                    self.stage_instructions(screen, self.stage_retry, self.stage21, self.stage22)

                else:
                    self.stage_instructions(screen, self.stage20, self.stage21, self.stage22)
                        
            if self.stage == 3:
                if self.needs_reset:
                    self.reset_player()
                    self.needs_reset = False
                    self.stage_instructions(screen, self.stage30, self.stage31, self.stage32)

                else:
                    self.stage_instructions(screen, self.stage30, self.stage31, self.stage32)

        if self.play:

            #draw the level elements to the screen
            self.draw(screen, 0, 0)
            self.bots.draw(screen)
            self.bots.update()
            self.player.draw(screen)
            self.player.update()
            if (self.playerCar.rect.x > (self.width / 3)) and (self.playerCar.rect.x < (self.width / 2) + 108):
                if (self.playerCar.getSpeed() == 0):
                    self.stopped_at_sign = True

            match self.stage:
                case 0:
                    print("Stage 0")
                    if self.stopped_at_sign:
                        self.stage = 1
                        self.play = False
                        self.explain = True

                case 1:
                    print("Stage 1")
                    if (self.playerCar.rect.x < 0):
                        self.stage = 2
                        self.playerCar.velocity = 0
                        self.play = False
                        self.explain = True

                case 2:
                    print("Stage 2")
                    if self.playerCar.getAngle() >= 110:
                        self.needs_reset = True
                        self.play = False
                        self.explain = True
                        
                    if self.playerCar.rect.y > (self.height + 100) and self.stopped_at_sign:
                        self.stage = 3
                        self.needs_reset = True
                        self.stopped_at_sign = False
                        self.play = False
                        self.explain = True

                case 3:
                    print("Stage 3")
                    if self.playerCar.getAngle() <= 250 and self.playerCar.getAngle() >= 160:
                        self.needs_reset = True
                        self.play = False
                        self.explain = True
                        
                    if self.playerCar.rect.y < (-100) and self.stopped_at_sign:
                        self.stage = -1
            
            self.check_bots()


            #this checks that the player is on the road
            onRoad = self.get_targets(self.playerCar)

            #here be road rules
                        
            #records time
            timer = pygame.time.get_ticks()
            if self.playerCar.isStopped():
                #wait 3 seconds to allow explosion visual and sound to play
                print(pygame.time.get_ticks() - timer)
                if (pygame.time.get_ticks() - timer) >= 2000:
                    print("Crashed fail")
                    return "Fail"
                
            if len(onRoad) < 1 and not self.needs_reset:
                if not self.playerCar.isOffRoad():
                    self.playerCar.offRoad = True
                    self.timeOffroad = pygame.time.get_ticks()
                
                else:
                    if pygame.time.get_ticks() - self.timeOffroad >= 1000:
                        print("Offroad fail")
                        return "Fail"
            
            else:
                self.playerCar.offRoad = False
                
            if not self.stopped_at_sign:
                if (self.playerCar.rect.y < (self.height / 2) - 50) and (self.playerCar.getAngle() < 90 or self.playerCar.getAngle() > 270):
                    print("Crossed median fail 1")
                    return "Fail"
            
            if self.playerCar.getAngle() >= 260 and self.playerCar.getAngle() <= 300:
                if (self.playerCar.rect.x < (self.width / 2) - 65):
                    print("Crossed median fail 2")
                    return "Fail"
                    
                elif self.playerCar.rect.y >= self.height + 100 and not self.stopped_at_sign:
                    print("Stop Fail 1")
                    return "Fail"
                    
            if self.playerCar.getAngle() <= 110 and self.playerCar.getAngle() >= 70:
                if (self.playerCar.rect.x > (self.width / 2) + 65):
                    print("Crossed median fail 3")
                    return "Fail"
                    
                elif self.playerCar.rect.y <= -100 and not self.stopped_at_sign:
                    print("Stop Fail 2")
                    return "Fail"
            
            if self.stage == -1:
                print("Passed")
                return "Pass"
            
            else: 
                return "NA"
            
    def pause(self):
        self.pauseTime = pygame.time.get_ticks()
        
    def resume(self):
        self.timeOffroad += pygame.time.get_ticks() - self.pauseTime
        
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
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
