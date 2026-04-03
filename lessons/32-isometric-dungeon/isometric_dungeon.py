import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
MAP_WIDTH = 40
MAP_HEIGHT = 30
TILE_WIDTH = 64
TILE_HEIGHT = 32
WALL_HEIGHT = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (45, 45, 50)
FLOOR_GRAY = (60, 60, 65)
BROWN = (120, 70, 30)
DARK_BROWN = (80, 45, 15)
SIDE_BROWN = (90, 50, 20)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
YELLOW = (200, 200, 0)
GRAY = (120, 120, 120)
OUTLINE = (40, 40, 40)

# Tile types
FLOOR = 0
WALL = 1
DOOR = 2
CHEST = 3
STAIRS = 4


# --- Procedural Map Generation ---
def generate_map(width, height):
    tile_map = [[WALL] * width for _ in range(height)]
    rooms = []

    for _ in range(25):
        rw = random.randint(4, 8)
        rh = random.randint(4, 7)
        rx = random.randint(1, width - rw - 1)
        ry = random.randint(1, height - rh - 1)

        overlap = False
        for room in rooms:
            if (rx < room[0] + room[2] + 1 and rx + rw + 1 > room[0] and
                    ry < room[1] + room[3] + 1 and ry + rh + 1 > room[1]):
                overlap = True
                break

        if not overlap:
            rooms.append((rx, ry, rw, rh))
            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    tile_map[y][x] = FLOOR

    # Connect rooms with corridors
    for i in range(len(rooms) - 1):
        r1, r2 = rooms[i], rooms[i + 1]
        cx1, cy1 = r1[0] + r1[2] // 2, r1[1] + r1[3] // 2
        cx2, cy2 = r2[0] + r2[2] // 2, r2[1] + r2[3] // 2

        x = cx1
        while x != cx2:
            tile_map[cy1][x] = FLOOR
            x += 1 if cx2 > cx1 else -1
        y = cy1
        while y != cy2:
            tile_map[y][cx2] = FLOOR
            y += 1 if cy2 > cy1 else -1

    # Place doors and chests
    if len(rooms) > 1:
        # Door in second room entrance
        dr = rooms[1]
        tile_map[dr[1]][dr[0] + dr[2] // 2] = DOOR
    if len(rooms) > 2:
        # Chest in third room
        cr = rooms[2]
        tile_map[cr[1] + 1][cr[0] + 1] = CHEST

    # Stairs in last room
    if rooms:
        lr = rooms[-1]
        tile_map[lr[1] + lr[3] // 2][lr[0] + lr[2] // 2] = STAIRS

    return tile_map, rooms


# --- Isometric helpers ---
def grid_to_iso(gx, gy):
    screen_x = (gx - gy) * (TILE_WIDTH // 2)
    screen_y = (gx + gy) * (TILE_HEIGHT // 2)
    return screen_x, screen_y


def draw_diamond(surface, color, cx, cy, outline_color=None):
    hw = TILE_WIDTH // 2
    hh = TILE_HEIGHT // 2
    points = [
        (cx, cy - hh),
        (cx + hw, cy),
        (cx, cy + hh),
        (cx - hw, cy),
    ]
    pygame.draw.polygon(surface, color, points)
    if outline_color:
        pygame.draw.polygon(surface, outline_color, points, 1)


def draw_wall_block(surface, cx, cy):
    hw = TILE_WIDTH // 2
    hh = TILE_HEIGHT // 2
    top_y = cy - WALL_HEIGHT

    # Top face
    top_points = [
        (cx, top_y - hh),
        (cx + hw, top_y),
        (cx, top_y + hh),
        (cx - hw, top_y),
    ]
    pygame.draw.polygon(surface, BROWN, top_points)
    pygame.draw.polygon(surface, OUTLINE, top_points, 1)

    # Left side face
    left_points = [
        (cx - hw, top_y),
        (cx, top_y + hh),
        (cx, cy + hh),
        (cx - hw, cy),
    ]
    pygame.draw.polygon(surface, DARK_BROWN, left_points)
    pygame.draw.polygon(surface, OUTLINE, left_points, 1)

    # Right side face
    right_points = [
        (cx + hw, top_y),
        (cx, top_y + hh),
        (cx, cy + hh),
        (cx + hw, cy),
    ]
    pygame.draw.polygon(surface, SIDE_BROWN, right_points)
    pygame.draw.polygon(surface, OUTLINE, right_points, 1)


# --- Player ---
class Player:
    def __init__(self, gx, gy):
        self.grid_x = gx
        self.grid_y = gy
        self.move_cooldown = 0

    def move(self, dx, dy, tile_map):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        nx, ny = self.grid_x + dx, self.grid_y + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if tile_map[ny][nx] != WALL:
                self.grid_x = nx
                self.grid_y = ny
                self.move_cooldown = 4

    def draw(self, surface, cam_x, cam_y):
        iso_x, iso_y = grid_to_iso(self.grid_x, self.grid_y)
        dx = iso_x - cam_x
        dy = iso_y - cam_y - 10  # Float above floor
        hw = TILE_WIDTH // 4
        hh = TILE_HEIGHT // 2
        points = [
            (dx, dy - hh - 8),
            (dx + hw, dy),
            (dx, dy + hh - 4),
            (dx - hw, dy),
        ]
        pygame.draw.polygon(surface, GREEN, points)
        pygame.draw.polygon(surface, WHITE, points, 1)


# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric Dungeon")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

tile_map, rooms = generate_map(MAP_WIDTH, MAP_HEIGHT)

# Place player in first room
start_room = rooms[0]
player = Player(start_room[0] + start_room[2] // 2, start_room[1] + start_room[3] // 2)

# --- Tile color map ---
TILE_COLORS = {
    FLOOR: FLOOR_GRAY,
    DOOR: BLUE,
    CHEST: YELLOW,
    STAIRS: (200, 200, 200),
}

# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0, tile_map)
    elif keys[pygame.K_RIGHT]:
        player.move(1, 0, tile_map)
    elif keys[pygame.K_UP]:
        player.move(0, -1, tile_map)
    elif keys[pygame.K_DOWN]:
        player.move(0, 1, tile_map)

    # Camera follows player in isometric space
    p_iso_x, p_iso_y = grid_to_iso(player.grid_x, player.grid_y)
    cam_x = p_iso_x - SCREEN_WIDTH // 2
    cam_y = p_iso_y - SCREEN_HEIGHT // 2

    # --- Draw ---
    screen.fill(BLACK)

    # Draw tiles row by row
    for gy in range(MAP_HEIGHT):
        for gx in range(MAP_WIDTH):
            tile = tile_map[gy][gx]
            iso_x, iso_y = grid_to_iso(gx, gy)
            dx = iso_x - cam_x
            dy = iso_y - cam_y

            # Skip tiles far off screen
            if dx < -100 or dx > SCREEN_WIDTH + 100 or dy < -100 or dy > SCREEN_HEIGHT + 200:
                continue

            if tile == WALL:
                draw_wall_block(screen, dx, dy)
            else:
                color = TILE_COLORS.get(tile, FLOOR_GRAY)
                draw_diamond(screen, color, dx, dy, OUTLINE)

    # Draw player
    player.draw(screen, cam_x, cam_y)

    # HUD
    info = font.render(f"Pos: ({player.grid_x}, {player.grid_y}) | Arrow keys: move", True, GRAY)
    screen.blit(info, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
