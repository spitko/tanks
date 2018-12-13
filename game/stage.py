from game.sprite.tank import *
from pygame import Color, Surface
from pygame.mixer import music
from pygame.transform import scale


class Stage(Surface):

    BACKGROUND_COLOR = Color("black")
    LOCATION = (56, 16)
    SIZE = (208, 208)

    def __init__(self, level):
        super().__init__(Stage.SIZE)
        with open("data/levels/{}.txt".format(level)) as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "@":
                        SteelWall(8 * x, 8 * y)
                    if char == "#":
                        BrickWall(8 * x, 8 * y)
        Enemy(0, 0, Direction.SOUTH)
        Enemy(192, 0, Direction.SOUTH)
        Player(64, 192, 0)
        music.load("data/sounds/start.ogg")
        music.play()

    def draw(self, surface):
        self.fill(Stage.BACKGROUND_COLOR)
        Block.group.draw(self)
        Shell.group.draw(self)
        Enemy.group.draw(self)
        Player.group.draw(self)
        surface.blit(self, Stage.LOCATION)

    def update(self):
        Shell.group.update()
        Player.group.update()
        Enemy.group.update()


class StageScreen(Surface):

    BACKGROUND_COLOR = Color("gray40")
    LOCATION = (0, 0)
    SIZE = (320, 240)

    def __init__(self):
        super().__init__(StageScreen.SIZE)
        self.stage = Stage(1)

    def draw(self, surface):
        self.fill(StageScreen.BACKGROUND_COLOR)
        self.stage.draw(self)
        surface.blit(scale(self, surface.get_size()), StageScreen.LOCATION)

    def update(self):
        self.stage.update()
