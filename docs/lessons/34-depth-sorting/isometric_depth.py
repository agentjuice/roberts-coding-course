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
FLOOR_GRAY2 = (55, 55, 60)
BROWN = (120, 70, 30)
DARK_BROWN = (80, 45, 15)
SIDE_BROWN = (90, 50, 20)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
DARK_RED = (140, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (200, 200, 0)
GRAY = (120, 120, 120)
OUTLINE = (40, 40, 40)

# Tile types
FLOOR = 0
WALL = 1
DOOR = 2
CHEST = 3


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

    top_points = [
        (cx, top_y - hh),
        (cx + hw, top_y),
        (cx, top_y + hh),
        (cx - hw, top_y),
    ]
    pygame.draw.polygon(surface, BROWN, top_points)
    pygame.draw.polygon(surface, OUTLINE, top_points, 1)

    left_points = [
        (cx - hw, top_y),
        (cx, top_y + hh),
        (cx, cy + hh),
        (cx - hw, cy),
    ]
    pygame.draw.polygon(surface, DARK_BROWN, left_points)
    pygame.draw.polygon(surface, OUTLINE, left_points, 1)

    right_points = [
        (cx + hw, top_y),
        (cx, top_y + hh),
        (cx, cy + hh),
        (cx + hw, cy),
    ]
    pygame.draw.polygon(surface, SIDE_BROWN, right_points)
    pygame.draw.polygon(surface, OUTLINE, right_points, 1)


def draw_entity_diamond(surface, color, cx, cy, outline_color=WHITE):
    """Draw a smaller diamond for entities (player/enemies)."""
    hw = TILE_WIDTH // 4
    hh = TILE_HEIGHT // 2
    points = [
        (cx, cy - hh - 8),
        (cx + hw, cy),
        (cx, cy + hh - 4),
        (cx - hw, cy),
    ]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, outline_color, points, 1)


# --- Player ---
class Player:
    def __init__(self, gx, gy):
        self.grid_x = gx
        self.grid_y = gy
        self.health = 10
        self.max_health = 10
        self.damage = 3
        self.move_cooldown = 0
        self.attack_cooldown = 0
        self.facing_x = 1
        self.facing_y = 0
        self.attack_flash = 0

    def move(self, dx, dy, tile_map):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        nx, ny = self.grid_x + dx, self.grid_y + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if tile_map[ny][nx] != WALL:
                self.grid_x = nx
                self.grid_y = ny
                self.facing_x = dx
                self.facing_y = dy
                self.move_cooldown = 4

    def attack(self, enemies):
        if self.attack_cooldown > 0:
            return
        self.attack_cooldown = 10
        self.attack_flash = 4
        for enemy in enemies:
            dist = abs(enemy.grid_x - self.grid_x) + abs(enemy.grid_y - self.grid_y)
            if dist <= 2:
                enemy.take_damage(self.damage)

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_flash > 0:
            self.attack_flash -= 1

    def draw(self, surface, cam_x, cam_y):
        iso_x, iso_y = grid_to_iso(self.grid_x, self.grid_y)
        dx = iso_x - cam_x
        dy = iso_y - cam_y - 10
        color = WHITE if self.attack_flash > 0 else GREEN
        draw_entity_diamond(surface, color, dx, dy)


# --- Enemy ---
class Enemy:
    def __init__(self, gx, gy):
        self.grid_x = gx
        self.grid_y = gy
        self.health = 5
        self.max_health = 5
        self.damage = 1
        self.move_timer = 0
        self.hit_flash = 0
        self.alive = True

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 4
        if self.health <= 0:
            self.alive = False

    def update(self, player, tile_map):
        if not self.alive:
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.move_timer += 1
        if self.move_timer < 15:
            return
        self.move_timer = 0

        # Move toward player
        dx = 0 if player.grid_x == self.grid_x else (1 if player.grid_x > self.grid_x else -1)
        dy = 0 if player.grid_y == self.grid_y else (1 if player.grid_y > self.grid_y else -1)

        # Try horizontal first, then vertical
        nx, ny = self.grid_x + dx, self.grid_y
        if 0 <= nx < MAP_WIDTH and tile_map[ny][nx] != WALL:
            self.grid_x = nx
        else:
            nx, ny = self.grid_x, self.grid_y + dy
            if 0 <= ny < MAP_HEIGHT and tile_map[ny][nx] != WALL:
                self.grid_y = ny

        # Attack player if adjacent
        dist = abs(player.grid_x - self.grid_x) + abs(player.grid_y - self.grid_y)
        if dist <= 1:
            player.health -= self.damage

    def draw(self, surface, cam_x, cam_y):
        if not self.alive:
            return
        iso_x, iso_y = grid_to_iso(self.grid_x, self.grid_y)
        dx = iso_x - cam_x
        dy = iso_y - cam_y - 10
        color = WHITE if self.hit_flash > 0 else RED
        draw_entity_diamond(surface, color, dx, dy)

        # Health bar
        bar_w = 30
        bar_x = dx - bar_w // 2
        bar_y = dy - 24
        pct = self.health / self.max_health
        pygame.draw.rect(surface, DARK_RED, (bar_x, bar_y, bar_w, 4))
        pygame.draw.rect(surface, RED, (bar_x, bar_y, int(bar_w * pct), 4))


# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isometric Depth Sorting")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

tile_map, rooms = generate_map(MAP_WIDTH, MAP_HEIGHT)

# Place player
start_room = rooms[0]
player = Player(start_room[0] + start_room[2] // 2, start_room[1] + start_room[3] // 2)

# Spawn enemies in random rooms
enemies = []
for i in range(2, min(len(rooms), 10)):
    r = rooms[i]
    ex = r[0] + random.randint(1, r[2] - 2)
    ey = r[1] + random.randint(1, r[3] - 2)
    enemies.append(Enemy(ex, ey))

# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0, tile_map)
    elif keys[pygame.K_RIGHT]:
        player.move(1, 0, tile_map)
    elif keys[pygame.K_UP]:
        player.move(0, -1, tile_map)
    elif keys[pygame.K_DOWN]:
        player.move(0, 1, tile_map)
    if keys[pygame.K_SPACE]:
        player.attack(enemies)

    player.update()
    for enemy in enemies:
        enemy.update(player, tile_map)
    enemies = [e for e in enemies if e.alive]

    # Camera follows player
    p_iso_x, p_iso_y = grid_to_iso(player.grid_x, player.grid_y)
    cam_x = p_iso_x - SCREEN_WIDTH // 2
    cam_y = p_iso_y - SCREEN_HEIGHT // 2

    # --- Depth-sorted drawing ---
    screen.fill(BLACK)

    # Build draw list: (depth, type, data)
    draw_list = []

    for gy in range(MAP_HEIGHT):
        for gx in range(MAP_WIDTH):
            tile = tile_map[gy][gx]
            depth = gx + gy
            iso_x, iso_y = grid_to_iso(gx, gy)
            dx = iso_x - cam_x
            dy = iso_y - cam_y
            if dx < -100 or dx > SCREEN_WIDTH + 100 or dy < -150 or dy > SCREEN_HEIGHT + 200:
                continue
            draw_list.append((depth, "tile", tile, dx, dy, gx, gy))

    # Add player to draw list
    p_depth = player.grid_x + player.grid_y
    draw_list.append((p_depth, "player", None, 0, 0, 0, 0))

    # Add enemies to draw list
    for enemy in enemies:
        e_depth = enemy.grid_x + enemy.grid_y
        draw_list.append((e_depth, "enemy", enemy, 0, 0, 0, 0))

    # Sort by depth (back to front)
    draw_list.sort(key=lambda item: (item[0], 0 if item[1] == "tile" else 1))

    # Draw everything in sorted order
    for entry in draw_list:
        depth, kind = entry[0], entry[1]

        if kind == "tile":
            tile, dx, dy, gx, gy = entry[2], entry[3], entry[4], entry[5], entry[6]
            if tile == WALL:
                draw_wall_block(screen, dx, dy)
            else:
                # Checkerboard floor
                color = FLOOR_GRAY if (gx + gy) % 2 == 0 else FLOOR_GRAY2
                draw_diamond(screen, color, dx, dy, OUTLINE)

        elif kind == "player":
            player.draw(screen, cam_x, cam_y)

        elif kind == "enemy":
            entry[2].draw(screen, cam_x, cam_y)

    # HUD
    hp_text = f"HP: {player.health}/{player.max_health}"
    enemy_text = f"Enemies: {len(enemies)}"
    hp_label = font.render(hp_text, True, GREEN)
    enemy_label = font.render(enemy_text, True, RED)
    screen.blit(hp_label, (10, 10))
    screen.blit(enemy_label, (10, 32))

    info = font.render("Arrows: move | Space: attack", True, GRAY)
    screen.blit(info, (10, SCREEN_HEIGHT - 30))

    if player.health <= 0:
        over = font.render("GAME OVER", True, RED)
        screen.blit(over, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
