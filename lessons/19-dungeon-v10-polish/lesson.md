# Lesson 19: Dungeon v10 — Second Level & Polish

**Goal:** Add multiple levels, a new exploding enemy, a start screen, pause menu, high scores, and visual polish that makes the game feel professional.

## New Concepts

- **File I/O** — reading and writing files with `open()`, `read()`, and `write()`
- **Game states** — menu, playing, paused, game_over (using a string variable to control flow)
- **Particle effects** — simple physics where tiny dots fly outward and fade
- **Screen shake** — offsetting the whole screen by a few random pixels to feel impactful
- **Difficulty scaling** — making enemies tougher as levels increase
- **The Creeper enemy** — a new type that charges up and explodes

## Game States

Up until now, our game just starts and you play. Real games have menus, pause screens, and game over screens. The trick is a **game state** variable:

```python
self.state = "menu"  # Can be: "menu", "playing", "paused", "game_over"
```

In the game loop, you check the state and run different code:

```python
if self.state == "menu":
    self.draw_menu()
elif self.state == "playing":
    self.update_game()
    self.draw_game()
elif self.state == "paused":
    self.draw_pause()
elif self.state == "game_over":
    self.draw_game_over()
```

This is way cleaner than having a bunch of boolean flags like `is_paused`, `is_menu`, `is_game_over`. One variable controls everything.

## File I/O for High Scores

Python makes reading and writing files surprisingly easy. We'll save the top 5 scores to a text file:

```python
# Writing scores
def save_high_scores(self):
    with open("highscores.txt", "w") as f:
        for score in self.high_scores[:5]:
            f.write(str(score) + "\n")

# Reading scores
def load_high_scores(self):
    try:
        with open("highscores.txt", "r") as f:
            return [int(line.strip()) for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []
```

The `try`/`except` handles the first time you play — there's no file yet, so we just return an empty list. The **`with` statement** automatically closes the file when we're done. Always use `with` for files!

## Particle Effects

When an enemy dies, we want a burst of colored dots flying outward. Each **particle** has a position, velocity, color, and a life counter that ticks down:

```python
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.color = color
        self.life = 20

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
```

The math here uses `cos` and `sin` to shoot particles in random directions. Each frame, the particle moves by its velocity and loses 1 life. When life hits 0, we remove it.

We draw each particle as a small circle that gets more transparent as it fades:

```python
def draw(self, screen, cam_x, cam_y):
    if self.life > 0:
        alpha = int(255 * self.life / 20)
        r, g, b = self.color
        faded = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        size = max(1, self.life // 5)
        pygame.draw.circle(screen, faded, (int(self.x - cam_x), int(self.y - cam_y)), size)
```

## Screen Shake

This is one of the simplest tricks that makes a game feel 10x better. When the player takes damage, we offset the entire draw by a random few pixels:

```python
self.shake_frames = 0

# When player gets hit:
self.shake_frames = 10

# In the draw function:
shake_x, shake_y = 0, 0
if self.shake_frames > 0:
    shake_x = random.randint(-3, 3)
    shake_y = random.randint(-3, 3)
    self.shake_frames -= 1
```

Then add `shake_x` and `shake_y` to the camera offset. The whole screen jitters for 10 frames, then stops. It's subtle but powerful.

## The Creeper Enemy

Creepers are the scariest enemy type. They chase you like skeletons, but slower. When they get within 3 tiles, they start a **countdown** — flashing faster and faster. After 3 seconds, they explode and deal 5 damage to anything nearby.

```python
class Creeper(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "creeper")
        self.fuse_timer = 0
        self.fuse_max = 90  # 3 seconds at 30 fps
        self.armed = False
```

The flashing effect is cool — we toggle the color every few frames, and the toggle speed increases as the timer counts down:

```python
flash_speed = max(2, 10 - (self.fuse_timer // 10))
if self.fuse_timer % flash_speed < flash_speed // 2:
    color = (255, 255, 255)  # Flash white
```

Creepers only appear on Level 2 and beyond, so you get a surprise when you advance.

## Multiple Levels

After beating the boss, a **staircase tile** (type 4) appears. Walk on it and you go to Level 2 — a brand new procedurally generated dungeon. Enemies on Level 2 have 1.5x health and 1.3x speed. Level 3 scales even more.

```python
def next_level(self):
    self.level += 1
    self.generate_dungeon(seed=self.seed + self.level)
    self.level_text_timer = 90  # Show "LEVEL X" for 3 seconds
```

## Step-by-Step Build

The full file includes everything from lessons 10-18, plus:

1. `Particle` class for death effects
2. `Creeper` enemy type with fuse/explosion
3. Game state system: menu, playing, paused, game_over
4. Start screen with title and high score display
5. Pause menu (Escape key)
6. High score file I/O
7. Screen shake on damage
8. Multiple levels with scaling difficulty
9. Level transition with staircase tile
10. WASD movement support (alongside arrow keys)

The complete code is in `dungeon.py` — it's our biggest file yet!

## Run It!

```bash
cd lessons/19-dungeon-v10-polish
python dungeon.py
```

You'll see the start screen first. Press SPACE to begin. Move with arrows or WASD, attack with Space. Press Escape to pause. Beat the boss to find the staircase to Level 2!

## Experiments

1. **Crank up the particles** — change the particle count from `range(10)` to `range(50)`. It looks like fireworks!
2. **More screen shake** — change the random range from `(-3, 3)` to `(-10, 10)`. Earthquakes!
3. **Creeper damage** — change the explosion damage from 5 to 20. Now they're terrifying.
4. **Speed run scaling** — change the health multiplier from 1.5 to 3.0 per level. Level 3 will be brutal.
5. **Longer fuse** — change `fuse_max` from 90 to 30 (1 second). Creepers barely give you time to run!

## Challenge

Add a **score multiplier** that increases by 0.1x for each kill without taking damage. Getting hit resets it to 1.0x. Display the current multiplier on the HUD (like "x1.5"). This rewards skillful play and makes high scores much more interesting.

## What's Next

In our FINAL lesson, we'll add a second player for **co-op mode** — two heroes fighting through the dungeon together on the same keyboard!
