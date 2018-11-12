from pygame import *
from pygame.mixer import Sound, Channel
from pygame.sprite import Sprite
from pygame.transform import *


class Tank(Sprite):
    mixer.init()
    engine_sound = Sound("data/sounds/engine.ogg")
    engine_sound_channel = Channel(1)
    image_sheet = image.load("data/images/tank.png")

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.direction = Rect(0, 0, 0, 0)
        self.image = Tank.image_sheet.subsurface(Rect(0, 0, 16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.static_image = self.image

    def move_down(self):
        self.image = flip(self.static_image, False, True)
        self.direction.x = 0
        self.direction.y = +self.speed

    def move_left(self):
        self.image = flip(rotate(self.static_image, -90), True, False)
        self.direction.x = -self.speed
        self.direction.y = 0

    def move_right(self):
        self.image = rotate(self.static_image, -90)
        self.direction.x = +self.speed
        self.direction.y = 0

    def move_up(self):
        self.image = self.static_image
        self.direction.x = 0
        self.direction.y = -self.speed

    def stop(self):
        Tank.engine_sound_channel.stop()
        self.direction.x = 0
        self.direction.y = 0

    def update(self):
        if self.direction.x or self.direction.y:
            rect = self.rect.move(self.direction.x, self.direction.y)
            if display.get_surface().get_rect().contains(rect):
                if not Tank.engine_sound_channel.get_busy():
                    Tank.engine_sound_channel.play(Tank.engine_sound, -1)
                self.rect = rect
            else:
                self.stop()
