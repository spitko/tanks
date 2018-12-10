from sprite.tank import Tank
from random import choice

class Tank_AI(Tank):

    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.bot = True
        self.movements = [self.move_down, self.move_up, self.move_left, self.move_right]
        self.move = choice(self.movements)
        self.tick = 0

    def update(self, blocks, tanks):
        super().update(blocks, tanks)
        if self.tick >= 32:
            self.fire()
        if not self.moving or self.tick >= 48:
            self.move = choice(self.movements)
            self.tick = 0
        self.move()
        self.tick += 1
