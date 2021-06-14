import pygame
import random
import numpy as np

from game.Bird import Bird

class Obstacles:
    HOLE_SIZE = 200.0
    PIPE_WIDTH = 80.0

    OBSTALCES_VELOCITY = 3.0

    def __init__(self, width, height):
        self.height = height
        self.width = width

        step = (self.width + 2*Obstacles.PIPE_WIDTH)/3.0
        self.positions = [
            [700 + step, self.random_y()],
            [700 + 2*step, self.random_y()],
            [700 + 3*step, self.random_y()]
        ]

    def collides(self, bird: Bird):
        for position in self.positions:
            if position[0] <= Bird.X_POSITION + Bird.COLLIDER_SIZE[0]/2.0 + Obstacles.PIPE_WIDTH/2.0 and position[0] >= Bird.X_POSITION - Bird.COLLIDER_SIZE[0]/2.0 - Obstacles.PIPE_WIDTH/2.0:
                if bird.y_position + Bird.COLLIDER_SIZE[1]/2.0 >= position[1] + Obstacles.HOLE_SIZE/2.0 or bird.y_position - Bird.COLLIDER_SIZE[1]/2.0 <= position[1] - Obstacles.HOLE_SIZE/2.0:

                    return True, abs(bird.y_position - position[1])
        return False, 0

    def update(self):
        for position in self.positions:
            position[0] -= Obstacles.OBSTALCES_VELOCITY
            if position[0] <= -Obstacles.PIPE_WIDTH:
                position[0] = self.width + Obstacles.PIPE_WIDTH
                position[1] = self.random_y()
    

    def random_y(self):
        return random.randint(int(2*Obstacles.HOLE_SIZE/1.7), int(self.height - 2*Obstacles.HOLE_SIZE/1.7))
    
    def render(self, screen):
        for position in self.positions:
            pygame.draw.rect(screen, (240, 240, 240), ( position[0] - Obstacles.PIPE_WIDTH/2.0, 0.0, Obstacles.PIPE_WIDTH, position[1] - Obstacles.HOLE_SIZE/2.0 ), 0, 10)
            pygame.draw.rect(screen, (240, 240, 240), ( position[0] - Obstacles.PIPE_WIDTH/2.0, position[1] + Obstacles.HOLE_SIZE/2.0, Obstacles.PIPE_WIDTH, self.height - (position[1] + Obstacles.HOLE_SIZE/2.0) ), 0, 10)
