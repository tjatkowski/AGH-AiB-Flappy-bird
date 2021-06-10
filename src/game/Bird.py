import pygame

class Bird:
    COLLIDER_SIZE = (40, 40)
    X_POSITION = 230.0

    def __init__(self, height):
        self.y_position = 200.0
        self.y_velocity = 0.0
        self.height = height
        self.lost = False

        self.score = 0
    

    def apply_gravity(self, grav_acc):
        self.y_velocity += grav_acc
    
    def update(self):
        if self.lost:
            self.y_position = -self.height
            return

        self.score += 1
        self.y_position += self.y_velocity
        if self.y_position >= self.height:
            self.lost = True
        if self.y_position <= 0.0:
            self.y_velocity = 0.0
            self.y_position = 0.0
    
    def jump(self, jump_velocity):
        self.y_velocity = -jump_velocity
    
    def render(self, screen):
        pygame.draw.rect(screen, (189, 80, 80), (Bird.X_POSITION - Bird.COLLIDER_SIZE[0]/2.0, self.y_position - Bird.COLLIDER_SIZE[1]/2.0, Bird.COLLIDER_SIZE[0], Bird.COLLIDER_SIZE[1]), 0, 10)