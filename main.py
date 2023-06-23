import pygame
import utils
import item
import item_sprites

from player import Player
from animation import Animation


class BoundaryFactory:
    def __init__(self):
        self.contents = []
        self.colors = []

    def add_boundary(self, rect: pygame.Rect, color: pygame.Color) -> None:
        self.contents.append(rect)
        self.colors.append(color)

    def new_boundary(self, x: int, y: int, width: int, height: int, color: pygame.Color) -> None:
        self.contents.append(pygame.Rect(x, y, width, height))
        self.colors.append(color)

    def get_all(self):
        return self.contents, self.colors

    def get_contents(self):
        return self.contents

    def get_colors(self):
        return self.colors


class ItemFactory:
    def __init__(self):
        self.contents = []

    def add_item(self, item) -> None:
        self.contents.append(item)

    def new_item(self, shape, pixel_size, x, y) -> None:
        self.contents.append(item.Item(shape, pixel_size, x, y))

    def get_contents(self):
        return self.contents


pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Platformer")

done = False
clock = pygame.time.Clock()

pixel_size = 5

player = Player(300, 100, pixel_size)

b_factory = BoundaryFactory()
i_factory = ItemFactory()

bounds_color = utils.colors["Red"]
b_factory.new_boundary(100, 400, 600, 50, bounds_color)
b_factory.new_boundary(550, 100, 50, 260, bounds_color)
b_factory.new_boundary(100, 100, 50, 300, bounds_color)
b_factory.new_boundary(300, 250, 100, 50, bounds_color)

shotgun = item.Item(item_sprites.shotgun, pixel_size, 300, 10)

i_factory.add_item(shotgun)
i_factory.new_item(item_sprites.shotgun, pixel_size, 400, 10)

quack_ticker = 0
frame_ticker = 0

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
            if event.key == pygame.K_x:
                pygame.mixer.music.load("quack.mp3")
                pygame.mixer.music.play()
            if event.key == pygame.K_r:
                player.rect.x = 300
                player.rect.y = 100
            if event.key == pygame.K_f:
                if player.held_item is None:
                    player.grab_item(i_factory)
                else:
                    player.throw_item(i_factory)

    # --- Game logic should go here

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_x]:
        quack_ticker += 1
        if quack_ticker % (fps / 4) == 0:
            pygame.mixer.music.load("quack.mp3")
            pygame.mixer.music.play()
    else:
        quack_ticker = 0

    # --- Screen-clearing code goes here
    screen.fill(utils.colors["Quarter_Gray"])

    # --- Drawing code should go here

    items = i_factory.get_contents()

    for item in items:
        item.update(screen, b_factory, clock)

    player.update(screen, b_factory, clock)

    floors, colors = b_factory.get_all()

    for i in range(len(floors)):
        pygame.draw.rect(screen, colors[i], floors[i])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(fps)
    frame_ticker += 1

pygame.quit()
