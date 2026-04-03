import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Bouncing Ball")
clock = pygame.time.Clock()

# Ball state
x, y = 300, 200       # Starting position (center of window)
dx, dy = 4, 3         # Speed: 4 pixels right, 3 pixels down per frame

running = True
while running:
    # 1. INPUT -- check what the player is doing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # 2. UPDATE -- move the ball and bounce off walls
    x += dx
    y += dy
    if x <= 15 or x >= 585:   # Hit left or right wall
        dx = -dx
    if y <= 15 or y >= 385:   # Hit top or bottom wall
        dy = -dy

    # 3. DRAW -- clear screen and draw ball in new position
    screen.fill('Black')
    pygame.draw.circle(screen, 'Cyan', (x, y), 15)
    pygame.display.flip()

    # 4. TICK -- run at 60 frames per second
    clock.tick(60)

pygame.quit()
