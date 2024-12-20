import pygame
import random
import csv

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Fonts
MESSAGE_FONT = pygame.font.SysFont("Arial", 25)
SCORE_FONT = pygame.font.SysFont("Arial", 20)

class SnakeGame:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.snake_size = 10
        self.snake_speed = 15
        self.game_display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.log_file = "snake_game_log.csv"
        self.ensure_log_file()

    def ensure_log_file(self):
        """Ensure the CSV log file exists and has a header."""
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Add header only if the file is empty
                writer.writerow(["Score"])

    def log_attempt(self, score):
        """Log the player's score to the CSV file."""
        with open(self.log_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([score])

    def print_score(self, score):
        """Display the current score on the screen."""
        value = SCORE_FONT.render(f"Score: {score}", True, ORANGE)
        self.game_display.blit(value, [10, 10])

    def draw_snake(self, snake_size, snake_pixels):
        """Draw the snake on the screen."""
        for pixel in snake_pixels:
            pygame.draw.rect(self.game_display, WHITE, [pixel[0], pixel[1], snake_size, snake_size])

    def message(self, text, color, x, y):
        """Display a message on the screen."""
        msg = MESSAGE_FONT.render(text, True, color)
        self.game_display.blit(msg, [x, y])

    def run_game(self):
        """Run the main game loop."""
        game_over = False
        game_close = False

        # Initial snake position and movement
        snake_x = self.width // 2
        snake_y = self.height // 2
        snake_dx = 0
        snake_dy = 0

        # Snake body
        snake_pixels = []
        snake_length = 1

        # Target (food) position
        target_x = round(random.randrange(0, self.width - self.snake_size) / 10.0) * 10.0
        target_y = round(random.randrange(0, self.height - self.snake_size) / 10.0) * 10.0

        while not game_over:

            while game_close:
                self.game_display.fill(BLACK)
                self.message("Game Over! Press Q to Quit or C to Play Again", RED, self.width // 6, self.height // 3)
                self.print_score(snake_length - 1)
                pygame.display.update()
                self.run_game()

                # for event in pygame.event.get():
                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_q:
                #             game_over = True
                #             game_close = False
                #         if event.key == pygame.K_c:
                #             self.log_attempt(snake_length - 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake_dy == 0:
                        snake_dx = 0
                        snake_dy = -self.snake_size
                    elif event.key == pygame.K_DOWN and snake_dy == 0:
                        snake_dx = 0
                        snake_dy = self.snake_size
                    elif event.key == pygame.K_LEFT and snake_dx == 0:
                        snake_dx = -self.snake_size
                        snake_dy = 0
                    elif event.key == pygame.K_RIGHT and snake_dx == 0:
                        snake_dx = self.snake_size
                        snake_dy = 0

            # Update snake position
            snake_x += snake_dx
            snake_y += snake_dy

            # Check for boundary collision
            if snake_x >= self.width or snake_x < 0 or snake_y >= self.height or snake_y < 0:
                game_close = True

            # Fill background
            self.game_display.fill(BLACK)

            # Draw target (food)
            pygame.draw.rect(self.game_display, RED, [target_x, target_y, self.snake_size, self.snake_size])

            # Update snake body
            snake_head = [snake_x, snake_y]
            snake_pixels.append(snake_head)

            if len(snake_pixels) > snake_length:
                del snake_pixels[0]

            # Check for collision with itself
            for pixel in snake_pixels[:-1]:
                if pixel == snake_head:
                    game_close = True

            self.draw_snake(self.snake_size, snake_pixels)
            self.print_score(snake_length - 1)

            pygame.display.update()

            # Check if the snake eats the target
            if snake_x == target_x and snake_y == target_y:
                target_x = round(random.randrange(0, self.width - self.snake_size) / 10.0) * 10.0
                target_y = round(random.randrange(0, self.height - self.snake_size) / 10.0) * 10.0
                snake_length += 1

            self.clock.tick(self.snake_speed)

        self.log_attempt(snake_length - 1)
        pygame.quit()
        quit()


if __name__ == '__main__':
    game = SnakeGame()
    game.run_game()
