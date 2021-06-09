import os
from random import randint
from collections import deque

import pygame
from pygame.locals import *


FPS = 60
ANIMATION_SPEED = 0.18  # pixels per millisecond
WIN_WIDTH = 284 * 2     # BG image size: 284x512 px; tiled twice
WIN_HEIGHT = 512


class Bird(pygame.sprite.Sprite):


    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.18
    CLIMB_SPEED = 0.3
    CLIMB_DURATION = 333.3

    def __init__(self, x, y, msec_to_climb, images,speed):
        self.SINK_SPEED *= speed
        self.CLIMB_SPEED *= speed
        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)
        self.IS_ALIVE = True
        self.speed = speed

    
    def update(self, delta_frames=1):
        
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb/Bird.CLIMB_DURATION
            self.y -= (Bird.CLIMB_SPEED * frames_to_msec(delta_frames)) 
            self.msec_to_climb -= frames_to_msec(delta_frames)
        else:
            self.y += Bird.SINK_SPEED * frames_to_msec(delta_frames) 

    @property
    def jump(self):
        self.msec_to_climb = Bird.CLIMB_DURATION

    @property
    def image(self):
        
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_wingup
        else:
            return self._img_wingdown

    @property
    def mask(self):
        
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mask_wingup
        else:
            return self._mask_wingdown

    @property
    def rect(self):
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)

    @property
    def change_state(self):
        self.IS_ALIVE = False

    @property
    def check_state(self):
        return self.IS_ALIVE

    @property
    def get_bird_info(self): 
        if self.msec_to_climb > 0:
            s = -(Bird.CLIMB_SPEED * frames_to_msec(1))
        else:
            s = Bird.SINK_SPEED * frames_to_msec(1) 
        return({self.x,self.y,s})

class PipePair(pygame.sprite.Sprite):
    

    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000

    def __init__(self, pipe_end_img, pipe_body_img,number_of_birds,speed):
        self.speed = speed
        self.ADD_INTERVAL = self.ADD_INTERVAL//speed
        self.x = float(WIN_WIDTH - 1)
        self.score_counted = []
        for i in range(number_of_birds):
            self.score_counted.append(0)

        self.image = pygame.Surface((PipePair.WIDTH, WIN_HEIGHT), SRCALPHA)
        self.image.convert()   # speeds up blitting
        self.image.fill((0, 0, 0, 0))
        total_pipe_body_pieces = int(
            (WIN_HEIGHT -                  # fill window from top to bottom
             3 * Bird.HEIGHT -             # make room for bird to fit through
             3 * PipePair.PIECE_HEIGHT) /  # 2 end pieces + 1 body piece
            PipePair.PIECE_HEIGHT          # to get number of pipe pieces
        )
        self.bottom_pieces = randint(1, total_pipe_body_pieces)
        self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

        # bottom pipe
        for i in range(1, self.bottom_pieces + 1):
            piece_pos = (0, WIN_HEIGHT - i*PipePair.PIECE_HEIGHT)
            self.image.blit(pipe_body_img, piece_pos)
        bottom_pipe_end_y = WIN_HEIGHT - self.bottom_height_px
        bottom_end_piece_pos = (0, bottom_pipe_end_y - PipePair.PIECE_HEIGHT)
        self.image.blit(pipe_end_img, bottom_end_piece_pos)

        # top pipe
        for i in range(self.top_pieces):
            self.image.blit(pipe_body_img, (0, i * PipePair.PIECE_HEIGHT))
        top_pipe_end_y = self.top_height_px
        self.image.blit(pipe_end_img, (0, top_pipe_end_y))

        # compensate for added end pieces
        self.top_pieces += 1
        self.bottom_pieces += 1

        # for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    @property
    def top_height_px(self):
        return self.top_pieces * PipePair.PIECE_HEIGHT

    @property
    def bottom_height_px(self):
        return self.bottom_pieces * PipePair.PIECE_HEIGHT

    @property
    def visible(self):
        return -PipePair.WIDTH < self.x < WIN_WIDTH

    @property
    def rect(self):
        return Rect(self.x, 0, PipePair.WIDTH, PipePair.PIECE_HEIGHT)
    
    @property
    def pipe_info(self):
        return({self.x,})

    def update(self, delta_frames=1):
        self.x -= ANIMATION_SPEED*self.speed * frames_to_msec(delta_frames)

    def collides_with(self, bird):
        return pygame.sprite.collide_mask(self, bird)


def load_images():
    

    def load_image(img_file_name):
        
        file_name = os.path.join(os.path.dirname(__file__),
                                 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'background': load_image('background.png'),
            'pipe-end': load_image('pipe_end.png'),
            'pipe-body': load_image('pipe_body.png'),
            # images for animating the flapping bird -- animated GIFs are
            # not supported in pygame
            'bird-wingup': load_image('bird_wing_up.png'),
            'bird-wingdown': load_image('bird_wing_down.png')}


def frames_to_msec(frames, fps=FPS):
    
    return 1000.0 * frames / fps


def msec_to_frames(milliseconds, fps=FPS):
    
    return fps * milliseconds / 1000.0


def run_simulation(number_of_birds,speed):
    
    
    pygame.init()
    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pygame Flappy Bird')

    clock = pygame.time.Clock()
    images = load_images()

    birds = []
    birds_scorre = []
    for bird in range(number_of_birds):
        birds.append(Bird(50, int(WIN_HEIGHT/2 - Bird.HEIGHT/2), 2,
                (images['bird-wingup'], images['bird-wingdown']),speed))
    
    for bird in range(number_of_birds):
        birds_scorre.append(0) 

    pipes = deque()

    frame_clock = 0
    score = 0
    done = paused = False
    while not done:
        clock.tick(FPS)

        # Handle this 'manually'.  If we used pygame.time.set_timer(),
        # pipe addition would be messed up when paused.
        if not (paused or frame_clock % (msec_to_frames(PipePair.ADD_INTERVAL)/speed)):
            pp = PipePair(images['pipe-end'], images['pipe-body'],number_of_birds,speed)
            pipes.append(pp)

        

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key in (K_PAUSE, K_p):
                paused = not paused
            elif e.type == MOUSEBUTTONUP or (e.type == KEYUP and
                    e.key in (K_UP, K_RETURN, K_SPACE)):
                for bird in range(3):
                    birds[bird].jump

        if paused:
            continue  # don't draw anything

        for bird in birds:
            print(bird.get_bird_info)
        # check for collisions
        for bird in birds:
            if bird.check_state == True:
                pipe_collision = any(p.collides_with(bird) for p in pipes)
                if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
                    bird.change_state
        sum = 0
        for bird in birds:
            if bird.check_state == False:
                sum += 1
        if sum == number_of_birds:
            done = True
        for x in (0, WIN_WIDTH / 2):
            display_surface.blit(images['background'], (x, 0))

        while pipes and not pipes[0].visible:
            pipes.popleft()

        for p in pipes:
            p.update()
            display_surface.blit(p.image, p.rect)

        for bird in birds:
            if bird.check_state == True:
                bird.update()
                display_surface.blit(bird.image, bird.rect)

        for bird in range(len(birds)):
            for p in pipes:
                if p.x + PipePair.WIDTH < birds[bird].x and p.score_counted[bird] == 0 and birds[bird].check_state == True:
                    birds_scorre[bird] += 1
                    print("adding 1 to score")
                    p.score_counted[bird] = 1


        pygame.display.flip()
        frame_clock += 1
    pygame.quit()
    return birds_scorre


if __name__ == '__main__':
    results = run_simulation(5,1)
    print(results)
