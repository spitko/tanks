from pygame import *
from pygame.sprite import Group
from sprite.tank import Tank

init()
background = (0, 0, 0)
display.set_caption("Tanks")
mixer.music.load("data/sounds/start.ogg")
mixer.music.play()
screen = display.set_mode((640, 480))
player1 = Tank(312, 460)
players = Group(player1)
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
            if e.key == K_RETURN:
                if screen.get_flags() & FULLSCREEN:
                    display.set_mode((640, 480))
                else:
                    display.set_mode((640, 480), FULLSCREEN)
            if e.key == K_DOWN:
                player1.move_down()
            if e.key == K_LEFT:
                player1.move_left()
            if e.key == K_RIGHT:
                player1.move_right()
            if e.key == K_UP:
                player1.move_up()
        if e.type == KEYUP:
            if e.key in [K_DOWN, K_LEFT, K_RIGHT, K_UP]:
                player1.stop()
    screen.fill(background)
    players.update()
    players.draw(screen)
    display.update()
    time.delay(100)
