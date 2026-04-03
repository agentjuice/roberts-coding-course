# The Full Game

!!! success "🎯 Mission"
    Build the grand finale -- a complete isometric dungeon crawler with enemies, combat, loot, health bars, and a HUD. Your Minecraft Dungeons-style game is done!

!!! example "🎮 Play It! — Isometric Dungeon Crawler"
    By the end of this section, you'll have built a game just like this one. **Arrow keys to move, Space to attack!**

<iframe src="/games/isometric_showcase.html" width="100%" height="470" style="border: 5px solid #ffcc00; border-radius: 16px; box-shadow: 6px 6px 0px #ff00ff; background: #0b0b13;"></iframe>

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

Scroll back up and play that demo again. Let's break down the advanced features and how they work.

### Smooth Movement

Instead of snapping from tile to tile, characters **glide** between positions. The trick: keep track of where you ARE and where you're GOING, then interpolate between them each frame.

```python
# moveT counts down from 6 to 0 over 6 frames
progress = 1 - (move_timer / 6)
draw_x = old_x + (new_x - old_x) * progress
draw_y = old_y + (new_y - old_y) * progress
```

The game logic still works on a grid. Only the drawing smooths it out. This is the same technique Minecraft uses — entities are on a grid internally but rendered smoothly.

### 4 Enemy Types with Different AI

Each enemy type has its own behavior, defined by a simple `ai` field:

```python
if ai == 'wander':     # Zombie: pick a random direction
    dx, dy = random.choice([(0,-1),(0,1),(-1,0),(1,0)])

elif ai == 'chase':    # Skeleton: move toward the player
    if enemy.x < player.x: dx = 1
    elif enemy.x > player.x: dx = -1

elif ai == 'diagonal': # Bat: move diagonally, erratic
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])

elif ai == 'ranged':   # Goblin: keep distance, throw projectiles
    if distance < 3:   # Too close! Run away
        dx = -direction_to_player
    elif distance < 6:  # In range! Throw a projectile
        projectiles.append(Projectile(enemy.x, enemy.y, toward_player))
```

Same `if/elif` you learned in lesson 6. Each enemy just makes a different decision.

### Particle Effects

Particles are tiny colored dots that spray out and fade away. Each one is just an object with a position, velocity, and lifetime:

```python
def add_particles(x, y, color, count):
    for i in range(count):
        particles.append({
            'x': x, 'y': y,
            'vx': random.uniform(-2, 2),  # Random horizontal speed
            'vy': random.uniform(-3, 0),  # Shoot upward
            'life': 20,                   # Frames until it disappears
            'color': color
        })

# Each frame, update every particle
for p in particles:
    p['x'] += p['vx']
    p['y'] += p['vy']
    p['vy'] += 0.1  # Gravity pulls them down
    p['life'] -= 1

# Remove dead particles
particles = [p for p in particles if p['life'] > 0]
```

That's it. A list of tiny objects with physics. When you attack, spawn 10 pink particles. When an enemy dies, spawn 20 in their color. Instant game juice.

### Screen Shake

This one is embarrassingly simple and embarrassingly effective:

```python
if player_got_hit:
    shake_duration = 8  # Shake for 8 frames

if shake_duration > 0:
    camera_x += random.uniform(-3, 3)  # Jiggle the camera
    camera_y += random.uniform(-3, 3)
    shake_duration -= 1
```

Three lines of code. Makes the game feel 10x more impactful. Every action game uses this — Zelda, Mario, F1 games when you crash.

### Sound Effects (No Files Needed)

The demo generates sounds mathematically using Web Audio. In Python with Pygame, you'd load `.wav` files:

```python
pygame.mixer.init()
swing_sound = pygame.mixer.Sound('swing.wav')
hit_sound = pygame.mixer.Sound('hit.wav')

# Play when something happens
def attack():
    swing_sound.play()
    if enemy_hit:
        hit_sound.play()
```

But the demo shows you can also generate sounds from code — using oscillators and frequency sweeps. A sword swing is a quick sawtooth wave dropping from 200Hz. An enemy death is a descending tone from 300Hz to 50Hz. Math becomes music.

### Goblin Projectiles

The goblin throws projectiles — objects that travel across the grid and hurt the player on contact:

```python
if goblin.distance_to_player < 6 and cooldown <= 0:
    direction = toward_player()
    projectiles.append({
        'x': goblin.x, 'y': goblin.y,
        'dx': direction.x, 'dy': direction.y,
        'life': 10
    })
    cooldown = 40  # Can't shoot again for 40 frames

# Each frame, move projectiles
for p in projectiles:
    p['x'] += p['dx']
    p['y'] += p['dy']
    if p['x'] == player.x and p['y'] == player.y:
        player.hp -= 1  # Ouch!
```

Projectiles are just items that move. Same concept as the snake's body or a falling Connect 4 chip — objects in a list, updated each frame.

### Props & Decoration

Barrels, torches, and crates are placed randomly in rooms during map generation:

```python
for room in rooms:
    for i in range(2):  # 2 props per room
        x = random.randint(room.x + 1, room.x + room.width - 2)
        y = random.randint(room.y + 1, room.y + room.height - 2)
        prop_type = random.choice(['barrel', 'torch', 'crate'])
        props.append({'x': x, 'y': y, 'type': prop_type})
```

They're drawn in the depth-sorted render list just like enemies and the player. Torches even have a tiny flickering particle effect.

!!! info "🎮 Fun Fact"
    Minecraft Dungeons was built by a team of ~60 professional developers over several years. You built your own version from scratch. That's incredible.

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
