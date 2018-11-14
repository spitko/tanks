from pygame import *
from pygame.mixer import Sound, Channel
from pygame.sprite import Sprite, Group
from pygame.transform import *

from sprite.shell import Shell

class Tank(Sprite):
    mixer.init()
    engine_sound = Sound("resources/sounds/engine.ogg")
    engine_sound_channel = Channel(1)
    shell_sound = Sound("resources/sounds/shot.ogg")
    shell_sound_channel = Channel(2)
    image_sheet = image.load("resources/images/tank.png")

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.direction = Rect(0, 0, 0, 0)
        self.facing = 0
        self.image = Tank.image_sheet.subsurface(Rect(0, 0, 16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.static_image = self.image
        self.shells = Group()

    def move_down(self):
        self.image = flip(self.static_image, False, True)
        self.direction.x = 0
        self.direction.y = +self.speed
        self.facing = 2

    def move_left(self):
        self.image = flip(rotate(self.static_image, -90), True, False)
        self.direction.x = -self.speed
        self.direction.y = 0
        self.facing = 3

    def move_right(self):
        self.image = rotate(self.static_image, -90)
        self.direction.x = +self.speed
        self.direction.y = 0
        self.facing = 1

    def move_up(self):
        self.image = self.static_image
        self.direction.x = 0
        self.direction.y = -self.speed
        self.facing = 0

    def stop(self):
        Tank.engine_sound_channel.stop()
        self.direction.x = 0
        self.direction.y = 0

    def fire(self):
        self.shells.add(Shell(self.rect.x + 4, self.rect.y + 4, self.facing))
        Tank.shell_sound_channel.play(Tank.shell_sound)

    def update(self):
        self.shells.update()
        if self.direction.x or self.direction.y:
            rect = self.rect.move(self.direction.x, self.direction.y)
            if display.get_surface().get_rect().contains(rect):
                if not Tank.engine_sound_channel.get_busy():
                    Tank.engine_sound_channel.play(Tank.engine_sound, -1)
                self.rect = rect
            else:
                self.stop()
