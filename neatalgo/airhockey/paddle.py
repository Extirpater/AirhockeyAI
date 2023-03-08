import pygame


class Paddle:
    VEL = 4
    RADIUS = 20

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, left, win): # left is a binary 0 or one to determine which side of the screen the paddle is on
        # left is 0, right is 1
        # pygame.draw.rect(
        #     win, (255, 255, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))
        if left:
            pygame.draw.circle(win, (255,0,0), (int(self.x),int(self.y)), self.RADIUS)
        else:
            pygame.draw.circle(win, (0,0,255), (int(self.x),int(self.y)), self.RADIUS)


    def move(self, up=True, down=False, left=True, right=False):
        # right= True
        # left = False
        # the paddle game is always moving left
        y_prev = self.y
        x_prev = self.x
        if up:
            self.y -= self.VEL
        elif down:
            self.y += self.VEL
        if left:
            self.x -= self.VEL
        elif right:
            self.x += self.VEL
        self.y_vel = self.y - y_prev
        # print(self.y_vel, self.y, y_prev)
        self.x_vel = self.x - x_prev
    def reset(self):
        print("Resetting in paddle")
        self.x = self.original_x
        self.y = self.original_y
