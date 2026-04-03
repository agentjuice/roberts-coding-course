# Lesson 15: Dungeon v6 — The Boss

**Goal:** Add a boss fight to the final room with attack phases, a big health bar, and a victory screen.

## New Concepts

- **Boss** class — a larger, more complex enemy
- **State machine** — the boss switches between phases (chase, charge, summon, rest)
- **Phase timers** — controlling how long each behavior lasts
- **Win condition** — detecting when the boss dies and showing a victory screen
- **Game stats** — tracking time played, kills, and items used

## What Is a State Machine?

A **state machine** is when something has different "modes" and switches between them based on rules. You already know state machines from real life:

- A traffic light: green -> yellow -> red -> green (repeats)
- You in the morning: sleeping -> alarm -> getting ready -> school

Our boss works the same way. It has phases:

1. **Chase** — slowly follows the player for 5 seconds
2. **Charge** — picks a direction and zooms toward the player for 2 seconds (ouch!)
3. **Rest** — stops to catch its breath for 2 seconds
4. **Summon** — stops and spawns 2 zombie minions (only does this twice total)

The cycle goes: chase -> charge -> rest -> chase -> summon -> charge -> rest -> repeat

In code, the boss has a `phase` variable (a string like `"chase"` or `"charge"`) and a `phase_timer` that counts down. When the timer hits zero, it switches to the next phase.

## The Boss Class

The boss is bigger than regular enemies — it takes up a 2x2 tile area. Here's the core of the class:

```python
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.max_health = 50
        self.size = 2  # 2x2 tiles
        self.phase = "chase"
        self.phase_timer = 150  # 5 seconds at 30fps
        self.charge_dx = 0
        self.charge_dy = 0
        self.minions_spawned = 0  # only spawns twice
        self.hit_flash = 0
        self.move_timer = 0
        self.phase_cycle = 0  # tracks position in the phase cycle
```

## Phase Logic

Each frame, we check what phase the boss is in and act accordingly:

```python
def update(self, player, tile_map, enemies):
    self.phase_timer -= 1
    if self.phase_timer <= 0:
        self.next_phase()
    
    if self.phase == "chase":
        # Move toward player slowly (every 15 frames)
        ...
    elif self.phase == "charge":
        # Move fast in chosen direction (every 3 frames)
        ...
    elif self.phase == "summon":
        # Spawn minions once, then wait
        ...
    elif self.phase == "rest":
        # Do nothing, just wait
        pass
```

The `next_phase()` method handles the cycle:

```python
def next_phase(self):
    cycle = ["chase", "charge", "rest", "chase", "summon", "charge", "rest"]
    self.phase_cycle = (self.phase_cycle + 1) % len(cycle)
    self.phase = cycle[self.phase_cycle]
    # Set timer based on new phase
    ...
```

## Charge Attack

The charge is the boss's scariest move. It picks the direction toward the player and then rushes that way:

```python
if self.phase == "charge" and self.charge_dx == 0 and self.charge_dy == 0:
    # Pick direction toward player
    if abs(player.x - self.x) > abs(player.y - self.y):
        self.charge_dx = 1 if player.x > self.x else -1
    else:
        self.charge_dy = 1 if player.y > self.y else -1
```

During the charge, the boss moves every 3 frames instead of every 15. If it hits the player, it deals 3 damage — nasty!

## Summoning Minions

The boss can only summon minions twice total. When it enters the summon phase, it spawns 2 zombies near itself:

```python
if self.phase == "summon" and self.minions_spawned < 2:
    # Spawn 2 zombies near the boss
    for offset in [(-2, 0), (2, 0)]:
        enemies.append(Enemy(self.x + offset[0], self.y + offset[1], "zombie"))
    self.minions_spawned += 1
```

## Boss Health Bar

The boss gets a big health bar across the top of the screen, separate from regular enemy health bars:

```python
# Boss health bar
bar_x = SCREEN_WIDTH // 2 - 150
bar_y = 40
bar_w = 300
bar_h = 20
ratio = boss.health / boss.max_health
pygame.draw.rect(screen, (80, 0, 0), (bar_x, bar_y, bar_w, bar_h))
pygame.draw.rect(screen, RED, (bar_x, bar_y, int(bar_w * ratio), bar_h))
# Label
label = font.render("DUNGEON BOSS", True, RED)
screen.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, 30)))
```

## Victory Screen

When the boss's health hits zero, it's celebration time! We show:

- "YOU WIN!" in big text
- Total time played
- Total kills
- Then "Press SPACE to play again"

```python
if self.boss and self.boss.health <= 0:
    self.you_win = True
```

## Drawing the Boss

The boss is drawn as a 2x2 tile purple/red square. When it's hit, it flashes white just like regular enemies:

```python
def draw(self, screen, cam_x, cam_y):
    sx = self.x * TILE_SIZE - cam_x
    sy = self.y * TILE_SIZE - cam_y
    w = self.size * TILE_SIZE
    color = WHITE if self.hit_flash > 0 and self.hit_flash % 2 == 0 else (180, 40, 40)
    pygame.draw.rect(screen, color, (sx, sy, w, w))
    # Evil eyes
    pygame.draw.rect(screen, YELLOW, (sx + 12, sy + 16, 10, 8))
    pygame.draw.rect(screen, YELLOW, (sx + 42, sy + 16, 10, 8))
```

## Step-by-Step Build

This is the big one — the whole game comes together:

1. `Boss` class with phase state machine
2. Boss spawns in Room 4 when you first enter
3. Boss collision detection (2x2 area instead of 1x1)
4. Boss health bar at top of screen
5. Minion spawning during summon phase
6. Victory screen when boss dies
7. Full game restart on win

The complete code is in `dungeon.py`.

## Run It!

```bash
cd lessons/15-dungeon-v6-boss
python dungeon.py
```

Fight your way through 4 rooms to reach the boss in Room 4. Use your items wisely — the boss hits hard! Defeat it to see the victory screen.

## Experiments

1. **Buff the boss** — change health from 50 to 100. Can you still win?
2. **Faster charges** — change the charge move delay from 3 to 1. Much scarier!
3. **More minions** — let the boss summon 3 times instead of 2, or spawn 3 minions each time.
4. **Boss color by phase** — make the boss change color based on its current phase (red for chase, yellow for charge, purple for summon, gray for rest).
5. **Rage mode** — when the boss drops below 25% health, make it permanently faster.

## Challenge

Add a **second phase** to the boss fight. When the boss drops below half health, it enters "rage mode": it moves faster in chase phase (every 8 frames instead of 15), charges deal 5 damage instead of 3, and its color changes to bright red. Display "RAGE MODE!" text on screen when this happens.

## What's Next

Our game works, but everything is colored squares. In Lesson 16, we'll replace them with **actual sprites and pixel art** to make the game look like a real dungeon crawler!
