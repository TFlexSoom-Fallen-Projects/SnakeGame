"""
Tristan Hilbert
7/1/2020
SnakeGame Script
"""

import pygame
from pygame.locals import *
import random

class Snake:

    def __init__(self, width=10):
        self.body = []
        self.width = width
        self.speed = width

        self.grow(3)
    
    def set_speed(self, speed):
        self.speed = speed

    def set_location(self, x, y):
        for rect in self.body:
            rect.x, rect.y = x, y

    def move(self, direction):
        rect = self.body[-1]
        self.body.pop()
        
        rect.x = self.body[0].x
        rect.y = self.body[0].y

        if direction == 0: #up
            rect.y -= self.speed
        
        if direction == 1: #right
            rect.x += self.speed
        
        if direction == 2: #down
            rect.y += self.speed
        
        if direction == 3: #left
            rect.x -= self.speed
        

        self.body.insert(0, rect)
    
    def grow(self, count=2):
        for i in range(count):
            self.body.append(pygame.Rect(0, 0, self.width, self.width))
    
    def __repr__(self):
        res = "Snake: "
        for rect in self.body:
            res += str(rect.x) + " " + str(rect.y) + "|"
        
        return res

    def get_head(self):
        return self.body[0]
    
    def get_body(self):
        return self.body
    
    def get_length(self):
        return len(self.body)

"""
   ______                        ______          __   
  / ____/___ _____ ___  ___     / ____/___  ____/ /__ 
 / / __/ __ `/ __ `__ \/ _ \   / /   / __ \/ __  / _ \
/ /_/ / /_/ / / / / / /  __/  / /___/ /_/ / /_/ /  __/
\____/\__,_/_/ /_/ /_/\___/   \____/\____/\__,_/\___/ 
"""


# Globals
snake = Snake()
snake.set_location(100, 100)
apple = pygame.Rect(0, 0, 10, 10)
direction = 1


def randomly_place(rect, lim_x, lim_y):
    rect.x = random.randint(0, lim_x)
    rect.y = random.randint(0, lim_y)

# Function for rendering multiple rectangles
def render_colors(surface, color, rects):
    for rect in rects:
        surface.fill(color, rect)

# Funciton called every loop to move player
def movement_loop():
    global snake
    snake.move(direction)

def collision_loop():
    global snake, apple

    head = snake.get_head()

    if head.colliderect(apple):
        randomly_place(apple, 800, 600)
        snake.grow()
    
    if head.x < 0 or head.x > 800:
        return True
    
    if head.y < 0 or head.y > 600:
        return True
    
    counter = 1
    length = snake.get_length()
    while counter < length:
        if head.colliderect(snake.get_body()[counter]):\
            return True
        counter += 1
    
    return False

### Standard Code
# Create Screen
pygame.display.init()

# Set Dimensions of the display
# Get "Surface Object" to Draw on
screen = pygame.display.set_mode((800, 600))

# Pygame works based on these Surface Objects
# Rendered sprites are placed on Surface in rectangular areas

# define Colors
WHITE = pygame.Color(255, 255, 255, 255)
BLACK = pygame.Color(0, 0, 0, 255)
GREEN = pygame.Color(11, 102, 35)
RED   = pygame.Color(150, 0, 24)

# Clock for FPS
clock = pygame.time.Clock()
randomly_place(apple, 800, 600)

# Loop Forever! In Main
def main():
  global direction
  while True:
    # detect events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit(0)
    
    # Another Way to Get Keyboard Input
    # Pump Events (Prepare "key" structure)
    pygame.event.pump()
    key = pygame.key.get_pressed()

    # Defined by pygame.locals
    if key[K_UP]:
      direction = 0
    if key[K_RIGHT]:
      direction = 1
    if key[K_DOWN]:
      direction = 2
    if key[K_LEFT]:
      direction = 3

    # call movement function
    movement_loop()
    end = collision_loop()

    # Tick Clock (60 FPS)
    clock.tick(60)

    # Fill screen with black
    screen.fill(BLACK)
    render_colors(screen, GREEN, snake.get_body())
    screen.fill(RED, apple)
    pygame.display.flip()

    pygame.time.delay(int(1000 / (snake.get_length())))

    if end == True:
        break


if __name__ == "__main__":
    main()