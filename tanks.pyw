from pygame import *
from pygame import event as events
from pygame.sprite import Group
from pygame.time import Clock, set_timer

from data.tank_ai import Tank_AI
from sprite.tank import Tank
from sprite.block import load

BACKGROUND_COLOR = Color("black")
RESOLUTION = (640, 480)
SPAWNBOT = USEREVENT + 1


def main():
    init()
    clock = Clock()
    blocks = load("resources/levels/1.txt")
    display.set_caption("Tanks")
    mixer.music.load("resources/sounds/start.ogg")
    mixer.music.play()
    player1 = Tank(64, 192, Rect(0, -1, 0, 0))
    player1_pressed_keys = []
    bot1 = Tank_AI(0, 0, Rect(0, 1, 0, 0))
    bot2 = Tank_AI(192, 0, Rect(0, 1, 0, 0))
    players = Group(player1)
    bots = Group(bot1, bot2)
    running = True
    screen = display.set_mode(RESOLUTION)
    stage = Surface((208, 208))
    stage_screen = Surface((320, 240))
    stage_screen.fill(Color("gray40"))
    set_timer(SPAWNBOT, 10000)
    while running:
        for event in events.get():
            if event.type == SPAWNBOT:
                if len(bots) % 2 == 0:
                    bots.add(Tank_AI(0, 0, Rect(0, 1, 0, 0)))
                else:
                    bots.add(Tank_AI(192, 0, Rect(0, 1, 0, 0)))
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

        stage.fill(BACKGROUND_COLOR)
        blocks.update()
        blocks.draw(stage)
        players.update(blocks, bots)
        players.draw(stage)
        bots.update(blocks, players)
        bots.draw(stage)
        for player in players:
            player.shells.draw(stage)
        for bot in bots:
            bot.shells.draw(stage)
        stage_screen.blit(stage, (56, 16))
        screen.blit(transform.scale(stage_screen, RESOLUTION), (0, 0))
        display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
