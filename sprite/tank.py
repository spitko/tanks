from pygame import *
from pygame.mixer import Sound, Channel
from pygame.sprite import Sprite, Group
from pygame.transform import *


class Tank(Sprite):
    mixer.init()
    engine_sound = Sound("resources/sounds/engine.ogg")
    engine_sound_channel = Channel(1)
    gun_sound = Sound("resources/sounds/shot.ogg")
    gun_sound_channel = Channel(2)
    image_sheet = image.load("resources/images/tank.png")
    image_sheet.set_colorkey(Color("black"))

    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.image = Tank.image_sheet.subsurface(Rect(0, 0, 16, 16))
        self.moving = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shell_image = Shell.image
        self.shells = Group()
        self.speed = 1
        self.static_image = self.image
        self.stopping = False

    def fire(self):
        if not self.shells:
            Tank.gun_sound_channel.play(Tank.gun_sound)
            self.shells.add(Shell(self))

    def move_down(self):
        self.direction.x = 0
        self.direction.y = 1
        self.image = flip(self.static_image, False, True)
        self.moving = True
        self.shell_image = flip(Shell.image, False, True)

    def move_left(self):
        self.direction.x = -1
        self.direction.y = 0
        self.image = flip(rotate(self.static_image, -90), True, False)
        self.moving = True
        self.shell_image = flip(rotate(Shell.image, -90), True, False)

    def move_right(self):
        self.direction.x = 1
        self.direction.y = 0
        self.image = rotate(self.static_image, -90)
        self.moving = True
        self.shell_image = rotate(Shell.image, -90)

    def move_up(self):
        self.direction.x = 0
        self.direction.y = -1
        self.image = self.static_image.copy()
        self.moving = True
        self.shell_image = Shell.image.copy()

    def stop(self):
        self.stopping = True
        if self.rect.x % 4 == 0 and self.rect.y % 4 == 0:
            self.moving = False
            self.stopping = False
            Tank.engine_sound_channel.stop()

    def update(self, blocks):
        self.shells.update(blocks)
        if self.moving:
            if not Tank.engine_sound_channel.get_busy():
                Tank.engine_sound_channel.play(Tank.engine_sound, -1)
            for _ in range(self.speed):
                rect = self.rect
                self.rect = self.rect.move(self.direction.x, self.direction.y)
                if sprite.spritecollide(self, blocks, False):
                    self.rect = rect
                if self.rect.x > 192 or self.rect.y > 192:
                    self.rect = rect
                if self.rect.x < 0 or self.rect.y < 0:
                    self.rect = rect
        if self.stopping:
            self.stop()


class Shell(Sprite):
    image = image.load("resources/images/shell.png")
    image.set_colorkey(Color("black"))

    def __init__(self, tank):
        super().__init__()
        self.direction = tank.direction.copy()
        self.image = tank.shell_image
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x + 4
        self.rect.y = tank.rect.y + 4
        self.speed = 2

    def update(self, blocks):
        for _ in range(self.speed):
            self.rect = self.rect.move(self.direction.x, self.direction.y)
            if sprite.spritecollide(self, blocks, False):
                self.kill()
                break
            if self.rect.x > 200 or self.rect.y > 200:
                self.kill()
                break
            if self.rect.x < 0 or self.rect.y < 0:
                self.kill()
                break
