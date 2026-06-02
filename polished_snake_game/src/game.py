import pygame
import json
import os

from snake import Snake
from food import Food
from ui import UIManager
from effects import Particle
from settings import *

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to scores.json
SCORE_FILE = os.path.join(BASE_DIR, "data", "scores.json")


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Neon Snake")

        self.clock = pygame.time.Clock()

        self.snake = Snake()
        self.food = Food()
        self.ui = UIManager()

        self.score = 0
        self.running = True
        self.game_over = False

        self.move_timer = 0
        self.move_delay = 110

        self.particles = [Particle(i * 40, i * 15) for i in range(50)]

        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            if not os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, "w") as file:
                    json.dump({"high_score": 0}, file)

            with open(SCORE_FILE, "r") as file:
                data = json.load(file)

            return data.get("high_score", 0)

        except Exception as e:
            print("Error loading high score:", e)
            return 0

    def save_high_score(self):
        try:
            with open(SCORE_FILE, "w") as file:
                json.dump({"high_score": self.high_score}, file)

        except Exception as e:
            print("Error saving high score:", e)

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (x, 0),
                (x, HEIGHT)
            )

        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, y),
                (WIDTH, y)
            )

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))

                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))

                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))

                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))

                elif event.key == pygame.K_r and self.game_over:
                    self.reset()

    def update(self):

        if self.game_over:
            return

        self.move_timer += self.clock.get_time()

        if self.move_timer >= self.move_delay:

            self.move_timer = 0

            self.snake.move()

            head_x, head_y = self.snake.body[0]

            # Wall collision
            if (
                head_x < 0
                or head_x >= WIDTH // GRID_SIZE
                or head_y < 0
                or head_y >= HEIGHT // GRID_SIZE
            ):
                self.game_over = True

            # Self collision
            if self.snake.collision_with_self():
                self.game_over = True

            # Food collision
            if self.snake.body[0] == self.food.position:

                self.snake.grow()

                self.food.position = self.food.randomize()

                self.score += 1

                if self.score > self.high_score:

                    self.high_score = self.score

                    self.save_high_score()

    def render(self):

        self.screen.fill(BG_COLOR)

        # Particle effects
        for particle in self.particles:

            particle.update()

            if particle.y > HEIGHT:
                particle.y = 0

            particle.draw(self.screen)

        self.draw_grid()

        self.food.draw(self.screen)

        self.snake.draw(self.screen)

        self.ui.draw_score(
            self.screen,
            self.score
        )

        high_score_text = pygame.font.SysFont(
            "arial",
            24
        ).render(
            f"High Score: {self.high_score}",
            True,
            (180, 180, 180)
        )

        self.screen.blit(
            high_score_text,
            (20, 55)
        )

        if self.game_over:
            self.ui.draw_game_over(
                self.screen,
                self.score
            )

        pygame.display.flip()

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.handle_events()

            self.update()

            self.render()

        pygame.quit()