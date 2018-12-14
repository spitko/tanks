from game.menu import MenuScreen
from game.stage import StageScreen
from pygame import FULLSCREEN, init, K_ESCAPE, K_RETURN, KEYDOWN, KEYUP, QUIT
from pygame.display import get_surface, set_caption, set_mode, update
from pygame.event import get as get_events
from pygame.time import Clock, wait

RESOLUTION = (640, 480)

init()
set_caption("Tanks")
set_mode(RESOLUTION)

clock = Clock()
running = True
screen = get_surface()
scenes = [MenuScreen, StageScreen]
scene = scenes[0]()

while running:
    for event in get_events():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_RETURN:
            if screen.get_flags() & FULLSCREEN:
                set_mode(RESOLUTION)
            else:
                set_mode(RESOLUTION, FULLSCREEN)
        scene.handle_event(event)
    scene.draw(screen)
    if scene.update():
        update()
        if scene.next_level > 0:
            scene = scenes[1](scene.next_level)
        else:
            wait(5000)
            scene = scenes[0]()
    update()
    clock.tick(60)
