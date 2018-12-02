from pygame import *
from pygame import event as events
from pygame.sprite import Group
from pygame.time import Clock
from sprite.tank import Tank
from sprite.block import load

BACKGROUND_COLOR = Color("black")
RESOLUTION = (640, 480)


def main():
    init()
    clock = Clock()
    blocks = load("resources/levels/1.txt")
    display.set_caption("Tanks")
    mixer.music.load("resources/sounds/start.ogg")
    mixer.music.play()
    player1 = Tank(312, 420, Rect(0, -1, 0, 0))
    player1_pressed_keys = []
    players = Group(player1)
    running = True
    screen = display.set_mode(RESOLUTION)
    while running:
        for event in events.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    if screen.get_flags() & FULLSCREEN:
                        display.set_mode(RESOLUTION)
                    else:
                        display.set_mode(RESOLUTION, FULLSCREEN)
                if event.key == K_DOWN:
                    player1.move_down()
                    player1_pressed_keys.append(event.key)
                if event.key == K_LEFT:
                    player1.move_left()
                    player1_pressed_keys.append(event.key)
                if event.key == K_RIGHT:
                    player1.move_right()
                    player1_pressed_keys.append(event.key)
                if event.key == K_UP:
                    player1.move_up()
                    player1_pressed_keys.append(event.key)
                if event.key == K_SPACE:
                    player1.fire()
            if event.type == KEYUP:
                if event.key in [K_DOWN, K_LEFT, K_RIGHT, K_UP]:
                    player1_pressed_keys.remove(event.key)
                    if not player1_pressed_keys:
                        player1.stop()
                    else:
                        key = player1_pressed_keys[-1]
                        if key == K_DOWN:
                            player1.move_down()
                        if key == K_LEFT:
                            player1.move_left()
                        if key == K_RIGHT:
                            player1.move_right()
                        if key == K_UP:
                            player1.move_up()
        screen.fill(BACKGROUND_COLOR)
        blocks.update()
        blocks.draw(screen)
        players.update(blocks)
        players.draw(screen)
        for player in players:
            player.shells.draw(screen)
        display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
