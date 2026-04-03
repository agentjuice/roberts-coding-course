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

    def move(self, dx, dy, tile_map):
        """Try to move by (dx, dy) tiles. Only move if the target tile is floor."""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            if tile_map[new_y][new_x] == 0:
                self.x = new_x
                self.y = new_y

    def update(self):
        """Tick down cooldown timers."""
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

    def draw(self, screen, camera_x, camera_y):
        """Draw the player as a colored rectangle."""
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        # Flash white when recently damaged
        color = self.color
        if self.damage_cooldown > 50:
            color = WHITE
        pygame.draw.rect(screen, color, (px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4))


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.move_timer = 0

        if enemy_type == "zombie":
            self.color = ZOMBIE_GREEN
            self.health = 3
            self.move_delay = 30  # moves every 30 frames
        elif enemy_type == "skeleton":
            self.color = SKELETON_WHITE
            self.health = 5
            self.move_delay = 20  # moves every 20 frames

    def update(self, tile_map, player):
        """Move the enemy based on its AI type."""
        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return

        self.move_timer = 0
        dx, dy = 0, 0

        if self.enemy_type == "zombie":
            # Random wandering
            direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            dx, dy = direction

        elif self.enemy_type == "skeleton":
            # Chase the player: pick one axis to move on
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
        """Draw the enemy."""
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        pygame.draw.rect(screen, self.color, (px + 4, py + 4, TILE_SIZE - 8, TILE_SIZE - 8))


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
        self.running = True
        self.game_over = False

    def spawn_enemies(self):
        """Place enemies on floor tiles away from the player."""
        self.enemies = []
        # Zombie in the central area
        self.enemies.append(Enemy(7, 8, "zombie"))
        self.enemies.append(Enemy(11, 4, "zombie"))
        # Skeleton in the bottom rooms
        self.enemies.append(Enemy(20, 16, "skeleton"))
        self.enemies.append(Enemy(12, 14, "skeleton"))

    def restart(self):
        """Reset the game to its initial state."""
        self.player = Player(2, 2)
        self.enemies = []
        self.spawn_enemies()
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

    def update(self):
        """Update game state each frame."""
        if self.game_over:
            return

        # Update player cooldowns
        self.player.update()

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.tile_map, self.player)

        # Check enemy-player collision
        for enemy in self.enemies:
            if enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.damage_cooldown <= 0:
                    self.player.health -= 1
                    self.player.damage_cooldown = 60  # 1 second invincibility

        # Check for death
        if self.player.health <= 0:
            self.game_over = True

        # Camera follows player
        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

    def draw(self):
        """Draw the tile map, entities, and HUD."""
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
        # Health text
        hp_text = self.font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))

        # Position
        pos_text = self.font.render(f"Pos: ({self.player.x}, {self.player.y})", True, WHITE)
        self.screen.blit(pos_text, (10, 40))

        # Game over overlay
        if self.game_over:
            # Dark overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.big_font.render("GAME OVER", True, HEALTH_RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(game_over_text, text_rect)

            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
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
