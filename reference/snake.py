import pygame
import time
import random

snake = [(0, 0)]
snake_direction = 'right'
apple_position = None
game_over = False

pygame.init()

font = pygame.font.Font(None, 25)
screen = pygame.display.set_mode((800, 400))

pygame.display.set_caption('Snake')

while True:
    # get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                snake = [(0, 0)]
                snake_direction = 'right'
                apple_position = None
                game_over = False
            elif event.key == pygame.K_UP:
                if snake_direction != 'down':
                    snake_direction = 'up'
            elif event.key == pygame.K_DOWN:
                if snake_direction != 'up':
                    snake_direction = 'down'
            elif event.key == pygame.K_LEFT:
                if snake_direction != 'right':
                    snake_direction = 'left'
            elif event.key == pygame.K_RIGHT:
                if snake_direction != 'left':
                    snake_direction = 'right'
                
    # update state
    if not apple_position:
        apple_position = (random.randint(0, 19), random.randint(0, 14))
        
    if not game_over:
        last_snake_position = snake[0]
        new_snake_position = None
        
        if snake_direction == 'up':
            new_snake_position = (last_snake_position[0], last_snake_position[1] - 1)
        elif snake_direction == 'down':
            new_snake_position = (last_snake_position[0], last_snake_position[1] + 1)
        elif snake_direction == 'left':
            new_snake_position = (last_snake_position[0] - 1, last_snake_position[1])
        elif snake_direction == 'right':
            new_snake_position = (last_snake_position[0] + 1, last_snake_position[1])
    
        # check wall collision
        if new_snake_position[0] < 0 or new_snake_position[0] >= 20 or new_snake_position[1] < 0 or new_snake_position[1] >= 15:
            game_over = True
        
        # check snake collision
        for i in snake:
            if new_snake_position == i:
                game_over = True
        
        # add snake block
        if not game_over:
            snake.insert(0, new_snake_position)
    
        # check apple collission
        if new_snake_position == apple_position:
            apple_position = None
        elif not game_over:
            # remove the oldest block
            snake.pop()

    # draw world
    screen.fill('Blue')

    for x in range(20):
        for y in range(15):
            pygame.draw.rect(screen, 'Black', (x * 21 + 25, y * 21 + 25, 20, 20))

    # draw apple
    if apple_position:
        pygame.draw.rect(screen, 'Red', (apple_position[0] * 21 + 25, apple_position[1] * 21 + 25, 20, 20))
        
    # draw snake
    for t in snake:
        pygame.draw.rect(screen, 'Yellow', (t[0] * 21 + 25, t[1] * 21 + 25, 20, 20))

    # draw score
    score_text = font.render("SCORE: %d" % len(snake), True, 'Green')
    screen.blit(score_text, ((500, 25)))
        
    if game_over:
        game_over_text = font.render("GAME OVER", True, 'Green')
        screen.blit(game_over_text, ((25, 360)))
            
    pygame.display.update()
    time.sleep(1 / 10)
    