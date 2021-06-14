import random

import pygame
from network.nn import NeuralNetwork
from network.dense import Dense
from game.FlappyBird import FlappyBird
import numpy as np
from copy import deepcopy

class Trainer:
    def __init__(self, num_birds=100, max_generation=50, target_score=2000, scale_start=0.02):
        self.num_birds = num_birds
        self.max_gen = max_generation
        self.target_score = target_score
        self.current_gen = 0
        self.game = FlappyBird(1280, 720, self.num_birds)

        self.networks = [self.new_network() for _ in range(num_birds)]
        self.best_score = 0
        self.best_network = self.networks[0]
        self.best_last_network = self.networks[0]
        self.scale_start = scale_start
        self.scale_end = 0.01
        self.scale_decay = (self.scale_end - self.scale_start) / max_generation
        self.scale = self.scale_start

    def update_scale(self):
        self.scale = self.scale - (self.scale_start - self.scale_end) / self.max_gen
                     

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode([1280, 720])
        clock = pygame.time.Clock() 
        running = True
        print(self.best_network.layers[0].W)
        for i in range(self.max_gen):
            while running:
                # delta_time = clock.tick(500.0)/1000.0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game.jump(0)
                        if event.key == pygame.K_UP:
                            self.game.jump(1)
                        if event.key == pygame.K_m:
                            self.game.reset(10)

                game_over = self.decide()
                if game_over:
                    break
                self.game.update()

                screen.fill((37, 37, 48))
                #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
                # if i > self.max_gen - 5:
                self.game.render(screen)
                pygame.display.flip()
            
            best_id, best_score = self.selection()
            self.crossover()
            self.mutation()
            print(f"generation {i}:    best score now: {best_score}   best score overall {self.best_score}")

            if not running:
                break;

            self.game.reset(self.num_birds)
        print(self.best_network.layers[0].W)
        pygame.quit()
        print(self.best_network.layers[0].W)

    def decide(self):
        birds = self.game.get_birds()
        pipe = self.game.get_obstacle()

        max_vel = self.game.v_max()

        x_dist = pipe[0][0] - birds[0].X_POSITION
        y1, y2 = pipe[0][1], pipe[1][1]

        all_lost = True
        for i, bird in enumerate(birds):
            if bird.lost:
                continue
            all_lost = False
            y = bird.y_position
            input = np.array([[
                x_dist / 700,
                (y1 - y) / 400,
                (y2 - y) / 400,
                bird.y_velocity * 3 / max_vel
            ]])
            output = self.networks[i].predict(input)
            if output > 0.5:
                self.game.jump(i)
        return all_lost

    def selection(self):
        birds = self.game.get_birds()
        sorted_ids = sorted(range(self.num_birds), key=lambda x: -birds[x].score)
        best_id =  sorted_ids[0]
        self.best_last_network = self.networks[best_id]
        self.to_keep = [self.networks[sorted_ids[i]] for i in range(3)] # keep 3 best birds for the next gen
        self.to_cross = self.to_keep[:3] # two best will be crossed

        best_score = birds[best_id].score
        if best_score > self.best_score:
            self.best_score = best_score
            self.best_network = self.networks[best_id]
        return best_id, best_score

    def crossover(self):
        for i, net in enumerate(self.to_keep):
            self.networks[i] = net
        i += 1 
        self.networks[i] = self.best_network
        i += 1 
        p1, p2, p3 = self.to_cross
        crossed = p1.crossover(p2, method="mean")
        # self.networks[i:] = [deepcopy(p1).crossover(p2, p3, method="mean") for _ in range(self.num_birds - i)]
        self.networks[i:] = [net.crossover(crossed, method="random") for net in self.networks[i:]]

        if self.networks[0] is not self.to_keep[0] or self.networks[3] is not self.best_network:
            raise ValueError

    def mutation(self):
        self.update_scale()
        for network in self.networks[5:]:
            network.mutate(amount=0.25, scale=self.scale)


    def new_network(self):
        # x rury, y1 rury, y2 rury, y ptaka, y vel ptaka
        model = NeuralNetwork([
            Dense(size=(4, 5), activation='elu'),
            Dense(size=(5, 5), activation='elu'),
            Dense((5, 1), activation='sigmoid')
        ])

        return model
