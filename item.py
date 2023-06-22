import pygame
import utils
import collision_utils as cutils

class Item(pygame.sprite.Sprite):
    def __init__(self, shape, pixel_size, x, y):
        super(Item, self).__init__()
        # ignore now but need for throwing
        self.velocity = pygame.math.Vector2()

        self.shape = shape
        self.pixel_size = pixel_size

        self.width = len(self.shape[0]) * pixel_size
        self.height = len(self.shape) * pixel_size

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey([0,0,0])

        self.rect = self.surface.get_rect(top=y, left=x)

        self.onGround = False

    def update(self, screen, factory, clock):
        self.move(factory, clock)
        self.draw(screen)

    def move(self, factory, clock):
        self.onGround = False
        for floor in factory.get_contents():
            if not self.onGround:
                self.onGround = floor.colliderect(self.rect)
                val = cutils.is_colliding(floor, self, self.velocity)

        if not self.onGround:
            self.velocity.y += 0.2

        self.rect = self.rect.move(self.velocity.x * (clock.get_time() / 10), self.velocity.y * (clock.get_time() / 10))

    def draw(self, screen: pygame.Surface):
        pixel_map, color_map = utils.pixels_to_rect_list(self.shape, self.pixel_size, 0, 0)

        for i in range(len(pixel_map)):
            pygame.draw.rect(self.surface, color_map[i], pixel_map[i])

        screen.blit(self.surface, self.rect)