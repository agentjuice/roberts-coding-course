# Enemies

!!! success "🎯 Mission"
    Add wandering zombies and chasing skeletons to the dungeon, plus a health system.


!!! example "🎮 Play It! — Enemies Demo"
    By the end of this section, you'll be building a playable game just like this one. **Arrow keys to move!**

<iframe src="/games/dungeon_v2.html" width="100%" height="450" style="border: 5px solid #ffcc00; border-radius: 16px; box-shadow: 6px 6px 0px #ff00ff; background: #0b0b13;"></iframe>


## Two Kinds of Enemy Brains

Enemies need to decide where to move, and that decision-making is called **AI** (artificial intelligence). Don't worry, it's not actually intelligent -- it's just a few `if` statements pretending to be smart.

We'll make two enemy types, each with a different "brain":

If you've played Minecraft, zombies there work almost identically to what we're about to build — they shamble randomly unless they spot you, then they chase. Our skeleton AI is basically the same as Minecraft's skeleton pathfinding (just simpler).

**Zombie (green):** Dumb and random. Every 30 frames, it picks a random direction (up, down, left, right) and tries to move there. If there's a wall, it just stays put. Zombies wander around aimlessly -- think of them like bumper cars with no driver.

**Skeleton (white):** Smarter and scarier. Every 20 frames, it looks at where you are and moves one tile closer. If you're to the right, the skeleton moves right. If you're above, it moves up. Skeletons hunt you down, and they're relentless.

## Frame Counters

You know how the game runs at 60 frames per second? If enemies moved every single frame, they'd be zooming around like maniacs. Instead, each enemy has a **move_timer** that counts up. When it hits a certain number, the enemy moves and the timer resets to 0.

```python
self.move_timer += 1
if self.move_timer >= self.move_delay:
    self.move_timer = 0
    # Actually move now
```

This is a pattern you'll use constantly in game dev. Want something to happen every half second at 60 FPS? Set the delay to 30. Want it every two seconds? Set it to 120. Easy.

## Damage Cooldown

When the player touches an enemy, they should take damage -- but not 60 damage per second! That would be instant death. So we use a **damage cooldown**: after taking a hit, the player is invincible for 1 second (60 frames). This gives them time to run away.

```python
if self.damage_cooldown <= 0:
    self.health -= 1
    self.damage_cooldown = 60  # 1 second at 60 FPS
```

Think of it like those old games where your character blinks after getting hurt -- that blinking means you're temporarily safe.

## Step-by-Step Build

We're keeping everything from Lesson 20 and adding to it. Here's what's new.

### Step 1: Add health to the Player

```python
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 150, 255)
        self.speed = 1
        self.health = 10
        self.max_health = 10
        self.damage_cooldown = 0
```

The `damage_cooldown` counts down each frame. When it hits 0, the player can take damage again.

### Step 2: The Enemy class

```python
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.move_timer = 0

        if enemy_type == "zombie":
            self.color = (0, 180, 0)      # Green
            self.health = 3
            self.move_delay = 30           # Moves every 30 frames
        elif enemy_type == "skeleton":
            self.color = (220, 220, 220)   # White-ish
            self.health = 5
            self.move_delay = 20           # Moves every 20 frames
```

### Step 3: Enemy movement

The `update()` method is where the AI lives. Zombies pick random directions, skeletons chase the player.

```python
def update(self, tile_map, player):
    self.move_timer += 1
    if self.move_timer < self.move_delay:
        return

    self.move_timer = 0
    dx, dy = 0, 0

    if self.enemy_type == "zombie":
        direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        dx, dy = direction
    elif self.enemy_type == "skeleton":
        if player.x > self.x:
            dx = 1
        elif player.x < self.x:
            dx = -1
        elif player.y > self.y:
            dy = 1
        elif player.y < self.y:
            dy = -1

    new_x = self.x + dx
    new_y = self.y + dy
    if tile_map[new_y][new_x] == 0:
        self.x = new_x
        self.y = new_y
```

Notice the skeleton only moves in one direction at a time -- it picks horizontal first, then vertical. This makes it beeline toward you but not move diagonally.

### Step 4: Collision with the player

In the Game's `update()` method, check if any enemy is on the same tile as the player:

```python
for enemy in self.enemies:
    if enemy.x == self.player.x and enemy.y == self.player.y:
        if self.player.damage_cooldown <= 0:
            self.player.health -= 1
            self.player.damage_cooldown = 60
```

### Step 5: Health bar

Draw a red bar at the top of the screen that shrinks as health drops:

```python
bar_width = 200
bar_height = 20
health_ratio = self.player.health / self.player.max_health
# Background (dark red)
pygame.draw.rect(self.screen, (80, 0, 0), (10, 10, bar_width, bar_height))
# Foreground (bright red)
pygame.draw.rect(self.screen, (220, 0, 0), (10, 10, bar_width * health_ratio, bar_height))
```

### Step 6: Game Over

When health hits 0, show "GAME OVER" and wait for Space to restart:

```python
if self.player.health <= 0:
    self.game_over = True
```

### The Full Game

The complete file is saved as `dungeon.py` in this folder. It includes all the enemy logic, health system, game over screen, and restart functionality.

## Run It!

```bash
python3 dungeon.py
```

Walk around with arrow keys. You'll see green zombies wandering and white skeletons hunting you. Try to avoid them! Watch your health bar -- when it empties, it's game over. Press Space to restart.

## Experiments

1. **More enemies.** In the `spawn_enemies` method, add more enemies. Try 8 or 10. Does it get harder?

2. **Change enemy speed.** Set a zombie's `move_delay` to 10 (super fast zombie!) or a skeleton's to 60 (lazy skeleton).

3. **Different damage.** Make skeletons do 2 damage instead of 1 when they touch you.

4. **Faster cooldown.** Change the damage cooldown from 60 to 20. Now getting touched is much more dangerous!

5. **Player color flash.** When the player takes damage, briefly change their color to red, then back to blue.

## Challenge

Add a **safe room**. Use tile type `2` for safe zone tiles (draw them slightly green). When the player is standing on a safe tile, enemies can't damage them and the player slowly regenerates 1 HP every 2 seconds.

## What's Next

👉 [Next: Combat](../22-dungeon-v3-combat/lesson.md)