import pygame
from network.nn import NeuralNetwork
from network.dense import Dense
from game.FlappyBird import FlappyBird
import numpy as np
from copy import deepcopy

class Trainer:
    def __init__(self, num_birds= 20, max_generation = 100):
        self.num_birds = num_birds
        self.max_gen = max_generation
        self.current_gen = 0
        self.best_score = 0
        self.game = FlappyBird(1280, 720, self.num_birds)

        self.networks = [self.new_network() for _ in range(num_birds)]

        

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode([1280, 720])
        clock = pygame.time.Clock() 
        running = True

        for i in range(self.max_gen):
            while running:
                delta_time = clock.tick(300.0)/1000.0

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
                self.game.render(screen)
                pygame.display.flip()
            
            best_id, best_score = self.selection()
            self.crossover(best_id)
            self.mutation()
            print(f"generation {i}:    best score: {best_score}")

            if not running:
                break;

            self.game.reset(self.num_birds)
        pygame.quit()

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
                x_dist / 500,
                y / 720,
                y1 / 720,
                y2 / 720,
                bird.y_velocity / max_vel
            ]])
            output = self.networks[i].predict(input)
            if output > 0.5:
                self.game.jump(i)
        
        return all_lost


    def selection(self):
        birds = self.game.get_birds()
        best_id =  max(range(self.num_birds), key=lambda x: birds[x].score)
        best_score = birds[best_id].score
        return best_id, best_score

    def crossover(self, best_id):
        best_network = self.networks[best_id]
        self.networks = [deepcopy(best_network) for _ in range(self.num_birds)]
        

    def mutation(self):
        for network in self.networks:
            network.mutate(amount=0.3, scale=0.1)

    def new_network(self):
        # x rury, y1 rury, y2 rury, y ptaka, y vel ptaka
        model = NeuralNetwork([
            Dense(size=(5, 5), activation='relu', init_method='He'),
            Dense((5, 1), activation='sigmoid', init_method='He')
        ])

        return model