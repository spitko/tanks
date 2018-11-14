from pygame.sprite import Sprite
from pygame import *
from pygame.transform import *

class Shell(Sprite):
    image = image.load("resources/images/shell.png")

    def __init__(self, x, y, direction):
        Sprite.__init__(self)
        self.image = rotate_image(Shell.image, direction)
        self.speed = 25
        self.direction = get_direction(direction, self.speed)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if display.get_surface().get_rect().contains(self.rect):
            self.rect = self.rect.move(*self.direction)
        else:
            self.kill()


def rotate_image(image, dir):
    if dir == 0:
        return image
    if dir == 1:
        return rotate(image, -90)
    if dir == 2:
        return flip(image, False, True)
    if dir == 3:
        return rotate(image, 90)

def get_direction(dir, s):
    if dir == 0:
        return (0, -s)
    if dir == 1:
        return (s, 0)
    if dir == 2:
        return (0, s)
    if dir == 3:
        return (-s, 0)