import pygame
import sys

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

    def move(self, dx, dy, tile_map):
        """Try to move by (dx, dy) tiles. Only move if the target tile is floor."""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        # Check bounds
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            if tile_map[new_y][new_x] == 0:
                self.x = new_x
                self.y = new_y

    def draw(self, screen, camera_x, camera_y):
        """Draw the player as a colored rectangle."""
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        # Draw slightly smaller than a tile so floor shows around edges
        pygame.draw.rect(screen, self.color, (px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Crawler")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)

        self.tile_map = TILE_MAP
        self.player = Player(2, 2)  # Start in the top-left room
        self.camera_x = 0
        self.camera_y = 0
        self.running = True

    def handle_input(self):
        """Process events. Move player on arrow key press."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.player.move(0, -1, self.tile_map)
                elif event.key == pygame.K_DOWN:
                    self.player.move(0, 1, self.tile_map)
                elif event.key == pygame.K_LEFT:
                    self.player.move(-1, 0, self.tile_map)
                elif event.key == pygame.K_RIGHT:
                    self.player.move(1, 0, self.tile_map)

    def update(self):
        """Update camera to follow the player."""
        # Center camera on the player
        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

    def draw(self):
        """Draw the tile map, player, and HUD."""
        self.screen.fill(BLACK)

        # Draw tiles (only those visible on screen)
        for row in range(len(self.tile_map)):
            for col in range(len(self.tile_map[row])):
                sx = col * TILE_SIZE - self.camera_x
                sy = row * TILE_SIZE - self.camera_y

                # Skip tiles that are off-screen
                if sx < -TILE_SIZE or sx > SCREEN_WIDTH:
                    continue
                if sy < -TILE_SIZE or sy > SCREEN_HEIGHT:
                    continue

                tile = self.tile_map[row][col]
                if tile == 1:
                    # Wall: brown
                    pygame.draw.rect(self.screen, BROWN, (sx, sy, TILE_SIZE, TILE_SIZE))
                else:
                    # Floor: dark gray
                    pygame.draw.rect(self.screen, DARK_GRAY, (sx, sy, TILE_SIZE, TILE_SIZE))

        # Draw the player
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # HUD: player position
        pos_text = self.font.render(
            f"Position: ({self.player.x}, {self.player.y})", True, WHITE
        )
        self.screen.blit(pos_text, (10, 10))

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
