from game.sprite.tank import Player
from game.stage import StageScreen
from pygame import FULLSCREEN, init, K_ESCAPE, K_RETURN, KEYDOWN, KEYUP, QUIT
from pygame.display import get_surface, set_caption, set_mode, update
from pygame.event import get as get_events
from pygame.time import Clock

RESOLUTION = (640, 480)

init()
set_caption("Tanks")
set_mode(RESOLUTION)

clock = Clock()
running = True
screen = get_surface()
stage_screen = StageScreen()

while running:
    for event in get_events():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_RETURN:
            if screen.get_flags() & FULLSCREEN:
                set_mode(RESOLUTION)
            else:
                set_mode(RESOLUTION, FULLSCREEN)
        if event.type == KEYDOWN or event.type == KEYUP:
            for player in Player.group:
                player.control(event.key)
    stage_screen.draw(screen)
    stage_screen.update()
    update()
    clock.tick(60)
