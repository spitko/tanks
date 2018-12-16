from pygame import image, Color, Rect
from pygame.sprite import Sprite, Group


class Block(Sprite):
    group = Group()
    image_sheet = image.load("data/images/block.png")
    image_sheet.set_colorkey(Color("black"))

    def __init__(self, x, y, i):
        super().__init__()
        self.image = i
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Block.group.add(self)


class BrickWall(Block):
    group = Group()
    image = Block.image_sheet.subsurface(Rect(8, 0, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y, BrickWall.image)
        BrickWall.group.add(self)


class Ice(Block):
    group = Group()
    image = Block.image_sheet.subsurface(Rect(0, 8 * 2, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y, Ice.image)
        Ice.group.add(self)

    def kill(self):
        pass


class SteelWall(Block):
    group = Group()
    image = Block.image_sheet.subsurface(Rect(0, 0, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y, SteelWall.image)
        SteelWall.group.add(self)

    def kill(self):
        pass


class Tree(Block):
    group = Group()
    image = Block.image_sheet.subsurface(Rect(8 * 2, 0, 8, 8))

    def __init__(self, x, y):
        super().__init__(x, y, Tree.image)
        Tree.group.add(self)

    def kill(self):
        pass


class Water(Block):
    group = Group()
    images = [Block.image_sheet.subsurface(Rect(8 * 0, 8, 8, 8)),
              Block.image_sheet.subsurface(Rect(8 * 1, 8, 8, 8)),
              Block.image_sheet.subsurface(Rect(8 * 2, 8, 8, 8))]

    def __init__(self, x, y):
        super().__init__(x, y, Water.images[0])
        self.frame = 0
        Water.group.add(self)

    def kill(self):
        pass

    def update(self):
        self.frame += 1
        if self.frame > 60:
            self.frame = 0
        self.image = Water.images[self.frame // 30]
