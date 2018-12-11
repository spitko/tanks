from sprite.tank import Tank
from random import choice, randint

class Tank_AI(Tank):

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.bot = True
        self.movements = [self.move_down, self.move_up, self.move_left, self.move_right]
        self.move = choice(self.movements)
        self.tick = 0

    def update(self, blocks, tanks):
        super().update(blocks, tanks)
        if not self.shells:
            self.fire()
        if not self.moving:
            self.move = choice(self.movements)
            self.tick = 0
        elif self.tick == 16:
            if randint(0, 24) == 0:
                self.move = choice(self.movements)
            self.tick = 0
        self.move()
        self.tick += 1