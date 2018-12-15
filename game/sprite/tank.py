from enum import Enum
from game.sprite.block import *
from pygame import *
from pygame.mixer import Sound, Channel
from pygame.sprite import collide_rect, spritecollide, spritecollideany, Sprite, Group
from random import choice, randint


class Direction(Enum):
    NORTH = 0, Rect(0, -1, 0, 0)
    EAST = 1, Rect(-1, 0, 0, 0)
    SOUTH = 2, Rect(0, 1, 0, 0)
    WEST = 3, Rect(1, 0, 0, 0)

    def __new__(cls, index, rect):
        direction = object.__new__(cls)
        direction._value_ = index
        direction.rect = rect
        return direction


class Tank(Sprite):
    group = Group()
    image_sheet = image.load("data/images/tank.png")
    image_sheet.set_colorkey(Color("black"))

    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.frame = 0
        self.image = Tank.image_sheet.subsurface(Rect(0, 0, 16, 16))
        self.image_sheet = Tank.image_sheet
        self.moving = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shell_image = Shell.images[0]
        self.shell_group = Group()
        self.speed = 1
        self.static_image = self.image
        self.stopping = False
        self.score = 0
        Tank.group.add(self)

    def move(self, direction):
        self.direction = direction
        self.moving = True

    def stop(self):
        self.moving = False
        if self.rect.x % 4 != 0:
            self.rect.x = self.rect.x // 4 * 4 + 4
        if self.rect.y % 4 != 0:
            self.rect.y = self.rect.y // 4 * 4 + 4

    def update(self):
        self.image = self.image_sheet.subsurface(self.direction.value * 32 + self.frame * 16, 0, 16, 16)
        if self.moving:
            self.frame = not self.frame
            for _ in range(self.speed):
                rect = self.rect
                self.rect = self.rect.move(self.direction.rect.x, self.direction.rect.y)
                if spritecollideany(self, Block.group):
                    self.moving = False
                    self.rect = rect
                    break
                if spritecollideany(self, Tank.group, collided=lambda s, o: False if s is o else collide_rect(s, o)):
                    self.moving = False
                    self.rect = rect
                    break
                if self.rect.x > 192 or self.rect.y > 192:
                    self.moving = False
                    self.rect = rect
                    break
                if self.rect.x < 0 or self.rect.y < 0:
                    self.moving = False
                    self.rect = rect
                    break


class Shell(Sprite):
    group = Group()
    image_sheet = image.load("data/images/shell.png")
    image_sheet.set_colorkey(Color("black"))
    images = (image_sheet.subsurface(Rect(8 * 0, 0, 8, 8)),
              image_sheet.subsurface(Rect(8 * 1, 0, 8, 8)),
              image_sheet.subsurface(Rect(8 * 2, 0, 8, 8)),
              image_sheet.subsurface(Rect(8 * 3, 0, 8, 8)))

    def __init__(self, tank):
        super().__init__()
        self.tank = tank
        self.tank.shell_group.add(self)
        self.direction = tank.direction
        self.image = Shell.images[self.direction.value]
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x
        self.rect.y = tank.rect.y
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            self.rect.x += 3
        else:
            self.rect.y += 4
        self.speed = 2
        Shell.group.add(self)

    def update(self):
        for _ in range(self.speed):
            self.rect = self.rect.move(self.direction.rect.x, self.direction.rect.y)
            if (self.rect.x > 200 or self.rect.y > 200) or (self.rect.x < 0 or self.rect.y < 0):
                self.kill()
                break
            block_collisions = spritecollide(self, Block.group, False)
            if block_collisions:
                self.kill()
                for block in block_collisions:
                    block.kill()
                break
            tank_collisions = spritecollide(self, Tank.group, False)
            if tank_collisions:
                for tank in tank_collisions:
                    if self.tank != tank:
                        if isinstance(self.tank, Player):
                            self.tank.score += 1
                            tank.kill()
                        elif isinstance(tank, Player):
                            tank.kill()
                        self.kill()

class Enemy(Tank):
    group = Group()
    shell_group = Group()
    spawns = [(0, 0), (192, 0), (16, 0), (176, 0), (32, 0), (160, 0), (0, 16), (192, 16), (0, 32), (192, 32)]

    def __init__(self, x, y):
        self.direction = choice(list(Direction))
        super().__init__(x, y, self.direction)
        self.tick = 0
        Enemy.group.add(self)

    @staticmethod
    def add_enemy(amount):
        for i in range(min(amount, len(Enemy.spawns))):
            Enemy(*Enemy.spawns[i])

    def fire(self):
        if not self.shell_group:
            Enemy.shell_group.add(Shell(self))

    def update(self):
        super().update()
        self.fire()
        if not self.moving:
            self.direction = choice(list(Direction))
            self.tick = 0
        elif self.tick == 16:
            if randint(0, 24) == 0:
                self.direction = choice(list(Direction))
            self.tick = 0
        self.move(self.direction)
        self.tick += 1


class Player(Tank):
    CONTROLS = ((K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RCTRL, K_SPACE), (K_w, K_a, K_s, K_d, K_LCTRL))

    mixer.init()
    engine_sound = Sound("data/sounds/engine.ogg")
    engine_sound_channel = Channel(1)
    group = Group()
    gun_sound = Sound("data/sounds/shot.ogg")
    gun_sound_channel = Channel(2)
    shell_group = Group()

    def __init__(self, x, y, index):
        super().__init__(x, y, Direction.NORTH)
        self.controls = Player.CONTROLS[index]
        self.spawn_location = self.rect.copy()
        self.pressed_controls = []
        self.lives = 3
        Player.group.add(self)

    def control(self, control):
        if control in self.controls[:4]:
            if control in self.pressed_controls:
                self.pressed_controls.remove(control)
                if not self.pressed_controls:
                    self.stop()
                    return
                control = self.pressed_controls[-1]
            else:
                self.pressed_controls.append(control)
            self.move(Direction(self.controls.index(control)))
        elif control in self.controls[4:]:
            self.fire()

    def fire(self):
        if not self.shell_group:
            Player.gun_sound_channel.play(Player.gun_sound)
            Player.shell_group.add(Shell(self))

    def kill(self):
        self.lives -= 1
        self.rect = self.spawn_location

    def reset(self):
        self.lives += 1
        self.rect = self.spawn_location

    def stop(self):
        super().stop()
        Player.engine_sound_channel.stop()

    def update(self):
        if self.moving and not Player.engine_sound_channel.get_busy():
            Player.engine_sound_channel.play(Player.engine_sound, -1)
        super().update()
