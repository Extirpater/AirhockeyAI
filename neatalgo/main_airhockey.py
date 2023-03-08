# https://neat-python.readthedocs.io/en/latest/xor_example.html
from airhockey import Game
import pygame
import neat
import os
import time
import pickle


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

            if decision == 1:  # AI moves up
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:  # AI moves down
                self.game.move_paddle(left=False, up=False)

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

    def train_ai(self, genome1, genome2, config, draw=False):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """
        run = True
        start_time = time.time()

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        max_hits = 50

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            game_info = self.game.loop()

            self.move_ai_paddles(net1, net2)
            # time.sleep(0.01)
            if draw:
                self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            duration = time.time() - start_time
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.calculate_fitness(game_info, duration)
                # print("Game over")
                break

        return False

    def move_ai_paddles(self, net1, net2):
        """
        Determine where to move the left and the right paddle based on the two 
        neural networks that control them. 
        """
        players = [(self.genome1, net1, self.left_paddle, True), (self.genome2, net2, self.right_paddle, False)]
        for (genome, net, paddle, left) in players:
            output = net.activate(
                (paddle.y, paddle.x, self.ball.x, self.ball.y))
            # print(left, output)
            decision = output.index(max(output))
            # six outputs: don't move vert, up, down, don't move horiz, left, right
            no_lateral = False
            no_vertical = False
            move_up = False
            move_left = False
            if decision == 0:  # Don't move
                genome.fitness -= 0.01  # we want to discourage this
                no_vertical = True
            elif decision == 1:  # Move up
                move_up = True
            elif decision ==2:  # Move down
                move_up = False
            
            if decision == 3:  # Don't move
                genome.fitness -= 0.01  # we want to discourage this
                no_lateral = True
            elif decision == 4:  # Move right
                move_left = False
            elif decision ==5:  # Move left
                move_left = True
            valid = self.game.move_paddle(left_paddle=left, up=move_up, move_left=move_left, no_lateral=no_lateral, no_vertical = no_vertical)
            if not valid:  # If the movement makes the paddle go off the screen punish the AI
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration


def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Airhockey")

    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            airhockey = AirhockeyGame(win, width, height)

            force_quit = airhockey.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()


def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Airhockey")
    pong = AirhockeyGame(win, width, height)
    pong.test_ai(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)

    config_path = os.path.join(local_dir, 'config_airhockey.txt')
    print(config_path)

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
    test_best_network(config)
