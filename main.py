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
        self.surface.set_colorkey([0,0,0])

        self.rect = self.surface.get_rect(top=y, left=x)

        self.crouching = False
        self.crouching_first = False

        self.point_left = True

        self.want_jump = 0
        self.allowed_jumps = 1
        self.jumps = 0
        self.onGround = False

    def update(self, screen, factory):
        self.move(factory)
        self.draw(screen)

    def draw(self, screen: pygame.Surface):
        pixel_map, color_map = utils.pixels_to_rect_list(self.shape, self.pixel_size, 0, 0)

        for i in range(len(pixel_map)):
            pygame.draw.rect(self.surface, color_map[i], pixel_map[i])

        if player.crouching:
            player.rect.height = player.height / 2
            if not player.crouching_first:
                player.crouching_first = True
                player.rect.y += player.height / 2
            scaled_screen = pygame.transform.scale(player.surface, (player.width, (player.height / 2)))
            if not player.point_left:
                scaled_screen = pygame.transform.flip(scaled_screen, True, False)
            screen.blit(scaled_screen, (player.rect.x, player.rect.y))
        else:
            if not player.crouching and player.crouching_first:
                player.crouching_first = False
                player.rect.y -= player.height / 2
            player.crouching_first = False
            player.rect.height = player.height
            if not player.point_left:
                screen.blit(pygame.transform.flip(self.surface, True, False), player.rect)
            else:
                screen.blit(self.surface, player.rect)

    def move(self, factory):
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
                self.velocity.x -= 0.05
            else:
                self.velocity.x -= 0.1
        if pressed[pygame.K_d]:
            self.point_left = False
            if self.crouching:
                self.velocity.x += 0.05
            else:
                self.velocity.x += 0.1

        if not pressed[pygame.K_a] and not pressed[pygame.K_d] and self.onGround and not self.crouching:
            self.velocity.x *= 0.8
        else:
            self.velocity.x *= 0.99

        if not self.onGround:
            self.velocity.y += 0.1

        if self.jumps < self.allowed_jumps and pressed[pygame.K_SPACE] and not self.crouching:
            self.velocity.y -= 5
            self.jumps += 1
            self.want_jump = False

        self.rect = self.rect.move(self.velocity.x * (clock.get_time() / 10), self.velocity.y * (clock.get_time() / 10))


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
player_shape = [
    [" "," "," ","W","W","W","W"," "," "," "],
    [" "," ","O","O","W","B","W","W"," "," "],
    [" ","O","O","O","W","W","W","W"," "," "],
    [" "," "," ","W","W","W","W"," "," "," "],
    [" "," "," ","W","W","W","W"," ","W"," "],
    [" "," ","W","W","W","W","W","W","W"," "],
    [" ","W","W","W","W","W","W","W"," "," "],
    [" ","W"," ","W","W","W","W"," "," "," "],
    [" "," "," ","O"," "," ","O"," "," "," "],
    [" "," ","O","O"," ","O","O"," "," "," "],
]

player = Player(300, 100, player_shape, pixel_size)

factory = BoundaryFactory()

bounds_color = utils.colors["Red"]
factory.new_boundary(100, 400, 600, 50, bounds_color)
factory.new_boundary(550, 100, 50, 260, bounds_color)
factory.new_boundary(100,100, 50, 300, bounds_color)
factory.new_boundary(300, 200, 100, 50, bounds_color)

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

    player.update(screen, factory)

    floors, colors = factory.get_all()

    for i in range(len(floors)):
        pygame.draw.rect(screen, colors[i], floors[i])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(fps)

pygame.quit()
