# Depth Sorting

!!! success "🎯 Mission"
    Fix the drawing order so walls, floors, and characters overlap correctly -- using the Painter's Algorithm to draw back-to-front, just like real isometric games do.

## The Problem

In the last lesson, you probably noticed the player sometimes appearing on top of walls that should be in front of them. Or walls from the bottom of the screen drawing over walls that should be closer.

This happens because we drew tiles in a simple loop: row by row, left to right. But in isometric view, "closer to the camera" isn't just about the row -- it's about the **diagonal** position.

## The Painter's Algorithm

Imagine you're painting a scene on canvas. You paint the farthest things first (background mountains), then closer things on top (trees), then the closest things last (a person in front). Each new layer covers what's behind it.

That's the **Painter's Algorithm**: sort everything by distance, then draw far-to-near.

In isometric view, the "distance" of a tile is simply:

```python
depth = grid_x + grid_y
```

Lower depth = farther from camera (drawn first). Higher depth = closer to camera (drawn last, on top). This works because in our isometric view, things in the bottom-right of the grid are "closer" to the viewer.

## Where Does the Player Go?

The player (and enemies) aren't tiles -- they're *between* tiles. But they still need a depth value:

```python
player_depth = player.grid_x + player.grid_y
```

When sorting, the player gets drawn at the right moment: after the tiles behind them, before the tiles in front of them. If a wall has `depth = 8` and the player has `depth = 7`, the wall draws on top -- the player is hidden behind it. Exactly right!

## Drawing Walls with Depth

Walls are taller than floors, so they need extra care. The wall's **base** determines its depth (where it sits on the ground). The tall part extends upward, which means it visually covers tiles that are "behind" it. As long as we sort by the base position, it all works out.

We also draw the left and right side faces of each wall block to give them a solid 3D appearance.

## Step by Step

Here's what [`isometric_depth.py`](isometric_depth.py) builds:

1. **Depth-sorted rendering** -- all tiles and entities sorted by `grid_x + grid_y`
2. **Player and enemies in the sort** -- characters are inserted into the draw order at the right depth
3. **Proper wall occlusion** -- player hides behind walls correctly
4. **Multiple enemies** -- zombies that wander the dungeon, drawn at correct depth
5. **Wall side faces** -- left and right faces give walls a solid 3D look

## The Code

```python
python3 isometric_depth.py
```

Use **arrow keys** to move. Watch how the player goes *behind* walls that are in front of them, and *in front of* walls that are behind them. The zombies (red diamonds) also sort correctly. Press **Space** to attack.

## Why This Matters

Depth sorting is what separates "isometric-looking" from "actually isometric." Without it, the illusion breaks -- things pop in front of each other randomly and your brain can't make sense of the space. With it, your eyes automatically see a 3D room.

Every isometric game does this. Minecraft Dungeons, Hades, Diablo -- they all sort their draw order every single frame.

## Experiments

1. **Debug mode** -- press D to toggle showing each tile's depth number drawn on it. Great for understanding the sort order.
2. **More enemies** -- add 10 zombies. Do they all sort correctly against walls and each other?
3. **Depth tinting** -- make farther tiles slightly darker and closer tiles slightly brighter. This adds atmospheric depth.
4. **Moving walls** -- (just for fun) make one wall tile slowly move. Watch how the depth sorting keeps it correct even when moving.
5. **Tall vs short walls** -- give some walls double height. The depth sort still works because it's based on the base position, not the visual height.

## Challenge

Add **pillars** -- single-tile walls in the middle of rooms. They should be thinner than regular walls (draw them as a narrow diamond with tall sides). The player should be able to walk around them, appearing in front or behind depending on position. This really tests your depth sorting!

## What's Next

👉 [The Full Game](../35-isometric-game/lesson.md) -- the grand finale! Enemies, combat, loot, and a full HUD, all in beautiful isometric view.
