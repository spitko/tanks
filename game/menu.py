from pygame import Surface, Color, sysfont, K_DOWN, K_UP, KEYDOWN, K_RIGHT, K_LEFT, K_RETURN


class MenuScreen(Surface):
    SIZE = (640, 480)
    BACKGROUND_COLOR = Color("gray10")
    TEXT_COLOR = Color("white")

    def __init__(self):
        super().__init__(MenuScreen.SIZE)
        self.done = False
        self.index = 0
        self.players = 1
        self.next_level = 1
        self.title_font = sysfont.SysFont("impact", 120, False)
        self.default_font = sysfont.SysFont("Arial", 55, True)
        self.start_font = sysfont.SysFont("Arial", 70, True)
        self.player_font = sysfont.SysFont("Arial", 40, True)

    def draw(self, surface):
        if self.index == 0:
            arrow_height = 190
        elif self.index == 1:
            arrow_height = 230
        else:
            arrow_height = 270
        self.fill(MenuScreen.BACKGROUND_COLOR)
        self.blit(self.title_font.render("TANKS", True, Color("red")), (60, 40))
        self.blit(self.start_font.render("START", True, MenuScreen.TEXT_COLOR), (370, 190))
        self.blit(self.player_font.render("PLAYERS  " + str(self.players), True, MenuScreen.TEXT_COLOR), (370, 252))
        self.blit(self.default_font.render("LEVEL  " + str(self.next_level), True, MenuScreen.TEXT_COLOR), (370, 282))
        self.blit(self.start_font.render("\u2192", True, MenuScreen.TEXT_COLOR), (295, arrow_height))
        surface.blit(self, (0, 0))

    def update(self):
        if self.done:
            return True
        return False

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                index = self.index + 1
                self.index = 0 if index > 2 else index
            if event.key == K_UP:
                index = self.index - 1
                self.index = 2 if index < 0 else index
            if event.key == K_RIGHT:
                if self.index == 2:
                    self.next_level = self.next_level + 1 if self.next_level < 4 else 1
                elif self.index == 1:
                    self.players = 3 - self.players
            if event.key == K_LEFT:
                if self.index == 2:
                    self.next_level = self.next_level - 1 if self.next_level > 1 else 4
                elif self.index == 1:
                    self.players = 3 - self.players
            if event.key == K_RETURN:
                self.done = True
