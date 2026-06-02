import pygame
from settings import GRID_SIZE, SNAKE_COLOR, HEAD_COLOR

class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.grow_pending = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def change_direction(self, direction):
        dx, dy = self.direction
        ndx, ndy = direction

        if (dx + ndx, dy + ndy) != (0, 0):
            self.direction = direction

    def collision_with_self(self):
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(
                x * GRID_SIZE,
                y * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )

            color = HEAD_COLOR if i == 0 else SNAKE_COLOR

            pygame.draw.rect(surface, color, rect, border_radius=8)