import numpy as np
import pygame
import random
from collections import deque

class SnakeGameAI:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.snake_size = 10
        self.snake_speed = 15
        self.reset()

    def reset(self):
        """Reset the game to its initial state."""
        self.snake_x = self.width // 2
        self.snake_y = self.height // 2
        self.snake_dx = 0
        self.snake_dy = 0
        self.snake_body = [[self.snake_x, self.snake_y]]
        self.snake_length = 1
        self.food_x = random.randint(0, (self.width - self.snake_size) // 10) * 10
        self.food_y = random.randint(0, (self.height - self.snake_size) // 10) * 10
        self.game_over = False
        self.score = 0
        return self.get_state()

    def get_state(self):
        """Return the current state as a numpy array."""
        state = [
            # Snake's relative position to the food
            (self.snake_x - self.food_x) / self.width,
            (self.snake_y - self.food_y) / self.height,
            # Snake's direction
            self.snake_dx / self.snake_size,
            self.snake_dy / self.snake_size,
            # Obstacles (walls or self-collision danger)
            int(self.snake_x <= 0),  # Left wall
            int(self.snake_x >= self.width - self.snake_size),  # Right wall
            int(self.snake_y <= 0),  # Top wall
            int(self.snake_y >= self.height - self.snake_size),  # Bottom wall
        ]
        return np.array(state, dtype=np.float32)

    def step(self, action):
        """Take a step in the environment based on the agent's action."""
        # Define actions: [UP, DOWN, LEFT, RIGHT]
        if action == 0:  # UP
            if self.snake_dy == 0:
                self.snake_dx, self.snake_dy = 0, -self.snake_size
        elif action == 1:  # DOWN
            if self.snake_dy == 0:
                self.snake_dx, self.snake_dy = 0, self.snake_size
        elif action == 2:  # LEFT
            if self.snake_dx == 0:
                self.snake_dx, self.snake_dy = -self.snake_size, 0
        elif action == 3:  # RIGHT
            if self.snake_dx == 0:
                self.snake_dx, self.snake_dy = self.snake_size, 0

        # Update snake position
        self.snake_x += self.snake_dx
        self.snake_y += self.snake_dy

        # Check for collisions
        if (
            self.snake_x < 0 or self.snake_x >= self.width or
            self.snake_y < 0 or self.snake_y >= self.height or
            [self.snake_x, self.snake_y] in self.snake_body[:-1]
        ):
            self.game_over = True
            return self.get_state(), -10, True  # Game over reward

        # Update snake's body
        self.snake_body.append([self.snake_x, self.snake_y])
        if len(self.snake_body) > self.snake_length:
            self.snake_body.pop(0)

        # Check if food is eaten
        reward = 0
        if self.snake_x == self.food_x and self.snake_y == self.food_y:
            self.snake_length += 1
            self.score += 1
            reward = 10
            self.food_x = random.randint(0, (self.width - self.snake_size) // 10) * 10
            self.food_y = random.randint(0, (self.height - self.snake_size) // 10) * 10

        return self.get_state(), reward, False

    def render(self):
        """Render the game (optional, for visualization)."""
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game AI")
        display.fill((0, 0, 0))
        for segment in self.snake_body:
            pygame.draw.rect(display, (255, 255, 255), [segment[0], segment[1], self.snake_size, self.snake_size])
        pygame.draw.rect(display, (255, 0, 0), [self.food_x, self.food_y, self.snake_size, self.snake_size])
        pygame.display.update()

    def close(self):
        pygame.quit()
