# Combat

!!! success "🎯 Mission"
    Give the hero a sword attack so they can fight back against enemies.


![Combat system in action!](/images/dungeon_v3.png)


## Facing Direction

So up until now, the player was just a square scooting around. But if we want to swing a sword, we need to know which way the player is actually *looking*.

This is exactly how combat works in Zelda — Link always swings his sword in the direction he's facing. The game tracks which way you moved last and uses that to aim your attack.

Think of it like this: if you press the right arrow, you're now facing right. If you attack, the sword swings to the right and hits whatever is on the tile next to you.

We keep track of facing as a simple string: `"up"`, `"down"`, `"left"`, or `"right"`. Every time you move, we update it:

```python
def move(self, dx, dy, tile_map):
    if dx == 1:
        self.facing = "right"
    elif dx == -1:
        self.facing = "left"
    elif dy == -1:
        self.facing = "up"
    elif dy == 1:
        self.facing = "down"
    # ... then actually move
```

## Attack Mechanics

When you press Space, the player attacks. Here's what happens behind the scenes:

1. Check if the attack cooldown is 0 (can we swing yet?)
2. Find the tile in front of the player (based on facing direction)
3. Check if any enemy is standing on that tile
4. If so, deal 3 damage to that enemy
5. Start the attack cooldown (30 frames = 0.5 seconds)
6. Start the attack animation (show a yellow slash for a few frames)

```python
def attack(self, enemies):
    if self.attack_timer > 0:
        return  # Still cooling down

    self.attack_timer = 30  # 0.5 second cooldown
    self.attacking = True
    self.attack_frame = 6  # Show animation for 6 frames

    # Find the tile we're attacking
    tx, ty = self.x, self.y
    if self.facing == "up":    ty -= 1
    if self.facing == "down":  ty += 1
    if self.facing == "left":  tx -= 1
    if self.facing == "right": tx += 1

    for enemy in enemies:
        if enemy.x == tx and enemy.y == ty:
            enemy.take_damage(3)
```

The cooldown is important because without it, you could just mash Space and destroy everything instantly. You know how in most games there's a little pause between swings? That's exactly what `attack_timer` does.

## Enemy Hit Flash and Death

When an enemy gets hit, we want it to *feel* like it got hit. Just subtracting health silently would be boring. So we do two things:

**Hit flash:** The enemy turns white for 5 frames, then goes back to normal. It's a quick "your attack connected!" signal.

**Death animation:** When an enemy's health drops to 0 or below, it doesn't just vanish. Instead it rapidly flashes between white and its normal color for 10 frames, then disappears. This looks way better than just popping out of existence.

```python
def take_damage(self, amount):
    self.health -= amount
    self.hit_flash = 5  # Flash white for 5 frames
    if self.health <= 0:
        self.death_timer = 10  # Death animation
```

## Step-by-Step Build

Everything from Lessons 12 and 13 is still here. Here's what we're adding.

### Step 1: Player gains attack abilities

New attributes for the Player class:

```python
self.facing = "down"       # Which direction we're looking
self.attack_timer = 0      # Cooldown counter (counts down to 0)
self.attacking = False     # Are we currently showing an attack animation?
self.attack_frame = 0      # Frames left in attack animation
```

### Step 2: The attack method

When Space is pressed, calculate the target tile and check for enemies there:

```python
def attack(self, enemies):
    if self.attack_timer > 0:
        return

    self.attack_timer = 30
    self.attacking = True
    self.attack_frame = 6

    tx, ty = self.x, self.y
    if self.facing == "up":    ty -= 1
    if self.facing == "down":  ty += 1
    if self.facing == "left":  tx -= 1
    if self.facing == "right": tx += 1

    for enemy in enemies:
        if enemy.x == tx and enemy.y == ty:
            enemy.take_damage(3)
```

### Step 3: Attack animation drawing

Draw a yellow/orange rectangle on the tile the player is attacking:

```python
if self.attacking and self.attack_frame > 0:
    tx, ty = self.x, self.y
    if self.facing == "up":    ty -= 1
    if self.facing == "down":  ty += 1
    if self.facing == "left":  tx -= 1
    if self.facing == "right": tx += 1
    ax = tx * TILE_SIZE - camera_x
    ay = ty * TILE_SIZE - camera_y
    pygame.draw.rect(screen, (255, 200, 0), (ax + 4, ay + 4, TILE_SIZE - 8, TILE_SIZE - 8))
```

### Step 4: Enemy takes damage

Add `hit_flash`, `death_timer`, `take_damage()`, and `is_alive()` to the Enemy class:

```python
def take_damage(self, amount):
    self.health -= amount
    self.hit_flash = 5
    if self.health <= 0:
        self.death_timer = 10

def is_alive(self):
    if self.health > 0:
        return True
    return self.death_timer > 0  # Still "alive" during death animation
```

### Step 5: Enemy draw with flash effects

When drawing, check if the enemy should flash:

```python
def draw(self, screen, camera_x, camera_y):
    px = self.x * TILE_SIZE - camera_x
    py = self.y * TILE_SIZE - camera_y

    color = self.color
    if self.health <= 0:
        # Death flash: alternate white and normal
        color = WHITE if self.death_timer % 2 == 0 else self.color
    elif self.hit_flash > 0:
        color = WHITE

    pygame.draw.rect(screen, color, (px + 4, py + 4, TILE_SIZE - 8, TILE_SIZE - 8))
```

### Step 6: Kill counter

The Game class tracks `kill_count`. When we remove dead enemies, we count them:

```python
before = len(self.enemies)
self.enemies = [e for e in self.enemies if e.is_alive()]
self.kill_count += before - len(self.enemies)
```

### Step 7: Attack cooldown bar

A small blue bar under the health bar shows when you can attack again:

```python
cooldown_ratio = self.player.attack_timer / 30
pygame.draw.rect(screen, (0, 80, 160), (10, 35, int(100 * cooldown_ratio), 8))
```

When the bar is empty, you can swing again.

### The Full Game

The complete file is saved as `dungeon.py` in this folder. It has the full combat system with all the visual effects.

## Run It!

```bash
python3 dungeon.py
```

Walk around with arrow keys. Press **Space** to attack in the direction you're facing. You'll see a yellow flash on the tile you hit. Enemies flash white when damaged, then flash rapidly and disappear when they die. Your kill count shows in the HUD.

## Experiments

1. **Change attack damage.** In the `attack()` method, change the damage from 3 to 1. Now enemies take more hits to kill — more challenging!

2. **Bigger attack range.** What if your sword could hit 2 tiles ahead? Change the target calculation to multiply the direction by 2.

3. **Faster attacks.** Set `attack_timer = 10` instead of 30. Now you can swing super fast!

4. **More enemies.** Add 6 more enemies in `spawn_enemies`. With this many, combat gets intense.

5. **Different attack colors.** Change the attack flash from yellow `(255, 200, 0)` to whatever you want. Try red `(255, 50, 0)` for a fiery look.

## Challenge

Add an **area attack**. When the player presses X (instead of Space), they do a spin attack that hits all 4 tiles around them (up, down, left, right) at once. But it does less damage (1 instead of 3) and has a longer cooldown (60 frames instead of 30). You'll need a separate cooldown timer for it.

## What's Next

👉 [Go to #24 — Dungeon: Loot & Items](../24-dungeon-v4-loot/lesson.md)