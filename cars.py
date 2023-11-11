import pygame
import math

class AbstractCar(pygame.sprite.Sprite):
    def __init__(self, startPos, startAngle = 0):
        super().__init__()
        
        self.length = 100
        self.maxSpeed = 8
        self.turnSpeed = 0.4
        self.velocity = 0
        self.acceleration = 0.2
        self.angle = startAngle % 360 # Direction the car is facing (increased angle is clockwise rotation)
        self.stopped = False
        self.collideGroups = []
        
        self.subX, self.subY = 0, 0 # Keeps track of small changes in position
        
        self.setImage()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(startPos))
        
    def setImage(self):
        ratio = self.IMG.get_width() / self.IMG.get_height()
        self.image = pygame.transform.smoothscale(self.IMG, (self.length*ratio, self.length)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 270 - self.angle)
      
    # Makes it easy to stop the car when it hits something
    def stop(self):
        self.velocity = 0
        self.stopped = True
    
    def accelerate(self):
        self.velocity += self.acceleration
        self.velocity = min(self.maxSpeed, self.velocity)
    
    def decelerate(self):
        self.velocity -= self.acceleration
        self.velocity = max(-0.5*self.maxSpeed, self.velocity)
        
    def brake(self):
        if self.velocity > 0:
            self.velocity -= self.acceleration
            self.velocity = max(0, self.velocity)
        else:
            self.velocity += self.acceleration
            self.velocity = min(0, self.velocity)
        
    def turn(self, dir, scale = 1):
        oldCenter = self.rect.center
        turnAmount = self.turnSpeed * abs(self.velocity) * scale
        snapBuffer = turnAmount
        
        if dir.lower() == "left":
            self.angle -= turnAmount
            
        elif dir.lower() == "right":
            self.angle += turnAmount
              
        self.angle %= 360
        
        self.setImage()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=oldCenter)        
    
    def snapTurn(self):
        snapBuffer = 4 #Need to dial this in to make it work right
        if (abs(self.velocity)*self.turnSpeed) > snapBuffer:
            #Snap up
            if self.angle < 270 + snapBuffer and self.angle > 270 - snapBuffer:
                self.angle = 270 
            
            #Snap down
            if self.angle < 90 + snapBuffer and self.angle > 90 - snapBuffer:
                self.angle = 90  
            
            #Snap right
            if self.angle < 0 + snapBuffer and self.angle > 0 - snapBuffer:
                self.angle = 0
                
            #Snap left
            if self.angle < 180 + snapBuffer and self.angle > 180 - snapBuffer:
                self.angle = 180
                
            #Snap up-right
            if self.angle < 315 + snapBuffer and self.angle > 315 - snapBuffer:
                self.angle = 315
                
            #Snap down-right
            if self.angle < 45 + snapBuffer and self.angle > 45 - snapBuffer:
                self.angle = 45
                
            #Snap up-left
            if self.angle < 225 + snapBuffer and self.angle > 225 - snapBuffer:
                self.angle = 225
                
            #Snap down-left
            if self.angle < 135 + snapBuffer and self.angle > 135 - snapBuffer:
                self.angle = 135
        
    def move(self):
        delta_x = self.velocity * math.cos(math.radians(self.angle))
        delta_y = self.velocity * math.sin(math.radians(self.angle))
        
        self.subX += delta_x - int(delta_x)
        self.subY += delta_y - int(delta_y)
        
        delta_x += int(self.subX)
        delta_y += int(self.subY)
        self.subX -= int(self.subX)
        self.subY -= int(self.subY)
        
        self.rect.move_ip(delta_x, delta_y)
        
    def getRect(self):
        return self.rect
    
    def checkCollison(self):
        if len(self.collideGroups) > 0:
            for group in self.collideGroups:
                if len(pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_mask)) > 0 and not self.stopped:
                    self.stop()
                    pygame.mixer.Sound.play(self.crash_sound)
                    self.image = pygame.image.load("assets\\explosion.png")
                    self.image = pygame.transform.smoothscale(self.image, (self.length, self.length)).convert_alpha()
            
    def setCollide(self, groups):
        self.collideGroups = groups
        
    def isStopped(self):
        return self.stopped
    
    def getAngle(self):
        return self.angle
    
    def getSpeed(self):
        return self.velocity
    
    def getPos(self):
        return self.rect.center
    
    def setPos(self, pos):
        self.rect.center = pos
    
    def setAngle(self, angle):
        self.angle = angle % 360
        self.setImage()
        
class PlayerCar(AbstractCar):
    IMG = pygame.image.load("assets\\unicorn-car-blue.png")
    
    def __init__(self, startPos, angle = 0):
        super().__init__(startPos, angle)
        self.crash_sound = pygame.mixer.Sound("assets\\crash.mp3")
        self.crash_sound.set_volume(0.3)
        
    def player_input(self):
        turned = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.accelerate()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.decelerate()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.velocity > 0:
                self.turn("left")
            else:
                self.turn("right")
            turned = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.velocity > 0:
                self.turn("right")
            else:
                self.turn("left")
            turned = True
            
        """
        if keys[pygame.K_RIGHT] == False and keys[pygame.K_d] == False:
            self.snapTurn()
        if keys[pygame.K_LEFT] == False and keys[pygame.K_a] == False:
            self.snapTurn()
        """
        
        if not turned:
            self.autoTurn()
        
        if keys[pygame.K_SPACE]:
            self.brake()
            
    def autoTurn(self):
        angleInterval = self.angle % 45
        buffer = 1
        
        if angleInterval > 45/2 and angleInterval < 45 - buffer:
            self.turn("right", 0.4)
        elif angleInterval <= 45/2 and angleInterval > buffer:
            self.turn("left", 0.4)
    
    def update(self):
        self.checkCollison()
        if self.stopped == False:
            self.player_input()
            self.move()
            
class BotCar(AbstractCar):
    IMG = pygame.image.load("assets\\unicorn-car-red.png")
    
    def __init__(self, startPos, angle = 0):
        super().__init__(startPos, angle)
        self.target = (self.rect.center, True)
        self.crash_sound = pygame.mixer.Sound("assets\\crash.mp3")
        self.crash_sound.set_volume(0.3)
        self.nextTargets = []
        self.targetBuffer = 30
        self.stopSigns = []
    
    #Move the bot towards the target
    def bot_move(self):
        x, y = self.rect.center
        targetX, targetY = self.target[0]
        dX, dY = targetX - x, targetY - y
        distance = math.sqrt(dX**2 + dY**2)
        targetAngle = math.degrees(math.atan2(dY, dX)) % 360
        dAngle = (targetAngle - self.angle) % 360
        
        # Change angle
        if distance > 20: # Buffer zone to prevent spinning near target       
            if dAngle > 2 and dAngle <= 180:
                self.turn("right")
            elif dAngle > 180 and dAngle < 358:
                self.turn("left")
                
        # Change speed
        if self.target[1]:
            targetSpeed = (0.015*distance)**1.6
        else:
            targetSpeed = float("inf")
        
        if distance > self.targetBuffer:
            angleBuffer = 30
            if dAngle <= 90 - angleBuffer or dAngle >= 270 + angleBuffer:
                speedBuffer = 2
                if self.velocity < targetSpeed - speedBuffer:
                    self.accelerate()
                elif self.velocity > targetSpeed + speedBuffer:
                    self.decelerate()
            else:
                self.decelerate()
        else:
            self.brake()
    
    def setTarget(self, target):
        self.target = target # Target should be in format ((x, y), True/False (Stop or Not)), eg ((50, 50), True) to stop at (50, 50)
        
    def addTargets(self, targets):
        for target in targets:
            self.nextTargets.append(target)
    
    # Returns True when near target and ready for next one
    def newTarget(self):
        x, y = self.rect.center
        targetX, targetY = self.target[0]
        dX, dY = targetX - x, targetY - y
        distance = math.sqrt(dX**2 + dY**2)
        
        return distance <= self.targetBuffer
    
    def queuedTargets(self):
        return len(self.nextTargets)

                
    def checkStopSign(self, stopSigns):
        for signCoords in self.stopSigns:
            sign_x, sign_y = signCoords
            distance = math.sqrt((self.rect.centerx - sign_x) ** 2 + (self.rect.centery - sign_y) ** 2)
            if distance < 50:
                self.velocity = 0
                break
            else:
                self.velocity = 3
    
    def update(self):
        self.checkCollison()
        if self.stopped == False:
            self.bot_move()
            self.checkStopSign(self.stopSigns) 
            self.move()
            if self.newTarget() and len(self.nextTargets) > 0:
                self.target = self.nextTargets.pop(0)
    
#May move this to another file later
class Pedestrian(pygame.sprite.Sprite):
    def __init__(self, startPos, startAngle = 0):
        super().__init__()
        self.angle = startAngle % 360
        self.collideGroups = []
        self.hit = False
        self.length = 50
        self.setImage()
        self.rect = self.image.get_rect(center=(startPos))
        self.target = (self.rect.center)
        self.speed = 0.03
        
    def setImage(self):
        #Added logic for walking animation
        frame_1 = pygame.image.load("assets\\Pedestrian1.png")
        ratio = frame_1.get_width() / frame_1.get_height()
        frame_1 = pygame.transform.smoothscale(frame_1, (self.length*ratio, self.length)).convert_alpha()
        frame_2 = pygame.image.load("assets\\Pedestrian2.png")
        ratio = frame_2.get_width() / frame_2.get_height()
        frame_2 = pygame.transform.smoothscale(frame_2, (self.length*ratio, self.length)).convert_alpha()
        pygame.transform.smoothscale(frame_2, (self.length*ratio, self.length)).convert_alpha()
        
        self.walk_frames = [frame_1,frame_2]
        self.walk_index = 0
        self.image = self.walk_frames[self.walk_index]
        self.image = pygame.transform.rotate(self.image, self.angle)
        

    def checkCollison(self):
        if self.collideGroups != []:
            for group in self.collideGroups:
                if len(pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_mask)) > 0 and not self.stopped:
                    self.hit = True
                    pygame.mixer.Sound.play(self.crash_sound)
                    self.image = pygame.image.load("assets\\explosion.png")
                    self.image = pygame.transform.smoothscale(self.image, (self.length, self.length)).convert_alpha()
                    
    def setCollide(self, group):
        self.collideGroups.append(group)
    
    def setTarget(self,target):
        self.target = target
        
    def walk(self):
        x, y = self.rect.center
        targetX, targetY = self.target
        delta_x = targetX - x
        delta_y = targetY - y
        self.buffer = 5
        if abs(delta_x) > self.buffer or abs(delta_y) > self.buffer:
            self.rect.move_ip(self.speed*delta_x, self.speed*delta_y)
            self.walk_index += 0.1
            if self.walk_index > len(self.walk_frames):
                self.walk_index = 0
            self.image = self.walk_frames[int(self.walk_index)]
            
    def update(self):
        if self.hit == False:
            self.walk()
            
              
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("AI Car demo")
    
    BotCars = pygame.sprite.Group()
    myCar = BotCar((100, 100))
    BotCars.add(myCar)
    
    player = pygame.sprite.GroupSingle()
    playerCar = PlayerCar((1000, 400))
    player.add(playerCar)
    
    Pedestrians = pygame.sprite.Group()
    guy = Pedestrian((500,200))
    Pedestrians.add(guy)
    
    playerCar.setCollide([BotCars,Pedestrians])
    myCar.setCollide([player,Pedestrians])
    guy.setCollide([BotCars,player])
    
    # List of targets to hit before following user mouse
    myCar.addTargets([((700, 200), False), ((600, 500), False), ((200, 200), False), ((600, 400), False)])
        
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        screen.fill((50, 200, 50))
        guy.setTarget(pygame.mouse.get_pos())
        if myCar.queuedTargets() == 0:
            myCar.setTarget((pygame.mouse.get_pos(), True)) # True to stop at mouse, False to continue
        BotCars.update()
        player.update()
        Pedestrians.update()
        BotCars.draw(screen)
        player.draw(screen)
        Pedestrians.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        pygame.display.flip()
    
    pygame.quit()