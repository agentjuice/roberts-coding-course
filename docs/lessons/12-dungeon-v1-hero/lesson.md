# Lesson 12: Dungeon v1 -- The Hero

!!! success "🎯 Mission"
    Build a tile-based dungeon world with a player that moves around and a camera that follows them.


![Your first dungeon — you're the blue square!](/images/dungeon_v1.png)


## How Tile Maps Work

In the Snake game, everything lived on one screen. But real dungeon crawlers have big worlds you explore. So how do they pull that off?

The trick is a **tile map** -- a 2D list where each number means a different kind of tile. Think of it like graph paper where you've colored in certain squares:

```python
tile_map = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]
```

Here, `0` means floor (you can walk on it) and `1` means wall (you can't). That little map is a room with walls around it.

Each tile is `TILE_SIZE` pixels wide and tall. We'll use `TILE_SIZE = 32`, so a 25x20 map is 800x640 pixels -- bigger than our 800x600 screen. That's the whole point: the map is bigger than the screen, so we need a **camera** to show just part of it.

## Grid-Based Movement

Instead of moving pixel by pixel, our hero moves one whole tile at a time. Press Right, and the player jumps from tile (3, 5) to tile (4, 5). This keeps everything neat and lined up.

Before moving, we check: is the tile we want to move to a wall? If it is, we just don't move. That's **wall collision** -- and it's surprisingly simple.

```python
# Check if the tile at (new_x, new_y) is walkable
if tile_map[new_y][new_x] == 0:
    self.x = new_x
    self.y = new_y
```

Now here's something that trips up everyone at first: it's `tile_map[y][x]`, not `tile_map[x][y]`. The first index picks the row (y), the second picks the column (x). Keep an eye on that -- it'll bite you if you mix them up.

## The Camera

You know how in a big game, the world scrolls as your character moves? That's what the camera does. If the player is at tile (15, 10) and each tile is 32 pixels, they're at pixel (480, 320). But our screen is only 800x600. If we just drew everything starting at pixel (0, 0), the player would eventually walk right off the screen.

The fix: calculate a **camera offset**. We figure out where the player is in pixels, then subtract half the screen size so the player stays in the center:

```python
camera_x = player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
camera_y = player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2
```

Then when drawing every tile, we subtract the camera offset:

```python
screen_x = col * TILE_SIZE - camera_x
screen_y = row * TILE_SIZE - camera_y
```

The player stays in the middle, and the world scrolls around them. Pretty neat, right?

## Step-by-Step Build

### Step 1: Imports and constants

```python
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60
```

### Step 2: The tile map

We define a big map as a list of lists. Ones are walls, zeros are floors. We'll make some rooms connected by corridors.

```python
TILE_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    # ... (the full map is in dungeon.py)
]
```

### Step 3: The Player class

```python
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 150, 255)
        self.speed = 1

    def move(self, dx, dy, tile_map):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if tile_map[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        pygame.draw.rect(screen, self.color, (px + 2, py + 2, TILE_SIZE - 4, TILE_SIZE - 4))
```

The `+ 2` and `- 4` make the player slightly smaller than a tile so you can see the floor underneath. It looks way better.

### Step 4: The Game class

The Game class holds everything together: the screen, the map, the player, and the game loop.

```python
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Crawler")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.tile_map = TILE_MAP
        self.player = Player(2, 2)
        self.camera_x = 0
        self.camera_y = 0
        self.running = True
```

### Step 5: Input handling

We handle movement in `KEYDOWN` events, which fire once per press. That way the player moves one tile each time you tap a key -- no weirdness from holding it down.

```python
def handle_input(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move(0, -1, self.tile_map)
            elif event.key == pygame.K_DOWN:
                self.player.move(0, 1, self.tile_map)
            elif event.key == pygame.K_LEFT:
                self.player.move(-1, 0, self.tile_map)
            elif event.key == pygame.K_RIGHT:
                self.player.move(1, 0, self.tile_map)
```

### Step 6: Camera update

```python
def update(self):
    self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
    self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2
```

### Step 7: Drawing

```python
def draw(self):
    self.screen.fill((0, 0, 0))

    # Draw tiles
    for row in range(len(self.tile_map)):
        for col in range(len(self.tile_map[row])):
            sx = col * TILE_SIZE - self.camera_x
            sy = row * TILE_SIZE - self.camera_y
            if -TILE_SIZE < sx < SCREEN_WIDTH and -TILE_SIZE < sy < SCREEN_HEIGHT:
                if self.tile_map[row][col] == 1:
                    pygame.draw.rect(self.screen, (100, 60, 20), (sx, sy, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50), (sx, sy, TILE_SIZE, TILE_SIZE))

    # Draw player
    self.player.draw(self.screen, self.camera_x, self.camera_y)

    # HUD
    pos_text = self.font.render(f"Position: ({self.player.x}, {self.player.y})", True, (255, 255, 255))
    self.screen.blit(pos_text, (10, 10))

    pygame.display.flip()
```

Notice the `if -TILE_SIZE < sx < SCREEN_WIDTH` check -- we skip tiles that are off-screen. No point drawing what you can't see.

### Step 8: Main loop

```python
def run(self):
    while self.running:
        self.handle_input()
        self.update()
        self.draw()
        self.clock.tick(FPS)
    pygame.quit()
    sys.exit()
```

### The Full Game

The complete file is saved as `dungeon.py` in this folder. It has a full 25x20 map with multiple rooms and corridors to explore.

## Run It!

```bash
python3 dungeon.py
```

Use the arrow keys to walk around. You should see the dungeon scroll as you move. Walls are brown, floors are dark gray, and you're the blue square.

## Experiments

1. **Make a bigger map.** Add more rows and columns to `TILE_MAP`. Make a maze! Just remember to surround it with walls.

2. **Change the player color.** Try `(255, 0, 0)` for red or `(0, 255, 0)` for green. Pick your hero's color.

3. **Speed up movement.** What happens if you change `self.speed = 1` to `self.speed = 2` in the Player class? (Hint: you might jump over walls!)

4. **Change the tile size.** Try `TILE_SIZE = 64` for a zoomed-in view or `TILE_SIZE = 16` for a zoomed-out view. The whole feel of the game changes.

5. **Add a new tile type.** Use `2` for water tiles. Draw them blue and let the player walk on them (but maybe slowly later).

## Challenge

Add a **treasure tile**. Use the number `2` in the tile map for treasure spots. Draw them as yellow squares. When the player walks onto a treasure tile, change it to `0` (regular floor) and add 1 to a score counter. Show the score in the HUD next to the position.

## What's Next

In Lesson 13, we'll add enemies that roam the dungeon -- zombies that wander randomly and skeletons that chase you down.
