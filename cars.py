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
        
