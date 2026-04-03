"""
Dungeon v6: The Boss
Robert's Coding Course - Lesson 17

Arrow keys to move, Space to attack, 1-5 to use items.
Walk into doors to move between rooms. Defeat the boss in Room 4!
"""

import pygame
import random
import time

# --- Constants ---
TILE_SIZE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (60, 60, 60)
BROWN = (139, 90, 43)
YELLOW = (220, 200, 50)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (160, 50, 200)
DOOR_COLOR = (80, 60, 30)
BOSS_RED = (180, 40, 40)

# --- Room Maps ---
# 0=floor, 1=wall, 2=door, 3=chest
# Each room is ~20 cols x 15 rows

ROOM_0_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROOM_1_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,3,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,3,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROOM_2_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROOM_3_MAP = [
    [1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,3,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,2],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,3,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROOM_4_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


# --- Item Class ---
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        if item_type == "health_potion":
            self.color = RED
        elif item_type == "speed_boost":
            self.color = CYAN
        elif item_type == "power_sword":
            self.color = ORANGE

    def draw(self, screen, cam_x, cam_y):
        sx = self.x * TILE_SIZE - cam_x + TILE_SIZE // 4
        sy = self.y * TILE_SIZE - cam_y + TILE_SIZE // 4
        size = TILE_SIZE // 2
        pygame.draw.rect(screen, self.color, (sx, sy, size, size))
        pygame.draw.rect(screen, WHITE, (sx + 2, sy + 2, 4, 4))


# --- Player Class ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 20
        self.max_health = 20
        self.facing = "right"
        self.attack_cooldown = 15
        self.attack_timer = 0
        self.attacking = False
        self.attack_frame = 0
        self.damage_cooldown = 0
        self.inventory = []
        self.speed_boost_timer = 0
        self.damage_boost_timer = 0
        self.kill_count = 0
        self.move_delay = 0

    def move(self, dx, dy, tile_map):
        rows = len(tile_map)
        cols = len(tile_map[0])
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x < 0 or new_x >= cols or new_y < 0 or new_y >= rows:
            return False
        tile = tile_map[new_y][new_x]
        if tile == 1:
            return False
        if dx > 0:
            self.facing = "right"
        elif dx < 0:
            self.facing = "left"
        elif dy > 0:
            self.facing = "down"
        elif dy < 0:
            self.facing = "up"
        if tile == 2:
            return "door"
        if tile == 3:
            return "chest"
        self.x = new_x
        self.y = new_y
        return True

    def attack(self):
        if self.attack_timer <= 0:
            self.attacking = True
            self.attack_frame = 6
            self.attack_timer = self.attack_cooldown

    def get_attack_tile(self):
        if self.facing == "right":
            return (self.x + 1, self.y)
        elif self.facing == "left":
            return (self.x - 1, self.y)
        elif self.facing == "down":
            return (self.x, self.y + 1)
        elif self.facing == "up":
            return (self.x, self.y - 1)

    def update(self):
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.attack_frame > 0:
            self.attack_frame -= 1
        else:
            self.attacking = False
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
        if self.damage_boost_timer > 0:
            self.damage_boost_timer -= 1
        if self.move_delay > 0:
            self.move_delay -= 1

    def draw(self, screen, cam_x, cam_y):
        sx = self.x * TILE_SIZE - cam_x
        sy = self.y * TILE_SIZE - cam_y

        if self.damage_cooldown > 0 and self.damage_cooldown % 4 < 2:
            color = WHITE
        else:
            color = BLUE

        if self.speed_boost_timer > 0:
            pygame.draw.rect(screen, CYAN, (sx - 3, sy - 3, TILE_SIZE + 6, TILE_SIZE + 6), 2)
        if self.damage_boost_timer > 0:
            pygame.draw.rect(screen, ORANGE, (sx - 3, sy - 3, TILE_SIZE + 6, TILE_SIZE + 6), 2)

        pygame.draw.rect(screen, color, (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))

        ec = WHITE
        if self.facing == "right":
            pygame.draw.rect(screen, ec, (sx + 20, sy + 8, 4, 4))
            pygame.draw.rect(screen, ec, (sx + 20, sy + 20, 4, 4))
        elif self.facing == "left":
            pygame.draw.rect(screen, ec, (sx + 8, sy + 8, 4, 4))
            pygame.draw.rect(screen, ec, (sx + 8, sy + 20, 4, 4))
        elif self.facing == "up":
            pygame.draw.rect(screen, ec, (sx + 8, sy + 8, 4, 4))
            pygame.draw.rect(screen, ec, (sx + 20, sy + 8, 4, 4))
        elif self.facing == "down":
            pygame.draw.rect(screen, ec, (sx + 8, sy + 20, 4, 4))
            pygame.draw.rect(screen, ec, (sx + 20, sy + 20, 4, 4))

        if self.attack_frame > 0:
            atk_x, atk_y = self.get_attack_tile()
            ax = atk_x * TILE_SIZE - cam_x
            ay = atk_y * TILE_SIZE - cam_y
            swing_color = ORANGE if self.damage_boost_timer > 0 else YELLOW
            pygame.draw.rect(screen, swing_color, (ax + 4, ay + 4, TILE_SIZE - 8, TILE_SIZE - 8))


# --- Enemy Class ---
class Enemy:
    def __init__(self, x, y, enemy_type="zombie"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.move_timer = 0
        self.hit_flash = 0
        self.death_timer = -1

        if enemy_type == "zombie":
            self.health = 6
            self.max_health = 6
            self.color = GREEN
            self.move_delay = 20
        elif enemy_type == "skeleton":
            self.health = 4
            self.max_health = 4
            self.color = WHITE
            self.move_delay = 12

    def update(self, player, tile_map, enemies):
        if self.death_timer >= 0:
            self.death_timer -= 1
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1

        rows = len(tile_map)
        cols = len(tile_map[0])

        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return
        self.move_timer = 0

        if self.enemy_type == "zombie":
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        elif self.enemy_type == "skeleton":
            dx, dy = 0, 0
            if abs(player.x - self.x) > abs(player.y - self.y):
                dx = 1 if player.x > self.x else -1
            else:
                dy = 1 if player.y > self.y else -1

        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < cols and 0 <= new_y < rows:
            if tile_map[new_y][new_x] == 0:
                blocked = False
                for other in enemies:
                    if other is not self and other.x == new_x and other.y == new_y and other.is_alive():
                        blocked = True
                        break
                if not blocked:
                    self.x = new_x
                    self.y = new_y

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 6
        if self.health <= 0:
            self.death_timer = 8

    def is_alive(self):
        return self.death_timer < 0

    def is_gone(self):
        return self.death_timer == 0

    def draw(self, screen, cam_x, cam_y):
        sx = self.x * TILE_SIZE - cam_x
        sy = self.y * TILE_SIZE - cam_y

        if self.death_timer >= 0:
            if self.death_timer % 2 == 0:
                pygame.draw.rect(screen, WHITE, (sx + 4, sy + 4, TILE_SIZE - 8, TILE_SIZE - 8))
            return

        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            color = WHITE
        else:
            color = self.color

        pygame.draw.rect(screen, color, (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))

        if self.health < self.max_health:
            bar_w = TILE_SIZE - 4
            ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, (sx + 2, sy - 6, bar_w, 4))
            pygame.draw.rect(screen, GREEN, (sx + 2, sy - 6, int(bar_w * ratio), 4))


# --- Boss Class ---
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.max_health = 50
        self.size = 2  # 2x2 tiles
        self.phase = "chase"
        self.phase_timer = 150  # 5 seconds
        self.charge_dx = 0
        self.charge_dy = 0
        self.minions_spawned = 0  # max 2 summons
        self.hit_flash = 0
        self.move_timer = 0
        self.phase_cycle = 0
        self.summon_done = False  # did we already spawn minions this summon phase?
        self.death_timer = -1
        # Phase cycle: chase -> charge -> rest -> chase -> summon -> charge -> rest
        self.cycle_order = ["chase", "charge", "rest", "chase", "summon", "charge", "rest"]

    def next_phase(self):
        self.phase_cycle = (self.phase_cycle + 1) % len(self.cycle_order)
        self.phase = self.cycle_order[self.phase_cycle]
        self.charge_dx = 0
        self.charge_dy = 0
        self.summon_done = False
        # Set timer for each phase
        if self.phase == "chase":
            self.phase_timer = 150   # 5 seconds
        elif self.phase == "charge":
            self.phase_timer = 60    # 2 seconds
        elif self.phase == "rest":
            self.phase_timer = 60    # 2 seconds
        elif self.phase == "summon":
            self.phase_timer = 60    # 2 seconds

    def update(self, player, tile_map, enemies):
        if self.death_timer >= 0:
            self.death_timer -= 1
            return

        if self.hit_flash > 0:
            self.hit_flash -= 1

        self.phase_timer -= 1
        if self.phase_timer <= 0:
            self.next_phase()

        rows = len(tile_map)
        cols = len(tile_map[0])

        if self.phase == "chase":
            # Move slowly toward player (every 15 frames)
            self.move_timer += 1
            if self.move_timer >= 15:
                self.move_timer = 0
                dx, dy = 0, 0
                if abs(player.x - self.x) > abs(player.y - self.y):
                    dx = 1 if player.x > self.x else -1
                else:
                    dy = 1 if player.y > self.y else -1
                new_x = self.x + dx
                new_y = self.y + dy
                # Check all 4 corners of 2x2 boss
                if self.can_move_to(new_x, new_y, tile_map):
                    self.x = new_x
                    self.y = new_y

        elif self.phase == "charge":
            # Pick direction on first frame
            if self.charge_dx == 0 and self.charge_dy == 0:
                if abs(player.x - self.x) > abs(player.y - self.y):
                    self.charge_dx = 1 if player.x > self.x else -1
                else:
                    self.charge_dy = 1 if player.y > self.y else -1
            # Move fast (every 3 frames)
            self.move_timer += 1
            if self.move_timer >= 3:
                self.move_timer = 0
                new_x = self.x + self.charge_dx
                new_y = self.y + self.charge_dy
                if self.can_move_to(new_x, new_y, tile_map):
                    self.x = new_x
                    self.y = new_y
                else:
                    # Hit a wall, stop charging
                    self.charge_dx = 0
                    self.charge_dy = 0

        elif self.phase == "summon":
            if not self.summon_done and self.minions_spawned < 2:
                # Spawn 2 zombies near the boss
                spawn_offsets = [(-2, 0), (self.size + 1, 0)]
                for ox, oy in spawn_offsets:
                    sx = self.x + ox
                    sy = self.y + oy
                    if 0 <= sx < cols and 0 <= sy < rows and tile_map[sy][sx] == 0:
                        enemies.append(Enemy(sx, sy, "zombie"))
                self.minions_spawned += 1
                self.summon_done = True

        # phase == "rest": do nothing

        # Damage player on contact (check if player is within boss 2x2 area)
        if self.is_alive():
            if (self.x <= player.x <= self.x + self.size - 1 and
                    self.y <= player.y <= self.y + self.size - 1):
                if player.damage_cooldown <= 0:
                    damage = 3
                    player.health -= damage
                    player.damage_cooldown = 30

    def can_move_to(self, new_x, new_y, tile_map):
        """Check if the 2x2 boss can move to new position."""
        rows = len(tile_map)
        cols = len(tile_map[0])
        for dy in range(self.size):
            for dx in range(self.size):
                cx = new_x + dx
                cy = new_y + dy
                if cx < 0 or cx >= cols or cy < 0 or cy >= rows:
                    return False
                if tile_map[cy][cx] != 0:
                    return False
        return True

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 6
        if self.health <= 0:
            self.death_timer = 20  # longer death animation for boss

    def is_alive(self):
        return self.health > 0 and self.death_timer < 0

    def is_gone(self):
        return self.death_timer == 0

    def occupies(self, tx, ty):
        """Check if a tile coordinate is within the boss's 2x2 area."""
        return (self.x <= tx <= self.x + self.size - 1 and
                self.y <= ty <= self.y + self.size - 1)

    def draw(self, screen, cam_x, cam_y):
        sx = self.x * TILE_SIZE - cam_x
        sy = self.y * TILE_SIZE - cam_y
        w = self.size * TILE_SIZE

        if self.death_timer >= 0:
            # Boss death: flash and shrink
            if self.death_timer % 3 == 0:
                shrink = (20 - self.death_timer) * 2
                pygame.draw.rect(screen, WHITE,
                                 (sx + shrink, sy + shrink, w - shrink * 2, w - shrink * 2))
            return

        # Hit flash
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            color = WHITE
        else:
            # Color changes slightly by phase
            if self.phase == "charge":
                color = (220, 60, 30)   # brighter red when charging
            elif self.phase == "summon":
                color = PURPLE
            else:
                color = BOSS_RED

        # Boss body
        pygame.draw.rect(screen, color, (sx + 2, sy + 2, w - 4, w - 4))

        # Dark border
        pygame.draw.rect(screen, (80, 20, 20), (sx + 2, sy + 2, w - 4, w - 4), 3)

        # Evil eyes
        pygame.draw.rect(screen, YELLOW, (sx + 12, sy + 16, 10, 8))
        pygame.draw.rect(screen, YELLOW, (sx + 42, sy + 16, 10, 8))
        # Pupils
        pygame.draw.rect(screen, BLACK, (sx + 15, sy + 18, 4, 4))
        pygame.draw.rect(screen, BLACK, (sx + 45, sy + 18, 4, 4))

        # Mouth
        pygame.draw.rect(screen, BLACK, (sx + 16, sy + 36, 32, 6))
        pygame.draw.rect(screen, WHITE, (sx + 20, sy + 36, 6, 4))
        pygame.draw.rect(screen, WHITE, (sx + 30, sy + 36, 6, 4))
        pygame.draw.rect(screen, WHITE, (sx + 40, sy + 36, 6, 4))

        # Phase indicator above boss
        phase_colors = {
            "chase": GREEN,
            "charge": RED,
            "summon": PURPLE,
            "rest": GRAY,
        }
        ind_color = phase_colors.get(self.phase, WHITE)
        pygame.draw.rect(screen, ind_color, (sx + w // 2 - 4, sy - 10, 8, 8))


# --- Room Class ---
class Room:
    def __init__(self, tile_map, enemy_spawns, chest_positions, player_start, door_connections):
        self.original_map = [row[:] for row in tile_map]
        self.tile_map = [row[:] for row in tile_map]
        self.enemies = []
        self.items = []
        self.enemy_spawns = enemy_spawns
        self.chest_positions = chest_positions
        self.player_start = player_start
        self.door_connections = door_connections
        self.visited = False
        self.chests_opened = set()
        self.boss = None  # only room 4 has a boss

    def spawn_enemies(self):
        for x, y, etype in self.enemy_spawns:
            self.enemies.append(Enemy(x, y, etype))


# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robert's Dungeons v6 - The Boss")
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.big_font = pygame.font.Font(None, 72)
        self.reset()

    def create_rooms(self):
        room0 = Room(
            tile_map=ROOM_0_MAP,
            enemy_spawns=[
                (5, 4, "zombie"),
                (12, 9, "zombie"),
                (15, 5, "zombie"),
            ],
            chest_positions=[(14, 3)],
            player_start=(2, 2),
            door_connections={(19, 7): (1, 1, 7)},
        )

        room1 = Room(
            tile_map=ROOM_1_MAP,
            enemy_spawns=[
                (4, 5, "skeleton"),
                (10, 4, "zombie"),
                (15, 9, "skeleton"),
                (8, 10, "zombie"),
                (12, 6, "zombie"),
            ],
            chest_positions=[(16, 3), (3, 11)],
            player_start=(1, 7),
            door_connections={
                (0, 7): (0, 18, 7),
                (19, 7): (2, 1, 7),
            },
        )

        room2 = Room(
            tile_map=ROOM_2_MAP,
            enemy_spawns=[
                (5, 3, "zombie"),
                (14, 3, "skeleton"),
                (5, 11, "zombie"),
                (14, 11, "skeleton"),
                (10, 7, "zombie"),
                (8, 5, "skeleton"),
                (12, 9, "zombie"),
            ],
            chest_positions=[(9, 5), (9, 10)],
            player_start=(1, 7),
            door_connections={
                (0, 7): (1, 18, 7),
                (9, 13): (3, 9, 1),
            },
        )

        room3 = Room(
            tile_map=ROOM_3_MAP,
            enemy_spawns=[
                (2, 2, "skeleton"),
                (7, 5, "skeleton"),
                (16, 3, "skeleton"),
                (3, 9, "zombie"),
                (12, 10, "skeleton"),
                (16, 10, "zombie"),
            ],
            chest_positions=[(17, 4), (3, 11)],
            player_start=(9, 1),
            door_connections={
                (9, 0): (2, 9, 12),
                (19, 7): (4, 2, 7),
            },
        )

        room4 = Room(
            tile_map=ROOM_4_MAP,
            enemy_spawns=[],
            chest_positions=[],
            player_start=(2, 7),
            door_connections={(0, 7): (3, 18, 7)},
        )
        # Boss room!
        room4.boss = None  # boss spawns on first visit

        return [room0, room1, room2, room3, room4]

    def reset(self):
        self.rooms = self.create_rooms()
        self.current_room_idx = 0
        self.rooms[0].visited = True
        self.rooms[0].spawn_enemies()
        self.player = Player(*self.rooms[0].player_start)
        self.camera_x = 0
        self.camera_y = 0
        self.game_over = False
        self.you_win = False
        self.kill_count = 0
        self.flash_timer = 0
        self.start_time = time.time()
        self.play_time = 0
        self.items_collected = 0

    def current_room(self):
        return self.rooms[self.current_room_idx]

    def transition_to_room(self, room_idx, spawn_x, spawn_y):
        self.flash_timer = 8
        self.current_room_idx = room_idx
        room = self.current_room()
        if not room.visited:
            room.visited = True
            room.spawn_enemies()
            # Spawn boss in room 4
            if room_idx == 4:
                room.boss = Boss(10, 6)
        self.player.x = spawn_x
        self.player.y = spawn_y

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_over or self.you_win:
                        if event.key == pygame.K_SPACE:
                            self.reset()
                        continue
                    if event.key == pygame.K_SPACE:
                        self.player.attack()
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                        slot = event.key - pygame.K_1
                        if slot < len(self.player.inventory):
                            self.use_item(slot)

            if not self.game_over and not self.you_win:
                self.handle_input()
                self.update()
                self.play_time = time.time() - self.start_time
            self.draw()
            time.sleep(1 / FPS)

        pygame.quit()

    def use_item(self, slot):
        item_type = self.player.inventory.pop(slot)
        self.items_collected += 1
        if item_type == "health_potion":
            self.player.health = min(self.player.health + 5, self.player.max_health)
        elif item_type == "speed_boost":
            self.player.speed_boost_timer = 150
        elif item_type == "power_sword":
            self.player.damage_boost_timer = 150

    def handle_input(self):
        if self.flash_timer > 0:
            return

        keys = pygame.key.get_pressed()
        room = self.current_room()

        if self.player.move_delay <= 0:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -1
            elif keys[pygame.K_RIGHT]:
                dx = 1
            elif keys[pygame.K_UP]:
                dy = -1
            elif keys[pygame.K_DOWN]:
                dy = 1

            if dx != 0 or dy != 0:
                result = self.player.move(dx, dy, room.tile_map)
                if result == "door":
                    door_x = self.player.x + dx
                    door_y = self.player.y + dy
                    if (door_x, door_y) in room.door_connections:
                        ri, sx, sy = room.door_connections[(door_x, door_y)]
                        self.transition_to_room(ri, sx, sy)
                elif result == "chest":
                    chest_x = self.player.x + dx
                    chest_y = self.player.y + dy
                    room.tile_map[chest_y][chest_x] = 0
                    item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
                    room.items.append(Item(chest_x, chest_y, item_type))
                elif result:
                    self.player.move_delay = 1 if self.player.speed_boost_timer > 0 else 4

    def update(self):
        if self.flash_timer > 0:
            self.flash_timer -= 1
            return

        self.player.update()
        room = self.current_room()

        # Update enemies
        for enemy in room.enemies:
            enemy.update(self.player, room.tile_map, room.enemies)

        # Update boss
        if room.boss and room.boss.is_alive():
            room.boss.update(self.player, room.tile_map, room.enemies)
        elif room.boss and room.boss.death_timer >= 0:
            room.boss.death_timer -= 1
            if room.boss.is_gone():
                self.you_win = True

        # Player attack hits on enemies
        if self.player.attack_frame == 5:
            atk_x, atk_y = self.player.get_attack_tile()
            damage = 4 if self.player.damage_boost_timer > 0 else 2
            for enemy in room.enemies:
                if enemy.is_alive() and enemy.x == atk_x and enemy.y == atk_y:
                    enemy.take_damage(damage)
            # Attack boss
            if room.boss and room.boss.is_alive():
                if room.boss.occupies(atk_x, atk_y):
                    room.boss.take_damage(damage)

        # Enemy contact damage
        for enemy in room.enemies:
            if enemy.is_alive() and enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.damage_cooldown <= 0:
                    self.player.health -= 1
                    self.player.damage_cooldown = 30

        # Boss contact damage is handled in boss.update()

        # Dead enemies + drops
        for enemy in room.enemies[:]:
            if enemy.is_gone():
                self.kill_count += 1
                self.player.kill_count += 1
                if random.random() < 0.4:
                    item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
                    room.items.append(Item(enemy.x, enemy.y, item_type))
                room.enemies.remove(enemy)

        # Pick up items
        for item in room.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                if len(self.player.inventory) < 5:
                    self.player.inventory.append(item.item_type)
                    room.items.remove(item)

        # Player death
        if self.player.health <= 0:
            self.game_over = True

        # Camera
        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

    def draw(self):
        self.screen.fill(BLACK)

        # Transition flash
        if self.flash_timer > 0:
            brightness = int(255 * (self.flash_timer / 8))
            self.screen.fill((brightness, brightness, brightness))
            pygame.display.update()
            return

        room = self.current_room()
        tile_map = room.tile_map
        rows = len(tile_map)
        cols = len(tile_map[0])

        # Draw tiles
        for row in range(rows):
            for col in range(cols):
                sx = col * TILE_SIZE - self.camera_x
                sy = row * TILE_SIZE - self.camera_y
                if sx < -TILE_SIZE or sx > SCREEN_WIDTH or sy < -TILE_SIZE or sy > SCREEN_HEIGHT:
                    continue
                tile = tile_map[row][col]
                if tile == 0:
                    pygame.draw.rect(self.screen, DARK_GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (50, 50, 50), (sx, sy, TILE_SIZE, TILE_SIZE), 1)
                elif tile == 1:
                    pygame.draw.rect(self.screen, GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (80, 80, 80), (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                elif tile == 2:
                    pygame.draw.rect(self.screen, DOOR_COLOR, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (60, 40, 20), (sx + 4, sy + 2, TILE_SIZE - 8, TILE_SIZE - 4))
                elif tile == 3:
                    pygame.draw.rect(self.screen, DARK_GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, BROWN, (sx + 4, sy + 8, TILE_SIZE - 8, TILE_SIZE - 12))
                    pygame.draw.rect(self.screen, YELLOW, (sx + 6, sy + 10, TILE_SIZE - 12, 6))
                    pygame.draw.rect(self.screen, (180, 150, 30), (sx + 12, sy + 16, 8, 6))

        # Items
        for item in room.items:
            item.draw(self.screen, self.camera_x, self.camera_y)

        # Enemies
        for enemy in room.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        # Boss
        if room.boss and (room.boss.is_alive() or room.boss.death_timer > 0):
            room.boss.draw(self.screen, self.camera_x, self.camera_y)

        # Player
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # --- HUD ---
        # Health bar
        bar_x, bar_y = 10, 10
        bar_w, bar_h = 200, 20
        ratio = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, (80, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2)
        hp_text = self.font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + 5, bar_y + 1))

        # Kill count
        self.screen.blit(self.font.render(f"Kills: {self.kill_count}", True, WHITE), (10, 38))

        # Attack cooldown bar
        cd_x, cd_y = 10, 62
        cd_w, cd_h = 100, 8
        if self.player.attack_timer > 0:
            cd_ratio = self.player.attack_timer / self.player.attack_cooldown
            pygame.draw.rect(self.screen, (80, 80, 0), (cd_x, cd_y, cd_w, cd_h))
            pygame.draw.rect(self.screen, YELLOW, (cd_x, cd_y, int(cd_w * (1 - cd_ratio)), cd_h))
        else:
            pygame.draw.rect(self.screen, YELLOW, (cd_x, cd_y, cd_w, cd_h))

        # Active effects
        effect_x = 220
        if self.player.speed_boost_timer > 0:
            secs = self.player.speed_boost_timer / FPS
            self.screen.blit(self.small_font.render(f"SPEED {secs:.1f}s", True, CYAN), (effect_x, 12))
            effect_x += 110
        if self.player.damage_boost_timer > 0:
            secs = self.player.damage_boost_timer / FPS
            self.screen.blit(self.small_font.render(f"POWER {secs:.1f}s", True, ORANGE), (effect_x, 12))

        # Room label
        room_names = ["Start Room", "Corridor", "Arena", "Maze", "Boss Chamber"]
        name = room_names[self.current_room_idx]
        name_text = self.font.render(name, True, WHITE)
        self.screen.blit(name_text, name_text.get_rect(center=(SCREEN_WIDTH // 2, 18)))

        # Boss health bar (big bar at top)
        if room.boss and room.boss.is_alive():
            boss_bar_w = 300
            boss_bar_h = 20
            boss_bar_x = SCREEN_WIDTH // 2 - boss_bar_w // 2
            boss_bar_y = 42
            boss_ratio = room.boss.health / room.boss.max_health
            pygame.draw.rect(self.screen, (80, 0, 0), (boss_bar_x, boss_bar_y, boss_bar_w, boss_bar_h))
            pygame.draw.rect(self.screen, (200, 30, 30), (boss_bar_x, boss_bar_y, int(boss_bar_w * boss_ratio), boss_bar_h))
            pygame.draw.rect(self.screen, WHITE, (boss_bar_x, boss_bar_y, boss_bar_w, boss_bar_h), 2)
            boss_label = self.font.render("DUNGEON BOSS", True, RED)
            self.screen.blit(boss_label, boss_label.get_rect(center=(SCREEN_WIDTH // 2, boss_bar_y + 10)))
            # Phase text
            phase_text = self.small_font.render(f"Phase: {room.boss.phase.upper()}", True, YELLOW)
            self.screen.blit(phase_text, phase_text.get_rect(center=(SCREEN_WIDTH // 2, boss_bar_y + 30)))

        # Minimap
        self.draw_minimap()

        # Inventory bar
        inv_y = SCREEN_HEIGHT - 50
        pygame.draw.rect(self.screen, (30, 30, 30), (0, inv_y - 5, SCREEN_WIDTH, 55))
        self.screen.blit(self.small_font.render("Inventory:", True, WHITE), (10, inv_y - 2))

        item_colors = {"health_potion": RED, "speed_boost": CYAN, "power_sword": ORANGE}
        item_labels = {"health_potion": "HP", "speed_boost": "SPD", "power_sword": "PWR"}
        for i in range(5):
            x = 100 + i * 55
            y = inv_y
            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, 40, 36))
            pygame.draw.rect(self.screen, WHITE, (x, y, 40, 36), 1)
            self.screen.blit(self.small_font.render(str(i + 1), True, (180, 180, 180)), (x + 2, y + 1))
            if i < len(self.player.inventory):
                it = self.player.inventory[i]
                pygame.draw.rect(self.screen, item_colors.get(it, WHITE), (x + 8, y + 8, 24, 20))
                self.screen.blit(self.small_font.render(item_labels.get(it, "?"), True, BLACK), (x + 10, y + 10))

        # Game over screen
        if self.game_over:
            self.draw_overlay_screen("GAME OVER", RED)

        # Victory screen
        if self.you_win:
            self.draw_victory_screen()

        pygame.display.update()

    def draw_overlay_screen(self, title, color):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        text = self.big_font.render(title, True, color)
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))

        stats = self.font.render(f"Kills: {self.kill_count}", True, WHITE)
        self.screen.blit(stats, stats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))

        restart = self.font.render("Press SPACE to restart", True, WHITE)
        self.screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

    def draw_victory_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Title
        title = self.big_font.render("YOU WIN!", True, YELLOW)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))

        # Stats
        minutes = int(self.play_time // 60)
        seconds = int(self.play_time % 60)
        time_text = self.font.render(f"Time: {minutes}m {seconds}s", True, WHITE)
        self.screen.blit(time_text, time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        kills_text = self.font.render(f"Enemies Defeated: {self.kill_count}", True, WHITE)
        self.screen.blit(kills_text, kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 15)))

        items_text = self.font.render(f"Items Used: {self.items_collected}", True, WHITE)
        self.screen.blit(items_text, items_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

        # Restart prompt
        restart = self.font.render("Press SPACE to play again", True, WHITE)
        self.screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

    def draw_minimap(self):
        base_x = SCREEN_WIDTH - 140
        base_y = 10
        positions = [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)]

        pygame.draw.rect(self.screen, (20, 20, 20), (base_x - 5, base_y - 5, 120, 60))
        pygame.draw.rect(self.screen, (60, 60, 60), (base_x - 5, base_y - 5, 120, 60), 1)

        for i, (mx, my) in enumerate(positions):
            rx = base_x + mx * 28
            ry = base_y + my * 22
            if i == self.current_room_idx:
                color = WHITE
                pygame.draw.rect(self.screen, color, (rx, ry, 22, 16))
                pygame.draw.rect(self.screen, YELLOW, (rx, ry, 22, 16), 2)
            elif self.rooms[i].visited:
                pygame.draw.rect(self.screen, GRAY, (rx, ry, 22, 16))
            # Unvisited rooms are not drawn


# --- Run the game! ---
if __name__ == "__main__":
    game = Game()
    game.run()
