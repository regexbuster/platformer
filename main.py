import pygame
import utils
import collision_utils as cutils


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, shape, pixel_size):
        super(Player, self).__init__()
        self.velocity = pygame.math.Vector2(0, 0)

        self.shape = shape
        self.pixel_size = pixel_size

        self.width = len(shape[0]) * pixel_size
        self.height = len(shape) * pixel_size

        self.surface = pygame.Surface((self.width, self.height))

        self.rect = self.surface.get_rect(top=y, left=x)

        self.crouching = False

    def update(self, screen):
        self.move()
        self.draw(screen)

    def draw(self, screen: pygame.Surface):
        pixel_map, color_map = utils.pixels_to_rect_list(self.shape, self.pixel_size, 0, 0)

        for i in range(len(pixel_map)):
            pygame.draw.rect(self.surface, color_map[i], pixel_map[i])

        if player.crouching:
            player.rect.height = player.height / 2
            scaled_screen = pygame.transform.scale(player.surface, (player.width, (player.height / 2)))
            screen.blit(scaled_screen, (player.rect.x, player.rect.y))
        else:
            player.rect.height = player.height
            screen.blit(self.surface, player.rect)

    def move(self):
        """
        States:
            Moving L/R Grounded UnCrouched
            Moving L/R Midair UnCrouched
            Moving L/R Grounded Crouched
            Moving L/R Midair Crouched
            Jumping UnCrouched
            Jumping Crouched
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        pass


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

pixel_size = 10
player_shape = [
    ["T","T","T","T","T",],
    ["T","B","T","B","T",],
    ["T","T","T","T","T",],
    ["T","R","R","R","T",],
    ["T","T","T","T","T",],
]

player = Player(300, 100, player_shape, pixel_size)

factory = BoundaryFactory()

bounds_color = utils.colors["Red"]
factory.new_boundary(100, 400, 500, 50, bounds_color)
factory.new_boundary(550, 100, 50, 260, bounds_color)
factory.new_boundary(100,100, 50, 300, bounds_color)
factory.new_boundary(300, 200, 100, 50, bounds_color)

want_jump = 0
allowed_jumps = 1
jumps = 0

crouching = False

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

    # --- Game logic should go here

    onGround = False
    for floor in factory.get_contents():
        if not onGround:
            onGround = floor.colliderect(player.rect)
            #print(onGround)
            if onGround:
                val = cutils.is_colliding(floor, player, player.velocity)
                if val == 1:
                    jumps = 0

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_f]:
        quack_ticker += 1
        if quack_ticker % (fps/4) == 0:
            pygame.mixer.music.load("quack.mp3")
            pygame.mixer.music.play()
    else:
        quack_ticker = 0

    if pressed[pygame.K_a]:
        if crouching:
            player.velocity.x -= 0.025
        else:
            player.velocity.x -= 0.1
    if pressed[pygame.K_d]:
        if crouching:
            player.velocity.x += 0.025
        else:
            player.velocity.x += 0.1

    if not pressed[pygame.K_a] and not pressed[pygame.K_d] and onGround and not player.crouching:
        player.velocity.x *= 0.8
    else:
        player.velocity.x *= 0.99

    if not onGround:
        player.velocity.y += 0.1

    if jumps < allowed_jumps and pressed[pygame.K_SPACE] and not player.crouching:
        player.velocity.y -= 5
        jumps += 1
        want_jump = False

    player.rect = player.rect.move(player.velocity.x * (clock.get_time() / 10), player.velocity.y * (clock.get_time() / 10))

    # --- Screen-clearing code goes here
    screen.fill(utils.colors["White"])

    # --- Drawing code should go here

    player.update(screen)

    floors, colors = factory.get_all()

    for i in range(len(floors)):
        pygame.draw.rect(screen, colors[i], floors[i])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(fps)

pygame.quit()
