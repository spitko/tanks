from pygame import *
from pygame.sprite import Sprite, Group


def load(filename):
    group = Group()
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line):
                if char == "@":
                    group.add(SteelWall(8 * x, 8 * y))
                if char == "#":
                    group.add(BrickWall(8 * x, 8 * y))
    return group


class Block(Sprite):
    image_sheet = image.load("resources/images/block.png")

    def __init__(self, x, y):
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fragile = False


class BrickWall(Block):
    image = Block.image_sheet.subsurface(Rect(8, 0, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = BrickWall.image
        self.fragile = True


class Ice(Block):
    image = Block.image_sheet.subsurface(Rect(0, 8 * 2, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = Ice.image


class SteelWall(Block):
    image = Block.image_sheet.subsurface(Rect(0, 0, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = SteelWall.image


class Tree(Block):
    image = Block.image_sheet.subsurface(Rect(8 * 2, 0, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = Tree.image


class Water(Block):
    images = [Block.image_sheet.subsurface(Rect(8 * 0, 8, 8, 8)),
              Block.image_sheet.subsurface(Rect(8 * 1, 8, 8, 8)),
              Block.image_sheet.subsurface(Rect(8 * 2, 8, 8, 8))]

    def __init__(self, x, y):
        super().__init__(x, y)
        self.frame = 0
        self.image = Water.images[self.frame]

    def update(self):
        self.frame += 1
        if self.frame > 2:
            self.frame = 0
        self.image = Water.images[self.frame]
