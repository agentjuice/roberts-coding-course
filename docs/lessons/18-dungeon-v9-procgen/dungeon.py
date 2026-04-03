import pygame
import sys
import random
import time

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Tile types
FLOOR = 0
WALL = 1
DOOR = 2
CHEST = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
DARK_GRAY = (50, 50, 50)
BROWN = (100, 60, 20)
ORANGE = (255, 165, 0)
PURPLE = (150, 0, 200)
DARK_RED = (150, 0, 0)
GOLD = (255, 215, 0)


# ============================================================
# SPRITE CREATION FUNCTIONS
# ============================================================

def create_player_sprite(facing_right=True):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 100, 220), (8, 14, 16, 12))
    pygame.draw.circle(surf, (240, 200, 160), (16, 10), 7)
    eye_x = 18 if facing_right else 12
    pygame.draw.circle(surf, BLACK, (eye_x, 9), 2)
    pygame.draw.rect(surf, (120, 120, 140), (9, 3, 14, 5))
    pygame.draw.rect(surf, (60, 60, 80), (10, 26, 5, 5))
    pygame.draw.rect(surf, (60, 60, 80), (17, 26, 5, 5))
    if facing_right:
        pygame.draw.rect(surf, (200, 200, 220), (26, 8, 3, 14))
        pygame.draw.rect(surf, (180, 160, 60), (24, 18, 7, 3))
    else:
        pygame.draw.rect(surf, (200, 200, 220), (3, 8, 3, 14))
        pygame.draw.rect(surf, (180, 160, 60), (1, 18, 7, 3))
    return surf


def create_enemy_sprite(enemy_type):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    if enemy_type == "zombie":
        pygame.draw.rect(surf, (60, 140, 50), (8, 12, 16, 14))
        pygame.draw.circle(surf, (80, 160, 60), (16, 9), 7)
        pygame.draw.circle(surf, RED, (13, 8), 2)
        pygame.draw.circle(surf, RED, (19, 8), 2)
        pygame.draw.rect(surf, (60, 140, 50), (2, 14, 6, 4))
        pygame.draw.rect(surf, (60, 140, 50), (24, 14, 6, 4))
        pygame.draw.rect(surf, (50, 100, 40), (10, 26, 5, 5))
        pygame.draw.rect(surf, (50, 100, 40), (17, 26, 5, 5))
    else:
        pygame.draw.circle(surf, WHITE, (16, 9), 7)
        pygame.draw.circle(surf, BLACK, (13, 8), 2)
        pygame.draw.circle(surf, BLACK, (19, 8), 2)
        pygame.draw.rect(surf, BLACK, (13, 12, 6, 2))
        pygame.draw.rect(surf, (200, 200, 200), (11, 16, 10, 2))
        pygame.draw.rect(surf, (200, 200, 200), (11, 20, 10, 2))
        pygame.draw.rect(surf, (200, 200, 200), (11, 24, 10, 2))
        pygame.draw.rect(surf, WHITE, (15, 16, 2, 12))
        pygame.draw.rect(surf, WHITE, (11, 28, 3, 3))
        pygame.draw.rect(surf, WHITE, (18, 28, 3, 3))
    return surf


def create_boss_sprite():
    size = TILE_SIZE * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (160, 30, 30), (12, 24, 40, 30))
    pygame.draw.circle(surf, (180, 40, 40), (32, 18), 14)
    pygame.draw.polygon(surf, (80, 20, 20), [(20, 10), (24, 0), (28, 10)])
    pygame.draw.polygon(surf, (80, 20, 20), [(36, 10), (40, 0), (44, 10)])
    pygame.draw.circle(surf, YELLOW, (27, 16), 4)
    pygame.draw.circle(surf, YELLOW, (37, 16), 4)
    pygame.draw.circle(surf, BLACK, (27, 16), 2)
    pygame.draw.circle(surf, BLACK, (37, 16), 2)
    pygame.draw.rect(surf, BLACK, (26, 24, 12, 4))
    pygame.draw.rect(surf, WHITE, (28, 24, 3, 3))
    pygame.draw.rect(surf, WHITE, (33, 24, 3, 3))
    pygame.draw.rect(surf, (160, 30, 30), (2, 28, 10, 8))
    pygame.draw.rect(surf, (160, 30, 30), (52, 28, 10, 8))
    pygame.draw.rect(surf, (120, 20, 20), (16, 54, 10, 8))
    pygame.draw.rect(surf, (120, 20, 20), (38, 54, 10, 8))
    return surf


def create_tile_sprites():
    sprites = {}
    floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
    floor.fill((55, 55, 60))
    pygame.draw.line(floor, (65, 65, 70), (0, 0), (TILE_SIZE, 0), 1)
    pygame.draw.line(floor, (65, 65, 70), (0, 0), (0, TILE_SIZE), 1)
    for _ in range(4):
        x = random.randint(4, TILE_SIZE - 4)
        y = random.randint(4, TILE_SIZE - 4)
        pygame.draw.circle(floor, (45, 45, 50), (x, y), 1)
    sprites[FLOOR] = floor

    wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall.fill((110, 65, 25))
    pygame.draw.line(wall, (80, 50, 20), (0, 8), (TILE_SIZE, 8), 1)
    pygame.draw.line(wall, (80, 50, 20), (0, 16), (TILE_SIZE, 16), 1)
    pygame.draw.line(wall, (80, 50, 20), (0, 24), (TILE_SIZE, 24), 1)
    pygame.draw.line(wall, (80, 50, 20), (16, 0), (16, 8), 1)
    pygame.draw.line(wall, (80, 50, 20), (8, 8), (8, 16), 1)
    pygame.draw.line(wall, (80, 50, 20), (24, 8), (24, 16), 1)
    pygame.draw.line(wall, (80, 50, 20), (16, 16), (16, 24), 1)
    pygame.draw.line(wall, (80, 50, 20), (8, 24), (8, 32), 1)
    pygame.draw.line(wall, (80, 50, 20), (24, 24), (24, 32), 1)
    pygame.draw.line(wall, (70, 40, 15), (0, 0), (TILE_SIZE, 0), 2)
    sprites[WALL] = wall

    door = pygame.Surface((TILE_SIZE, TILE_SIZE))
    door.fill((80, 50, 30))
    pygame.draw.rect(door, (60, 35, 15), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4), 2)
    pygame.draw.line(door, (60, 35, 15), (16, 2), (16, 30), 1)
    pygame.draw.circle(door, GOLD, (22, 16), 3)
    sprites[DOOR] = door

    chest = pygame.Surface((TILE_SIZE, TILE_SIZE))
    chest.fill((55, 55, 60))
    pygame.draw.rect(chest, (139, 90, 43), (4, 10, 24, 16))
    pygame.draw.rect(chest, (160, 110, 50), (4, 6, 24, 6))
    pygame.draw.circle(chest, GOLD, (16, 18), 3)
    pygame.draw.rect(chest, GOLD, (15, 18, 2, 4))
    pygame.draw.rect(chest, (100, 70, 30), (4, 12, 24, 2))
    sprites[CHEST] = chest

    return sprites


def create_item_sprites():
    sprites = {}
    hp = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(hp, (200, 30, 30), (10, 12, 12, 14), border_radius=3)
    pygame.draw.rect(hp, (180, 180, 180), (13, 6, 6, 8))
    pygame.draw.rect(hp, (220, 60, 60), (12, 16, 8, 6))
    sprites["health_potion"] = hp

    sp = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.polygon(sp, (50, 150, 255), [
        (18, 4), (10, 16), (15, 16), (12, 28), (22, 14), (17, 14)
    ])
    sprites["speed_boost"] = sp

    sw = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(sw, (220, 200, 60), (14, 2, 4, 18))
    pygame.draw.rect(sw, (160, 120, 40), (8, 20, 16, 3))
    pygame.draw.rect(sw, (120, 80, 30), (14, 23, 4, 6))
    sprites["power_sword"] = sw

    return sprites


def try_load_sprite(filename, fallback_surface):
    try:
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, (fallback_surface.get_width(), fallback_surface.get_height()))
        return img
    except (pygame.error, FileNotFoundError):
        return fallback_surface


# ============================================================
# SOUND MANAGER
# ============================================================

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = None
        self.volume = 0.7
        self.enabled = True

        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return

        sound_files = {
            "sword_swing": "assets/sword_swing.wav",
            "enemy_hit": "assets/enemy_hit.wav",
            "enemy_death": "assets/enemy_death.wav",
            "item_pickup": "assets/item_pickup.wav",
            "chest_open": "assets/chest_open.wav",
            "player_hurt": "assets/player_hurt.wav",
            "door_open": "assets/door_open.wav",
        }
        for name, filepath in sound_files.items():
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
            except (pygame.error, FileNotFoundError):
                self.sounds[name] = None

        self.music_files = {
            "dungeon": "assets/dungeon_music.wav",
            "boss": "assets/boss_music.wav",
        }

    def play(self, sound_name):
        if not self.enabled:
            return
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()

    def play_music(self, track_name):
        if not self.enabled or self.music_playing == track_name:
            return
        filepath = self.music_files.get(track_name)
        if filepath:
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.volume * 0.5)
                pygame.mixer.music.play(-1)
                self.music_playing = track_name
            except (pygame.error, FileNotFoundError):
                self.music_playing = None

    def stop_music(self):
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
            self.music_playing = None

    def set_volume(self, vol):
        self.volume = max(0.0, min(1.0, vol))
        if not self.enabled:
            return
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.volume)
        try:
            pygame.mixer.music.set_volume(self.volume * 0.5)
        except pygame.error:
            pass

    def volume_up(self):
        self.set_volume(self.volume + 0.1)

    def volume_down(self):
        self.set_volume(self.volume - 0.1)


# ============================================================
# PROCEDURAL DUNGEON GENERATION
# ============================================================

class DungeonRoom:
    """Represents a rectangular room within the larger dungeon grid."""
    def __init__(self, x, y, w, h):
        self.x = x       # left column
        self.y = y        # top row
        self.w = w        # width in tiles
        self.h = h        # height in tiles
        self.center_x = x + w // 2
        self.center_y = y + h // 2

    def intersects(self, other, padding=1):
        """Check if this room overlaps another (with padding)."""
        return (self.x - padding < other.x + other.w and
                self.x + self.w + padding > other.x and
                self.y - padding < other.y + other.h and
                self.y + self.h + padding > other.y)


def generate_dungeon(seed):
    """Generate a dungeon map, enemy positions, chest positions,
    player start, and boss position from a seed number.

    Returns: (tile_map, enemy_list, chest_positions, player_start, boss_pos, room_rects)
    """
    rng = random.Random(seed)

    # Dungeon grid size
    MAP_W = 60
    MAP_H = 45

    # Start with everything as walls
    tile_map = [[WALL for _ in range(MAP_W)] for _ in range(MAP_H)]

    # --- Place rooms ---
    rooms = []
    max_attempts = 200
    target_rooms = rng.randint(6, 8)

    for _ in range(max_attempts):
        if len(rooms) >= target_rooms:
            break
        # Random room size and position
        w = rng.randint(5, 10)
        h = rng.randint(5, 8)
        x = rng.randint(1, MAP_W - w - 1)
        y = rng.randint(1, MAP_H - h - 1)

        new_room = DungeonRoom(x, y, w, h)

        # Check for overlap with existing rooms
        overlaps = False
        for existing in rooms:
            if new_room.intersects(existing, padding=2):
                overlaps = True
                break

        if not overlaps:
            rooms.append(new_room)
            # Carve out the room (set tiles to FLOOR)
            for row in range(y, y + h):
                for col in range(x, x + w):
                    tile_map[row][col] = FLOOR

    # --- Connect rooms with corridors ---
    # Connect each room to the next one in the list
    for i in range(len(rooms) - 1):
        r1 = rooms[i]
        r2 = rooms[i + 1]

        # L-shaped corridor: go horizontal first, then vertical
        cx1 = r1.center_x
        cy1 = r1.center_y
        cx2 = r2.center_x
        cy2 = r2.center_y

        # Horizontal segment
        x_start = min(cx1, cx2)
        x_end = max(cx1, cx2)
        for col in range(x_start, x_end + 1):
            if 0 < cy1 < MAP_H - 1:
                tile_map[cy1][col] = FLOOR
                # Make corridor 2 tiles wide for comfort
                if cy1 + 1 < MAP_H - 1:
                    tile_map[cy1 + 1][col] = FLOOR

        # Vertical segment
        y_start = min(cy1, cy2)
        y_end = max(cy1, cy2)
        for row in range(y_start, y_end + 1):
            if 0 < cx2 < MAP_W - 1:
                tile_map[row][cx2] = FLOOR
                if cx2 + 1 < MAP_W - 1:
                    tile_map[row][cx2 + 1] = FLOOR

    # --- Place doors at corridor-room transitions ---
    # We'll place doors where corridors meet room edges.
    # Keep it simple: place a couple doors per room boundary.
    door_positions = []
    for room in rooms:
        # Check each edge tile of the room
        for col in range(room.x, room.x + room.w):
            # Top edge
            if room.y > 0 and tile_map[room.y - 1][col] == FLOOR:
                # Corridor leads into room from above
                if tile_map[room.y][col] == FLOOR:
                    door_positions.append((col, room.y))
            # Bottom edge
            bot = room.y + room.h - 1
            if bot + 1 < MAP_H and tile_map[bot + 1][col] == FLOOR:
                if tile_map[bot][col] == FLOOR:
                    door_positions.append((col, bot))
        for row in range(room.y, room.y + room.h):
            # Left edge
            if room.x > 0 and tile_map[row][room.x - 1] == FLOOR:
                if tile_map[row][room.x] == FLOOR:
                    door_positions.append((room.x, row))
            # Right edge
            rgt = room.x + room.w - 1
            if rgt + 1 < MAP_W and tile_map[row][rgt + 1] == FLOOR:
                if tile_map[row][rgt] == FLOOR:
                    door_positions.append((rgt, row))

    # Only place a few doors (not too many)
    rng.shuffle(door_positions)
    placed_doors = 0
    for dx, dy in door_positions:
        if placed_doors >= len(rooms) * 2:
            break
        # Make sure it's a reasonable doorway (not in the middle of a room)
        # Count adjacent floor tiles; a door should be in a narrow spot
        adj_walls = 0
        for ddx, ddy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = dx + ddx, dy + ddy
            if 0 <= ny < MAP_H and 0 <= nx < MAP_W:
                if tile_map[ny][nx] == WALL:
                    adj_walls += 1
        if adj_walls >= 2:  # At least 2 walls nearby = narrow passage
            tile_map[dy][dx] = DOOR
            placed_doors += 1

    # --- Place enemies ---
    enemy_list = []
    for i, room in enumerate(rooms):
        if i == 0:
            continue  # No enemies in start room
        if i == len(rooms) - 1:
            continue  # Boss room gets the boss, not regular enemies

        num_enemies = rng.randint(2, 4)
        for _ in range(num_enemies):
            ex = rng.randint(room.x + 1, room.x + room.w - 2)
            ey = rng.randint(room.y + 1, room.y + room.h - 2)
            if tile_map[ey][ex] == FLOOR:
                etype = rng.choice(["zombie", "zombie", "skeleton"])
                enemy_list.append((etype, ex, ey))

    # --- Place chests ---
    chest_positions = []
    chest_rooms = rng.sample(range(1, len(rooms) - 1), min(2, len(rooms) - 2))
    for ri in chest_rooms:
        room = rooms[ri]
        cx = rng.randint(room.x + 1, room.x + room.w - 2)
        cy = rng.randint(room.y + 1, room.y + room.h - 2)
        if tile_map[cy][cx] == FLOOR:
            tile_map[cy][cx] = CHEST
            chest_positions.append((cx, cy))

    # --- Player starts in the first room ---
    player_start = (rooms[0].center_x, rooms[0].center_y)

    # --- Boss goes in the last room ---
    boss_room = rooms[-1]
    boss_pos = (boss_room.center_x - 1, boss_room.center_y - 1)

    return tile_map, enemy_list, chest_positions, player_start, boss_pos, rooms


# ============================================================
# GAME CLASSES
# ============================================================

class Player:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.health = 10
        self.max_health = 10
        self.attack_power = 2
        self.facing = "right"
        self.speed = 1
        self.inventory = []
        self.attack_cooldown = 0
        self.attacking = False
        self.attack_timer = 0
        self.hurt_timer = 0
        self.kills = 0
        self.speed_boost_timer = 0
        self.sprite_right = sprites["player_right"]
        self.sprite_left = sprites["player_left"]

    def move(self, dx, dy, tile_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            tile = tile_map[new_y][new_x]
            if tile != WALL:
                self.x = new_x
                self.y = new_y
        if dx > 0:
            self.facing = "right"
        elif dx < 0:
            self.facing = "left"
        elif dy < 0:
            self.facing = "up"
        elif dy > 0:
            self.facing = "down"

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = 8
            self.attack_cooldown = 20

    def get_attack_tile(self):
        if self.facing == "right":
            return (self.x + 1, self.y)
        elif self.facing == "left":
            return (self.x - 1, self.y)
        elif self.facing == "up":
            return (self.x, self.y - 1)
        elif self.facing == "down":
            return (self.x, self.y + 1)
        return (self.x + 1, self.y)

    def use_item(self, index):
        if 0 <= index < len(self.inventory):
            item_type = self.inventory.pop(index)
            if item_type == "health_potion":
                self.health = min(self.health + 5, self.max_health)
            elif item_type == "speed_boost":
                self.speed_boost_timer = 300
            elif item_type == "power_sword":
                self.attack_power = 4

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attacking = False
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        sprite = self.sprite_left if self.facing == "left" else self.sprite_right

        if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
            flash = sprite.copy()
            flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
            screen.blit(flash, (px, py))
        else:
            screen.blit(sprite, (px, py))

        if self.attacking:
            ax, ay = self.get_attack_tile()
            apx = ax * TILE_SIZE - camera_x
            apy = ay * TILE_SIZE - camera_y
            attack_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.arc(attack_surf, (255, 255, 200, 180), (0, 0, TILE_SIZE, TILE_SIZE), 0, 3.14, 4)
            screen.blit(attack_surf, (apx, apy))


class Enemy:
    def __init__(self, enemy_type, x, y, sprites):
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.health = 4 if enemy_type == "zombie" else 3
        self.max_health = self.health
        self.move_timer = 0
        self.move_delay = 20 if enemy_type == "zombie" else 15
        self.alive = True
        self.hit_flash = 0
        self.death_timer = 0
        self.sprite = sprites.get(enemy_type, sprites.get("zombie"))

    def update(self, player, tile_map):
        if not self.alive:
            self.death_timer -= 1
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            if self.enemy_type == "zombie":
                dx = random.choice([-1, 0, 0, 1])
                dy = random.choice([-1, 0, 0, 1]) if dx == 0 else 0
            else:
                dx, dy = 0, 0
                if abs(player.x - self.x) > abs(player.y - self.y):
                    dx = 1 if player.x > self.x else -1
                else:
                    dy = 1 if player.y > self.y else -1
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
                if tile_map[new_y][new_x] in (FLOOR, DOOR):
                    self.x = new_x
                    self.y = new_y

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 10
        if self.health <= 0:
            self.alive = False
            self.death_timer = 15

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if not self.alive:
            if self.death_timer > 0:
                alpha = int(255 * (self.death_timer / 15))
                death_surf = self.sprite.copy()
                death_surf.set_alpha(alpha)
                screen.blit(death_surf, (px, py))
            return
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            flash = self.sprite.copy()
            flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
            screen.blit(flash, (px, py))
        else:
            screen.blit(self.sprite, (px, py))
        if self.health < self.max_health:
            bar_w = TILE_SIZE - 4
            fill = int(bar_w * self.health / self.max_health)
            pygame.draw.rect(screen, RED, (px + 2, py - 5, bar_w, 3))
            pygame.draw.rect(screen, GREEN, (px + 2, py - 5, fill, 3))


class Boss:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.health = 50
        self.max_health = 50
        self.alive = True
        self.phase = "chase"
        self.phase_timer = 0
        self.move_timer = 0
        self.hit_flash = 0
        self.charge_dx = 0
        self.charge_dy = 0
        self.death_timer = 0
        self.summon_count = 0
        self.sprite = sprite

    def update(self, player, tile_map, enemies, enemy_sprites):
        if not self.alive:
            self.death_timer -= 1
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.phase_timer += 1
        self.move_timer += 1

        if self.phase == "chase":
            if self.move_timer >= 12:
                self.move_timer = 0
                dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
                dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_y < len(tile_map) - 1 and 0 <= new_x < len(tile_map[0]) - 1:
                    if tile_map[new_y][new_x] != WALL:
                        self.x = new_x
                        self.y = new_y
            if self.phase_timer > 120:
                self.phase = "charge"
                self.phase_timer = 0
                self.charge_dx = 1 if player.x > self.x else -1
                self.charge_dy = 1 if player.y > self.y else -1

        elif self.phase == "charge":
            if self.move_timer >= 3:
                self.move_timer = 0
                new_x = self.x + self.charge_dx
                new_y = self.y + self.charge_dy
                if 0 <= new_y < len(tile_map) - 1 and 0 <= new_x < len(tile_map[0]) - 1:
                    if tile_map[new_y][new_x] != WALL:
                        self.x = new_x
                        self.y = new_y
                    else:
                        self.phase = "summon"
                        self.phase_timer = 0
                        self.summon_count = 0
                else:
                    self.phase = "summon"
                    self.phase_timer = 0
                    self.summon_count = 0
            if self.phase_timer > 60:
                self.phase = "summon"
                self.phase_timer = 0
                self.summon_count = 0

        elif self.phase == "summon":
            if self.phase_timer == 30 and self.summon_count < 2:
                spawn_x = self.x + random.choice([-2, 2])
                spawn_y = self.y + random.choice([-2, 2])
                spawn_x = max(1, min(spawn_x, len(tile_map[0]) - 2))
                spawn_y = max(1, min(spawn_y, len(tile_map) - 2))
                if tile_map[spawn_y][spawn_x] != WALL:
                    enemies.append(Enemy("skeleton", spawn_x, spawn_y, enemy_sprites))
                    self.summon_count += 1
            if self.phase_timer > 90:
                self.phase = "rest"
                self.phase_timer = 0

        elif self.phase == "rest":
            if self.phase_timer > 60:
                self.phase = "chase"
                self.phase_timer = 0

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 10
        if self.health <= 0:
            self.alive = False
            self.death_timer = 60

    def touches_player(self, player):
        return (self.x <= player.x <= self.x + 1 and
                self.y <= player.y <= self.y + 1)

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if not self.alive:
            if self.death_timer > 0:
                alpha = int(255 * (self.death_timer / 60))
                death_surf = self.sprite.copy()
                death_surf.set_alpha(alpha)
                screen.blit(death_surf, (px, py))
            return
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            flash = self.sprite.copy()
            flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
            screen.blit(flash, (px, py))
        else:
            screen.blit(self.sprite, (px, py))


class Item:
    def __init__(self, item_type, x, y, sprites):
        self.item_type = item_type
        self.x = x
        self.y = y
        self.collected = False
        self.sprite = sprites.get(item_type)

    def draw(self, screen, camera_x, camera_y):
        if self.collected:
            return
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if self.sprite:
            screen.blit(self.sprite, (px, py))
        else:
            color = RED if self.item_type == "health_potion" else BLUE if self.item_type == "speed_boost" else GOLD
            pygame.draw.rect(screen, color, (px + 8, py + 8, TILE_SIZE - 16, TILE_SIZE - 16))


# ============================================================
# MAIN GAME CLASS
# ============================================================

class Game:
    def __init__(self, seed=None):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robert's Dungeons v9 - Procgen!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 48)

        # Sound
        self.sound = SoundManager()

        # Sprites
        self.sprites = {}
        self.sprites["player_right"] = create_player_sprite(facing_right=True)
        self.sprites["player_left"] = create_player_sprite(facing_right=False)
        self.sprites["zombie"] = create_enemy_sprite("zombie")
        self.sprites["skeleton"] = create_enemy_sprite("skeleton")
        self.sprites["boss"] = create_boss_sprite()
        self.sprites["tiles"] = create_tile_sprites()
        self.sprites["items"] = create_item_sprites()

        self.sprites["player_right"] = try_load_sprite("assets/player_right.png", self.sprites["player_right"])
        self.sprites["player_left"] = try_load_sprite("assets/player_left.png", self.sprites["player_left"])

        # Game state
        self.state = "title"  # "title", "playing", "game_over", "victory"
        self.seed = seed
        self.seed_input = ""
        self.tile_map = None
        self.enemies = []
        self.items = []
        self.boss = None
        self.player = None
        self.dungeon_rooms = []
        self.explored = set()  # Set of (room_index) that player has visited
        self.camera_x = 0
        self.camera_y = 0
        self.running = True
        self.start_time = 0

    def start_game(self, seed=None):
        """Generate a new dungeon and start playing."""
        if seed is None:
            seed = random.randint(1, 999999)
        self.seed = seed
        print(f"Dungeon seed: {self.seed}")
        print(f"Share this seed with friends to play the same dungeon!")

        # Generate dungeon
        result = generate_dungeon(self.seed)
        self.tile_map, enemy_data, chest_pos, player_start, boss_pos, self.dungeon_rooms = result

        # Create game objects
        enemy_sprites = {"zombie": self.sprites["zombie"], "skeleton": self.sprites["skeleton"]}
        self.enemies = [Enemy(etype, ex, ey, enemy_sprites) for etype, ex, ey in enemy_data]
        self.items = []
        self.boss = Boss(boss_pos[0], boss_pos[1], self.sprites["boss"])

        player_sprites = {"player_right": self.sprites["player_right"], "player_left": self.sprites["player_left"]}
        self.player = Player(player_start[0], player_start[1], player_sprites)

        # Track explored areas
        self.explored = set()
        self.update_explored()

        self.state = "playing"
        self.start_time = time.time()
        self.sound.play_music("dungeon")

    def update_explored(self):
        """Mark the room the player is in as explored."""
        for i, room in enumerate(self.dungeon_rooms):
            if (room.x <= self.player.x < room.x + room.w and
                    room.y <= self.player.y < room.y + room.h):
                self.explored.add(i)
                # If in boss room, switch music
                if i == len(self.dungeon_rooms) - 1 and self.boss and self.boss.alive:
                    self.sound.play_music("boss")
                break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if self.state == "title":
                    if event.key == pygame.K_RETURN:
                        # Start with entered seed or random
                        if self.seed_input.strip():
                            try:
                                seed = int(self.seed_input.strip())
                            except ValueError:
                                # Use hash of string as seed
                                seed = abs(hash(self.seed_input.strip())) % 999999
                        else:
                            seed = None
                        self.start_game(seed)
                    elif event.key == pygame.K_BACKSPACE:
                        self.seed_input = self.seed_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.unicode.isdigit() and len(self.seed_input) < 6:
                        self.seed_input += event.unicode

                elif self.state == "playing":
                    if event.key == pygame.K_UP:
                        self.player.move(0, -1, self.tile_map)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(0, 1, self.tile_map)
                    elif event.key == pygame.K_LEFT:
                        self.player.move(-1, 0, self.tile_map)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(1, 0, self.tile_map)
                    elif event.key == pygame.K_SPACE:
                        self.player.attack()
                        self.sound.play("sword_swing")
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                        idx = event.key - pygame.K_1
                        if idx < len(self.player.inventory):
                            self.player.use_item(idx)
                            self.sound.play("item_pickup")
                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        self.sound.volume_up()
                    elif event.key == pygame.K_MINUS:
                        self.sound.volume_down()

                elif self.state in ("game_over", "victory"):
                    if event.key == pygame.K_r:
                        self.sound.stop_music()
                        self.state = "title"
                        self.seed_input = ""

    def update(self):
        if self.state != "playing":
            return

        self.player.update()
        self.update_explored()

        enemy_sprites = {"zombie": self.sprites["zombie"], "skeleton": self.sprites["skeleton"]}

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.tile_map)
            if enemy.alive and enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.hurt_timer <= 0:
                    self.player.health -= 1
                    self.player.hurt_timer = 30
                    self.sound.play("player_hurt")

        # Player attack
        if self.player.attacking and self.player.attack_timer == 7:
            ax, ay = self.player.get_attack_tile()
            for enemy in self.enemies:
                if enemy.alive and enemy.x == ax and enemy.y == ay:
                    enemy.take_damage(self.player.attack_power)
                    self.sound.play("enemy_hit")
                    if not enemy.alive:
                        self.player.kills += 1
                        self.sound.play("enemy_death")
                        if random.random() < 0.4:
                            loot = random.choice(["health_potion", "speed_boost", "power_sword"])
                            self.items.append(Item(loot, enemy.x, enemy.y, self.sprites["items"]))

            # Check boss hit
            if self.boss and self.boss.alive:
                if (self.boss.x <= ax <= self.boss.x + 1) and (self.boss.y <= ay <= self.boss.y + 1):
                    self.boss.take_damage(self.player.attack_power)
                    self.sound.play("enemy_hit")
                    if not self.boss.alive:
                        self.state = "victory"
                        self.player.kills += 1
                        self.sound.play("enemy_death")
                        self.sound.stop_music()

        # Update boss
        if self.boss and self.boss.alive:
            self.boss.update(self.player, self.tile_map, self.enemies, enemy_sprites)
            if self.boss.touches_player(self.player):
                if self.player.hurt_timer <= 0:
                    self.player.health -= 2
                    self.player.hurt_timer = 30
                    self.sound.play("player_hurt")

        # Clean up dead enemies
        self.enemies = [e for e in self.enemies if e.alive or e.death_timer > 0]

        # Pick up items
        for item in self.items:
            if not item.collected and item.x == self.player.x and item.y == self.player.y:
                if len(self.player.inventory) < 5:
                    self.player.inventory.append(item.item_type)
                    item.collected = True
                    self.sound.play("item_pickup")

        # Check chests
        if self.tile_map[self.player.y][self.player.x] == CHEST:
            self.tile_map[self.player.y][self.player.x] = FLOOR
            loot = random.choice(["health_potion", "speed_boost", "power_sword"])
            if len(self.player.inventory) < 5:
                self.player.inventory.append(loot)
                self.sound.play("chest_open")

        # Camera
        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

        # Death check
        if self.player.health <= 0:
            self.state = "game_over"
            self.sound.stop_music()

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == "title":
            self.draw_title_screen()
        elif self.state in ("playing", "game_over", "victory"):
            self.draw_game()

        pygame.display.flip()

    def draw_title_screen(self):
        # Title
        title = self.big_font.render("Robert's Dungeons", True, GOLD)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))

        subtitle = self.font.render("Procedurally Generated Edition", True, WHITE)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 190))

        # Seed input
        prompt = self.font.render("Enter a seed number (or leave blank for random):", True, WHITE)
        self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 280))

        # Input box
        box_w = 200
        box_x = SCREEN_WIDTH // 2 - box_w // 2
        box_y = 320
        pygame.draw.rect(self.screen, (40, 40, 40), (box_x, box_y, box_w, 40))
        pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_w, 40), 2)

        seed_text = self.title_font.render(self.seed_input if self.seed_input else "______", True,
                                            WHITE if self.seed_input else (80, 80, 80))
        self.screen.blit(seed_text, (box_x + box_w // 2 - seed_text.get_width() // 2, box_y + 5))

        # Instructions
        start_text = self.font.render("Press ENTER to start", True, GREEN)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 400))

        hint = self.small_font.render("Same seed = same dungeon. Share seeds with friends!", True, (150, 150, 150))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 450))

    def draw_game(self):
        tile_sprites = self.sprites["tiles"]
        map_h = len(self.tile_map)
        map_w = len(self.tile_map[0])

        # Calculate visible tile range for performance
        start_col = max(0, self.camera_x // TILE_SIZE - 1)
        end_col = min(map_w, (self.camera_x + SCREEN_WIDTH) // TILE_SIZE + 2)
        start_row = max(0, self.camera_y // TILE_SIZE - 1)
        end_row = min(map_h, (self.camera_y + SCREEN_HEIGHT) // TILE_SIZE + 2)

        # Draw tiles
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                sx = col * TILE_SIZE - self.camera_x
                sy = row * TILE_SIZE - self.camera_y
                tile_type = self.tile_map[row][col]
                if tile_type in tile_sprites:
                    self.screen.blit(tile_sprites[tile_type], (sx, sy))
                else:
                    self.screen.blit(tile_sprites[FLOOR], (sx, sy))

        # Draw items
        for item in self.items:
            item.draw(self.screen, self.camera_x, self.camera_y)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        # Draw boss
        if self.boss:
            self.boss.draw(self.screen, self.camera_x, self.camera_y)

        # Draw player
        if self.player:
            self.player.draw(self.screen, self.camera_x, self.camera_y)

        # HUD
        self.draw_hud()

        # Game over overlay
        if self.state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            text = self.big_font.render("GAME OVER", True, RED)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))
            seed_info = self.font.render(f"Seed: {self.seed}", True, WHITE)
            self.screen.blit(seed_info, (SCREEN_WIDTH // 2 - seed_info.get_width() // 2, 280))
            restart = self.font.render("Press R for title screen", True, WHITE)
            self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 330))

        # Victory overlay
        if self.state == "victory":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            text = self.big_font.render("YOU WIN!", True, GOLD)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 130))
            elapsed = int(time.time() - self.start_time)
            stats = [
                f"Seed: {self.seed}",
                f"Time: {elapsed // 60}m {elapsed % 60}s",
                f"Kills: {self.player.kills}",
                f"Rooms explored: {len(self.explored)}/{len(self.dungeon_rooms)}",
                "Press R for title screen",
            ]
            for i, line in enumerate(stats):
                t = self.font.render(line, True, WHITE)
                self.screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 220 + i * 35))

    def draw_hud(self):
        if not self.player:
            return

        # Health bar
        bar_x, bar_y = 10, 10
        bar_width, bar_height = 200, 20
        fill = int(bar_width * max(0, self.player.health) / self.player.max_health)
        pygame.draw.rect(self.screen, DARK_RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        hp_text = self.small_font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + 5, bar_y + 2))

        # Kill counter
        kill_text = self.font.render(f"Kills: {self.player.kills}", True, WHITE)
        self.screen.blit(kill_text, (bar_x, bar_y + 28))

        # Seed display
        seed_text = self.small_font.render(f"Seed: {self.seed}", True, (150, 150, 150))
        self.screen.blit(seed_text, (bar_x, bar_y + 55))

        # Attack cooldown
        if self.player.attack_cooldown > 0:
            cd_fill = int(60 * (1 - self.player.attack_cooldown / 20))
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y + 75, 60, 8))
            pygame.draw.rect(self.screen, YELLOW, (bar_x, bar_y + 75, cd_fill, 8))

        # Volume
        vol_text = self.small_font.render(f"Vol: {int(self.sound.volume * 100)}%", True, (150, 150, 150))
        self.screen.blit(vol_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 25))

        # Inventory
        inv_y = SCREEN_HEIGHT - 50
        inv_text = self.small_font.render("Inventory (1-5):", True, WHITE)
        self.screen.blit(inv_text, (10, inv_y - 18))
        for i in range(5):
            slot_x = 10 + i * 40
            pygame.draw.rect(self.screen, (60, 60, 60), (slot_x, inv_y, 34, 34))
            pygame.draw.rect(self.screen, WHITE, (slot_x, inv_y, 34, 34), 1)
            if i < len(self.player.inventory):
                item_type = self.player.inventory[i]
                item_sprite = self.sprites["items"].get(item_type)
                if item_sprite:
                    self.screen.blit(item_sprite, (slot_x + 1, inv_y + 1))

        # Speed boost
        if self.player.speed_boost_timer > 0:
            boost_text = self.small_font.render("SPEED BOOST!", True, BLUE)
            self.screen.blit(boost_text, (SCREEN_WIDTH // 2 - 50, 10))

        # Boss health bar
        if self.boss and self.boss.alive:
            # Check if player is in boss room
            boss_room = self.dungeon_rooms[-1]
            if (boss_room.x <= self.player.x < boss_room.x + boss_room.w and
                    boss_room.y <= self.player.y < boss_room.y + boss_room.h):
                boss_bar_w = 400
                boss_bar_x = SCREEN_WIDTH // 2 - boss_bar_w // 2
                boss_bar_y = 50
                boss_fill = int(boss_bar_w * self.boss.health / self.boss.max_health)
                pygame.draw.rect(self.screen, (80, 0, 0), (boss_bar_x, boss_bar_y, boss_bar_w, 24))
                pygame.draw.rect(self.screen, (200, 30, 30), (boss_bar_x, boss_bar_y, boss_fill, 24))
                pygame.draw.rect(self.screen, WHITE, (boss_bar_x, boss_bar_y, boss_bar_w, 24), 2)
                boss_name = self.font.render("DEMON KING", True, WHITE)
                self.screen.blit(boss_name, (SCREEN_WIDTH // 2 - boss_name.get_width() // 2, boss_bar_y + 28))

        # Minimap
        self.draw_minimap()

    def draw_minimap(self):
        """Draw a minimap showing explored rooms."""
        if not self.dungeon_rooms:
            return

        # Find the bounds of all rooms
        min_x = min(r.x for r in self.dungeon_rooms)
        max_x = max(r.x + r.w for r in self.dungeon_rooms)
        min_y = min(r.y for r in self.dungeon_rooms)
        max_y = max(r.y + r.h for r in self.dungeon_rooms)

        # Scale to fit in a minimap area
        mm_width = 120
        mm_height = 90
        mm_x = SCREEN_WIDTH - mm_width - 10
        mm_y = 10

        # Background
        mm_bg = pygame.Surface((mm_width + 4, mm_height + 4), pygame.SRCALPHA)
        mm_bg.fill((0, 0, 0, 140))
        self.screen.blit(mm_bg, (mm_x - 2, mm_y - 2))

        range_x = max(max_x - min_x, 1)
        range_y = max(max_y - min_y, 1)
        scale_x = mm_width / range_x
        scale_y = mm_height / range_y
        scale = min(scale_x, scale_y)

        for i, room in enumerate(self.dungeon_rooms):
            rx = mm_x + int((room.x - min_x) * scale)
            ry = mm_y + int((room.y - min_y) * scale)
            rw = max(int(room.w * scale), 3)
            rh = max(int(room.h * scale), 3)

            if i in self.explored:
                color = (80, 80, 120)
                if i == len(self.dungeon_rooms) - 1:
                    color = (150, 40, 40)  # Boss room is red
            else:
                color = (50, 50, 50)

            pygame.draw.rect(self.screen, color, (rx, ry, rw, rh))
            pygame.draw.rect(self.screen, (100, 100, 100), (rx, ry, rw, rh), 1)

        # Player dot
        px = mm_x + int((self.player.x - min_x) * scale)
        py = mm_y + int((self.player.y - min_y) * scale)
        pygame.draw.circle(self.screen, GREEN, (px, py), 3)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


# ============================================================
# START THE GAME
# ============================================================
if __name__ == "__main__":
    game = Game()
    game.run()
