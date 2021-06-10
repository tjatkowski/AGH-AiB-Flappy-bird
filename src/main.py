import pygame
from game.FlappyBird import FlappyBird;

pygame.init()

screen = pygame.display.set_mode([1280, 720])

running = True

flappy_bird = FlappyBird(1280, 720, 10);

clock = pygame.time.Clock()         
while running:
    delta_time = clock.tick(60.0)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flappy_bird.jump(0)
            if event.key == pygame.K_UP:
                flappy_bird.jump(1)
            if event.key == pygame.K_m:
                flappy_bird.reset(10)

    flappy_bird.update()

    screen.fill((37, 37, 48))

    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    flappy_bird.render(screen)

    pygame.display.flip()


pygame.quit()