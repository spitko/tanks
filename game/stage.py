from game.sprite.tank import *
from pygame import Color, Surface
from pygame.mixer import music, stop
from pygame.transform import scale


class Stage(Surface):
    BACKGROUND_COLOR = Color("black")
    LOCATION = (56, 16)
    SIZE = (208, 208)

    def __init__(self, level, players, restart):
        super().__init__(Stage.SIZE)
        Block.group.empty()
        BrickWall.group.empty()
        Ice.group.empty()
        SteelWall.group.empty()
        Tree.group.empty()
        Water.group.empty()
        Shell.group.empty()
        Enemy.group.empty()
        Explosion.group.empty()
        if restart:
            Tank.group.empty()
            Player.group.empty()
            Player(1)
            if players == 2:
                Player(2)
        else:
            for tank in Tank.group:
                if isinstance(tank, Player):
                    tank.reset()
                else:
                    tank.kill()

        with open("data/levels/{}.txt".format(level)) as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "#":
                        BrickWall(8 * x, 8 * y)
                    if char == "-":
                        Ice(8 * x, 8 * y)
                    if char == "@":
                        SteelWall(8 * x, 8 * y)
                    if char == "%":
                        Tree(8 * x, 8 * y)
                    if char == "~":
                        Water(8 * x, 8 * y)

        music.load("data/sounds/game_start.ogg")
        music.play()

    def draw(self, surface):
        self.fill(Stage.BACKGROUND_COLOR)
        BrickWall.group.draw(self)
        Ice.group.draw(self)
        SteelWall.group.draw(self)
        Water.group.draw(self)
        Shell.group.draw(self)
        Enemy.group.draw(self)
        Player.group.draw(self)
        Tree.group.draw(self)
        Explosion.group.draw(self)
        surface.blit(self, Stage.LOCATION)

    def update(self):
        Water.group.update()
        Shell.group.update()
        Player.group.update()
        Enemy.group.update()
        Explosion.group.update()


class Stats(Surface):
    SIZE = (112, 240)
    LOCATION = (0, 32)
    TEXT_COLOR = Color("red")

    def __init__(self, level):
        super().__init__(Stats.SIZE)
        self.score = sum(player.score for player in Player.group)
        self.spawn_amount = 1 if self.score == 0 else self.score // 5
        self.enemies = max(level * 5, self.score)
        self.font = sysfont.SysFont("Arial", 25, True)
        self.over_font = sysfont.SysFont("Arial", 100, True)
        self.over, self.done = False, False

    def draw(self, surface):
        self.fill(StageScreen.BACKGROUND_COLOR)
        killed = 0
        for i, player in enumerate(Player.group):
            self.blit(self.font.render("P " + str(i + 1), True, Stats.TEXT_COLOR), (0, i * 90))
            self.blit(self.font.render("Score: " + str(player.score), True, Stats.TEXT_COLOR), (0, i * 90 + 27))
            self.blit(self.font.render("Lives: " + str(player.lives), True, Stats.TEXT_COLOR), (0, i * 90 + 54))
            killed += player.score
        surface.blit(self, Stats.LOCATION)
        if len(Player.group) == 1:
            surface.blit(
                self.font.render("{} of {} left".format(self.enemies - killed + self.score, self.enemies), True,
                                 Stats.TEXT_COLOR), (120, 450))
            if killed >= self.enemies + self.score:
                self.done = True
        if self.over:
            surface.blit(self.over_font.render("GAME OVER", True, Color("white")), (16, 180))
            music.load("data/sounds/game_over.ogg")
            music.play()
            self.done = True

    def update(self):
        if len(Player.group) == 1 and len(Enemy.group) == 0:
            Enemy.add_enemy(self.spawn_amount)
            self.spawn_amount += 1
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

    def __init__(self, level, players, reset):
        super().__init__(StageScreen.SIZE)
        self.players = players
        self.stage = Stage(level, players, reset)
        self.stats = Stats(level)
        self.next_level = 1 if level == 4 else level + 1

    def draw(self, surface):
        self.fill(StageScreen.BACKGROUND_COLOR)
        self.stage.draw(self)
        surface.blit(scale(self, surface.get_size()), StageScreen.LOCATION)
        self.stats.draw(surface)

    def update(self):
        self.stage.update()
        if self.stats.update():
            if self.stats.over:
                self.next_level = 0
            return True

    def handle_event(self, event):
        if event.type == KEYDOWN or event.type == KEYUP:
            for player in Player.group:
                player.control(event.key)
