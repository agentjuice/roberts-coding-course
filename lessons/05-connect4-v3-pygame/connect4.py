import pygame
import time
import numpy

world = numpy.zeros((6, 6))
player = 1
winner = 0

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Connect 4')
font = pygame.font.Font(None, 25)

while True:
    i = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            else:
                i = int(event.unicode)

    if i > 0 and winner == 0:
        for y in range(6):
            if y == 5 or world[y + 1][i - 1] > 0:
                world[y][i - 1] = player
                break
        for y in range(6):
            for x in range(6):
                if world[y][x] != player:
                    continue
                if x <= 2 and world[y][x + 1] == player and world[y][x + 2] == player and world[y][x + 3] == player:
                    winner = player
                if y <= 2 and world[y + 1][x] == player and world[y + 2][x] == player and world[y + 3][x] == player:
                    winner = player
                if x <= 2 and y <= 2 and world[y + 1][x + 1] == player and world[y + 2][x + 2] == player and world[y + 3][x + 3] == player:
                    winner = player
                if x <= 2 and y > 2 and world[y - 1][x + 1] == player and world[y - 2][x + 2] == player and world[y - 3][x + 3] == player:
                    winner = player
        if world[0][0] > 0 and world[0][1] > 0 and world[0][2] > 0 and world[0][3] > 0 and world[0][4] > 0 and world[0][5] > 0:
            winner = -1
        if player == 1:
            player = 2
        else:
            player = 1

    screen.fill('Blue')
    for x in range(6):
        text = font.render(str(x + 1), True, 'Green')
        screen.blit(text, ((x * 30 + 45, 10)))
    for y in range(6):
        for x in range(6):
            if world[y][x] == 0:
                pygame.draw.circle(screen, 'Black', (x * 30 + 50, y * 30 + 50), 10)
            elif world[y][x] == 1:
                pygame.draw.circle(screen, 'Red', (x * 30 + 50, y * 30 + 50), 10)
            elif world[y][x] == 2:
                pygame.draw.circle(screen, 'Yellow', (x * 30 + 50, y * 30 + 50), 10)
    if winner < 0:
        text = font.render('DRAW', True, 'Green')
        screen.blit(text, ((10, 350)))
    elif winner > 0:
        text = font.render("WINNER - PLAYER: %d" % winner, True, 'Green')
        screen.blit(text, ((10, 350)))
    pygame.display.update()
    time.sleep(0.1)
