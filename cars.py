import pygame
import math

class AbstractCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.length = 200
        self.maxSpeed = 10
        self.turnSpeed = 0.5
        self.velocity = 0
        self.acceleration = 0.2
        self.angle = 0 #Direction the car is facing
        
        self.setImage()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.START))
        
    def setImage(self):
        ratio = self.IMG.get_width() / self.IMG.get_height()
        self.image = pygame.transform.smoothscale(self.IMG, (self.length*ratio, self.length)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 270 - self.angle)
        
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
        self.player_input()
        self.move()
            
class BotCar(AbstractCar):
    IMG = pygame.image.load("assets\\unicorn-car-red.svg")
    START = (100, 100)
    
    def __init__(self):
        super().__init__()
        self.target = (self.rect.center)
    
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
        pygame.draw.rect(screen, "purple", myCar.getRect())
        myGroup.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        pygame.display.flip()
    
    pygame.quit()