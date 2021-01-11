import pygame
import sys
import random
import neat

# main class


pygame.init()
screen = pygame.display.set_mode((288, 512))
# width and height of window
clock = pygame.time.Clock()
# you need to put this on the display surface when you have an image
pipe_list = []
pipe_height = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
# a constant used to trigger an event
pygame.time.set_timer(SPAWNPIPE, 1000)
# the interval of the event
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
# Game variables
gravity = 0.25
game_active = True
bird_amount = 0

bird_image1 = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_image2 = pygame.image.load('assets/bluebird-upflap.png').convert()
bird_image3 = pygame.image.load('assets/bluebird-downflap.png').convert()
bird_images = [bird_image1, bird_image2, bird_image3]
background_surface = pygame.image.load('assets/background-day.png').convert()
# background_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png')).convert()
# not changing the size because my screen is not big enough lol
# doubles the size of the surface and returns a new surface, needs to be stored
# .covert helps pygame to run more consistently
floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()


class Bird:
    bird_rect = bird_image1.get_rect(center=(50, 256))
    bird_image = bird_images

    def __init__(self):
        self.velocity_y = 0
        self.image_index = 0
        self.bird_surface = bird_images[self.image_index]
        self.rect = self.bird_rect
        self.rect.y = 256

    def move_bird(self):
        self.rect.centery += self.velocity_y

    def draw_bird(self):
        screen.blit(self.rotate_bird(), self.bird_rect)

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird_surface, self.velocity_y * -5, 1)
        return new_bird

    def collision_detection(self, pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                return False
            if self.bird_rect.top <= 10 or self.bird_rect.bottom >= 450:
                return False
        return True

    def animation(self):
        self.bird_surface = bird_images[self.image_index]


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def move_floor():
    global floor_x_pos
    floor_x_pos -= 1


def reset_floor_position():
    global floor_x_pos
    if floor_x_pos <= -288:
        floor_x_pos = 0


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(300, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(300, random_pipe_pos - 150))
    pipes = (bottom_pipe, top_pipe)
    return pipes
    # this creates an event that will be triggered every 1 second


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
        if pipe.centerx <= -50:
            pipes.remove(pipe)
    return pipes


first = True
bird1 = None

while True:
    # this is what a basic game loop could look like
    if first:
        bird1 = Bird()
        first = False

    for event in pygame.event.get():
        # this is the event loop
        # looks for all the event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    bird1 = Bird()
                    pipe_list.clear()
                    game_active = True
                else:
                    bird1.velocity_y = 0
                    bird1.velocity_y -= 6
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            bird1.image_index += 1
            if bird1.image_index > 2:
                bird1.image_index = 0
            bird1.animation()

    screen.blit(background_surface, (0, 0))
    # this is the method that allows you to put a surface(image) on the main surface(screen or frame)
    # (0,0) represents the top left of the surface where you image will start appearing
    if game_active:
        # pipe
        draw_pipe(pipe_list)
        pipe_list = move_pipe(pipe_list)

        # bird
        bird1.velocity_y += gravity
        bird1.move_bird()
        bird1.draw_bird()
        game_active = bird1.collision_detection(pipe_list)

    # floor
    move_floor()
    draw_floor()
    reset_floor_position()
    pygame.display.update()
    # update's the graphics, must be put at the end after all the graphics has been updated
    clock.tick(60)
