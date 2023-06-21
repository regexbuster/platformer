import pygame

import utils
from player import Player

class BoundaryFactory:
    def __init__(self):
        self.contents = []
        self.colors = []

    def add_boundary(self, rect: pygame.Rect, color: pygame.Color) -> None:
        self.contents.append(rect)
        self.colors.append(color)

    def new_boundary(self, x: int, y: int, width: int, height: int, color: pygame.Color) -> None:
        self.contents.append(pygame.Rect(x,y,width,height))
        self.colors.append(color)

    def get_all(self):
        return self.contents, self.colors

    def get_contents(self):
        return self.contents

    def get_colors(self):
        return self.colors


pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Platformer")

done = False
clock = pygame.time.Clock()

pixel_size = 5

player = Player(300, 100, pixel_size)

factory = BoundaryFactory()

bounds_color = utils.colors["Red"]
factory.new_boundary(100, 400, 600, 50, bounds_color)
factory.new_boundary(550, 100, 50, 260, bounds_color)
factory.new_boundary(100,100, 50, 300, bounds_color)
factory.new_boundary(300, 250, 100, 50, bounds_color)

quack_ticker = 0

fps = 60

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player.crouching = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                want_jump = pygame.time.get_ticks()
            if event.key == pygame.K_s:
                player.crouching = True
            if event.key == pygame.K_f:
                pygame.mixer.music.load("quack.mp3")
                pygame.mixer.music.play()
            if event.key == pygame.K_r:
                player.rect.x = 300
                player.rect.y = 100

    # --- Game logic should go here

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_f]:
        quack_ticker += 1
        if quack_ticker % (fps / 4) == 0:
            pygame.mixer.music.load("quack.mp3")
            pygame.mixer.music.play()
    else:
        quack_ticker = 0

    # --- Screen-clearing code goes here
    screen.fill(utils.colors["Quarter_Gray"])

    # --- Drawing code should go here

    player.update(screen, factory, clock)

    floors, colors = factory.get_all()

    for i in range(len(floors)):
        pygame.draw.rect(screen, colors[i], floors[i])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(fps)

pygame.quit()
