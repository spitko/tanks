from pygame.sprite import Sprite, Group
from pygame import *

def load(file):
    group = Group()
    with open(file) as f:
        y = 0
        for line in f.readlines():
            x = 0
            for char in line:
                block = get_block(char, x, y)
                if block is not None:
                    group.add(get_block(char, x, y))
                x += 8
            y += 8
    return group

def get_block(string, x, y):
    if string == ".":
        return Metal(x, y)
    return None


class Block(Sprite):

    image_sheet = image.load("resources/images/block.png")

    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class Metal(Block):

    img = Block.image_sheet.subsurface(Rect(0, 0, 8, 8))

    def __init__(self, x, y):
        self.image = Metal.img
        super().__init__(x, y)

class Brick(Block):

    img = Block.image_sheet.subsurface(Rect(8, 0, 8, 8))

    def __init__(self, x, y):
        self.image = Brick.img
        super().__init__(x, y)

class Grass(Block):

    img = Block.image_sheet.subsurface(Rect(16, 0, 8, 8))

    def __init__(self, x, y):
        self.image = Grass.img
        super().__init__(x, y)

class Water(Block):

    img = Block.image_sheet.subsurface(Rect(0, 8, 8, 8))
    img1 = Block.image_sheet.subsurface(Rect(8, 8, 8, 8))
    img2 = Block.image_sheet.subsurface(Rect(16, 8, 8, 8))

    def __init__(self, x, y):
        self.image = Water.img
        self.frame = 0
        super().__init__(x, y)

    def update(self):
        if self.frame == 0:
            self.image = Water.img1
        elif self.frame == 1:
            self.image = Water.img2
        else:
            self.image = Water.img
        self.frame += 1
        if self.frame == 3:
            self.frame = 0
