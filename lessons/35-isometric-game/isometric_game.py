import pygame
import sys
import random
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
MAP_WIDTH = 45
MAP_HEIGHT = 35
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
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
DARK_RED = (140, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (220, 200, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 220, 220)
PURPLE = (150, 0, 200)
MAGENTA = (220, 50, 220)
GRAY = (120, 120, 120)
OUTLINE = (40, 40, 40)
STAIRS_COLOR = (180, 180, 200)

# Tile types
FLOOR = 0
WALL = 1
DOOR = 2
CHEST = 3
STAIRS = 4


# --- Procedural Map Generation ---
def generate_map(width, height, level=1):
    random.seed(None)
    tile_map = [[WALL] * width for _ in range(height)]
    rooms = []
    num_rooms = 20 + level * 3

    for _ in range(num_rooms):
        rw = random.randint(4, 9)
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

    # Chests in some rooms
    for i in range(2, min(len(rooms), 6)):
        r = rooms[i]
        tile_map[r[1] + 1][r[0] + 1] = CHEST

    # Stairs in last room
    if rooms:
        lr = rooms[-1]
        tile_map[lr[1] + lr[3] // 2][lr[0] + lr[2] // 2] = STAIRS

    return tile_map, rooms


# --- Isometric helpers ---
def grid_to_iso(gx, gy):
    sx = (gx - gy) * (TILE_WIDTH // 2)
    sy = (gx + gy) * (TILE_HEIGHT // 2)
    return sx, sy


def draw_diamond(surface, color, cx, cy, outline_color=None):
    hw = TILE_WIDTH // 2
    hh = TILE_HEIGHT // 2
    points = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
    pygame.draw.polygon(surface, color, points)
    if outline_color:
        pygame.draw.polygon(surface, outline_color, points, 1)


def draw_wall_block(surface, cx, cy):
    hw = TILE_WIDTH // 2
    hh = TILE_HEIGHT // 2
    top_y = cy - WALL_HEIGHT
    top = [(cx, top_y - hh), (cx + hw, top_y), (cx, top_y + hh), (cx - hw, top_y)]
    pygame.draw.polygon(surface, BROWN, top)
    pygame.draw.polygon(surface, OUTLINE, top, 1)
    left = [(cx - hw, top_y), (cx, top_y + hh), (cx, cy + hh), (cx - hw, cy)]
    pygame.draw.polygon(surface, DARK_BROWN, left)
    pygame.draw.polygon(surface, OUTLINE, left, 1)
    right = [(cx + hw, top_y), (cx, top_y + hh), (cx, cy + hh), (cx + hw, cy)]
    pygame.draw.polygon(surface, SIDE_BROWN, right)
    pygame.draw.polygon(surface, OUTLINE, right, 1)


def draw_entity_diamond(surface, color, cx, cy, outline=WHITE):
    hw = TILE_WIDTH // 4
    hh = TILE_HEIGHT // 2
    points = [(cx, cy - hh - 8), (cx + hw, cy), (cx, cy + hh - 4), (cx - hw, cy)]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, outline, points, 1)


def draw_health_bar(surface, cx, cy, hp, max_hp, bar_color=GREEN):
    bar_w = 30
    bx = cx - bar_w // 2
    by = cy - 28
    pct = max(0, hp / max_hp)
    pygame.draw.rect(surface, DARK_RED, (bx, by, bar_w, 4))
    pygame.draw.rect(surface, bar_color, (bx, by, int(bar_w * pct), 4))


# --- Item ---
class Item:
    def __init__(self, gx, gy, kind):
        self.grid_x = gx
        self.grid_y = gy
        self.kind = kind  # "health", "damage", "speed"
        self.collected = False
        self.colors = {"health": RED, "damage": ORANGE, "speed": CYAN}

    def draw(self, surface, cam_x, cam_y):
        if self.collected:
            return
        iso_x, iso_y = grid_to_iso(self.grid_x, self.grid_y)
        dx = iso_x - cam_x
        dy = iso_y - cam_y - 5
        color = self.colors.get(self.kind, WHITE)
        pygame.draw.circle(surface, color, (int(dx), int(dy)), 6)
        pygame.draw.circle(surface, WHITE, (int(dx), int(dy)), 6, 1)


# --- Player ---
class Player:
    def __init__(self, gx, gy):
        self.grid_x = gx
        self.grid_y = gy
        self.health = 15
        self.max_health = 15
        self.damage = 3
        self.speed_boost = 0
        self.move_cooldown = 0
        self.attack_cooldown = 0
        self.attack_flash = 0
        self.score = 0
        self.inventory = []  # up to 5 items
        self.facing_x = 1
        self.facing_y = 0

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
                self.move_cooldown = 3 if self.speed_boost > 0 else 4

    def attack(self, enemies):
        if self.attack_cooldown > 0:
            return
        self.attack_cooldown = 10
        self.attack_flash = 4
        for enemy in enemies:
            dist = abs(enemy.grid_x - self.grid_x) + abs(enemy.grid_y - self.grid_y)
            if dist <= 2:
                enemy.take_damage(self.damage)

    def pick_up(self, items):
        for item in items:
            if item.collected:
                continue
            if item.grid_x == self.grid_x and item.grid_y == self.grid_y:
                if len(self.inventory) < 5:
                    self.inventory.append(item.kind)
                    item.collected = True
                    break

    def use_item(self, index):
        if index >= len(self.inventory):
            return
        kind = self.inventory.pop(index)
        if kind == "health":
            self.health = min(self.max_health, self.health + 5)
        elif kind == "damage":
            self.damage += 1
        elif kind == "speed":
            self.speed_boost = 150  # frames

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_flash > 0:
            self.attack_flash -= 1
        if self.speed_boost > 0:
            self.speed_boost -= 1

    def draw(self, surface, cam_x, cam_y):
        iso_x, iso_y = grid_to_iso(self.grid_x, self.grid_y)
        dx = iso_x - cam_x
        dy = iso_y - cam_y - 10
        color = WHITE if self.attack_flash > 0 else GREEN
        draw_entity_diamond(surface, color, dx, dy)
        draw_health_bar(surface, dx, dy, self.health, self.max_health, GREEN)


# --- Enemy ---
class Enemy:
    def __init__(self, gx, gy, kind="zombie", level=1):
        self.grid_x = gx
        self.grid_y = gy
        self.kind = kind
        self.alive = True
        self.hit_flash = 0
        self.move_timer = 0
        self.attack_timer = 0
        self.exploding = False
        self.explode_timer = 0

        stats = {
            "zombie": {"health": 4, "damage": 1, "speed": 18, "color": RED},
            "skeleton": {"health": 3, "damage": 2, "speed": 22, "color": GRAY},
            "creeper": {"health": 3, "damage": 4, "speed": 14, "color": DARK_GREEN},
        }
        s = stats.get(kind, stats["zombie"])
        self.health = int(s["health"] * (1 + level * 0.3))
        self.max_health = self.health
        self.damage = s["damage"] + level - 1
        self.speed = s["speed"]
        self.color = s["color"]

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
        if self.move_timer < self.speed:
            return
        self.move_timer = 0

        dist = abs(player.grid_x - self.grid_x) + abs(player.grid_y - self.grid_y)

        # Creeper explodes when adjacent
        if self.kind == "creeper" and dist <= 1:
            if not self.exploding:
                self.exploding = True
                self.explode_timer = 10
            else:
                self.explode_timer -= 1
                if self.explode_timer <= 0:
                    player.health -= self.damage
                    self.alive = False
            return

        # Move toward player
        dx = 0 if player.grid_x == self.grid_x else (1 if player.grid_x > self.grid_x else -1)
        dy = 0 if player.grid_y == self.grid_y else (1 if player.grid_y > self.grid_y else -1)

        nx = self.grid_x + dx
        if 0 <= nx < MAP_WIDTH and tile_map[self.grid_y][nx] != WALL:
            self.grid_x = nx
        else:
            ny = self.grid_y + dy
            if 0 <= ny < MAP_HEIGHT and tile_map[ny][self.grid_x] != WALL:
                self.grid_y = ny

        # Skeleton ranged attack
        if self.kind == "skeleton" and dist <= 4 and dist > 1:
            self.attack_timer += 1
            if self.attack_timer >= 3:
                player.health -= 1
                self.attack_timer = 0
        elif self.kind == "zombie" and dist <= 1:
            player.health -= self.damage

    def draw(self, surface, cam_x, cam_y):
        if not self.alive:
            return
        iso_x, iso_y = grid_to_iso(self.grid_x, self.grid_y)
        dx = iso_x - cam_x
        dy = iso_y - cam_y - 10
        color = WHITE if self.hit_flash > 0 else self.color
        if self.exploding and self.explode_timer % 2 == 0:
            color = YELLOW
        draw_entity_diamond(surface, color, dx, dy)
        draw_health_bar(surface, dx, dy, self.health, self.max_health, RED)


# --- Game ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Isometric Dungeon Crawler")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        self.state = "menu"
        self.level = 1
        self.start_level()

    def start_level(self):
        self.tile_map, self.rooms = generate_map(MAP_WIDTH, MAP_HEIGHT, self.level)
        start = self.rooms[0]
        self.player = Player(start[0] + start[2] // 2, start[1] + start[3] // 2)
        self.enemies = []
        self.items = []
        kinds = ["zombie", "skeleton", "creeper"]

        for i in range(2, min(len(self.rooms), 12)):
            r = self.rooms[i]
            num = random.randint(1, 2 + self.level)
            for _ in range(num):
                ex = r[0] + random.randint(1, max(1, r[2] - 2))
                ey = r[1] + random.randint(1, max(1, r[3] - 2))
                kind = random.choice(kinds)
                self.enemies.append(Enemy(ex, ey, kind, self.level))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if event.key == pygame.K_RETURN:
                            self.state = "playing"
                    elif self.state == "game_over":
                        if event.key == pygame.K_r:
                            self.level = 1
                            self.start_level()
                            self.state = "playing"
                    elif self.state == "playing":
                        if event.key == pygame.K_e:
                            self.player.pick_up(self.items)
                        if event.key == pygame.K_1:
                            self.player.use_item(0)
                        if event.key == pygame.K_2:
                            self.player.use_item(1)
                        if event.key == pygame.K_3:
                            self.player.use_item(2)

            if self.state == "playing":
                self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1, 0, self.tile_map)
        elif keys[pygame.K_RIGHT]:
            self.player.move(1, 0, self.tile_map)
        elif keys[pygame.K_UP]:
            self.player.move(0, -1, self.tile_map)
        elif keys[pygame.K_DOWN]:
            self.player.move(0, 1, self.tile_map)
        if keys[pygame.K_SPACE]:
            self.player.attack(self.enemies)

        self.player.update()

        # Drop loot from dead enemies
        for enemy in self.enemies:
            if not enemy.alive:
                self.player.score += 10
                if random.random() < 0.5:
                    kinds = ["health", "damage", "speed"]
                    self.items.append(Item(enemy.grid_x, enemy.grid_y, random.choice(kinds)))

        for enemy in self.enemies:
            enemy.update(self.player, self.tile_map)
        self.enemies = [e for e in self.enemies if e.alive]

        # Check stairs
        px, py = self.player.grid_x, self.player.grid_y
        if self.tile_map[py][px] == STAIRS:
            self.level += 1
            old_score = self.player.score
            old_inv = self.player.inventory[:]
            self.start_level()
            self.player.score = old_score
            self.player.inventory = old_inv

        if self.player.health <= 0:
            self.state = "game_over"

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "menu":
            title = self.big_font.render("ISOMETRIC DUNGEON", True, GREEN)
            sub = self.font.render("Press ENTER to start", True, GRAY)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 280))
            pygame.display.flip()
            return

        if self.state == "game_over":
            title = self.big_font.render("GAME OVER", True, RED)
            score = self.font.render(f"Score: {self.player.score} | Press R to restart", True, GRAY)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
            self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, 280))
            pygame.display.flip()
            return

        # Camera
        p_iso_x, p_iso_y = grid_to_iso(self.player.grid_x, self.player.grid_y)
        cam_x = p_iso_x - SCREEN_WIDTH // 2
        cam_y = p_iso_y - SCREEN_HEIGHT // 2

        # Build depth-sorted draw list
        draw_list = []

        for gy in range(MAP_HEIGHT):
            for gx in range(MAP_WIDTH):
                tile = self.tile_map[gy][gx]
                iso_x, iso_y = grid_to_iso(gx, gy)
                dx = iso_x - cam_x
                dy = iso_y - cam_y
                if dx < -100 or dx > SCREEN_WIDTH + 100 or dy < -150 or dy > SCREEN_HEIGHT + 200:
                    continue
                depth = gx + gy
                draw_list.append((depth, 0, "tile", tile, dx, dy, gx, gy))

        # Player
        p_depth = self.player.grid_x + self.player.grid_y
        draw_list.append((p_depth, 1, "player", None, 0, 0, 0, 0))

        # Enemies
        for enemy in self.enemies:
            e_depth = enemy.grid_x + enemy.grid_y
            draw_list.append((e_depth, 1, "enemy", enemy, 0, 0, 0, 0))

        # Items
        for item in self.items:
            if not item.collected:
                i_depth = item.grid_x + item.grid_y
                draw_list.append((i_depth, 1, "item", item, 0, 0, 0, 0))

        draw_list.sort(key=lambda e: (e[0], e[1]))

        # Draw sorted
        for entry in draw_list:
            kind = entry[2]
            if kind == "tile":
                tile, dx, dy, gx, gy = entry[3], entry[4], entry[5], entry[6], entry[7]
                if tile == WALL:
                    draw_wall_block(self.screen, dx, dy)
                elif tile == STAIRS:
                    draw_diamond(self.screen, STAIRS_COLOR, dx, dy, WHITE)
                elif tile == CHEST:
                    draw_diamond(self.screen, YELLOW, dx, dy, OUTLINE)
                else:
                    color = FLOOR_GRAY if (gx + gy) % 2 == 0 else FLOOR_GRAY2
                    draw_diamond(self.screen, color, dx, dy, OUTLINE)
            elif kind == "player":
                self.player.draw(self.screen, cam_x, cam_y)
            elif kind == "enemy":
                entry[3].draw(self.screen, cam_x, cam_y)
            elif kind == "item":
                entry[3].draw(self.screen, cam_x, cam_y)

        # --- HUD (flat overlay) ---
        # Health bar
        pygame.draw.rect(self.screen, DARK_GRAY, (10, 10, 154, 24))
        hp_pct = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, GREEN, (12, 12, int(150 * hp_pct), 20))
        hp_text = self.font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (16, 14))

        # Score and level
        score_text = self.font.render(f"Score: {self.player.score}", True, YELLOW)
        level_text = self.font.render(f"Floor {self.level}", True, CYAN)
        self.screen.blit(score_text, (SCREEN_WIDTH - 120, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH - 120, 32))

        # Inventory
        inv_y = SCREEN_HEIGHT - 40
        inv_label = self.font.render("Inv:", True, GRAY)
        self.screen.blit(inv_label, (10, inv_y))
        item_colors = {"health": RED, "damage": ORANGE, "speed": CYAN}
        for i, item_kind in enumerate(self.player.inventory):
            color = item_colors.get(item_kind, WHITE)
            bx = 55 + i * 30
            pygame.draw.rect(self.screen, DARK_GRAY, (bx, inv_y - 2, 24, 24))
            pygame.draw.circle(self.screen, color, (bx + 12, inv_y + 10), 8)
            key_label = self.font.render(str(i + 1), True, WHITE)
            self.screen.blit(key_label, (bx + 7, inv_y - 16))

        # Controls
        controls = self.font.render("Arrows:move  Space:attack  E:pickup  1-3:use item", True, GRAY)
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 20))

        pygame.display.flip()


# --- Run ---
if __name__ == "__main__":
    game = Game()
    game.run()
