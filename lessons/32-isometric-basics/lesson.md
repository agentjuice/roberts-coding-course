# Isometric Basics

!!! success "🎯 Mission"
    Learn what isometric perspective is and build a scrollable diamond-shaped grid -- the foundation for making your dungeon look like Minecraft Dungeons.

## What Is Isometric?

You know how in Minecraft Dungeons, you look down at the world from an angle? Everything looks 3D, but you can't rotate the camera -- it's always that same tilted view. That's **isometric perspective**.

It's a trick. The game is still 2D (flat images on your screen), but by drawing everything at an angle, it *looks* 3D. Your dungeon goes from looking like a boring checkerboard to looking like an actual place you could walk around in.

Other games that use isometric view: Hades, Diablo, Animal Crossing (sort of), and the original Pokemon Mystery Dungeon.

## The Magic Math

Here's the big idea. Right now, converting a grid position to screen position is simple:

```python
screen_x = grid_x * tile_size
screen_y = grid_y * tile_size
```

That gives you a flat, top-down grid. Boring. For isometric, we use two different formulas:

```python
screen_x = (grid_x - grid_y) * (tile_width // 2)
screen_y = (grid_x + grid_y) * (tile_height // 2)
```

**Why does this work?** The subtraction in screen_x makes the grid slant sideways -- moving right on the grid goes down-right on screen. The addition in screen_y makes everything stack diagonally. Together, your square grid becomes a diamond.

The `tile_width` is usually twice the `tile_height`. A common size is 64 wide by 32 tall -- this gives you that classic isometric diamond shape.

## Step by Step

Here's what [`isometric_grid.py`](isometric_grid.py) builds:

1. **Grid setup** -- a 2D list where some tiles are colored differently
2. **Iso conversion function** -- the math that turns grid positions into screen positions
3. **Diamond tile drawing** -- each tile is drawn as a diamond (4-point polygon)
4. **Scrolling camera** -- use arrow keys to pan around the grid
5. **Grid coordinates display** -- hover over tiles to see their grid position

## The Code

```python
python3 isometric_grid.py
```

Use **arrow keys** to scroll around the grid. Hover your mouse over tiles to see their grid coordinates. The green tiles are randomly placed -- every time you run it, the pattern changes.

## Why Diamonds?

In a normal top-down view, each tile is a square. In isometric view, that square gets rotated 45 degrees and squished vertically. That's why each tile looks like a diamond. It's the same grid, just viewed from an angle.

Think of it like looking at a chess board from the corner instead of straight above. The squares become diamonds, but the grid is still 8x8.

## Experiments

1. **Bigger grid** -- change `GRID_SIZE` to 30 and scroll around. How does it feel compared to a flat grid?
2. **Checkerboard** -- color tiles based on `(grid_x + grid_y) % 2` to make an isometric checkerboard pattern.
3. **Height preview** -- for green tiles, draw the diamond 10 pixels higher than normal. Notice how it starts to look like a raised platform?
4. **Tile sizes** -- try `TILE_WIDTH = 128, TILE_HEIGHT = 64`. Bigger tiles! Then try `96x48`. How does the aspect ratio change the feel?
5. **Click to paint** -- add click detection: when you click a tile, toggle its color between green and gray. You'll need to reverse the isometric formula (this is tricky!).

## Challenge

Add **elevation**. Give some tiles a `height` value of 1 or 2. Draw those tiles higher on the screen (subtract `height * 16` from their screen_y). Then draw the sides of the raised tiles as darker rectangles to make them look like 3D blocks. You're basically building Minecraft at this point.

## What's Next

👉 [Isometric Dungeon](../33-isometric-dungeon/lesson.md) -- time to render your actual dungeon map in isometric view!
