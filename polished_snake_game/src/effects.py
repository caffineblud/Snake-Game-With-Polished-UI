import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 5)
        self.speed = random.uniform(0.5, 2)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, (40,40,60), (int(self.x), int(self.y)), self.radius)