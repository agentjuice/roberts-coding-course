import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
GRID_SIZE = 15
TILE_WIDTH = 64
TILE_HEIGHT = 32

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (60, 60, 60)
GRAY = (100, 100, 100)
GREEN = (0, 160, 0)
LIGHT_GREEN = (0, 200, 0)
OUTLINE = (80, 80, 80)


# --- Isometric conversion ---
def grid_to_iso(gx, gy):
    """Convert grid coordinates to isometric screen coordinates."""
    screen_x = (gx - gy) * (TILE_WIDTH // 2)
    screen_y = (gx + gy) * (TILE_HEIGHT // 2)
    return screen_x, screen_y


def iso_to_grid(sx, sy):
    """Convert isometric screen coordinates back to grid coordinates."""
    gx = (sx / (TILE_WIDTH // 2) + sy / (TILE_HEIGHT // 2)) / 2
    gy = (sy / (TILE_HEIGHT // 2) - sx / (TILE_WIDTH // 2)) / 2
    return int(gx), int(gy)


def draw_diamond(surface, color, cx, cy, outline_color=None):
    """Draw a diamond-shaped tile at the given center position."""
    hw = TILE_WIDTH // 2
    hh = TILE_HEIGHT // 2
    points = [
        (cx, cy - hh),       # top
        (cx + hw, cy),       # right
        (cx, cy + hh),       # bottom
        (cx - hw, cy),       # left
    ]
    pygame.draw.polygon(surface, color, points)
    if outline_color:
        pygame.draw.polygon(surface, outline_color, points, 1)


# --- Build the grid ---
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Randomly color some tiles
for _ in range(25):
    rx = random.randint(0, GRID_SIZE - 1)
    ry = random.randint(0, GRID_SIZE - 1)
    grid[ry][rx] = 1

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric Grid Viewer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Camera offset (scrolling)
cam_x = -SCREEN_WIDTH // 2
cam_y = -50
scroll_speed = 8

# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Scroll with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cam_x -= scroll_speed
    if keys[pygame.K_RIGHT]:
        cam_x += scroll_speed
    if keys[pygame.K_UP]:
        cam_y -= scroll_speed
    if keys[pygame.K_DOWN]:
        cam_y += scroll_speed

    # --- Draw ---
    screen.fill(BLACK)

    # Draw the isometric grid
    hover_gx, hover_gy = -1, -1
    mx, my = pygame.mouse.get_pos()

    for gy in range(GRID_SIZE):
        for gx in range(GRID_SIZE):
            iso_x, iso_y = grid_to_iso(gx, gy)
            draw_x = iso_x - cam_x
            draw_y = iso_y - cam_y

            # Pick color based on grid value
            if grid[gy][gx] == 1:
                color = GREEN
            else:
                color = DARK_GRAY

            draw_diamond(screen, color, draw_x, draw_y, OUTLINE)

    # Figure out which tile the mouse is over
    world_mx = mx + cam_x
    world_my = my + cam_y
    hover_gx, hover_gy = iso_to_grid(world_mx, world_my)

    # Highlight hovered tile
    if 0 <= hover_gx < GRID_SIZE and 0 <= hover_gy < GRID_SIZE:
        iso_x, iso_y = grid_to_iso(hover_gx, hover_gy)
        draw_x = iso_x - cam_x
        draw_y = iso_y - cam_y
        draw_diamond(screen, LIGHT_GREEN, draw_x, draw_y, WHITE)

        # Show grid coordinates
        label = font.render(f"({hover_gx}, {hover_gy})", True, WHITE)
        screen.blit(label, (mx + 15, my - 10))

    # Instructions
    info = font.render("Arrow keys: scroll | Hover: see grid coords", True, GRAY)
    screen.blit(info, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
