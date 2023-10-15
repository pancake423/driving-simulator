import pygame
import math

class AbstractCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = self.IMG
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.START))
        
        self.maxSpeed = 20
        self.turnSpeed = 2
        self.velocity = 0
        self.acceleration = 2
        self.angle = 0 #Direction the car is facing
        
    def accelerate(self):
        self.velocity += self.acceleration
        self.velocity = min(self.maxSpeed, self.velocity)
    
    def decelerate(self):
        self.velocity -= self.acceleration
        
    def turn(self, dir):
        oldCenter = self.rect.center
        turnAmount = self.turnSpeed * self.velocity
        
        if dir.lower() == "left":
            self.angle -= turnAmount
            self.image = pygame.transform.rotate(self.image, -turnAmount)
        elif dir.lower() == "right":
            self.angle += self.turnSpeed * self.velocity
            self.image = pygame.transform.rotate(self.image, turnAmount)
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=oldCenter)
        
    def move(self):
        delta_x = self.velocity * math.cos(math.radians(self.angle))
        delta_y = self.velocity * math.sin(math.radians(self.angle))
        
        self.rect.move(delta_x, delta_y)
        
class PlayerCar(AbstractCar):
    def __init__(self):
        super().__init__()
        
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
            
    def update(self):
        player_input()
        self.move()
            
class BotCar(AbstractCar):
    IMG = pygame.image.load("assets\\unicorn-car-blue.svg")
    START = (100, 100)
    
    def __init__(self):
        self.IMG = pygame.transform.scale(self.IMG, (200, 200)).convert_alpha()
        super().__init__()
        self.target = (self.rect.center)
    
    #Move the bot towards the target
    def bot_move(self):
        x, y = self.rect.center
        targetX, targetY = self.target
        dX, dY = targetX - x, targetY - y
        distance = math.sqrt(dX**2 + dY**2)
        targetAngle = math.degrees(math.atan2(dY, dX)) % 360
        dAngle = targetAngle - self.angle
        
        # Change angle
        if distance < 5: # Buffer zone to prevent spinning near target       
            if dAngle < 180:
                self.turn("left")
            else:
                self.turn("right")
                
        # Change speed
        if distance > 3:
            if dAngle <= 90 or dAngle >= 270:
                self.accelerate()
            else:
                self.decelerate()
        
    def setTarget(self, target):
        self.target = target
        
    def newTarget(self):
        x, y = self.rect.center
        targetX, targetY = self.target
        dX, dY = targetX - x, targetY - y
        distance = math.sqrt(dX**2 + dY**2)
        
        return distance < 4
    
    def update(self):
        self.bot_move()
        self.move()
    
if __name__ == "__main__":
    screen = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption("AI Car demo")
    
    myGroup = pygame.sprite.Group()
    myCar = BotCar()
    myGroup.add(myCar)
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        screen.fill((50, 200, 50))
        myCar.setTarget(pygame.mouse.get_pos())
        myGroup.update()
        myGroup.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        pygame.display.flip()
    
    pygame.quit()