import pygame
import math

class AbstractCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.length = 50
        self.maxSpeed = 10
        self.turnSpeed = 0.5
        self.velocity = 0
        self.acceleration = 0.2
        self.angle = 0 #Direction the car is facing
        self.stopped = False
        
        self.setImage()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.START))
        
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
        self.velocity = max(-self.maxSpeed, self.velocity)
        
    def turn(self, dir):
        oldCenter = self.rect.center
        turnAmount = self.turnSpeed * abs(self.velocity)
        
        if dir.lower() == "left":
            self.angle -= turnAmount
        elif dir.lower() == "right":
            self.angle += turnAmount
        
        self.angle %= 360
        
        self.setImage()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=oldCenter)
        
    def move(self):
        delta_x = self.velocity * math.cos(math.radians(self.angle))
        delta_y = self.velocity * math.sin(math.radians(self.angle))
        
        self.rect.move_ip(delta_x, delta_y)
        
    def getRect(self):
        return self.rect
        
class PlayerCar(AbstractCar):
    IMG = pygame.image.load("assets\\unicorn-car-blue.png")
    START = (1000,400)
    
    def __init__(self):
        super().__init__()
        self.crash_sound = pygame.mixer.Sound("assets\\crash.mp3")
        self.crash_sound.set_volume(0.3)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.accelerate()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.decelerate()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.turn("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turn("right")
            
    def checkCollison(self):
        if len(pygame.sprite.spritecollide(self,BotCars,False,pygame.sprite.collide_mask)) > 0:
            self.stop()
            pygame.mixer.Sound.play(self.crash_sound)
            self.image = pygame.image.load("assets\\explosion.png")
            self.image = pygame.transform.smoothscale(self.image, (50, 50)).convert_alpha()
            
    def update(self):
        self.checkCollison()
        if self.stopped == False:
            self.player_input()
            self.move()
            
class BotCar(AbstractCar):
    IMG = pygame.image.load("assets\\unicorn-car-red.png")
    START = (100, 100)
    
    def __init__(self):
        super().__init__()
        self.target = (self.rect.center)
        self.crash_sound = pygame.mixer.Sound("assets\\crash.mp3")
        self.crash_sound.set_volume(0.3)
    
    #Move the bot towards the target
    def bot_move(self):
        x, y = self.rect.center
        targetX, targetY = self.target
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
        if distance > 20:
            if dAngle <= 90 or dAngle >= 270:
                self.accelerate()
            else:
                self.decelerate()
    
    def setTarget(self, target):
        self.target = target
        
    # Returns True when near target and ready for next one
    def newTarget(self):
        x, y = self.rect.center
        targetX, targetY = self.target
        dX, dY = targetX - x, targetY - y
        distance = math.sqrt(dX**2 + dY**2)
        
        return distance <= 20
    
    def checkCollison(self):
        if len(pygame.sprite.spritecollide(self,player,False,pygame.sprite.collide_mask)) > 0:
            self.stop()
            pygame.mixer.Sound.play(self.crash_sound)
            self.image = pygame.image.load("assets\\explosion.png")
            self.image = pygame.transform.smoothscale(self.image, (50, 50)).convert_alpha()
    
    def update(self):
        self.checkCollison()
        if self.stopped == False:
            self.bot_move()
            self.move()
    
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("AI Car demo")
    
    BotCars = pygame.sprite.Group()
    myCar = BotCar()
    BotCars.add(myCar)
    
    player = pygame.sprite.GroupSingle()
    playerCar = PlayerCar()
    player.add(playerCar)
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        screen.fill((50, 200, 50))
        myCar.setTarget(pygame.mouse.get_pos())
        BotCars.update()
        player.update()
        BotCars.draw(screen)
        player.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        pygame.display.flip()
    
    pygame.quit()