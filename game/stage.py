from game.sprite.tank import *
from pygame import Color, Surface
from pygame.time import set_timer
from pygame.mixer import music, stop
from pygame.transform import scale


class Stage(Surface):

    BACKGROUND_COLOR = Color("black")
    LOCATION = (56, 16)
    SIZE = (208, 208)

    def __init__(self, level):
        super().__init__(Stage.SIZE)
        Block.group.empty()
        Shell.group.empty()
        Enemy.group.empty()
        Player.group.empty()
        Tank.group.empty()
        with open("data/levels/{}.txt".format(level)) as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "@":
                        SteelWall(8 * x, 8 * y)
                    if char == "#":
                        BrickWall(8 * x, 8 * y)
        set_timer(25, 8000)
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

class Stats(Surface):

    SIZE = (112, 240)
    LOCATION = (0, 32)
    TEXT_COLOR = Color("red")

    def __init__(self):
        super().__init__(Stats.SIZE)
        self.enemies = 1.5
        self.font = sysfont.SysFont("Arial", 25, True)
        self.over_font = sysfont.SysFont("Arial", 100, True)
        self.over, self.done = False, False

    def draw(self, surface):
        self.fill(StageScreen.BACKGROUND_COLOR)
        for i, player in enumerate(Player.group):
            self.blit(self.font.render("P " + str(i+1), True, Stats.TEXT_COLOR), (0, i*70))
            self.blit(self.font.render("Score: " + str(player.score), True, Stats.TEXT_COLOR), (0, i*70 + 27))
            self.blit(self.font.render("Lives: " + str(player.lives), True, Stats.TEXT_COLOR), (0, i*70 + 54))
        surface.blit(self, Stats.LOCATION)
        surface.blit(self.font.render("Current enemies {}/{}".format(len(Enemy.group), int(self.enemies)), True, Stats.TEXT_COLOR), (120, 450))
        if self.over:
            surface.blit(self.over_font.render("GAME OVER", True, Color("white")), (80, 180))
            self.done = True

    def update(self):
        for player in Player.group:
            if player.lives <= 0:
                stop()
                self.over = True
                break
        return self.done

class StageScreen(Surface):

    BACKGROUND_COLOR = Color("gray40")
    LOCATION = (0, 0)
    SIZE = (320, 240)

    def __init__(self, level):
        super().__init__(StageScreen.SIZE)
        self.stage = Stage(level)
        self.stats = Stats()
        self.next_level = 0

    def draw(self, surface):
        self.fill(StageScreen.BACKGROUND_COLOR)
        self.stage.draw(self)
        surface.blit(scale(self, surface.get_size()), StageScreen.LOCATION)
        self.stats.draw(surface)

    def update(self):
        self.stage.update()
        return self.stats.update()

    def handle_event(self, event):
        if event.type == 25:
            self.stats.enemies += 0.25
            if len(Enemy.group) < int(self.stats.enemies):
                if self.stats.enemies % 2 == 0:
                    Enemy.group.add(Enemy(0, 0, Direction.SOUTH))
                else : Enemy.group.add(Enemy(192, 0, Direction.SOUTH))

        if event.type == KEYDOWN or event.type == KEYUP:
            for player in Player.group:
                player.control(event.key)