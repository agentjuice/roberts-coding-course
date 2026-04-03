# Isometric Dungeon

!!! success "🎯 Mission"
    Take your dungeon's tile map and render it in isometric view -- floors become diamonds, walls become tall blocks, and your player walks through it all like Minecraft Dungeons.

## From Flat to Isometric

In the last lesson, you drew a simple colored grid in isometric. Now we're going to take your actual dungeon -- walls, floors, doors -- and render it the same way. The grid data doesn't change at all. Only how we *draw* it changes.

This is one of the coolest things about good code structure: your `generate_map()` function doesn't care if the map is drawn top-down or isometric. It just makes the data. The rendering is separate.

## Walls Need Height

Floors are flat diamonds, just like last lesson. But walls need to look like tall blocks -- like the stone blocks in Minecraft Dungeons.

The trick: draw the **top face** of a wall at a higher position (subtract height from screen_y), then draw **side faces** connecting the top to the ground. Two side faces are enough -- the left side and the right side of the diamond.

```python
# Floor: just a diamond at ground level
# Wall: diamond drawn higher + side panels connecting to ground
wall_height = 40  # pixels tall
top_y = screen_y - wall_height
```

This creates the illusion of a 3D block sitting on the ground.

## Camera Follows Player

The camera needs to follow the player, but now in isometric space. Convert the player's grid position to isometric screen coordinates, then center the camera on that point:

```python
player_iso_x, player_iso_y = grid_to_iso(player.grid_x, player.grid_y)
cam_x = player_iso_x - SCREEN_WIDTH // 2
cam_y = player_iso_y - SCREEN_HEIGHT // 2
```

The player still moves on the grid (up/down/left/right), but everything is *drawn* in isometric.

## Step by Step

Here's what [`isometric_dungeon.py`](isometric_dungeon.py) builds:

1. **Procedural map** -- reuses `generate_map()` from earlier lessons
2. **Isometric rendering** -- floors as diamonds, walls as tall blocks with side faces
3. **Player on the grid** -- moves with arrow keys, position converted to isometric for drawing
4. **Smooth camera** -- follows player's isometric position
5. **Doors and chests** -- special tiles with unique colors

## The Code

```python
python3 isometric_dungeon.py
```

Use **arrow keys** to move your player through the dungeon. The green diamond is you. Brown blocks are walls. Darker tiles are floors. Yellow diamonds are chests, and blue are doors.

## It Looks Wrong... Sometimes

You might notice something weird: sometimes the player appears *in front of* a wall that should be blocking them, or *behind* a floor tile. Things overlap in the wrong order.

This is called the **depth sorting problem**, and it's totally normal. In a flat top-down view, you just draw the floor first and the player on top. In isometric view, the draw order depends on *where* things are in the grid. We'll fix this properly in the next lesson.

For now, enjoy the fact that your dungeon looks like an actual 3D place!

## Experiments

1. **Wall colors** -- give different rooms different wall colors. Use the room index to pick from a color list.
2. **Taller walls** -- change `WALL_HEIGHT` to 60 or 80. How does it change the feel? What about 20 for a low-wall style?
3. **Animated player** -- make the player diamond pulse (grow and shrink slightly) using a sine wave timer.
4. **Minimap** -- draw a tiny flat top-down version of the map in the corner, showing where the player is. Two views of the same data!
5. **Torch glow** -- place orange circles at certain floor tiles to simulate torchlight. In isometric, the glow should be an ellipse, not a circle.

## Challenge

Add **floor patterns**. Instead of plain gray floors, alternate between two shades of gray in a checkerboard pattern (`(gx + gy) % 2`). Then add some random "cracked" floor tiles that are a slightly different color. Small details like this make the dungeon feel way more real.

## What's Next

👉 [Next: Depth Sorting](../34-depth-sorting/lesson.md)