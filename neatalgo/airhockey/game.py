from .paddle import Paddle
from .ball import Ball
import pygame
import time
import random
pygame.init()


class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class Game:
    """
    To use this class simply initialize and instance and call the .loop() method
    inside of a pygame event loop (i.e while loop). Inside of your event loop
    you can call the .draw() and .move_paddle() methods according to your use case.
    Use the information returned from .loop() to determine when to end the game by calling
    .reset().
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.left_paddle = Paddle(
            10, self.window_height // 2 - Paddle.RADIUS // 2)
        self.right_paddle = Paddle(
            self.window_width - 10 - Paddle.RADIUS, self.window_height // 2 - Paddle.RADIUS//2)
        self.ball = Ball(self.window_width // 2, self.window_height // 2)

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window
        self.start_time = time.time()
        self.game_time = 5

    def _draw_score(self):
        left_score_text = self.SCORE_FONT.render(
            f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(
            f"{self.right_score}", 1, self.WHITE)
        self.window.blit(left_score_text, (self.window_width //
                                           4 - left_score_text.get_width()//2, 20))
        self.window.blit(right_score_text, (self.window_width * (3/4) -
                                            right_score_text.get_width()//2, 20))

    def _draw_hits(self):
        hits_text = self.SCORE_FONT.render(
            f"{self.left_hits + self.right_hits}", 1, self.RED)
        self.window.blit(hits_text, (self.window_width //
                                     2 - hits_text.get_width()//2, 10))
    def _draw_goals(self):
        goal_height = self.window_height//10
        goal_width = 4
        # draw two goals on the left and right side of the screen centered on the midline
        pygame.draw.rect(self.window, self.WHITE, (0, self.window_height//2 - goal_height//2, goal_width, goal_height))
        pygame.draw.rect(self.window, self.WHITE, (self.window_width - goal_width, self.window_height//2 - goal_height//2, goal_width, goal_height))

    def _draw_divider(self):
        for i in range(10, self.window_height, self.window_height//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.window, self.WHITE, (self.window_width//2 - 5, i, 10, self.window_height//20))

    def _handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle
        ball.y_vel = ball.y_vel*0.999
        ball.x_vel = ball.x_vel*0.999
        # handle collision of ball with horizontal walls
        if ball.y + ball.RADIUS >= self.window_height:
            # print("hit bottom wall")
            ball.y_vel = - abs(ball.y_vel)
        elif ball.y - ball.RADIUS <= 0:
            # print("hit top wall")
            ball.y_vel = abs(ball.y_vel)
        
        # handle collision of ball with vertical walls
        if ball.x + ball.RADIUS >= self.window_width:
            # print("hit right wall")
            ball.x_vel *= -1
        elif ball.x - ball.RADIUS <= 0:
            # print("hit left wall")
            # self.right_score += 1
            ball.x_vel *= -1
        
        # if the ball hits the left paddle
        if ((left_paddle.x-ball.x)**2 + (left_paddle.y-ball.y)**2)**0.5<Paddle.RADIUS+Ball.RADIUS:
            # print("hit left paddle")
            self.left_hits +=1
            distance = 2*Paddle.RADIUS - (((left_paddle.x-ball.x)**2 + (left_paddle.y-ball.y)**2)**0.5)
            vec = (left_paddle.x-ball.x, left_paddle.y-ball.y)
            vec_magnitude = (vec[0]**2 + vec[1]**2)**0.5
            if vec_magnitude!=0:
                scaled_vec = ((distance/vec_magnitude)*vec[0], (distance/vec_magnitude)*vec[1])
            else:
                scaled_vec = (0,0)
            d =((left_paddle.x-ball.x)**2 + (left_paddle.y-ball.y)**2)**0.5
            nx = (ball.x-left_paddle.x)/d
            ny = (ball.y-left_paddle.y)/d
            p = 2*(left_paddle.x_vel*nx + left_paddle.y_vel*ny-ball.x_vel*nx-ball.y_vel*ny)/(1)
            ball.x_vel += p*nx
            ball.y_vel += p*ny
            ball.x -= 2*scaled_vec[0]
            ball.y -= 2*scaled_vec[1]
            # ball.x += ball.x_vel
            # ball.y += ball.y_vel
        if ((left_paddle.x-ball.x)**2 + (left_paddle.y-ball.y)**2)**0.5<=Paddle.RADIUS+Ball.RADIUS:
            # print("hit left paddle")
            d = ((left_paddle.x-ball.x)**2+(left_paddle.y-ball.y)**2)**0.5
            nx = (ball.x-left_paddle.x)/d
            ny = (ball.y-left_paddle.y)/d
            p = 2*(left_paddle.x_vel*nx+left_paddle.y_vel*ny-ball.x_vel*nx-ball.y_vel*ny)/(1)
            ball.x_vel += p*nx
            ball.y_vel += p*ny
        if ((right_paddle.x-ball.x)**2 + (right_paddle.y-ball.y)**2)**0.5<Paddle.RADIUS+Ball.RADIUS:
            # print("hit right paddle")
            self.right_hits +=1
            distance = 2*Paddle.RADIUS - (((right_paddle.x-ball.x)**2 + (right_paddle.y-ball.y)**2)**0.5)
            vec = (right_paddle.x-ball.x, right_paddle.y-ball.y)
            vec_magnitude = (vec[0]**2 + vec[1]**2)**0.5
            if vec_magnitude!=0:
                scaled_vec = ((distance/vec_magnitude)*vec[0], (distance/vec_magnitude)*vec[1])
            else:
                scaled_vec = (0,0)
            d =((right_paddle.x-ball.x)**2 + (right_paddle.y-ball.y)**2)**0.5
            nx = (ball.x-right_paddle.x)/d
            ny = (ball.y-right_paddle.y)/d
            p = 2*(right_paddle.x_vel*nx + right_paddle.y_vel*ny-ball.x_vel*nx-ball.y_vel*ny)/(1)
            ball.x_vel += p*nx
            ball.y_vel += p*ny
            ball.x -= 2*scaled_vec[0]
            ball.y -= 2*scaled_vec[1]
            # ball.x += ball.x_vel
            # ball.y += ball.y_vel
        if ((right_paddle.x-ball.x)**2 + (right_paddle.y-ball.y)**2)**0.5<=Paddle.RADIUS+Ball.RADIUS:
            # print("hit right paddle")
            d = ((right_paddle.x-ball.x)**2+(right_paddle.y-ball.y)**2)**0.5
            nx = (ball.x-right_paddle.x)/d
            ny = (ball.y-right_paddle.y)/d
            p = 2*(right_paddle.x_vel*nx+right_paddle.y_vel*ny-ball.x_vel*nx-ball.y_vel*ny)/(1)
            ball.x_vel += p*nx
            ball.y_vel += p*ny    
    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.BLACK)
        self._draw_goals()
        self._draw_divider()

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for left, paddle in enumerate([self.left_paddle, self.right_paddle]):
            paddle.draw(left, self.window)

        self.ball.draw(self.window)

    def move_paddle(self, left_paddle=True, up=True, move_left=True, no_lateral=False, no_vertical=False):
        """
        Move the left or right paddle.

        :returns: boolean indicating if paddle movement is valid. 
                  Movement is invalid if it causes paddle to go 
                  off the screen
        Location on the screen: (0,0) is at the top left corner

        have to add move_right, because you should be able to move up and down, but not left and right at the same time
        """
        move_right = not move_left
        down = not up
        valid = True
        if left_paddle:
            if no_vertical:
                up=False
                down=False
            else:
                if up and self.left_paddle.y - Paddle.VEL - Paddle.RADIUS < 0: # if paddle is moving up and it will go off the screen
                    valid = False
                    self.left_paddle.y_vel = 0
                    self.left_paddle.x_vel = 0
                if not up and self.left_paddle.y + Paddle.RADIUS + Paddle.VEL > self.window_height: # if paddle is moving up and it will go off the screen
                    valid = False
                    self.left_paddle.y_vel = 0
                    self.left_paddle.x_vel = 0
                down = not up
            if no_lateral:
                move_left=False
                move_right=False
            else:
                if move_left and self.left_paddle.x - Paddle.VEL - Paddle.RADIUS < 0: # if paddle is moving left and it will go off the screen
                    valid = False
                    self.left_paddle.y_vel = 0
                    self.left_paddle.x_vel = 0
                if not move_left and self.left_paddle.x + Paddle.RADIUS + Paddle.VEL > self.window_width/2: # if paddle is moving right and it will go off the screen
                    valid = False
                    self.left_paddle.y_vel = 0
                    self.left_paddle.x_vel = 0
                move_right = not move_left
            if valid:
                self.left_paddle.move(up, down, move_left, move_right)
        else:
            if no_vertical:
                up=False
                down=False
            else:
                if up and self.right_paddle.y - Paddle.VEL - Paddle.RADIUS < 0: # if paddle is moving up and it will go off the screen
                    valid = False
                    self.right_paddle.y_vel = 0
                    self.right_paddle.x_vel = 0
                    up=False
                if not up and self.right_paddle.y + Paddle.RADIUS + Paddle.VEL > self.window_height: # if paddle is moving up and it will go off the screen
                    valid = False
                    self.right_paddle.y_vel = 0
                    self.right_paddle.x_vel = 0
                    up=True
                down = not up
            if no_lateral:
                move_left=False
                move_right=False
            else:
                # invert decisions for the right paddle
                move_left = not move_left
                move_right = not move_right
                if move_left and self.right_paddle.x - Paddle.VEL - Paddle.RADIUS < self.window_width/2: # if paddle is moving left and it will go off the screen
                    valid = False
                    self.right_paddle.y_vel = 0
                    self.right_paddle.x_vel = 0
                    move_left=False
                if not move_left and self.right_paddle.x + Paddle.RADIUS + Paddle.VEL > self.window_width: # if paddle is moving right and it will go off the screen
                    valid = False
                    self.right_paddle.y_vel = 0
                    self.right_paddle.x_vel = 0
                    move_left=True
                move_right = not move_left
            if valid:
                self.right_paddle.move(up, down, move_left, move_right)

        return valid

    def loop(self):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """
        self.ball.move()
        self._handle_collision()

        if self.ball.x <= Paddle.RADIUS and self.ball.y >= self.window_height/2 - 50 and self.ball.y <= self.window_height/2 + 50:
            # print(self.ball.x, self.ball.y, self.window_height, self.window_width)
            self.ball.reset()
            self.right_score += 1
        if self.ball.x >= self.window_width-Paddle.RADIUS and self.ball.y >= self.window_height/2 - 50 and self.ball.y <= self.window_height/2 + 50:
            # print(self.ball.x, self.ball.y, self.window_height, self.window_width)
            self.ball.reset()
            self.left_score += 1
        # if time is up, reset the game
        if time.time() - self.start_time > self.game_time:
            self.ball.reset()
            self.left_score +=1
            self.right_score +=1

        game_info = GameInformation(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return game_info

    def reset(self):
        print("resent for some reason")
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
