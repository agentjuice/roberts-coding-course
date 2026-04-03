# Lesson 26: Dungeon v7 -- Sprites & Art

!!! success "🎯 Mission"
    Replace all those colored squares with actual character sprites -- drawn in code so you don't need any image files.


## What's a Sprite?

Up until now, our player was a blue square, enemies were red and green squares, and the walls were brown rectangles. That works for testing, but it doesn't exactly look like a real game.

In game development, a **sprite** is an image that represents something in your game -- the player character, an enemy, a floor tile, anything. Every character in Fortnite, every block in Minecraft, every kart in Mario Kart — they're all sprites (or their 3D equivalent, models). We're making 2D sprites, which is how classic games like the original Zelda did it. Usually sprites are loaded from PNG files. But here's the thing: we don't have any PNG files yet. So we're going to *create* our sprites using code, which is actually pretty cool.

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
player_image = pygame.transform.scale(player_image, (32, 32))
```

In our code, we have a helper function that tries to load a file and falls back to the generated sprite if the file doesn't exist:

```python
def try_load_sprite(filename, fallback_surface):
    try:
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, fallback_surface.get_size())
        print(f"Loaded sprite: {filename}")
        return img
    except (pygame.error, FileNotFoundError):
        return fallback_surface
```

This is really nice because it means you can start with the code-generated sprites, and whenever you make real art, just drop it in the right folder and the game picks it up automatically. No code changes needed.

## Step-by-Step Build

### Step 1: Sprite creation functions

At the top of the file (after constants), add all the `create_*` functions:
- `create_player_sprite(facing_right)` -- draws the knight
- `create_enemy_sprite(enemy_type)` -- draws zombie or skeleton
- `create_boss_sprite()` -- draws the 64x64 demon king
- `create_tile_sprites()` -- returns a dictionary of tile surfaces
- `create_item_sprites()` -- returns a dictionary of item surfaces
- `try_load_sprite(filename, fallback)` -- tries file, uses fallback

### Step 2: Create sprites in Game.__init__

```python
self.sprites = {}
self.sprites["player_right"] = create_player_sprite(facing_right=True)
self.sprites["player_left"] = create_player_sprite(facing_right=False)
self.sprites["zombie"] = create_enemy_sprite("zombie")
self.sprites["skeleton"] = create_enemy_sprite("skeleton")
self.sprites["boss"] = create_boss_sprite()
self.sprites["tiles"] = create_tile_sprites()
self.sprites["items"] = create_item_sprites()
```

### Step 3: Pass sprites to game objects

When creating a Player, Enemy, Boss, or Item, pass the relevant sprites so each object knows what to draw:

```python
self.player = Player(x, y, {"player_right": ..., "player_left": ...})
enemy = Enemy("zombie", x, y, {"zombie": ..., "skeleton": ...})
```

### Step 4: Use sprites in draw methods

Instead of `pygame.draw.rect(screen, self.color, ...)`, now do:

```python
screen.blit(self.sprite, (px, py))
```

For the player, pick the sprite based on facing:

```python
if self.facing == "left":
    sprite = self.sprite_left
else:
    sprite = self.sprite_right
```

### Step 5: Hit flash effect with sprites

When an enemy gets hit, we want a white flash. Here's the trick:

```python
if self.hit_flash > 0:
    flash = self.sprite.copy()
    flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
    screen.blit(flash, (px, py))
```

`BLEND_ADD` adds white to every pixel, making the whole sprite look bright. Then next frame it goes back to normal. It's the same "flash white when hit" idea from before, but now it works with sprites instead of just changing a rectangle's color.

### The Full Game

The complete file is `dungeon.py` in this folder. It has all the sprite creation functions, all the game classes (Player, Enemy, Boss, Item, Room, Game), and the full 5-room dungeon.

## Run It!

```bash
python3 dungeon.py
```

Use arrow keys to move, Space to attack, 1-5 for items. You should see actual character shapes instead of colored squares. The walls have a brick pattern, the floor has texture, and items have distinct shapes.

## Experiments

1. **Change the player's tunic color.** In `create_player_sprite`, change `(0, 100, 220)` to `(220, 0, 0)` for a red tunic, or `(0, 180, 0)` for green.

2. **Make the zombie scarier.** Add more details to `create_enemy_sprite` -- maybe draw sharp teeth or bigger arms.

3. **Try pygame.transform.scale.** Create the boss at 32x32 and then scale it up to 64x64: `pygame.transform.scale(small_boss, (64, 64))`. Notice how it gets pixelated -- that's the retro look!

4. **Add a face to the floor tiles.** Draw a tiny smiley on the floor sprite. Now every tile has a face. Creepy dungeon.

5. **Create your own item sprite.** Add a "shield" item type with a shield shape (maybe a rounded rectangle with a cross on it).

## Challenge

Create a `create_player_sprite_up()` and `create_player_sprite_down()` function that shows the player from behind (walking up) and from the front (walking down). Use them when `self.facing` is `"up"` or `"down"`. Hint: for the "up" version, don't draw the eye -- just the back of the helmet.

## What's Next

👉 [Go to #27 — Dungeon: Sound & Music](../27-dungeon-v8-sound/lesson.md)