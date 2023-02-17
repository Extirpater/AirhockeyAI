import pygame


class Paddle:
    VEL = 4
    RADIUS = 20

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        # pygame.draw.rect(
        #     win, (255, 255, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))
        pygame.draw.circle(win, (255,255,255), (int(self.x),int(self.y)), self.RADIUS)


    def move(self, up=True, down=False, left=True, right=False):
        # right= True
        # left = False
        # the paddle game is always moving left
        if up:
            self.y -= self.VEL
        if down:
            self.y += self.VEL
        if left:
            self.x -= self.VEL
        if right:
            self.x += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
