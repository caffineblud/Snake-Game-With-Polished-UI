import random
import pygame
from settings import GRID_SIZE, FOOD_COLOR, WIDTH, HEIGHT

class Food:
    def __init__(self):
        self.position = self.randomize()

    def randomize(self):
        cols = WIDTH // GRID_SIZE
        rows = HEIGHT // GRID_SIZE
        return (
            random.randint(0, cols - 1),
            random.randint(0, rows - 1)
        )

    def draw(self, surface):
        x, y = self.position

        center = (
            x * GRID_SIZE + GRID_SIZE // 2,
            y * GRID_SIZE + GRID_SIZE // 2
        )

        pygame.draw.circle(surface, FOOD_COLOR, center, GRID_SIZE // 2 - 2)