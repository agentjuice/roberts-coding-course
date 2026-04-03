import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
BROWN = (100, 60, 20)
PLAYER_BLUE = (0, 150, 255)
ZOMBIE_GREEN = (0, 180, 0)
SKELETON_WHITE = (220, 220, 220)
HEALTH_RED = (220, 0, 0)
HEALTH_BG = (80, 0, 0)
ATTACK_YELLOW = (255, 200, 0)
COOLDOWN_BLUE = (0, 80, 160)

# --- Tile Map (25 columns x 20 rows) ---
# 0 = floor, 1 = wall
TILE_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


class Player:
    def __init__(self, x, y):
        self.x = x  # tile x
        self.y = y  # tile y
        self.color = PLAYER_BLUE
        self.speed = 1
        self.health = 10
        self.max_health = 10
        self.damage_cooldown = 0  # frames until player can be hurt again
        self.facing = "down"      # last movement direction
        self.attack_timer = 0     # cooldown: frames until next attack
        self.attacking = False    # currently showing attack animation?
        self.attack_frame = 0     # frames left in attack animation

    def move(self, dx, dy, tile_map):
        """Try to move by (dx, dy) tiles. Update facing direction."""
        # Update facing regardless of whether we can move
        if dx == 1:
            self.facing = "right"
        elif dx == -1:
            self.facing = "left"
        elif dy == -1:
            self.facing = "up"
        elif dy == 1:
            self.facing = "down"

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            if tile_map[new_y][new_x] == 0:
                self.x = new_x
                self.y = new_y

    def attack(self, enemies):
        """Attack the tile in front of the player. Damages any enemy there."""
        if self.attack_timer > 0:
            return  # Still cooling down

        self.attack_timer = 30  # 0.5 second cooldown at 60 FPS
        self.attacking = True
        self.attack_frame = 6   # Show animation for 6 frames

        # Find the target tile
        tx, ty = self.x, self.y
        if self.facing == "up":
            ty -= 1
        elif self.facing == "down":
            ty += 1
        elif self.facing == "left":
            tx -= 1
        elif self.facing == "right":
            tx += 1

        # Check if any enemy is on that tile
        for enemy in enemies:
            if enemy.x == tx and enemy.y == ty and enemy.health > 0:
                enemy.take_damage(3)

    def update(self):
        """Tick down cooldown timers."""
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.attack_frame > 0:
            self.attack_frame -= 1
        else:
            self.attacking = False

    def draw(self, screen, camera_x, camera_y):
        """Draw the player."""
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y

        # Flash white when recently damaged
        color = self.color
        if self.damage_cooldown > 50:
            color = WHITE

        pygame.draw.rect(screen, color, (px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    def draw_attack(self, screen, camera_x, camera_y):
        """Draw the attack animation (yellow flash on target tile)."""
        if not self.attacking or self.attack_frame <= 0:
            return

        tx, ty = self.x, self.y
        if self.facing == "up":
            ty -= 1
        elif self.facing == "down":
            ty += 1
        elif self.facing == "left":
            tx -= 1
        elif self.facing == "right":
            tx += 1

        ax = tx * TILE_SIZE - camera_x
        ay = ty * TILE_SIZE - camera_y
        pygame.draw.rect(screen, ATTACK_YELLOW, (ax + 4, ay + 4, TILE_SIZE - 8, TILE_SIZE - 8))


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.move_timer = 0
        self.hit_flash = 0      # frames of white flash remaining
        self.death_timer = -1    # -1 means alive; > 0 means playing death animation

        if enemy_type == "zombie":
            self.color = ZOMBIE_GREEN
            self.health = 3
            self.move_delay = 30
        elif enemy_type == "skeleton":
            self.color = SKELETON_WHITE
            self.health = 5
            self.move_delay = 20

    def take_damage(self, amount):
        """Reduce health and trigger visual effects."""
        self.health -= amount
        self.hit_flash = 5
        if self.health <= 0:
            self.death_timer = 10  # Death animation lasts 10 frames

    def is_alive(self):
        """Returns True if enemy is still active (alive or dying)."""
        if self.health > 0:
            return True
        return self.death_timer > 0  # Still around during death animation

    def update(self, tile_map, player):
        """Move the enemy and tick timers."""
        # Tick visual effect timers
        if self.hit_flash > 0:
            self.hit_flash -= 1

        if self.death_timer > 0:
            self.death_timer -= 1
            return  # Don't move while dying

        if self.health <= 0:
            return  # Dead, waiting to be removed

        # Movement AI
        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return

        self.move_timer = 0
        dx, dy = 0, 0

        if self.enemy_type == "zombie":
            direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            dx, dy = direction

        elif self.enemy_type == "skeleton":
            if player.x > self.x:
                dx = 1
            elif player.x < self.x:
                dx = -1
            elif player.y > self.y:
                dy = 1
            elif player.y < self.y:
                dy = -1

        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            if tile_map[new_y][new_x] == 0:
                self.x = new_x
                self.y = new_y

    def draw(self, screen, camera_x, camera_y):
        """Draw the enemy with hit flash and death effects."""
        if self.health <= 0 and self.death_timer <= 0:
            return  # Fully dead, don't draw

        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y

        # Pick the color
        color = self.color
        if self.health <= 0:
            # Death animation: rapid flash between white and normal color
            color = WHITE if self.death_timer % 2 == 0 else self.color
        elif self.hit_flash > 0:
            color = WHITE

        pygame.draw.rect(screen, color, (px + 4, py + 4, TILE_SIZE - 8, TILE_SIZE - 8))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Crawler")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)

        self.tile_map = TILE_MAP
        self.player = Player(2, 2)
        self.enemies = []
        self.spawn_enemies()
        self.camera_x = 0
        self.camera_y = 0
        self.kill_count = 0
        self.running = True
        self.game_over = False

    def spawn_enemies(self):
        """Place enemies on floor tiles."""
        self.enemies = []
        # Zombies
        self.enemies.append(Enemy(7, 8, "zombie"))
        self.enemies.append(Enemy(11, 4, "zombie"))
        self.enemies.append(Enemy(3, 15, "zombie"))
        # Skeletons
        self.enemies.append(Enemy(20, 16, "skeleton"))
        self.enemies.append(Enemy(12, 14, "skeleton"))

    def restart(self):
        """Reset the game to its initial state."""
        self.player = Player(2, 2)
        self.enemies = []
        self.spawn_enemies()
        self.kill_count = 0
        self.game_over = False

    def handle_input(self):
        """Process events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.restart()
                else:
                    if event.key == pygame.K_UP:
                        self.player.move(0, -1, self.tile_map)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(0, 1, self.tile_map)
                    elif event.key == pygame.K_LEFT:
                        self.player.move(-1, 0, self.tile_map)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(1, 0, self.tile_map)
                    elif event.key == pygame.K_SPACE:
                        self.player.attack(self.enemies)

    def update(self):
        """Update game state each frame."""
        if self.game_over:
            return

        # Update player timers
        self.player.update()

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.tile_map, self.player)

        # Remove fully dead enemies (death animation finished)
        before = len(self.enemies)
        self.enemies = [e for e in self.enemies if e.is_alive()]
        self.kill_count += before - len(self.enemies)

        # Check enemy-player collision (only living enemies deal damage)
        for enemy in self.enemies:
            if enemy.health <= 0:
                continue  # Dying enemies don't hurt you
            if enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.damage_cooldown <= 0:
                    self.player.health -= 1
                    self.player.damage_cooldown = 60

        # Check for player death
        if self.player.health <= 0:
            self.game_over = True

        # Camera follows player
        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

    def draw(self):
        """Draw the tile map, entities, effects, and HUD."""
        self.screen.fill(BLACK)

        # Draw tiles
        for row in range(len(self.tile_map)):
            for col in range(len(self.tile_map[row])):
                sx = col * TILE_SIZE - self.camera_x
                sy = row * TILE_SIZE - self.camera_y
                if sx < -TILE_SIZE or sx > SCREEN_WIDTH:
                    continue
                if sy < -TILE_SIZE or sy > SCREEN_HEIGHT:
                    continue

                tile = self.tile_map[row][col]
                if tile == 1:
                    pygame.draw.rect(self.screen, BROWN, (sx, sy, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(self.screen, DARK_GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))

        # Draw attack animation (behind enemies so it looks like a slash)
        self.player.draw_attack(self.screen, self.camera_x, self.camera_y)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        # Draw player
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # --- HUD ---
        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10
        health_ratio = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, HEALTH_BG, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, HEALTH_RED, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

        # Attack cooldown bar (small blue bar under health)
        cooldown_width = 100
        cooldown_height = 8
        if self.player.attack_timer > 0:
            cooldown_ratio = self.player.attack_timer / 30
            pygame.draw.rect(self.screen, COOLDOWN_BLUE,
                             (bar_x, bar_y + bar_height + 4, int(cooldown_width * cooldown_ratio), cooldown_height))

        # HP text
        hp_text = self.font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))

        # Kill counter
        kill_text = self.font.render(f"Kills: {self.kill_count}", True, WHITE)
        self.screen.blit(kill_text, (bar_x + bar_width + 10, bar_y + 25))

        # Position
        pos_text = self.font.render(f"Pos: ({self.player.x}, {self.player.y})", True, WHITE)
        self.screen.blit(pos_text, (10, 50))

        # Facing indicator
        face_text = self.font.render(f"Facing: {self.player.facing}", True, WHITE)
        self.screen.blit(face_text, (10, 75))

        # Game over overlay
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.big_font.render("GAME OVER", True, HEALTH_RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(game_over_text, text_rect)

            kills_text = self.font.render(f"Enemies defeated: {self.kill_count}", True, WHITE)
            kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            self.screen.blit(kills_text, kills_rect)

            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
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
