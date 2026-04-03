# Lesson 18: Dungeon v9 -- Procedural Generation

**Goal:** Make every playthrough different by generating dungeons randomly with code instead of designing them by hand.

## What Is Procedural Generation?

Up until now, every time you played Robert's Dungeons, the rooms were exactly the same. Same walls, same enemy positions, same chests. That works, but real dungeon crawlers like Minecraft Dungeons, Hades, and Spelunky are different every time you play. How do they pull that off?

**Procedural generation** is when a computer program builds game content using an algorithm (a set of steps) instead of a human designing it by hand. Instead of you typing out a tile map, you write code that *creates* the tile map.

Think of it like this: instead of drawing a maze on paper, you write instructions for *how* to draw a maze. Then the computer follows those instructions and makes a brand new maze every single time.

## The Algorithm

Our dungeon generator follows these steps:

1. Start with a big grid filled entirely with walls
2. Pick random spots to place rectangular rooms (5-10 tiles wide, 5-8 tiles tall)
3. Make sure rooms don't overlap -- check before placing each one
4. Connect rooms with L-shaped corridors between their centers
5. Place doors where corridors meet room edges
6. Scatter enemies in rooms (2-4 per room)
7. Put chests in a couple random rooms
8. First room = player start, last room = boss room

Let's walk through each piece.

## Step 1: Start with Walls

```python
MAP_W = 60
MAP_H = 45
tile_map = [[WALL for _ in range(MAP_W)] for _ in range(MAP_H)]
```

A 60x45 grid where every single tile is a wall. We'll "carve out" rooms and corridors from this solid block. You know how sculptors say the statue is already inside the block of marble? Same energy here.

## Step 2: Place Rooms

A room is just a rectangle. We define it with position (x, y) and size (w, h):

```python
class DungeonRoom:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center_x = x + w // 2
        self.center_y = y + h // 2
```

To place a room, we pick a random position and size, check if it overlaps with any existing room, and if not, carve it out:

```python
w = rng.randint(5, 10)
h = rng.randint(5, 8)
x = rng.randint(1, MAP_W - w - 1)
y = rng.randint(1, MAP_H - h - 1)

new_room = DungeonRoom(x, y, w, h)

# Check for overlap
overlaps = False
for existing in rooms:
    if new_room.intersects(existing, padding=2):
        overlaps = True
        break

if not overlaps:
    rooms.append(new_room)
    # Carve out floor tiles
    for row in range(y, y + h):
        for col in range(x, x + w):
            tile_map[row][col] = FLOOR
```

The `intersects` method checks if two rectangles overlap, with some padding so rooms aren't squished right up against each other:

```python
def intersects(self, other, padding=1):
    return (self.x - padding < other.x + other.w and
            self.x + self.w + padding > other.x and
            self.y - padding < other.y + other.h and
            self.y + self.h + padding > other.y)
```

## Step 3: Connect Rooms with Corridors

Rooms by themselves are islands -- you can't get from one to another. We need corridors to connect them.

The simplest approach: connect each room to the next one in the list with an **L-shaped corridor**. Go horizontal from room 1's center to room 2's column, then vertical to room 2's center:

```python
for i in range(len(rooms) - 1):
    r1 = rooms[i]
    r2 = rooms[i + 1]

    # Horizontal tunnel
    for col in range(min(r1.center_x, r2.center_x), max(r1.center_x, r2.center_x) + 1):
        tile_map[r1.center_y][col] = FLOOR
        tile_map[r1.center_y + 1][col] = FLOOR  # 2 tiles wide

    # Vertical tunnel
    for row in range(min(r1.center_y, r2.center_y), max(r1.center_y, r2.center_y) + 1):
        tile_map[row][r2.center_x] = FLOOR
        tile_map[row][r2.center_x + 1] = FLOOR
```

We make corridors 2 tiles wide so the player doesn't feel claustrophobic.

## Seeds: Same Dungeon Every Time

Here's a really cool trick. Computers can't actually be truly random -- they use formulas that *look* random. If you give the formula the same starting number (called a **seed**), you get the exact same sequence of "random" numbers every time.

```python
rng = random.Random(seed)
```

We create our own random number generator with a specific seed. If you use seed 12345, you'll get the same dungeon every time. Seed 99999 gives a totally different dungeon -- but the same one every time you use 99999.

This is how games let you share "world seeds" with friends. You know how in Minecraft the seed determines the entire world? Same idea here.

Our title screen lets you type in a seed number or leave it blank for a random one. The seed is printed in the terminal and shown on the HUD so you can share cool dungeons with people.

## One Big Map

Previous versions had separate room screens with door transitions. Now the entire dungeon is one big map. The player walks from room to room through corridors without any loading or transitions. The camera just follows the player smoothly across the whole dungeon.

This is actually simpler in some ways (no room transition code) but means enemies from all rooms exist on the map at once. We only create enemies at dungeon generation time, and they all update every frame. For our dungeon size this is totally fine -- there are maybe 15-20 enemies total.

## Step-by-Step Build

### Step 1: DungeonRoom class and generate_dungeon function

The `DungeonRoom` class stores position and size. The `generate_dungeon(seed)` function does all the heavy lifting and returns everything the game needs:

```python
def generate_dungeon(seed):
    # Returns: (tile_map, enemy_list, chest_positions,
    #           player_start, boss_pos, room_rects)
```

### Step 2: Title screen for seed input

Add a `"title"` state to the Game class. On this screen, the player can type a seed number or press Enter for a random dungeon.

```python
if self.state == "title":
    if event.key == pygame.K_RETURN:
        if self.seed_input.strip():
            seed = int(self.seed_input.strip())
        else:
            seed = None  # Random
        self.start_game(seed)
```

### Step 3: start_game method

This calls `generate_dungeon()` and creates all the game objects:

```python
def start_game(self, seed=None):
    if seed is None:
        seed = random.randint(1, 999999)
    self.seed = seed
    print(f"Dungeon seed: {self.seed}")

    result = generate_dungeon(self.seed)
    self.tile_map, enemy_data, chest_pos, player_start, boss_pos, self.dungeon_rooms = result

    # Create enemies, boss, player from the generated data
    ...
```

### Step 4: Exploration tracking

Instead of tracking room visits by index, we check which room rectangle contains the player:

```python
def update_explored(self):
    for i, room in enumerate(self.dungeon_rooms):
        if (room.x <= self.player.x < room.x + room.w and
                room.y <= self.player.y < room.y + room.h):
            self.explored.add(i)
            break
```

### Step 5: Minimap shows explored rooms

The minimap scales all room rectangles to fit in a small corner display. Explored rooms are colored; unexplored ones are dim. A green dot shows the player's position.

### Step 6: Optimize tile drawing

With a 60x45 map, we only draw tiles that are visible on screen:

```python
start_col = max(0, self.camera_x // TILE_SIZE - 1)
end_col = min(map_w, (self.camera_x + SCREEN_WIDTH) // TILE_SIZE + 2)
```

This way we draw maybe 27x20 tiles per frame instead of all 2700. Way faster.

### The Full Game

The complete file is `dungeon.py` in this folder. It has the dungeon generator, all sprites, sound support, and the full game with title screen.

## Run It!

```bash
python3 dungeon.py
```

You'll see a title screen where you can enter a seed number. Press Enter. The dungeon generates and you're dropped in. Look at the minimap in the top-right corner to see the rooms you've explored. Check the terminal for the seed number.

Try entering seed `42` -- you'll always get the same dungeon. Try `12345` for a different one. Leave it blank and get a surprise.

Controls: Arrow keys to move, Space to attack, 1-5 for items, +/- for volume, Esc to quit.

## Experiments

1. **Try different seeds.** Enter seeds 1, 100, 999, 12345, and 555555. Notice how different the layouts are. Find a seed you like and share it!

2. **Change room count.** In `generate_dungeon`, change `target_rooms = rng.randint(6, 8)` to `rng.randint(10, 15)` for a much bigger dungeon. Or try `3, 4` for a tiny one.

3. **Change room sizes.** Make rooms bigger (`rng.randint(8, 15)`) or smaller (`rng.randint(3, 5)`). Bigger rooms feel like arenas; smaller ones feel like closets.

4. **More enemies per room.** Change `num_enemies = rng.randint(2, 4)` to `rng.randint(5, 8)` for a real challenge.

5. **Add more chests.** Change the chest placement to put one in every room. You'll be swimming in loot.

## Challenge

Add a **difficulty selector** on the title screen. Before entering a seed, let the player press 1 for Easy, 2 for Normal, or 3 for Hard. Easy means fewer enemies (1-2 per room) and more chests. Hard means more enemies (4-6 per room), the boss has 75 HP instead of 50, and player starts with only 7 health. Show the difficulty on the HUD.

## What's Next

In Lesson 19, we'll add a second level, new enemy types, a start screen, pause menu, and polish effects like screen shake and particles.
