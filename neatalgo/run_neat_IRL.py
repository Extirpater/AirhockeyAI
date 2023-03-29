# https://neat-python.readthedocs.io/en/latest/xor_example.html
from airhockey import Game
import pygame
import neat
import os
import time
import pickle
import serial.tools.list_ports


class AirhockeyGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def test_ai(self, net):
        """
        Test the AI against a human player by passing a NEAT neural network
        """
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(20)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            # net.activate creates the inputs to the MLP
            output = net.activate((self.right_paddle.x, self.right_paddle.y, self.right_paddle.x_vel, self.right_paddle.y_vel, self.ball.x, self.ball.y, self.ball.x_vel, self.ball.y_vel))
            decision = output.index(max(output))
            no_lateral = False
            no_vertical = False
            move_up = False
            move_left = False
            if decision == 0:  # Don't move
                no_vertical = True
            elif decision == 1:  # Move up
                move_up = True
            elif decision ==2:  # Move down
                move_up = False
            
            if decision == 3:  # Don't move
                no_lateral = True
            elif decision == 4:  # Move right
                move_left = False
            elif decision ==5:  # Move left
                move_left = True
            valid = self.game.move_paddle(left_paddle=False, up=move_up, move_left=move_left, no_lateral=no_lateral, no_vertical = no_vertical)


            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                # self.game.move_paddle(left=True, up=True)
                self.game.move_paddle(left=True, up=True, move_left=True, move_right=True)
            elif keys[pygame.K_s]:
                # self.game.move_paddle(left=True, up=False)
                self.game.move_paddle(left=True, up=True, move_left=True, move_right=True)

            self.game.draw(draw_score=True)
            # delay(1000)
            pygame.display.update()
def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Airhockey")
    airhockey = AirhockeyGame(win, width, height)
    airhockey.test_ai(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)

    config_path = os.path.join(local_dir, 'config_airhockey.txt')
    print(config_path)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    ports = list(serial.tools.list_ports.comports())
    serialInst = serial.Serial()
    print("Available ports:")
    for port in ports:
        print(str(port.device))
    serialInst.baudrate = 9600
    serialInst.port = input("Enter port: ")
    serialInst.open()
    print("Commands are 2 numbers of 1, 0, or -1. The first number is the vertical movement, the second is the horizontal movement. 00 is no movement, 11 is up and right, -1-1 is down and left, etc.")
    while True:
        command = input("Enter command: ")
        serialInst.write(command.encode('utf-8'))

        if command == "exit":
            break

    # test_best_network(config)
