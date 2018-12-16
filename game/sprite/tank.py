from enum import Enum
from game.sprite.block import *
from pygame import *
from pygame.mixer import Sound, Channel
from pygame.sprite import collide_rect, spritecollide, spritecollideany, Sprite, Group
from random import choice, randint


class Direction(Enum):
    NORTH = Rect(0, -1, 0, 0)
    EAST = Rect(-1, 0, 0, 0)
    SOUTH = Rect(0, 1, 0, 0)
    WEST = Rect(1, 0, 0, 0)

    def __new__(cls, rect):
        direction = object.__new__(cls)
        direction._value_ = len(cls.__members__)
        direction.rect = rect
        return direction


class Tank(Sprite):
    mixer.init()
    engine_sound = Sound("data/sounds/engine.ogg")
    engine_sound_channel = Channel(1)
    explosion1_sound = Sound("data/sounds/explosion1.ogg")
    explosion2_sound = Sound("data/sounds/explosion2.ogg")
    group = Group()
    gun_sound = Sound("data/sounds/shot.ogg")
    gun_sound_channel = Channel(2)
    image_sheet = image.load("data/images/tank.png")
    image_sheet.set_colorkey(Color("black"))

    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.frame = 0
        self.image = Tank.image_sheet.subsurface(Rect(0, 0, 16, 16))
        self.image_sheet = Tank.image_sheet.copy()
        self.model = 0
        self.moving = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shell_image = Shell.images[0]
        self.shell_group = Group()
        self.silent = True
        self.speed = 1
        Tank.group.add(self)

    def kill(self):
        Explosion(self.rect.x, self.rect.y, 16)
        Shell.impact_sound_channel.play(Tank.explosion1_sound)
        super().kill()

    def move(self, direction):
        self.direction = direction
        self.moving = True

    def stop(self):
        self.frame = 0
        self.moving = False
        if self.rect.x % 4 != 0:
            self.rect.x = self.rect.x // 4 * 4 + 4
        if self.rect.y % 4 != 0:
            self.rect.y = self.rect.y // 4 * 4 + 4
        Tank.engine_sound_channel.stop()

    def update(self):
        self.image = self.image_sheet.subsurface(self.direction.value * 32 + self.frame * 16, self.model * 16, 16, 16)
        if self.moving:
            if not Player.engine_sound_channel.get_busy() and not self.silent:
                Player.engine_sound_channel.play(Player.engine_sound, -1)
            self.frame = not self.frame
            for _ in range(self.speed):
                rect = self.rect
                self.rect = self.rect.move(self.direction.rect.x, self.direction.rect.y)
                if spritecollideany(self, SteelWall.group):
                    self.moving = False
                    self.rect = rect
                    break
                if spritecollideany(self, BrickWall.group):
                    self.moving = False
                    self.rect = rect
                    break
                if spritecollideany(self, Water.group):
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


class Explosion(Sprite):
    group = Group()
    image_sheet = image.load("data/images/effect.png")
    image_sheet.set_colorkey(Color(0, 0, 1))
    images = (image_sheet.subsurface(Rect(0, 0, 16, 16)),
              image_sheet.subsurface(Rect(16, 0, 16, 16)),
              image_sheet.subsurface(Rect(32, 0, 16, 16)),
              image_sheet.subsurface(Rect(48, 0, 32, 32)),
              image_sheet.subsurface(Rect(80, 0, 32, 32)))

    def __init__(self, x, y, duration):
        super().__init__()
        self.duration = duration
        self.frame = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        Explosion.group.add(self)

    def update(self):
        self.frame += 1
        if self.frame == 12:
            self.rect.x -= 8
            self.rect.y -= 8
        self.image = Explosion.images[self.frame // 4]
        if self.frame >= self.duration:
            self.kill()


class Shell(Sprite):
    group = Group()
    image_sheet = image.load("data/images/shell.png")
    image_sheet.set_colorkey(Color("black"))
    images = (image_sheet.subsurface(Rect(8 * 0, 0, 8, 8)),
              image_sheet.subsurface(Rect(8 * 1, 0, 8, 8)),
              image_sheet.subsurface(Rect(8 * 2, 0, 8, 8)),
              image_sheet.subsurface(Rect(8 * 3, 0, 8, 8)))
    impact1_sound = Sound("data/sounds/hit1.ogg")
    impact2_sound = Sound("data/sounds/hit2.ogg")
    impact_sound_channel = Channel(3)

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
            self.rect.x += 4
        else:
            self.rect.y += 4
        self.speed = 2
        Shell.group.add(self)

    def update(self):
        for _ in range(self.speed):
            self.rect = self.rect.move(self.direction.rect.x, self.direction.rect.y)
            if (self.rect.x > 200 or self.rect.y > 200) or (self.rect.x < 0 or self.rect.y < 0):
                if not self.tank.silent and not Shell.impact_sound_channel.get_busy():
                    Shell.impact_sound_channel.play(Shell.impact1_sound)
                self.kill()
                Explosion(self.rect.x - 4, self.rect.y - 4, 8)
                break
            if spritecollideany(self, SteelWall.group, False):
                if not self.tank.silent and not Shell.impact_sound_channel.get_busy():
                    Shell.impact_sound_channel.play(Shell.impact1_sound)
                self.kill()
                Explosion(self.rect.x - 4, self.rect.y - 4, 8)
                break
            block_collisions = spritecollide(self, BrickWall.group, False)
            if block_collisions:
                if not self.tank.silent and not Shell.impact_sound_channel.get_busy():
                    Shell.impact_sound_channel.play(Shell.impact2_sound)
                self.kill()
                Explosion(self.rect.x - 4, self.rect.y - 4, 8)
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
            shell = spritecollideany(self, Shell.group)
            if shell and shell is not self:
                self.kill()
                shell.kill()


class Enemy(Tank):
    group = Group()
    shell_group = Group()
    spawns = ((0, 0), (192, 0), (16, 0), (176, 0), (32, 0), (160, 0), (0, 16), (192, 16), (0, 32), (192, 32))

    def __init__(self, x, y):
        self.turn()
        super().__init__(x, y, self.direction)
        self.model = 4
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
            self.turn()
            self.tick = 0
        elif self.tick == 16:
            if randint(0, 24) == 0:
                self.turn()
            self.tick = 0
        self.move(self.direction)
        self.tick += 1

    def turn(self):
        self.direction = choice(list(Direction))


class Player(Tank):
    group = Group()
    shell_group = Group()

    def __init__(self, number):
        if number == 1:
            super().__init__(64, 192, Direction.NORTH)
            self.controls = (K_UP, K_LEFT, K_DOWN, K_RIGHT, K_RCTRL, K_SPACE)
            self.image_sheet.set_palette_at(1, (231, 156, 33))
            self.image_sheet.set_palette_at(2, (107, 107, 0))
            self.image_sheet.set_palette_at(3, (231, 231, 148))
        else:
            super().__init__(128, 0, Direction.SOUTH)
            self.controls = (K_w, K_a, K_s, K_d, K_LCTRL)
            self.image_sheet.set_palette_at(1, (0, 140, 49))
            self.image_sheet.set_palette_at(2, (0, 82, 0))
            self.image_sheet.set_palette_at(3, (181, 247, 206))
        self.lives = 3
        self.score = 0
        self.silent = False
        self.spawn_rect = self.rect.copy()
        self.pressed_controls = []
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
            Tank.gun_sound_channel.play(Tank.gun_sound)
            Player.shell_group.add(Shell(self))

    def kill(self):
        Shell.impact_sound_channel.play(Tank.explosion2_sound)
        Explosion(self.rect.x, self.rect.y, 16)
        self.lives -= 1
        self.rect = self.spawn_rect

    def reset(self):
        self.lives += 1
        self.rect = self.spawn_rect
