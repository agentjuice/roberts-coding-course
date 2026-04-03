"""
Dungeon v4: Loot & Items
Robert's Coding Course - Lesson 13

Arrow keys to move, Space to attack, 1-5 to use items.
Walk over items to pick them up. Walk into chests to open them.
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
LIGHT_GREEN = (100, 220, 100)

# --- Tile Map ---
# 0 = floor, 1 = wall, 2 = door, 3 = chest
TILE_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,3,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,3,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,3,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,3,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

MAP_ROWS = len(TILE_MAP)
MAP_COLS = len(TILE_MAP[0])


# --- Item Class ---
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        # Set color based on type
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
        # Little shine highlight
        pygame.draw.rect(screen, WHITE, (sx + 2, sy + 2, 4, 4))


# --- Player Class ---
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 20
        self.max_health = 20
        self.facing = "right"
        self.attack_cooldown = 15  # frames between attacks
        self.attack_timer = 0
        self.attacking = False
        self.attack_frame = 0
        self.damage_cooldown = 0
        self.inventory = []       # list of item_type strings
        self.speed_boost_timer = 0
        self.damage_boost_timer = 0
        self.kill_count = 0
        self.move_delay = 0       # frames until next move allowed

    def move(self, dx, dy, tile_map):
        new_x = self.x + dx
        new_y = self.y + dy
        # Bounds check
        if new_x < 0 or new_x >= MAP_COLS or new_y < 0 or new_y >= MAP_ROWS:
            return False
        # Wall check
        tile = tile_map[new_y][new_x]
        if tile == 1:
            return False
        # Chest check — opening a chest is handled by Game
        if tile == 3:
            return "chest"
        # Update facing direction
        if dx > 0:
            self.facing = "right"
        elif dx < 0:
            self.facing = "left"
        elif dy > 0:
            self.facing = "down"
        elif dy < 0:
            self.facing = "up"
        self.x = new_x
        self.y = new_y
        return True

    def attack(self):
        if self.attack_timer <= 0:
            self.attacking = True
            self.attack_frame = 6
            self.attack_timer = self.attack_cooldown

    def get_attack_tile(self):
        """Return the tile coordinate the player is attacking."""
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

        # Flash when recently damaged
        if self.damage_cooldown > 0 and self.damage_cooldown % 4 < 2:
            color = WHITE
        else:
            color = BLUE

        # Speed boost glow
        if self.speed_boost_timer > 0:
            glow = (sx - 3, sy - 3, TILE_SIZE + 6, TILE_SIZE + 6)
            pygame.draw.rect(screen, CYAN, glow, 2)

        # Damage boost glow
        if self.damage_boost_timer > 0:
            glow = (sx - 3, sy - 3, TILE_SIZE + 6, TILE_SIZE + 6)
            pygame.draw.rect(screen, ORANGE, glow, 2)

        # Player body
        pygame.draw.rect(screen, color, (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))

        # Eyes based on facing
        eye_color = WHITE
        if self.facing == "right":
            pygame.draw.rect(screen, eye_color, (sx + 20, sy + 8, 4, 4))
            pygame.draw.rect(screen, eye_color, (sx + 20, sy + 20, 4, 4))
        elif self.facing == "left":
            pygame.draw.rect(screen, eye_color, (sx + 8, sy + 8, 4, 4))
            pygame.draw.rect(screen, eye_color, (sx + 8, sy + 20, 4, 4))
        elif self.facing == "up":
            pygame.draw.rect(screen, eye_color, (sx + 8, sy + 8, 4, 4))
            pygame.draw.rect(screen, eye_color, (sx + 20, sy + 8, 4, 4))
        elif self.facing == "down":
            pygame.draw.rect(screen, eye_color, (sx + 8, sy + 20, 4, 4))
            pygame.draw.rect(screen, eye_color, (sx + 20, sy + 20, 4, 4))

        # Attack animation (sword swing)
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
        self.death_timer = -1  # -1 means alive, counts down when dying

        if enemy_type == "zombie":
            self.health = 6
            self.max_health = 6
            self.color = GREEN
            self.move_delay = 20  # slow
        elif enemy_type == "skeleton":
            self.health = 4
            self.max_health = 4
            self.color = WHITE
            self.move_delay = 12  # faster, chases player

    def update(self, player, tile_map, enemies):
        if self.death_timer >= 0:
            self.death_timer -= 1
            return

        if self.hit_flash > 0:
            self.hit_flash -= 1

        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return
        self.move_timer = 0

        if self.enemy_type == "zombie":
            # Random movement
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
        elif self.enemy_type == "skeleton":
            # Chase player
            dx, dy = 0, 0
            if abs(player.x - self.x) > abs(player.y - self.y):
                dx = 1 if player.x > self.x else -1
            else:
                dy = 1 if player.y > self.y else -1

        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < MAP_COLS and 0 <= new_y < MAP_ROWS:
            if tile_map[new_y][new_x] == 0:
                # Don't move onto another enemy
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
            self.death_timer = 8  # flash for 8 frames then disappear

    def is_alive(self):
        return self.death_timer < 0

    def is_gone(self):
        return self.death_timer == 0

    def draw(self, screen, cam_x, cam_y):
        sx = self.x * TILE_SIZE - cam_x
        sy = self.y * TILE_SIZE - cam_y

        # Dying animation
        if self.death_timer >= 0:
            if self.death_timer % 2 == 0:
                pygame.draw.rect(screen, WHITE, (sx + 4, sy + 4, TILE_SIZE - 8, TILE_SIZE - 8))
            return

        # Hit flash
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            color = WHITE
        else:
            color = self.color

        pygame.draw.rect(screen, color, (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))

        # Health bar above enemy
        if self.health < self.max_health:
            bar_width = TILE_SIZE - 4
            bar_height = 4
            ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, (sx + 2, sy - 6, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (sx + 2, sy - 6, int(bar_width * ratio), bar_height))


# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robert's Dungeons v4 - Loot & Items")
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.reset()

    def reset(self):
        # Deep copy the tile map so chests can be re-opened on reset
        self.tile_map = [row[:] for row in TILE_MAP]
        self.player = Player(2, 2)
        self.enemies = []
        self.items = []
        self.camera_x = 0
        self.camera_y = 0
        self.game_over = False
        self.kill_count = 0
        self.spawn_enemies()

    def spawn_enemies(self):
        self.enemies = [
            # Top-left area
            Enemy(5, 5, "zombie"),
            Enemy(7, 3, "zombie"),
            # Middle area
            Enemy(14, 5, "skeleton"),
            Enemy(16, 8, "zombie"),
            Enemy(13, 14, "zombie"),
            Enemy(17, 12, "skeleton"),
            # Bottom-left area
            Enemy(4, 15, "zombie"),
            Enemy(6, 18, "skeleton"),
            Enemy(3, 20, "zombie"),
            # Right side
            Enemy(25, 3, "skeleton"),
            Enemy(26, 11, "zombie"),
            Enemy(24, 18, "skeleton"),
            Enemy(27, 20, "zombie"),
        ]

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
                    # Attack
                    if event.key == pygame.K_SPACE:
                        self.player.attack()
                    # Use items (1-5)
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
            self.player.speed_boost_timer = 150  # ~5 seconds
        elif item_type == "power_sword":
            self.player.damage_boost_timer = 150

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Movement with delay (faster if speed boost is active)
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
                result = self.player.move(dx, dy, self.tile_map)
                if result == "chest":
                    # Open chest
                    chest_x = self.player.x + dx
                    chest_y = self.player.y + dy
                    self.tile_map[chest_y][chest_x] = 0
                    item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
                    self.items.append(Item(chest_x, chest_y, item_type))
                if result:
                    # Set move delay: 1 frame if speed boost, 4 frames normally
                    self.player.move_delay = 1 if self.player.speed_boost_timer > 0 else 4

    def update(self):
        self.player.update()

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.tile_map, self.enemies)

        # Player attack hits
        if self.player.attack_frame == 5:  # check on first frame of attack
            atk_x, atk_y = self.player.get_attack_tile()
            damage = 4 if self.player.damage_boost_timer > 0 else 2
            for enemy in self.enemies:
                if enemy.is_alive() and enemy.x == atk_x and enemy.y == atk_y:
                    enemy.take_damage(damage)

        # Enemy touches player = damage
        for enemy in self.enemies:
            if enemy.is_alive() and enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.damage_cooldown <= 0:
                    self.player.health -= 1
                    self.player.damage_cooldown = 30

        # Check for dead enemies and drops
        for enemy in self.enemies[:]:
            if enemy.is_gone():
                self.kill_count += 1
                self.player.kill_count += 1
                # 40% chance to drop an item
                if random.random() < 0.4:
                    item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
                    self.items.append(Item(enemy.x, enemy.y, item_type))
                self.enemies.remove(enemy)

        # Pick up items
        for item in self.items[:]:
            if item.x == self.player.x and item.y == self.player.y:
                if len(self.player.inventory) < 5:
                    self.player.inventory.append(item.item_type)
                    self.items.remove(item)

        # Player death
        if self.player.health <= 0:
            self.game_over = True

        # Camera follows player
        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

    def draw(self):
        self.screen.fill(BLACK)

        # Draw tiles
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                sx = col * TILE_SIZE - self.camera_x
                sy = row * TILE_SIZE - self.camera_y
                # Skip tiles off screen
                if sx < -TILE_SIZE or sx > SCREEN_WIDTH or sy < -TILE_SIZE or sy > SCREEN_HEIGHT:
                    continue
                tile = self.tile_map[row][col]
                if tile == 0:
                    pygame.draw.rect(self.screen, DARK_GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))
                    # Floor pattern
                    pygame.draw.rect(self.screen, (50, 50, 50), (sx, sy, TILE_SIZE, TILE_SIZE), 1)
                elif tile == 1:
                    pygame.draw.rect(self.screen, GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, (80, 80, 80), (sx + 2, sy + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                elif tile == 2:
                    pygame.draw.rect(self.screen, (80, 60, 30), (sx, sy, TILE_SIZE, TILE_SIZE))
                elif tile == 3:
                    # Chest: brown base with yellow top
                    pygame.draw.rect(self.screen, DARK_GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, BROWN, (sx + 4, sy + 8, TILE_SIZE - 8, TILE_SIZE - 12))
                    pygame.draw.rect(self.screen, YELLOW, (sx + 6, sy + 10, TILE_SIZE - 12, 6))
                    pygame.draw.rect(self.screen, (180, 150, 30), (sx + 12, sy + 16, 8, 6))

        # Draw items on ground
        for item in self.items:
            item.draw(self.screen, self.camera_x, self.camera_y)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        # Draw player
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
            secs_left = self.player.speed_boost_timer / FPS
            eff_text = self.small_font.render(f"SPEED {secs_left:.1f}s", True, CYAN)
            self.screen.blit(eff_text, (effect_x, 12))
            effect_x += 110
        if self.player.damage_boost_timer > 0:
            secs_left = self.player.damage_boost_timer / FPS
            eff_text = self.small_font.render(f"POWER {secs_left:.1f}s", True, ORANGE)
            self.screen.blit(eff_text, (effect_x, 12))

        # Inventory bar at bottom
        inv_y = SCREEN_HEIGHT - 50
        pygame.draw.rect(self.screen, (30, 30, 30), (0, inv_y - 5, SCREEN_WIDTH, 55))
        inv_label = self.small_font.render("Inventory:", True, WHITE)
        self.screen.blit(inv_label, (10, inv_y - 2))

        item_colors = {
            "health_potion": RED,
            "speed_boost": CYAN,
            "power_sword": ORANGE,
        }
        item_labels = {
            "health_potion": "HP",
            "speed_boost": "SPD",
            "power_sword": "PWR",
        }
        for i in range(5):
            x = 100 + i * 55
            y = inv_y
            # Slot background
            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, 40, 36))
            pygame.draw.rect(self.screen, WHITE, (x, y, 40, 36), 1)
            # Number label
            num_text = self.small_font.render(str(i + 1), True, (180, 180, 180))
            self.screen.blit(num_text, (x + 2, y + 1))
            # Item in slot
            if i < len(self.player.inventory):
                item_t = self.player.inventory[i]
                color = item_colors.get(item_t, WHITE)
                pygame.draw.rect(self.screen, color, (x + 8, y + 8, 24, 20))
                lbl = self.small_font.render(item_labels.get(item_t, "?"), True, BLACK)
                self.screen.blit(lbl, (x + 10, y + 10))

        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            go_font = pygame.font.Font(None, 72)
            go_text = go_font.render("GAME OVER", True, RED)
            rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(go_text, rect)

            stats = self.font.render(f"Kills: {self.kill_count}", True, WHITE)
            rect2 = stats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(stats, rect2)

            restart = self.font.render("Press SPACE to restart", True, WHITE)
            rect3 = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(restart, rect3)

        pygame.display.update()


# --- Run the game! ---
if __name__ == "__main__":
    game = Game()
    game.run()
