# The Full Game

!!! success "🎯 Mission"
    Build the grand finale -- a complete isometric dungeon crawler with enemies, combat, loot, health bars, and a HUD. Your Minecraft Dungeons-style game is done!

!!! example "🎮 Play It! — Isometric Dungeon Crawler"
    By the end of this section, you'll have built a game just like this one. **Arrow keys to move, Space to attack!**

<iframe src="/games/isometric.html" width="100%" height="450" style="border: 5px solid #ffcc00; border-radius: 16px; box-shadow: 6px 6px 0px #ff00ff; background: #0b0b13;"></iframe>

## Everything Comes Together

You've spent this whole course building up skills one by one. Variables, loops, classes, Pygame, procedural generation, combat, loot, co-op... and now isometric rendering with depth sorting.

This lesson takes everything and puts it into one complete game. This is YOUR game. You built every piece of it.

## Combat in Isometric

The player attacks in the direction they're facing, but now we draw the attack in isometric space. The attack range is still grid-based (check grid distance to enemies), but the visual effect -- the swing animation -- gets converted through the isometric formulas.

```python
# Check if enemy is in attack range (grid distance)
dist = abs(enemy.grid_x - player.grid_x) + abs(enemy.grid_y - player.grid_y)
if dist <= attack_range:
    enemy.take_damage(player.damage)
```

The grid logic stays simple. Only the drawing changes.

## Health Bars Above Characters

In isometric view, health bars float above characters. Convert the character's grid position to isometric screen position, then draw the bar a few pixels higher:

```python
iso_x, iso_y = grid_to_iso(entity.grid_x, entity.grid_y)
bar_x = iso_x - cam_x - 15
bar_y = iso_y - cam_y - 30
pygame.draw.rect(screen, RED, (bar_x, bar_y, 30, 4))
pygame.draw.rect(screen, GREEN, (bar_x, bar_y, 30 * hp_pct, 4))
```

## The HUD Is Flat

Here's an important design choice: the HUD (health display, inventory, score) is drawn in regular flat 2D, right on top of the isometric world. It doesn't rotate or slant -- it's a UI overlay.

This is exactly what Minecraft Dungeons does. The world is isometric, but your health bar, minimap, and item slots are flat rectangles at the edges of the screen.

## Step by Step

Here's what [`isometric_game.py`](isometric_game.py) builds:

1. **Procedural isometric dungeon** -- generated map rendered in full isometric
2. **Player with attack** -- move with arrows, attack with Space
3. **Three enemy types** -- zombies (slow), skeletons (ranged), creepers (explosive)
4. **Depth-sorted rendering** -- everything draws in correct order
5. **Loot drops** -- enemies drop health potions and damage boosts
6. **Health bars** -- above every character, in isometric space
7. **HUD overlay** -- flat UI showing health, score, and inventory
8. **Stairs to level 2** -- beat the floor, find the stairs, go deeper

## The Code

```python
python3 isometric_game.py
```

Use **arrow keys** to move, **Space** to attack, **E** to pick up items, **1-3** to use inventory items. Find the stairs to reach level 2 where enemies are tougher!

## Look What You Built

Take a moment. Seriously. You started this course printing "Hello World" to a black terminal. Now you've built a full isometric dungeon crawler with procedural generation, multiple enemy types, a combat system, loot, depth sorting, and a HUD.

That's not a tutorial project. That's a real game. The same concepts you used here are the same ones used in Minecraft Dungeons, Hades, and Diablo.

## Taking It Further

Want to see how far you can push this? Check out the advanced version in [`isometric_showcase.py`](isometric_showcase.py) — it adds:

- **Custom pixel art sprites** for the hero, enemies, and dungeon props
- **Smooth walking and attack animations**
- **New enemy types** — goblins that throw projectiles, bats that fly diagonally
- **Particle effects** — bursts of color on attacks and deaths
- **Screen shake** — the world rumbles when you take damage
- **Sound effects** — sword swings, enemy deaths, item pickups
- **A massive 45×35 tile map** with multiple themed rooms

Every single concept in that file — you learned it in this course. There's nothing in there you haven't seen. It's just all of it working together.

!!! info "🎮 Fun Fact"
    Minecraft Dungeons was built by a team of ~60 professional developers over several years. You built a version of it by yourself. That's incredible.

## Experiments

1. **Boss room** -- add a boss that spawns in the largest room. Give it 3x health and a unique color. It drops a special item when defeated.
2. **Ranged attack** -- add a projectile that travels in the direction the player faces. It needs its own depth value that updates as it moves across the grid.
3. **Day/night cycle** -- slowly tint the entire screen darker, then lighter. At "night," enemies get faster. At "day," loot is worth more.
4. **Co-op isometric** -- combine this with lesson 31's co-op code. Two players in isometric view! The camera centers between both players.
5. **Sound effects** -- add attack sounds, damage sounds, and item pickup sounds from lesson 28. Audio brings everything to life.

## Challenge

Add a **shop room**. One room in the dungeon has a merchant (purple diamond) who doesn't move or attack. When you stand next to them and press B, a flat shop menu opens showing items you can buy with gold (dropped by enemies). This combines flat UI with isometric world interaction -- exactly how shops work in real isometric games.

## What's Next

!!! abstract "🏆 Congratulations, Robert!"
    You finished the entire course. Every lesson. Every project. Every challenge. From `print("hello world")` to a full isometric dungeon crawler with sprites, animations, and particle effects. You're a programmer now. Go make something amazing.
