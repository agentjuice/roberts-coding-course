import pygame
import sys
import random
import math
import time

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 30
MAP_WIDTH = 50
MAP_HEIGHT = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
GRAY = (120, 120, 120)
BROWN = (100, 60, 20)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (200, 200, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (220, 50, 220)
PURPLE = (150, 0, 200)

# Tile types: 0=floor, 1=wall, 2=door, 3=chest, 4=stairs
FLOOR = 0
WALL = 1
DOOR = 2
CHEST = 3
STAIRS = 4


# --- Sound helper ---
def load_sound(name):
    """Try to load a sound file, return None if not found."""
    try:
        return pygame.mixer.Sound(name)
    except Exception:
        return None


def play_sound(sound):
    if sound:
        sound.play()


# --- Procedural Map Generation ---
def generate_map(width, height, seed=None):
    """Generate a dungeon map with rooms and corridors."""
    if seed is not None:
        random.seed(seed)

    tile_map = [[WALL] * width for _ in range(height)]
    rooms = []

    # Place rooms
    for _ in range(30):
        rw = random.randint(4, 9)
        rh = random.randint(4, 7)
        rx = random.randint(1, width - rw - 1)
        ry = random.randint(1, height - rh - 1)

        # Check overlap
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
        r1 = rooms[i]
        r2 = rooms[i + 1]
        cx1 = r1[0] + r1[2] // 2
        cy1 = r1[1] + r1[3] // 2
        cx2 = r2[0] + r2[2] // 2
        cy2 = r2[1] + r2[3] // 2

        # Horizontal then vertical
        x = cx1
        while x != cx2:
            if 0 < x < width - 1:
                tile_map[cy1][x] = FLOOR
            x += 1 if cx2 > cx1 else -1
        y = cy1
        while y != cy2:
            if 0 < y < height - 1:
                tile_map[y][cx2] = FLOOR
            y += 1 if cy2 > cy1 else -1

    # Place chests in some rooms
    for room in rooms[2:]:
        if random.random() < 0.4:
            cx = room[0] + random.randint(1, room[2] - 2)
            cy = room[1] + random.randint(1, room[3] - 2)
            tile_map[cy][cx] = CHEST

    # Reset random seed so gameplay isn't deterministic
    random.seed()

    return tile_map, rooms


# --- Particle ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.color = color
        self.life = 20

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self, screen, cam_x, cam_y):
        if self.life > 0:
            size = max(1, self.life // 5)
            pygame.draw.circle(screen, self.color,
                               (int(self.x - cam_x), int(self.y - cam_y)), size)


# --- Item ---
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        if item_type == "health_potion":
            self.color = (255, 50, 50)
        elif item_type == "speed_boost":
            self.color = CYAN
        elif item_type == "power_sword":
            self.color = ORANGE

    def draw(self, screen, cam_x, cam_y):
        sx = self.x * TILE_SIZE - cam_x + TILE_SIZE // 4
        sy = self.y * TILE_SIZE - cam_y + TILE_SIZE // 4
        pygame.draw.rect(screen, self.color, (sx, sy, TILE_SIZE // 2, TILE_SIZE // 2))


# --- Player ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 20
        self.max_health = 20
        self.facing = "right"
        self.attack_cooldown = 0
        self.attack_timer = 0
        self.damage = 2
        self.inventory = []
        self.max_inventory = 5
        self.speed_boost_timer = 0
        self.damage_boost_timer = 0
        self.move_delay = 0
        self.hit_flash = 0

    def move(self, dx, dy, tile_map):
        if self.move_delay > 0:
            return False
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            tile = tile_map[new_y][new_x]
            if tile != WALL:
                self.x = new_x
                self.y = new_y
                # Update facing
                if dx > 0:
                    self.facing = "right"
                elif dx < 0:
                    self.facing = "left"
                elif dy > 0:
                    self.facing = "down"
                elif dy < 0:
                    self.facing = "up"
                self.move_delay = 4 if self.speed_boost_timer <= 0 else 2
                return True
        return False

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 12
            self.attack_timer = 6
            return True
        return False

    def get_attack_tile(self):
        if self.facing == "right":
            return self.x + 1, self.y
        elif self.facing == "left":
            return self.x - 1, self.y
        elif self.facing == "down":
            return self.x, self.y + 1
        elif self.facing == "up":
            return self.x, self.y - 1
        return self.x, self.y

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.move_delay > 0:
            self.move_delay -= 1
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
        if self.damage_boost_timer > 0:
            self.damage_boost_timer -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def get_damage(self):
        base = self.damage
        if self.damage_boost_timer > 0:
            base *= 2
        return base

    def draw(self, screen, cam_x, cam_y):
        px = self.x * TILE_SIZE - cam_x
        py = self.y * TILE_SIZE - cam_y
        color = GREEN if self.hit_flash <= 0 else WHITE
        # Body
        pygame.draw.rect(screen, color, (px + 4, py + 4, TILE_SIZE - 8, TILE_SIZE - 8))
        # Eyes
        eye_color = (0, 50, 0)
        if self.facing == "right":
            pygame.draw.rect(screen, eye_color, (px + 20, py + 8, 4, 4))
            pygame.draw.rect(screen, eye_color, (px + 20, py + 18, 4, 4))
        elif self.facing == "left":
            pygame.draw.rect(screen, eye_color, (px + 8, py + 8, 4, 4))
            pygame.draw.rect(screen, eye_color, (px + 8, py + 18, 4, 4))
        elif self.facing == "down":
            pygame.draw.rect(screen, eye_color, (px + 8, py + 20, 4, 4))
            pygame.draw.rect(screen, eye_color, (px + 18, py + 20, 4, 4))
        else:
            pygame.draw.rect(screen, eye_color, (px + 8, py + 8, 4, 4))
            pygame.draw.rect(screen, eye_color, (px + 18, py + 8, 4, 4))
        # Attack animation
        if self.attack_timer > 0:
            ax, ay = self.get_attack_tile()
            apx = ax * TILE_SIZE - cam_x
            apy = ay * TILE_SIZE - cam_y
            pygame.draw.rect(screen, YELLOW, (apx + 6, apy + 6, TILE_SIZE - 12, TILE_SIZE - 12), 2)
        # Boost indicators
        if self.speed_boost_timer > 0:
            pygame.draw.circle(screen, CYAN, (px + TILE_SIZE // 2, py - 4), 3)
        if self.damage_boost_timer > 0:
            pygame.draw.circle(screen, ORANGE, (px + TILE_SIZE // 2 + 8, py - 4), 3)


# --- Enemy Base ---
class Enemy:
    def __init__(self, x, y, enemy_type, health_mult=1.0, speed_mult=1.0):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.move_timer = 0
        self.hit_flash = 0
        self.death_timer = -1
        self.alive = True

        if enemy_type == "zombie":
            self.health = int(4 * health_mult)
            self.max_health = self.health
            self.damage = 2
            self.color = (0, 180, 0)
            self.move_speed = max(4, int(15 / speed_mult))
        elif enemy_type == "skeleton":
            self.health = int(3 * health_mult)
            self.max_health = self.health
            self.damage = 3
            self.color = (220, 220, 220)
            self.move_speed = max(3, int(10 / speed_mult))
        elif enemy_type == "creeper":
            self.health = int(5 * health_mult)
            self.max_health = self.health
            self.damage = 5
            self.color = MAGENTA
            self.move_speed = max(5, int(14 / speed_mult))
            self.fuse_timer = 0
            self.fuse_max = 90  # 3 seconds at 30fps
            self.armed = False

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 6
        if self.health <= 0:
            self.death_timer = 10
            self.alive = False

    def distance_to(self, tx, ty):
        return abs(self.x - tx) + abs(self.y - ty)

    def move_toward(self, tx, ty, tile_map):
        if self.move_timer > 0:
            self.move_timer -= 1
            return
        self.move_timer = self.move_speed
        dx = 0
        dy = 0
        if abs(tx - self.x) > abs(ty - self.y):
            dx = 1 if tx > self.x else -1
        else:
            dy = 1 if ty > self.y else -1
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            if tile_map[new_y][new_x] == FLOOR or tile_map[new_y][new_x] == DOOR:
                self.x = new_x
                self.y = new_y

    def wander(self, tile_map):
        if self.move_timer > 0:
            self.move_timer -= 1
            return
        self.move_timer = self.move_speed
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            if tile_map[new_y][new_x] == FLOOR:
                self.x = new_x
                self.y = new_y

    def update(self, player_x, player_y, tile_map):
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        if self.enemy_type == "zombie":
            dist = self.distance_to(player_x, player_y)
            if dist < 8:
                self.move_toward(player_x, player_y, tile_map)
            else:
                self.wander(tile_map)
        elif self.enemy_type == "skeleton":
            self.move_toward(player_x, player_y, tile_map)
        elif self.enemy_type == "creeper":
            dist = self.distance_to(player_x, player_y)
            if dist <= 3 and not self.armed:
                self.armed = True
                self.fuse_timer = 0
            if self.armed:
                self.fuse_timer += 1
                if self.fuse_timer >= self.fuse_max:
                    # Explode
                    self.alive = False
                    self.death_timer = 10
                    return
            if dist > 1:
                self.move_toward(player_x, player_y, tile_map)

    def draw(self, screen, cam_x, cam_y):
        if self.death_timer == 0:
            return
        px = self.x * TILE_SIZE - cam_x
        py = self.y * TILE_SIZE - cam_y

        color = self.color
        if self.hit_flash > 0:
            color = WHITE
        if not self.alive:
            # Death fade
            color = (color[0] // 2, color[1] // 2, color[2] // 2)

        # Creeper flash when armed
        if self.enemy_type == "creeper" and self.armed and self.alive:
            flash_speed = max(2, 10 - (self.fuse_timer // 10))
            if self.fuse_timer % flash_speed < flash_speed // 2:
                color = WHITE

        pygame.draw.rect(screen, color, (px + 4, py + 4, TILE_SIZE - 8, TILE_SIZE - 8))

        # Enemy-specific details
        if self.enemy_type == "zombie":
            pygame.draw.rect(screen, (0, 80, 0), (px + 10, py + 10, 4, 4))
            pygame.draw.rect(screen, (0, 80, 0), (px + 18, py + 10, 4, 4))
        elif self.enemy_type == "skeleton":
            pygame.draw.rect(screen, BLACK, (px + 10, py + 10, 4, 4))
            pygame.draw.rect(screen, BLACK, (px + 18, py + 10, 4, 4))
            pygame.draw.line(screen, BLACK, (px + 10, py + 20), (px + 22, py + 20), 1)
        elif self.enemy_type == "creeper":
            pygame.draw.rect(screen, (80, 0, 80), (px + 10, py + 10, 4, 4))
            pygame.draw.rect(screen, (80, 0, 80), (px + 18, py + 10, 4, 4))
            pygame.draw.rect(screen, (80, 0, 80), (px + 11, py + 18, 10, 4))


# --- Boss ---
class Boss:
    def __init__(self, x, y, health_mult=1.0, speed_mult=1.0):
        self.x = x
        self.y = y
        self.health = int(50 * health_mult)
        self.max_health = self.health
        self.phase = "chase"  # chase, charge, summon, rest
        self.phase_timer = 0
        self.move_timer = 0
        self.move_speed = max(4, int(8 / speed_mult))
        self.hit_flash = 0
        self.alive = True
        self.death_timer = -1
        self.charge_dx = 0
        self.charge_dy = 0
        self.summon_done = False
        self.damage = 4
        self.color = PURPLE

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 6
        if self.health <= 0:
            self.alive = False
            self.death_timer = 30

    def occupies(self, tx, ty):
        return (self.x <= tx <= self.x + 1) and (self.y <= ty <= self.y + 1)

    def distance_to(self, tx, ty):
        cx = self.x + 0.5
        cy = self.y + 0.5
        return abs(cx - tx) + abs(cy - ty)

    def move_toward(self, tx, ty, tile_map):
        if self.move_timer > 0:
            self.move_timer -= 1
            return
        self.move_timer = self.move_speed
        dx = 0
        dy = 0
        if abs(tx - self.x) > abs(ty - self.y):
            dx = 1 if tx > self.x else -1
        else:
            dy = 1 if ty > self.y else -1
        new_x = self.x + dx
        new_y = self.y + dy
        # Check all 4 tiles the boss would occupy
        can_move = True
        for bx in range(new_x, new_x + 2):
            for by in range(new_y, new_y + 2):
                if not (0 <= by < len(tile_map) and 0 <= bx < len(tile_map[0])):
                    can_move = False
                elif tile_map[by][bx] == WALL:
                    can_move = False
        if can_move:
            self.x = new_x
            self.y = new_y

    def update(self, player_x, player_y, tile_map, enemies):
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return []

        self.phase_timer += 1
        new_enemies = []

        if self.phase == "chase":
            self.move_toward(player_x, player_y, tile_map)
            if self.phase_timer > 90:
                self.phase = "charge"
                self.phase_timer = 0
                # Aim charge at player
                dx = player_x - self.x
                dy = player_y - self.y
                if abs(dx) > abs(dy):
                    self.charge_dx = 1 if dx > 0 else -1
                    self.charge_dy = 0
                else:
                    self.charge_dx = 0
                    self.charge_dy = 1 if dy > 0 else -1

        elif self.phase == "charge":
            # Move fast in charge direction
            if self.phase_timer % 2 == 0:
                new_x = self.x + self.charge_dx
                new_y = self.y + self.charge_dy
                can_move = True
                for bx in range(new_x, new_x + 2):
                    for by in range(new_y, new_y + 2):
                        if not (0 <= by < len(tile_map) and 0 <= bx < len(tile_map[0])):
                            can_move = False
                        elif tile_map[by][bx] == WALL:
                            can_move = False
                if can_move:
                    self.x = new_x
                    self.y = new_y
                else:
                    self.phase = "summon"
                    self.phase_timer = 0
                    self.summon_done = False
            if self.phase_timer > 30:
                self.phase = "summon"
                self.phase_timer = 0
                self.summon_done = False

        elif self.phase == "summon":
            if not self.summon_done and self.phase_timer > 15:
                self.summon_done = True
                # Spawn 1-2 zombies near the boss
                for _ in range(random.randint(1, 2)):
                    sx = self.x + random.randint(-3, 3)
                    sy = self.y + random.randint(-3, 3)
                    if (0 <= sy < len(tile_map) and 0 <= sx < len(tile_map[0])
                            and tile_map[sy][sx] == FLOOR):
                        new_enemies.append(Enemy(sx, sy, "zombie"))
            if self.phase_timer > 45:
                self.phase = "rest"
                self.phase_timer = 0

        elif self.phase == "rest":
            if self.phase_timer > 45:
                self.phase = "chase"
                self.phase_timer = 0

        return new_enemies

    def draw(self, screen, cam_x, cam_y):
        if self.death_timer == 0:
            return
        px = self.x * TILE_SIZE - cam_x
        py = self.y * TILE_SIZE - cam_y
        size = TILE_SIZE * 2

        color = self.color
        if self.hit_flash > 0:
            color = WHITE
        if not self.alive:
            color = (color[0] // 2, color[1] // 2, color[2] // 2)

        pygame.draw.rect(screen, color, (px + 4, py + 4, size - 8, size - 8))
        # Eyes
        pygame.draw.rect(screen, RED, (px + 16, py + 16, 8, 8))
        pygame.draw.rect(screen, RED, (px + 40, py + 16, 8, 8))
        # Mouth
        pygame.draw.rect(screen, RED, (px + 16, py + 38, 32, 6))

        # Health bar above boss
        bar_width = size - 8
        bar_x = px + 4
        bar_y = py - 12
        ratio = max(0, self.health / self.max_health)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, 8))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * ratio), 8))


# --- Main Game ---
class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robert's Dungeons")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)
        self.title_font = pygame.font.Font(None, 72)

        # Sounds (silent fallback)
        self.snd_hit = load_sound("hit.wav")
        self.snd_pickup = load_sound("pickup.wav")
        self.snd_explode = load_sound("explode.wav")

        # Game state
        self.state = "menu"  # menu, playing, paused, game_over
        self.seed = random.randint(0, 999999)
        self.level = 1
        self.total_kills = 0
        self.high_scores = self.load_high_scores()

        # Screen shake
        self.shake_frames = 0

        # Level transition text
        self.level_text_timer = 0

        # Particles
        self.particles = []

        # Initialize first level
        self.setup_level()

    def load_high_scores(self):
        try:
            with open("highscores.txt", "r") as f:
                scores = [int(line.strip()) for line in f.readlines() if line.strip()]
                return sorted(scores, reverse=True)[:5]
        except (FileNotFoundError, ValueError):
            return []

    def save_high_scores(self):
        self.high_scores.append(self.total_kills)
        self.high_scores = sorted(self.high_scores, reverse=True)[:5]
        try:
            with open("highscores.txt", "w") as f:
                for score in self.high_scores:
                    f.write(str(score) + "\n")
        except Exception:
            pass

    def setup_level(self):
        health_mult = 1.0 + (self.level - 1) * 0.5
        speed_mult = 1.0 + (self.level - 1) * 0.3

        self.tile_map, self.rooms = generate_map(MAP_WIDTH, MAP_HEIGHT,
                                                  seed=self.seed + self.level)
        # Place player in first room
        start_room = self.rooms[0]
        self.player = Player(start_room[0] + start_room[2] // 2,
                             start_room[1] + start_room[3] // 2)

        # Place enemies
        self.enemies = []
        for i, room in enumerate(self.rooms[1:-1], 1):
            cx = room[0] + room[2] // 2
            cy = room[1] + room[3] // 2
            if i % 3 == 0:
                self.enemies.append(Enemy(cx, cy, "skeleton", health_mult, speed_mult))
            else:
                self.enemies.append(Enemy(cx, cy, "zombie", health_mult, speed_mult))
            # Extra enemy in some rooms
            if random.random() < 0.4:
                ex = room[0] + random.randint(1, room[2] - 2)
                ey = room[1] + random.randint(1, room[3] - 2)
                self.enemies.append(Enemy(ex, ey, "zombie", health_mult, speed_mult))

        # Creepers only on level 2+
        if self.level >= 2:
            for room in self.rooms[2:]:
                if random.random() < 0.3:
                    cx = room[0] + random.randint(1, room[2] - 2)
                    cy = room[1] + random.randint(1, room[3] - 2)
                    self.enemies.append(Enemy(cx, cy, "creeper", health_mult, speed_mult))

        # Place boss in last room
        last_room = self.rooms[-1]
        bx = last_room[0] + last_room[2] // 2 - 1
        by = last_room[1] + last_room[3] // 2 - 1
        self.boss = Boss(bx, by, health_mult, speed_mult)

        # Items on ground
        self.items = []

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Stairs not placed yet
        self.stairs_placed = False

        # Level text
        self.level_text_timer = 90

    def next_level(self):
        """Advance to next level, keeping player kills and inventory."""
        old_kills = self.total_kills
        old_inventory = self.player.inventory[:]
        old_health = self.player.health
        old_max_health = self.player.max_health

        self.level += 1
        self.setup_level()

        self.total_kills = old_kills
        self.player.inventory = old_inventory[:self.player.max_inventory]
        self.player.health = old_health
        self.player.max_health = old_max_health
        self.particles = []

    def spawn_particles(self, x, y, color, count=10):
        px = x * TILE_SIZE + TILE_SIZE // 2
        py = y * TILE_SIZE + TILE_SIZE // 2
        for _ in range(count):
            self.particles.append(Particle(px, py, color))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.state = "playing"
                        self.level = 1
                        self.total_kills = 0
                        self.seed = random.randint(0, 999999)
                        self.setup_level()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

                elif self.state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "paused"
                    elif event.key == pygame.K_SPACE:
                        self.player.attack()
                    # Use items 1-5
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3,
                                       pygame.K_4, pygame.K_5]:
                        slot = event.key - pygame.K_1
                        if slot < len(self.player.inventory):
                            item_type = self.player.inventory.pop(slot)
                            if item_type == "health_potion":
                                self.player.health = min(
                                    self.player.health + 5, self.player.max_health)
                            elif item_type == "speed_boost":
                                self.player.speed_boost_timer = 150
                            elif item_type == "power_sword":
                                self.player.damage_boost_timer = 150

                elif self.state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "playing"

                elif self.state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.state = "menu"

        # Held-key movement (playing state only)
        if self.state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move(0, -1, self.tile_map)
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.move(0, 1, self.tile_map)
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-1, 0, self.tile_map)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(1, 0, self.tile_map)

    def update(self):
        if self.state != "playing":
            return

        self.player.update()

        # Check stairs
        if self.stairs_placed:
            if self.tile_map[self.player.y][self.player.x] == STAIRS:
                self.next_level()
                return

        # Check chests
        if self.tile_map[self.player.y][self.player.x] == CHEST:
            self.tile_map[self.player.y][self.player.x] = FLOOR
            item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
            self.items.append(Item(self.player.x, self.player.y, item_type))
            play_sound(self.snd_pickup)

        # Pick up items
        for item in self.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                if len(self.player.inventory) < self.player.max_inventory:
                    self.player.inventory.append(item.item_type)
                    self.items.remove(item)
                    play_sound(self.snd_pickup)

        # Player attack hits
        if self.player.attack_timer > 0:
            ax, ay = self.player.get_attack_tile()
            dmg = self.player.get_damage()
            for enemy in self.enemies:
                if enemy.alive and enemy.x == ax and enemy.y == ay:
                    enemy.take_damage(dmg)
                    play_sound(self.snd_hit)
            if self.boss and self.boss.alive and self.boss.occupies(ax, ay):
                self.boss.take_damage(dmg)
                play_sound(self.snd_hit)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y, self.tile_map)

            # Enemy touches player = damage
            if enemy.alive and enemy.x == self.player.x and enemy.y == self.player.y:
                self.player.health -= enemy.damage
                self.player.hit_flash = 8
                self.shake_frames = 10
                enemy.x -= (self.player.x - enemy.x) if enemy.x != self.player.x else 0

            # Creeper explosion
            if (enemy.enemy_type == "creeper" and not enemy.alive
                    and enemy.death_timer == 10):
                if enemy.distance_to(self.player.x, self.player.y) <= 3:
                    if hasattr(enemy, 'armed') and enemy.armed:
                        self.player.health -= enemy.damage
                        self.player.hit_flash = 8
                        self.shake_frames = 15
                        play_sound(self.snd_explode)
                self.spawn_particles(enemy.x, enemy.y, MAGENTA, 20)

            # Enemy death
            if not enemy.alive and enemy.death_timer <= 0:
                self.spawn_particles(enemy.x, enemy.y, enemy.color)
                self.total_kills += 1
                # Drop loot
                if random.random() < 0.4:
                    item_type = random.choice(
                        ["health_potion", "speed_boost", "power_sword"])
                    self.items.append(Item(enemy.x, enemy.y, item_type))
                self.enemies.remove(enemy)

        # Update boss
        if self.boss and self.boss.alive:
            new_enemies = self.boss.update(self.player.x, self.player.y,
                                           self.tile_map, self.enemies)
            self.enemies.extend(new_enemies)
            # Boss touches player
            if self.boss.occupies(self.player.x, self.player.y):
                self.player.health -= self.boss.damage
                self.player.hit_flash = 8
                self.shake_frames = 10
        elif self.boss and not self.boss.alive:
            if self.boss.death_timer > 0:
                self.boss.death_timer -= 1
            elif self.boss.death_timer == 0:
                self.spawn_particles(self.boss.x, self.boss.y, PURPLE, 25)
                self.spawn_particles(self.boss.x + 1, self.boss.y + 1, PURPLE, 25)
                self.total_kills += 5
                # Place stairs where boss was
                stair_x = self.boss.x + 1
                stair_y = self.boss.y + 1
                if (0 <= stair_y < MAP_HEIGHT and 0 <= stair_x < MAP_WIDTH):
                    self.tile_map[stair_y][stair_x] = STAIRS
                    self.stairs_placed = True
                self.boss = None

        # Update particles
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

        # Update camera
        self.camera_x = (self.player.x * TILE_SIZE - SCREEN_WIDTH // 2
                         + TILE_SIZE // 2)
        self.camera_y = (self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2
                         + TILE_SIZE // 2)

        # Level text timer
        if self.level_text_timer > 0:
            self.level_text_timer -= 1

        # Shake
        if self.shake_frames > 0:
            self.shake_frames -= 1

        # Player death
        if self.player.health <= 0:
            self.save_high_scores()
            self.state = "game_over"

    def draw_tiles(self, offset_x, offset_y):
        cam_x = self.camera_x + offset_x
        cam_y = self.camera_y + offset_y

        start_col = max(0, int(cam_x // TILE_SIZE))
        end_col = min(MAP_WIDTH, int((cam_x + SCREEN_WIDTH) // TILE_SIZE) + 2)
        start_row = max(0, int(cam_y // TILE_SIZE))
        end_row = min(MAP_HEIGHT, int((cam_y + SCREEN_HEIGHT) // TILE_SIZE) + 2)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                sx = col * TILE_SIZE - cam_x
                sy = row * TILE_SIZE - cam_y
                tile = self.tile_map[row][col]

                if tile == WALL:
                    pygame.draw.rect(self.screen, BROWN, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (80, 50, 15),
                                     (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                elif tile == FLOOR:
                    pygame.draw.rect(self.screen, DARK_GRAY,
                                     (sx, sy, TILE_SIZE, TILE_SIZE))
                elif tile == DOOR:
                    pygame.draw.rect(self.screen, (80, 80, 40),
                                     (sx, sy, TILE_SIZE, TILE_SIZE))
                elif tile == CHEST:
                    pygame.draw.rect(self.screen, DARK_GRAY,
                                     (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (180, 130, 20),
                                     (sx + 4, sy + 8, TILE_SIZE - 8, TILE_SIZE - 12))
                    pygame.draw.rect(self.screen, YELLOW,
                                     (sx + 12, sy + 12, 8, 8))
                elif tile == STAIRS:
                    pygame.draw.rect(self.screen, DARK_GRAY,
                                     (sx, sy, TILE_SIZE, TILE_SIZE))
                    # Draw staircase pattern
                    for i in range(4):
                        step_y = sy + 4 + i * 7
                        step_x = sx + 4 + i * 4
                        pygame.draw.rect(self.screen, YELLOW,
                                         (step_x, step_y, TILE_SIZE - 8 - i * 4, 5))

    def draw_game(self):
        self.screen.fill(BLACK)

        # Screen shake offset
        shake_x = 0
        shake_y = 0
        if self.shake_frames > 0:
            shake_x = random.randint(-3, 3)
            shake_y = random.randint(-3, 3)

        cam_x = self.camera_x + shake_x
        cam_y = self.camera_y + shake_y

        # Draw tiles
        self.draw_tiles(shake_x, shake_y)

        # Draw items
        for item in self.items:
            item.draw(self.screen, cam_x, cam_y)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, cam_x, cam_y)

        # Draw boss
        if self.boss:
            self.boss.draw(self.screen, cam_x, cam_y)

        # Draw player
        self.player.draw(self.screen, cam_x, cam_y)

        # Draw particles
        for p in self.particles:
            p.draw(self.screen, cam_x, cam_y)

        # --- HUD ---
        # Health bar
        bar_x = 10
        bar_y = 10
        bar_w = 150
        bar_h = 16
        ratio = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)
        hp_text = self.font.render(
            f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + bar_w + 8, bar_y - 2))

        # Kill count and level
        kill_text = self.font.render(
            f"Kills: {self.total_kills}  Level: {self.level}", True, WHITE)
        self.screen.blit(kill_text, (10, 34))

        # Inventory
        for i, item_type in enumerate(self.player.inventory):
            color = {"health_potion": (255, 50, 50), "speed_boost": CYAN,
                     "power_sword": ORANGE}.get(item_type, GRAY)
            ix = 10 + i * 50
            iy = SCREEN_HEIGHT - 50
            pygame.draw.rect(self.screen, color, (ix, iy, 32, 32))
            pygame.draw.rect(self.screen, WHITE, (ix, iy, 32, 32), 1)
            label = self.font.render(str(i + 1), True, WHITE)
            self.screen.blit(label, (ix + 12, iy - 18))

        # Minimap
        mm_x = SCREEN_WIDTH - 110
        mm_y = 10
        mm_scale = 2
        pygame.draw.rect(self.screen, (20, 20, 20),
                         (mm_x - 2, mm_y - 2,
                          MAP_WIDTH * mm_scale + 4, MAP_HEIGHT * mm_scale + 4))
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                if self.tile_map[row][col] != WALL:
                    pygame.draw.rect(self.screen, (60, 60, 60),
                                     (mm_x + col * mm_scale, mm_y + row * mm_scale,
                                      mm_scale, mm_scale))
        # Player on minimap
        pygame.draw.rect(self.screen, GREEN,
                         (mm_x + self.player.x * mm_scale,
                          mm_y + self.player.y * mm_scale,
                          mm_scale + 1, mm_scale + 1))
        # Boss on minimap
        if self.boss and self.boss.alive:
            pygame.draw.rect(self.screen, RED,
                             (mm_x + self.boss.x * mm_scale,
                              mm_y + self.boss.y * mm_scale,
                              mm_scale * 2, mm_scale * 2))

        # Level transition text
        if self.level_text_timer > 0:
            alpha = min(255, self.level_text_timer * 6)
            level_surf = self.big_font.render(
                f"LEVEL {self.level}", True, YELLOW)
            rect = level_surf.get_rect(center=(SCREEN_WIDTH // 2,
                                               SCREEN_HEIGHT // 3))
            self.screen.blit(level_surf, rect)

    def draw_menu(self):
        self.screen.fill(BLACK)

        # Title
        title = self.title_font.render("ROBERT'S DUNGEONS", True, YELLOW)
        rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, rect)

        # Subtitle
        sub = self.font.render("A Dungeon Crawler Adventure", True, GRAY)
        rect = sub.get_rect(center=(SCREEN_WIDTH // 2, 210))
        self.screen.blit(sub, rect)

        # Start prompt
        prompt = self.big_font.render("Press SPACE to start", True, WHITE)
        rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 320))
        self.screen.blit(prompt, rect)

        # Controls
        controls = self.font.render(
            "Arrows/WASD: Move   Space: Attack   1-5: Use Items", True, GRAY)
        rect = controls.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(controls, rect)

        # High scores
        if self.high_scores:
            hs_title = self.font.render("HIGH SCORES", True, ORANGE)
            rect = hs_title.get_rect(center=(SCREEN_WIDTH // 2, 440))
            self.screen.blit(hs_title, rect)
            for i, score in enumerate(self.high_scores[:5]):
                score_text = self.font.render(
                    f"{i + 1}. {score} kills", True, WHITE)
                rect = score_text.get_rect(
                    center=(SCREEN_WIDTH // 2, 470 + i * 25))
                self.screen.blit(score_text, rect)

    def draw_pause(self):
        # Draw game behind
        self.draw_game()
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        # Pause text
        pause_text = self.big_font.render("PAUSED", True, WHITE)
        rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2,
                                           SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(pause_text, rect)
        resume_text = self.font.render("Press Escape to resume", True, GRAY)
        rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2,
                                            SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(resume_text, rect)

    def draw_game_over(self):
        self.screen.fill(BLACK)
        title = self.big_font.render("GAME OVER", True, RED)
        rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, rect)

        score = self.font.render(
            f"Total Kills: {self.total_kills}  Level Reached: {self.level}",
            True, WHITE)
        rect = score.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score, rect)

        # Check if it's a high score
        if (len(self.high_scores) < 5
                or self.total_kills > min(self.high_scores)):
            new_hs = self.font.render("NEW HIGH SCORE!", True, YELLOW)
            rect = new_hs.get_rect(center=(SCREEN_WIDTH // 2, 320))
            self.screen.blit(new_hs, rect)

        prompt = self.font.render("Press SPACE for menu", True, GRAY)
        rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(prompt, rect)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "paused":
            self.draw_pause()
        elif self.state == "game_over":
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
