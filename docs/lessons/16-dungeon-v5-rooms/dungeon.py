"""
Dungeon v5: Multiple Rooms
Robert's Coding Course - Lesson 16

Arrow keys to move, Space to attack, 1-5 to use items.
Walk into doors (dark tiles) to move between rooms.
Minimap in the top-right shows rooms you've explored.
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
        # Doors and chests return special values
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

        # Eyes
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

        # Attack swing
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
        self.door_connections = door_connections  # {(x,y): (room_idx, spawn_x, spawn_y)}
        self.visited = False
        self.chests_opened = set()

    def spawn_enemies(self):
        for x, y, etype in self.enemy_spawns:
            self.enemies.append(Enemy(x, y, etype))


# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robert's Dungeons v5 - Multiple Rooms")
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.reset()

    def create_rooms(self):
        # Room 0: Start room (few enemies)
        room0 = Room(
            tile_map=ROOM_0_MAP,
            enemy_spawns=[
                (5, 4, "zombie"),
                (12, 9, "zombie"),
                (15, 5, "zombie"),
            ],
            chest_positions=[(14, 3)],
            player_start=(2, 2),
            door_connections={
                (19, 7): (1, 1, 7),  # right door -> room 1
            },
        )

        # Room 1: Corridor (moderate enemies)
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
                (0, 7): (0, 18, 7),   # left door -> room 0
                (19, 7): (2, 1, 7),   # right door -> room 2
            },
        )

        # Room 2: Arena (many enemies)
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
                (0, 7): (1, 18, 7),      # left door -> room 1
                (9, 13): (3, 9, 1),       # bottom door -> room 3
            },
        )

        # Room 3: Maze (skeletons)
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
                (9, 0): (2, 9, 12),      # top door -> room 2
                (19, 7): (4, 1, 7),      # right door -> room 4 (boss room)
            },
        )

        # Room 4: Boss room (empty for now - boss in lesson 17)
        room4 = Room(
            tile_map=ROOM_4_MAP,
            enemy_spawns=[],
            chest_positions=[],
            player_start=(1, 7),
            door_connections={
                (0, 7): (3, 18, 7),   # left door -> room 3
            },
        )

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
        self.kill_count = 0
        self.flash_timer = 0

    def current_room(self):
        return self.rooms[self.current_room_idx]

    def transition_to_room(self, room_idx, spawn_x, spawn_y):
        self.flash_timer = 8
        self.current_room_idx = room_idx
        room = self.current_room()
        if not room.visited:
            room.visited = True
            room.spawn_enemies()
        self.player.x = spawn_x
        self.player.y = spawn_y

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.reset()
                        continue
                    if event.key == pygame.K_SPACE:
                        self.player.attack()
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                        slot = event.key - pygame.K_1
                        if slot < len(self.player.inventory):
                            self.use_item(slot)

            if not self.game_over:
                self.handle_input()
                self.update()
            self.draw()
            time.sleep(1 / FPS)

        pygame.quit()

    def use_item(self, slot):
        item_type = self.player.inventory.pop(slot)
        if item_type == "health_potion":
            self.player.health = min(self.player.health + 5, self.player.max_health)
        elif item_type == "speed_boost":
            self.player.speed_boost_timer = 150
        elif item_type == "power_sword":
            self.player.damage_boost_timer = 150

    def handle_input(self):
        if self.flash_timer > 0:
            return  # don't move during transition

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
                    door_pos = (door_x, door_y)
                    if door_pos in room.door_connections:
                        room_idx, sx, sy = room.door_connections[door_pos]
                        self.transition_to_room(room_idx, sx, sy)
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

        # Player attack hits
        if self.player.attack_frame == 5:
            atk_x, atk_y = self.player.get_attack_tile()
            damage = 4 if self.player.damage_boost_timer > 0 else 2
            for enemy in room.enemies:
                if enemy.is_alive() and enemy.x == atk_x and enemy.y == atk_y:
                    enemy.take_damage(damage)

        # Enemy contact damage
        for enemy in room.enemies:
            if enemy.is_alive() and enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.damage_cooldown <= 0:
                    self.player.health -= 1
                    self.player.damage_cooldown = 30

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
        kill_text = self.font.render(f"Kills: {self.kill_count}", True, WHITE)
        self.screen.blit(kill_text, (10, 38))

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
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 18))
        self.screen.blit(name_text, name_rect)

        # Minimap (top-right)
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
            num_text = self.small_font.render(str(i + 1), True, (180, 180, 180))
            self.screen.blit(num_text, (x + 2, y + 1))
            if i < len(self.player.inventory):
                it = self.player.inventory[i]
                pygame.draw.rect(self.screen, item_colors.get(it, WHITE), (x + 8, y + 8, 24, 20))
                self.screen.blit(self.small_font.render(item_labels.get(it, "?"), True, BLACK), (x + 10, y + 10))

        # Game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            go_font = pygame.font.Font(None, 72)
            go_text = go_font.render("GAME OVER", True, RED)
            self.screen.blit(go_text, go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))

            stats = self.font.render(f"Kills: {self.kill_count}", True, WHITE)
            self.screen.blit(stats, stats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

            restart = self.font.render("Press SPACE to restart", True, WHITE)
            self.screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

        pygame.display.update()

    def draw_minimap(self):
        """Draw a small minimap in the top-right corner."""
        base_x = SCREEN_WIDTH - 140
        base_y = 10

        # Layout of rooms on the minimap grid
        # Room 0 at (0,0), Room 1 at (1,0), Room 2 at (2,0), Room 3 at (2,1), Room 4 at (3,1)
        positions = [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)]

        # Background
        pygame.draw.rect(self.screen, (20, 20, 20), (base_x - 5, base_y - 5, 120, 60))
        pygame.draw.rect(self.screen, (60, 60, 60), (base_x - 5, base_y - 5, 120, 60), 1)

        for i, (mx, my) in enumerate(positions):
            rx = base_x + mx * 28
            ry = base_y + my * 22
            if i == self.current_room_idx:
                color = WHITE
            elif self.rooms[i].visited:
                color = GRAY
            else:
                continue  # don't show unvisited rooms

            pygame.draw.rect(self.screen, color, (rx, ry, 22, 16))

            # Draw connections between rooms as lines
            if i == self.current_room_idx:
                pygame.draw.rect(self.screen, YELLOW, (rx, ry, 22, 16), 2)


# --- Run the game! ---
if __name__ == "__main__":
    game = Game()
    game.run()
