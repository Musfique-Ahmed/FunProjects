import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((500, 500))

# Set up clock
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 10
        self.dx = 5
        self.dy = 0

    def draw(self, screen):
        for element in self.elements:
            pygame.draw.circle(screen, white, element, self.radius)

    def move(self):
        # Move the snake by adding the current speed to the position
        for i in range(self.size - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]

        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy

# Food class
class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 10

    def draw(self, screen):
        pygame.draw.circle(screen, red, [self.x, self.y], self.radius)

    def random_location(self):
        self.x = random.randint(10, 490)
        self.y = random.randint(10, 490)

# Initialize objects
snake = Snake()
food = Food()
food.random_location()

# Game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Handle key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.dx = 0
        snake.dy = -5
    if keys[pygame.K_DOWN]:
        snake.dx = 0
        snake.dy = 5
    if keys[pygame.K_LEFT]:
        snake.dx = -5
        snake.dy = 0
    if keys[pygame.K_RIGHT]:
        snake.dx = 5
        snake.dy = 0

    # Clear screen
    screen.fill(black)

    # Draw snake and food
    snake.move()
    snake.draw(screen)
    food.draw(screen)

    # Check if snake is eating food
    if snake.elements[0][0] == food.x and snake.elements[0][1] == food.y:
        snake.size += 1
        snake.elements.append([0, 0])
        food.random_location()

    # Update screen
    pygame.display.update()
    clock.tick
