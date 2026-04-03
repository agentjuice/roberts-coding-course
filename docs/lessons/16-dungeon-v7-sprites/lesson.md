# Lesson 16: Dungeon v7 -- Sprites & Art

**Goal:** Replace all those colored squares with actual character sprites -- drawn in code so you don't need any image files.

## What's a Sprite?

Up until now, our player was a blue square, enemies were red and green squares, and the walls were brown rectangles. That works for testing, but it doesn't exactly look like a real game.

In game development, a **sprite** is an image that represents something in your game -- the player character, an enemy, a floor tile, anything. Usually sprites are loaded from PNG files. But here's the thing: we don't have any PNG files yet. So we're going to *create* our sprites using code, which is actually pretty cool.

The trick is **pygame.Surface**. Think of a Surface as a little canvas you can draw on. The screen itself is a Surface. But you can also create *new* Surfaces, draw on them, and then paste them onto the screen. That's exactly what a sprite is -- a mini canvas with a picture on it.

```python
# Create a 32x32 transparent surface
sprite = pygame.Surface((32, 32), pygame.SRCALPHA)

# Draw on it just like you draw on the screen
pygame.draw.circle(sprite, (255, 0, 0), (16, 16), 12)

# Later, paste it onto the screen
screen.blit(sprite, (100, 200))
```

The `pygame.SRCALPHA` flag means the surface supports transparency. Without it, the background of your sprite would be a solid black rectangle, which would look terrible -- imagine every character walking around with a black box behind them.

!!! tip "💡 Pro Tip"
    Always use `pygame.SRCALPHA` when creating sprite surfaces. Without it, you get ugly black boxes around your characters instead of transparency. It's the single most common "why does my sprite look wrong?" mistake.

!!! info "🎮 Fun Fact"
    In early NES games like the original Super Mario Bros, sprites were only 16x16 pixels -- half the size of ours! Mario's entire character was drawn in a 16x16 grid with just 3 colors. Constraints breed creativity.

## Drawing a Character

Let's think about what a tiny pixel-art character looks like at 32x32 pixels. You don't have much room, so keep it simple:

- A round head (circle)
- A rectangular body
- Two small legs
- Maybe a sword

Here's our player sprite function:

```python
def create_player_sprite(facing_right=True):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Body (blue tunic)
    pygame.draw.rect(surf, (0, 100, 220), (8, 14, 16, 12))
    # Head (skin color)
    pygame.draw.circle(surf, (240, 200, 160), (16, 10), 7)
    # Eye
    eye_x = 18 if facing_right else 12
    pygame.draw.circle(surf, (0, 0, 0), (eye_x, 9), 2)
    # Helmet
    pygame.draw.rect(surf, (120, 120, 140), (9, 3, 14, 5))
    # Legs
    pygame.draw.rect(surf, (60, 60, 80), (10, 26, 5, 5))
    pygame.draw.rect(surf, (60, 60, 80), (17, 26, 5, 5))
    # Sword
    if facing_right:
        pygame.draw.rect(surf, (200, 200, 220), (26, 8, 3, 14))
        pygame.draw.rect(surf, (180, 160, 60), (24, 18, 7, 3))
    else:
        pygame.draw.rect(surf, (200, 200, 220), (3, 8, 3, 14))
        pygame.draw.rect(surf, (180, 160, 60), (1, 18, 7, 3))

    return surf
```

Notice how we call it twice -- once with `facing_right=True` and once with `facing_right=False`. That gives us two versions of the player sprite. When the player walks left, we show the left-facing one. When they walk right, we show the right-facing one.

You could also use **pygame.transform.flip** to mirror a sprite instead of drawing both versions by hand:

```python
sprite_left = pygame.transform.flip(sprite_right, True, False)
```

The `True, False` means "flip horizontally, but not vertically." We manually drew both versions instead so the sword ends up on the correct side, but flipping is a handy shortcut when you don't need that level of control.

## Tile Sprites

Tiles get the same treatment. Instead of plain colored rectangles, we draw little patterns:

- **Floor tiles** get a subtle grid pattern and some specks -- looks like stone
- **Wall tiles** get a brick pattern with mortar lines
- **Door tiles** look like wooden planks with a gold handle
- **Chest tiles** show a little treasure chest

The wall sprite is a good example of how a few lines make a huge difference:

```python
wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
wall.fill((110, 65, 25))
# Horizontal mortar lines
pygame.draw.line(wall, (80, 50, 20), (0, 8), (TILE_SIZE, 8), 1)
pygame.draw.line(wall, (80, 50, 20), (0, 16), (TILE_SIZE, 16), 1)
pygame.draw.line(wall, (80, 50, 20), (0, 24), (TILE_SIZE, 24), 1)
# Offset vertical lines for brick pattern
pygame.draw.line(wall, (80, 50, 20), (16, 0), (16, 8), 1)
pygame.draw.line(wall, (80, 50, 20), (8, 8), (8, 16), 1)
```

Just a few lines of code and suddenly you have bricks instead of a brown blob. That's the magic of sprites -- a little detail goes a long way.

## Loading Real Images (Optional)

If you ever DO have PNG files (maybe you draw some pixel art in Aseprite or Piskel), loading them is easy:

```python
player_image = pygame.image.load("assets/player.png").convert_alpha()
```

The `.convert_alpha()` keeps transparency working. You can resize with:

```python
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
```

For now though, our code-drawn sprites look great and we don't need any external files. That's actually a big advantage -- the game is totally self-contained.

## Enemy Sprites

Each enemy type gets its own look:

- **Zombie** -- green body, dark clothes, lurching posture
- **Skeleton** -- white bones, visible ribcage, no skin
- **Boss** -- bigger (48x48 instead of 32x32), red eyes, horns, cape

The boss is drawn on a larger surface to make it feel more intimidating:

```python
def create_boss_sprite():
    surf = pygame.Surface((48, 48), pygame.SRCALPHA)
    # ... draw a fearsome boss
    return surf
```

## Item Sprites

Items are drawn small (16x16) and then placed on a 32x32 surface:

- **Health potion** -- red liquid in a flask shape
- **Speed boost** -- yellow lightning bolt
- **Power sword** -- glowing blue blade
- **Shield** -- rounded shape with a cross

```python
def create_item_sprite(item_type):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    if item_type == "health_potion":
        # Draw a flask with red liquid
        ...
    elif item_type == "speed_boost":
        # Draw a lightning bolt
        ...
```

## Step-by-Step Build

### Step 1: Sprite creation functions

Add all the `create_*_sprite()` functions at the top of your file, after the constants. These are plain functions, not methods -- they just return pygame Surfaces.

### Step 2: Cache sprites in Game.__init__

Create all sprites once when the game starts, not every frame:

```python
self.sprites = {
    "player_right": create_player_sprite(True),
    "player_left": create_player_sprite(False),
    "zombie": create_enemy_sprite("zombie"),
    "skeleton": create_enemy_sprite("skeleton"),
    "boss": create_boss_sprite(),
    "wall": create_wall_sprite(),
    "floor": create_floor_sprite(),
    "door": create_door_sprite(),
}
```

### Step 3: Use sprites in draw methods

Replace all `pygame.draw.rect(screen, color, rect)` calls with `screen.blit(sprite, position)`:

```python
# Old way
pygame.draw.rect(screen, BLUE, (px, py, TILE_SIZE, TILE_SIZE))

# New way
sprite = self.sprites["player_right"] if self.player.facing == "right" else self.sprites["player_left"]
screen.blit(sprite, (px, py))
```

### Step 4: Item sprites

Create sprites for each item type and blit them when drawing inventory and dropped items.

### The Full Game

The complete file is `dungeon.py` in this folder. It includes everything from lessons 10-15 plus all the sprite code.

## Run It!

```bash
python3 dungeon.py
```

Use arrow keys to move, Space to attack, 1-5 for items. You should see actual character shapes instead of colored squares. The walls have a brick pattern, the floor has texture, and items have distinct shapes.

!!! example "🧪 Experiments"
    1. **Change the player's tunic color.** In `create_player_sprite`, change `(0, 100, 220)` to `(220, 0, 0)` for a red tunic, or `(0, 180, 0)` for green.

    2. **Make the zombie scarier.** Add more details to `create_enemy_sprite` -- maybe draw sharp teeth or bigger arms.

    3. **Try pygame.transform.scale.** Create the boss at 32x32 and then scale it up to 64x64: `pygame.transform.scale(small_boss, (64, 64))`. Notice how it gets pixelated -- that's the retro look!

    4. **Add a face to the floor tiles.** Draw a tiny smiley on the floor sprite. Now every tile has a face. Creepy dungeon.

    5. **Create your own item sprite.** Add a "shield" item type with a shield shape (maybe a rounded rectangle with a cross on it).

!!! abstract "🏆 Challenge"
    Create a `create_player_sprite_up()` and `create_player_sprite_down()` function that shows the player from behind (walking up) and from the front (walking down). Use them when `self.facing` is `"up"` or `"down"`. Hint: for the "up" version, don't draw the eye -- just the back of the helmet.

## What's Next

In Lesson 17, we'll add sound effects and music to bring the dungeon to life -- sword clangs, enemy grunts, and boss battle music.
