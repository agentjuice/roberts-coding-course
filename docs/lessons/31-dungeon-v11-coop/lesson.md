# Co-op Mode

!!! success "🎯 Mission"
    Add a second player to the dungeon so two people can fight through it together on the same keyboard.


## The Power of Code Reuse

Right now our Player class is hard-coded to use arrow keys and Space. But what if we could make it use *any* keys? That's the magic of **configuration** -- instead of baking in specific keys, we pass them in as a parameter.

This is exactly how every multiplayer game works. Fortnite doesn't write separate code for each of the 100 players in a match — it uses one Player class and creates 100 *instances* of it, each with their own position, health, and inventory.

Here's the trick: we use a **dictionary** to map actions to keys:

```python
P1_CONTROLS = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "attack": pygame.K_SPACE,
}

P2_CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "attack": pygame.K_f,
}
```

Now the Player class takes a `controls` dict:

```python
class Player:
    def __init__(self, x, y, controls, color):
        self.controls = controls
        self.color = color
        # ... everything else
```

And in the input handling, we check `self.controls["up"]` instead of `pygame.K_UP`. One class, two totally different control schemes. This is one of the most important ideas in programming: **write code once, use it many ways**. You wrote the Player class once, and now it works for any number of players just by passing in different controls.

## Midpoint Camera

With two players, where should the camera look? Think about it -- you can't just follow Player 1 because then Player 2 might be off-screen. The answer: aim right between them. We calculate the **midpoint**, which is just the average of both positions:

```python
camera_x = (p1.x + p2.x) / 2 * TILE_SIZE - SCREEN_WIDTH // 2
camera_y = (p1.y + p2.y) / 2 * TILE_SIZE - SCREEN_HEIGHT // 2
```

This keeps both players visible as long as they stay reasonably close. If they wander too far apart, one might go off-screen -- that's part of the co-op challenge! Stick together!

## The Ghost Mechanic

When a player dies, the game doesn't end immediately. Instead, they become a **ghost** -- their sprite turns semi-transparent. They can't move or fight, but they're still on screen.

Here's the cool part: pressing their attack key **respawns** them with 5 HP, but only once per room. So if your partner goes down, you need to survive long enough for them to come back. It creates these super tense moments -- exactly what co-op games are all about.

```python
if player.dead and not player.used_respawn:
    player.health = 5
    player.dead = False
    player.used_respawn = True
```

## Separate Inventories

Each player has their own inventory. Player 1 uses keys 1-5, Player 2 uses keys 6-0. This means you have to decide who gets the health potions and who gets the power swords. Communication is key! Talk to each other!

```python
# Player 1 items: keys 1-5
# Player 2 items: keys 6, 7, 8, 9, 0
```

## Start Screen Selection

The start screen now lets you choose 1 Player or 2 Players by pressing the 1 or 2 key. In single-player mode, everything works exactly like Lesson 29.

## Step-by-Step Build

This is the final, complete version of the dungeon crawler! It includes everything:

1. Refactored `Player` class with configurable controls and colors
2. Player 2 with WASD + F controls
3. Midpoint camera between both players
4. Ghost/respawn mechanic for dead players
5. Separate inventories (1-5 for P1, 6-0 for P2)
6. Player count selection on start screen
7. Combined kill count for scoring
8. Everything from Lesson 29: levels, creepers, particles, screen shake, high scores, pause, etc.

## Run It!

```bash
python3 dungeon.py
```

On the start screen, press 1 for solo or 2 for co-op. Player 1 uses arrow keys + Space. Player 2 uses WASD + F. Survive together!

## Experiments

1. **Three players** -- try adding a third Player with IJK + L controls. You'll need to update the camera midpoint calculation to average three positions.
2. **PvP mode** -- make players' attacks damage each other. Friendly fire!
3. **Shared health pool** -- instead of separate health bars, both players share one big health bar. When either gets hit, it drains.
4. **Revive hug** -- instead of pressing a key to respawn, make the alive player stand next to the ghost for 3 seconds to revive them.
5. **Different classes** -- give Player 1 more health but less damage, and Player 2 more damage but less health. A tank and a glass cannon!

## Challenge

Add a **trading system**: when both players stand next to each other and one presses T, they drop their selected inventory item on the ground. The other player can pick it up. This lets players share health potions strategically.

## What's Next

🎉 **You finished the entire course!** You built a dungeon crawler from scratch. That's incredible. Now go build something of your own!