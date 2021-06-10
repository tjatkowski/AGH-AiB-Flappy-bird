import pygame

from game.Bird import Bird
from game.Obstacles import Obstacles
class FlappyBird:
    def __init__(self, width, height, birds_num):
        self.width = width
        self.height = height
        self.birds = [Bird(height) for _ in range(birds_num)]
        self.obstacles = Obstacles(width, height)

    def reset(self, birds_num):
        self.birds = [Bird(self.height) for _ in range(birds_num)]
        self.obstacles = Obstacles(self.width, self.height)

    def jump(self, index):
        self.birds[index].jump(12.0)

    def update(self):
        for bird in self.birds:
            bird.apply_gravity(0.4)
        for bird in self.birds:
            bird.update()
        self.obstacles.update()

        for bird in self.birds:
            if self.obstacles.collides(bird):
                bird.lost = True
    
    def get_birds(self):
        return self.birds
    
    def get_obstacle(self):
        result = None
        for position in self.obstacles.positions:
            if position[0] >= Bird.X_POSITION:
                if result == None or position[0] < result[0]:
                    result = position
        return [
            [result[0], result[1] - Obstacles.HOLE_SIZE/2.0],
            [result[0], result[1] + Obstacles.HOLE_SIZE/2.0]
        ]


    def render(self, screen):
        for bird in self.birds:
            bird.render(screen)
        self.obstacles.render(screen)
        [a, b] = self.get_obstacle()
        pygame.draw.circle(screen, (80, 189, 80), a, 10)
        pygame.draw.circle(screen, (80, 189, 80), b, 10)