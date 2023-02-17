from .paddle import Paddle
from .ball import Ball
import pygame
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

        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1

        if ball.x_vel < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + Paddle.RADIUS:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.RADIUS:
                    ball.x_vel *= -1

                    middle_y = left_paddle.y + Paddle.RADIUS / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.RADIUS / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.left_hits += 1

        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + Paddle.RADIUS:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + Paddle.RADIUS / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.RADIUS / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    self.right_hits += 1
        # paddle_loc = list([self._paddle1_location, self._paddle2_location])[paddle_num-1]
        # paddle_vel = list([self._paddle1_velocity, self._paddle2_velocity])[paddle_num-1]
        # paddle 1 puck 2
        # if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5<puck_radius+paddle_radius):
        #     dist_off = 2*paddle_radius-(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5)
        #     vec = (paddle_loc[0]-self._puck_location[0], paddle_loc[1]-self._puck_location[1])
        #     mag_vec = ((vec[0]**2)+(vec[1]**2))**0.5
        #     if mag_vec!=0:
        #         scaled_vec = ((dist_off/mag_vec)*vec[0], (dist_off/mag_vec)*vec[1])
        #     else:
        #         scaled_vec=(0,0)
        #     d = ((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5
        #     nx = (self._puck_location[0]-paddle_loc[0])/d
        #     ny = (self._puck_location[1]-paddle_loc[1])/d
        #     p = 2*(paddle_vel[0]*nx+paddle_vel[1]*ny-self._puck_velocity[0]*nx-self._puck_velocity[1]*ny)/(mass_puck+mass_paddle)
        #     self._puck_velocity[0] += p*mass_puck*nx
        #     self._puck_velocity[1] += p*mass_puck*ny
        #     # update location after updating new direction so it doesn't end up just sticking to the paddle
        #     self._puck_location[0] -= scaled_vec[0]
        #     self._puck_location[1] -= scaled_vec[1]
        #     self._puck_location += self._puck_velocity
        # if(((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5<=puck_radius+paddle_radius):
        #     d = ((paddle_loc[0]-self._puck_location[0])**2+(paddle_loc[1]-self._puck_location[1])**2)**0.5
        #     nx = (self._puck_location[0]-paddle_loc[0])/d
        #     ny = (self._puck_location[1]-paddle_loc[1])/d
        #     p = 2*(paddle_vel[0]*nx+paddle_vel[1]*ny -self._puck_velocity[0]*nx-self._puck_velocity[1]*ny)/(mass_puck+mass_paddle)
        #     self._puck_velocity[0] += p*mass_puck*nx
        #     self._puck_velocity[1] += p*mass_puck*ny
    def draw(self, draw_score=True, draw_hits=False):
        self.window.fill(self.BLACK)

        self._draw_divider()

        if draw_score:
            self._draw_score()

        if draw_hits:
            self._draw_hits()

        for paddle in [self.left_paddle, self.right_paddle]:
            paddle.draw(self.window)

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
                if not up and self.left_paddle.y + Paddle.RADIUS + Paddle.VEL > self.window_height: # if paddle is moving up and it will go off the screen
                    valid = False
                down = not up
            if no_lateral:
                move_left=False
                move_right=False
            else:
                if move_left and self.left_paddle.x - Paddle.VEL - Paddle.RADIUS < 0: # if paddle is moving left and it will go off the screen
                    valid=False
                if not move_left and self.left_paddle.x + Paddle.RADIUS + Paddle.VEL > self.window_width/2: # if paddle is moving right and it will go off the screen
                    valid=False
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
                    up=False
                if not up and self.right_paddle.y + Paddle.RADIUS + Paddle.VEL > self.window_height: # if paddle is moving up and it will go off the screen
                    valid = False
                    up=True
                down = not up
            if no_lateral:
                move_left=False
                move_right=False
            else:
                if move_left and self.right_paddle.x - Paddle.VEL - Paddle.RADIUS < self.window_width/2: # if paddle is moving left and it will go off the screen
                    valid = False
                    move_left=False
                if not move_left and self.right_paddle.x + Paddle.RADIUS + Paddle.VEL > self.window_width: # if paddle is moving right and it will go off the screen
                    valid = False
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

        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1

        game_info = GameInformation(
            self.left_hits, self.right_hits, self.left_score, self.right_score)

        return game_info

    def reset(self):
        """Resets the entire game."""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
