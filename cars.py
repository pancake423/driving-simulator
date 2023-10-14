import pygame
import math

class AbstractCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self)
        
        self.image = self.IMG
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.getrect(center=(self.START))
        
        self.maxSpeed = 20
        self.turnSpeed = 2
        self.velocity = 0
        self.acceleration = 2
        self.angle = 0 #Direction the car is facing
        
    def accelerate(self):
        self.velocity += self.acceleration
        self.velocity = min(maxSpeed, velocity)
    
    def decelerate(self):
        self.velocity -= self.acceleration
        
    def turn(self, dir):
        oldCenter = self.rect.center
        
        if dir.lower() == "left":
            self.angle -= self.turnSpeed
            self.image = pygame.transform.rotate(self.image, -self.turnSpeed)
        else dir.lower() == "right":
            self.angle += self.turnSpeed
            self.image = pygame.transform.rotate(self.image, -self.turnSpeed)
        
        self.rect = self.image.getrect(center=oldCenter)
        
    def move(self):
        delta_x = self.velocity * math.cos(self.angle)
        delta_y = self.velocity * math.sin(self.angle)
        
        self.x += delta_x
        self.y += delta_y
        
class PlayerCar(AbstractCar):
    def __init__(self):
        super().__init__(self)
        
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
    def __init__(self):
        super().__init__(self)
        self.target = (self.rect.center)
    
    #Move the bot towards the target
    def bot_move(self):
        
    
    def update(self):
        bot_move()
        self.move()
    
    