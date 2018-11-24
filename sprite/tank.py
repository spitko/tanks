from pygame import *
from pygame.mixer import Sound, Channel
from pygame.sprite import Sprite, Group
from pygame.transform import *


class Shell(Sprite):

    image = image.load("resources/images/shell.png")

    def __init__(self, tank):
        Sprite.__init__(self)
        self.direction = tank.direction.copy()
        self.image = tank.shell_image
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x + 4
        self.rect.y = tank.rect.y + 4
        self.speed = 10

    def update(self, blocks):
        for _ in range(self.speed):
            _rect = self.rect
            self.rect = self.rect.move(self.direction.x, self.direction.y)
            if sprite.spritecollide(self, blocks, False):
                self.rect = _rect
                self.kill()
                break
            if display.get_surface().get_rect().contains(self.rect):
                self.rect = self.rect.move(self.direction.x, self.direction.y)
            else:
                self.kill()


class Tank(Sprite):

    mixer.init()
    engine_sound = Sound("resources/sounds/engine.ogg")
    engine_sound_channel = Channel(1)
    gun_sound = Sound("resources/sounds/shot.ogg")
    gun_sound_channel = Channel(2)
    image_sheet = image.load("resources/images/tank.png")

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.direction = Rect(0, 0, 0, 0)
        self.image = Tank.image_sheet.subsurface(Rect(0, 0, 16, 16))
        self.moving = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shell_image = Shell.image
        self.speed = 2
        self.static_image = self.image
        self.shells = Group()

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
        self.moving = False
        Tank.engine_sound_channel.stop()

    def fire(self):
        Tank.gun_sound_channel.play(Tank.gun_sound)
        self.shells.add(Shell(self))

    def update(self, blocks):
        self.shells.update(blocks)
        if self.moving:
            for _ in range(self.speed):
                _rect = self.rect
                self.rect = self.rect.move(self.direction.x, self.direction.y)
                if sprite.spritecollide(self, blocks, False):
                    self.rect = _rect
                    break
                if not Tank.engine_sound_channel.get_busy():
                    Tank.engine_sound_channel.play(Tank.engine_sound, -1)


