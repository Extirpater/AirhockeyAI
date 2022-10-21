# Create an airhockey game with pygame

import pygame
import sys
import random
import time
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define some constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
BALL_RADIUS = 10
BALL_SPEED = 5

# Initialize pygame
pygame.init()

# Set the width and height of the screen [width, height]
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Air Hockey")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the paddles
paddle1 = pygame.Rect(0, HEIGHT/2 - PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - PADDLE_WIDTH, HEIGHT/2 - PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize the ball
ball = pygame.Rect(WIDTH/2 - BALL_RADIUS/2, HEIGHT/2 - BALL_RADIUS/2, BALL_RADIUS, BALL_RADIUS)

# Initialize the ball speed
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    pos = pygame.mouse.get_pos()

    # Set the left paddle to the mouse position
    paddle1.y = pos[1]

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce the ball if needed
    if ball.y > HEIGHT - BALL_RADIUS or ball.y < 0:
        ball_speed_y *= -1
    if ball.x > WIDTH - BALL_RADIUS or ball.x < 0:
        ball_speed_x *= -1

    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # Draw the paddles
    pygame.draw.rect(screen, BLACK, paddle1)
    pygame.draw.rect(screen, BLACK, paddle2)

    # Draw the ball
    pygame.draw.rect(screen, BLACK, ball)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()