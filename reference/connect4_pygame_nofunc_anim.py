import pygame
import time
import numpy

world = numpy.zeros((6, 6))
player = 1
winner = 0

pygame.init()

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Connect 4')
font = pygame.font.Font(None, 25)

chip_falling = False

while True:
    # get input
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
                if event.unicode.isnumeric():
                    i = int(event.unicode) 
                    chip_x = i - 1
                
    # update state
    if chip_falling:
        world[chip_y][chip_x] = player
        if chip_y > 0:
            world[chip_y - 1][chip_x] = 0
        
        if chip_y == 5 or world[chip_y + 1][chip_x] > 0:
            chip_falling = False
            
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
            
        chip_y = chip_y + 1
            
    if i > 0 and winner == 0:
        chip_falling = True
        chip_y = 0
    
    # draw screen
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
    time.sleep(1 / 20)