import pygame
import utils
import collision_utils as cutils
from player_sprites import player_default
from item import Item


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pixel_size):
        super(Player, self).__init__()
        self.velocity = pygame.math.Vector2(0, 0)

        self.shape = player_default
        self.pixel_size = pixel_size

        self.width = len(self.shape[0]) * pixel_size
        self.height = len(self.shape) * pixel_size

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey([0, 0, 0])

        self.rect = self.surface.get_rect(top=y, left=x)

        self.crouching = False
        self.crouching_first = False

        self.point_left = True

        self.want_jump = 0
        self.allowed_jumps = 1
        self.jumps = 0
        self.onGround = False

        self.held_item = None

    def update(self, screen, factory, clock):
        self.move(factory, clock)
        self.draw(screen)

    def draw(self, screen: pygame.Surface):
        pixel_map, color_map = utils.pixels_to_rect_list(self.shape, self.pixel_size, 0, 0)

        for i in range(len(pixel_map)):
            pygame.draw.rect(self.surface, color_map[i], pixel_map[i])

        if self.crouching:
            self.rect.height = self.height / 2
            if not self.crouching_first:
                self.crouching_first = True
                self.rect.y += self.height / 2
            scaled_screen = pygame.transform.scale(self.surface, (self.width, (self.height / 2)))
            if not self.point_left:
                scaled_screen = pygame.transform.flip(scaled_screen, True, False)
            screen.blit(scaled_screen, (self.rect.x, self.rect.y))
        else:
            if not self.crouching and self.crouching_first:
                self.crouching_first = False
                self.rect.y -= self.height / 2
            self.crouching_first = False
            self.rect.height = self.height
            if not self.point_left:
                screen.blit(pygame.transform.flip(self.surface, True, False), self.rect)
            else:
                screen.blit(self.surface, self.rect)

        if not self.held_item is None:
            self.held_item.rect.center = self.rect.center
            self.held_item.draw(screen, self.point_left)

    def move(self, factory, clock):
        """
        States:
            Moving L/R Grounded UnCrouched
            Moving L/R Midair UnCrouched
            Moving L/R Grounded Crouched
            Moving L/R Midair Crouched
            Jumping UnCrouched
            Jumping Crouched
        """
        self.onGround = False
        for floor in factory.get_contents():
            if not self.onGround:
                self.onGround = floor.colliderect(self.rect)
                if self.onGround:
                    val = cutils.is_colliding(floor, self, self.velocity)
                    if val == 1:
                        self.jumps = 0

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a]:
            self.point_left = True
            if self.crouching:
                pass
                # self.velocity.x -= 0.05
            else:
                self.velocity.x -= 0.1
        if pressed[pygame.K_d]:
            self.point_left = False
            if self.crouching:
                pass
                # self.velocity.x += 0.05
            else:
                self.velocity.x += 0.1

        if not pressed[pygame.K_a] and not pressed[pygame.K_d] and self.onGround and not self.crouching:
            self.velocity.x *= 0.8
        else:
            self.velocity.x *= 0.99

        if not self.onGround:
            if pressed[pygame.K_SPACE] and self.velocity.y > 0 and not self.crouching:
                self.velocity.y += 0.05
            else:
                self.velocity.y += 0.2

        if self.jumps < self.allowed_jumps and pressed[pygame.K_SPACE] and not self.crouching:
            self.velocity.y -= 7
            self.jumps += 1
            self.want_jump = False

        self.rect = self.rect.move(self.velocity.x * (clock.get_time() / 10), self.velocity.y * (clock.get_time() / 10))

    def grab_item(self, factory):
        contents = factory.get_contents()
        for i in range(len(contents)):
            if contents[i].rect.colliderect(self.rect):
                self.held_item = contents[i]
                contents.pop(i)
                break

    def throw_item(self, factory):
        factory.add_item(self.held_item)

        if self.point_left:
            self.held_item.velocity.x -= (abs(self.velocity.x) + 5)
        else:
            self.held_item.velocity.x += (abs(self.velocity.x) + 5)

        self.held_item = None
