# Robert's Coding Course — Full Specification

## Overview
A comprehensive Python coding course for an 11-year-old (6th grader) who already vibe-codes with Cursor/AI but wants to learn fundamentals. The course builds toward a Minecraft Dungeons-inspired dungeon crawler game.

**Philosophy:** Get into building real games ASAP. Start messy on purpose, then clean up. Every new concept is introduced because the code needs it, not as abstract theory. Each version of each project is playable.

**Target:** Robert Vassallo, 11, 6th grader. He plays Minecraft Dungeons and wants to build something like it.

**Setup:** VS Code + terminal side by side. Each lesson in its own folder. Python 3 + Pygame.

## Course Structure

### Warm-up (4 lessons)

**Lesson 1 — The Basics**
- What is a program? Instructions for the computer, run top to bottom
- `print()` — talking to the screen
- Variables — storing values (strings, ints, floats, booleans)
- `input()` — asking the user for info
- `int()` conversion, f-strings
- Running a script: `python lesson.py`
- 🎯 Build: Number guessing game (computer picks random number, player guesses, hot/cold hints)

**Lesson 2 — Conditions**
- `if`/`elif`/`else` — making decisions
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- 🎯 Build: Decision-making programs (terminal)

**Lesson 3 — Loops**
- `while True:` — doing something forever, `break` to escape
- `for` loops, `range()`
- 🎯 Build: Loop-based programs (terminal)

**Lesson 4 — Lists**
- Lists: creating, indexing, `append()`, `pop()`, `len()`, `in`
- 🎯 Build: List-based programs (terminal)

### Project 1: Connect 4 (5 versions)

Reference implementations are in the `reference/` folder. The lesson content should teach toward these implementations but explain every concept along the way.

**Lesson 5 — Connect 4 v1: Terminal, All Inline**
- Reference: `reference/connect4.py`
- 2D arrays with numpy (`numpy.zeros((6,6))`)
- Nested loops for drawing the board
- `input()` for player moves
- Win detection: checking 4 directions (horizontal, vertical, 2 diagonals)
- Draw detection
- Player switching
- Chip falling animation with `time.sleep()` and `os.system('clear')`
- Everything in one big while loop
- Explain: this works but it's getting long and hard to read

**Lesson 6 — Connect 4 v2: Functions**
- Reference: `reference/connect4_functions.py`
- Why functions? The code from v1 is messy. Let's organize it.
- Extract: `draw_world()`, `get_input()`, `check_winner()`, `switch()`, `animate_chip()`
- `global` keyword — why it's needed (and why it's not great, foreshadowing classes)
- Return values from functions
- The main loop is now readable: draw → input → animate → check → switch

**Lesson 7 — Connect 4 v3: Pygame, No Functions**
- Reference: `reference/connect4_pygame_nofunc.py`
- Installing pygame: `pip install pygame`
- Opening a window, setting caption
- The REAL game loop: `while True:` → events → update → draw → display.update → sleep
- RGB colors, `screen.fill()`
- Drawing: `pygame.draw.circle()`, `pygame.draw.rect()`
- Rendering text with `pygame.font`
- Keyboard events (`pygame.KEYDOWN`) vs terminal `input()`
- Coordinate system: (0,0) top-left, y goes DOWN
- Back to messy on purpose

**Lesson 8 — Connect 4 v4: Pygame with Animation**
- Reference: `reference/connect4_pygame_nofunc_anim.py`
- Adding chip falling animation in the graphical version
- State variables: `chip_falling`, `chip_x`, `chip_y`
- Frame-by-frame updates
- Why `time.sleep(1/20)` — frame rate

**Lesson 9 — Connect 4 v5: Pygame with Functions**
- Reference: `reference/connect4_pygame.py`
- Clean it up again with functions
- Same pattern as lesson 4 but now in Pygame
- By now he's felt the pain of messy code TWICE and understands why functions matter

### Project 2: Snake (2 versions)

**Lesson 10 — Snake v1: Pygame, Inline**
- Reference: `reference/snake.py`
- Tuples for coordinates: `(x, y)`
- Lists as data structures (snake body as list of tuples)
- Movement: direction variable, updating head position
- Preventing 180° turns
- Random apple placement with `random.randint()`
- Growing: insert new head, only pop tail if no apple eaten
- Collision detection: walls (bounds checking) and self (loop through body)
- Score display, game over, restart with Space
- He builds this more independently — less hand-holding

**Lesson 11 — Snake v2: OOP with Classes**
- Reference: `reference/snake_func.py`
- Why classes? The snake has data AND behavior. The apple has data AND behavior. Let's group them.
- `class Snake`: body, direction, draw(), update(), change_direction(), score()
- `class Apple`: position, regen(), draw()
- `class World`: screen, font, snake, apple, game_over, get_input(), update_state(), draw(), quit()
- `self` and `__init__()` explained simply: "self is the object talking about itself"
- The main loop becomes 4 beautiful lines
- "This is how real games are structured"

### Project 3: Dungeon Crawler — "Robert's Dungeons" (10 versions + stretch goals)

This is the big one. A top-down action game inspired by Minecraft Dungeons. Each version adds a new system. Every version is playable.

**Lesson 12 — Dungeon v1: The Hero**
- Tile-based world: 2D list where numbers mean different tiles (0=floor, 1=wall, 2=door)
- Draw the map as colored rectangles
- Player character (colored square) moves with arrow keys
- Wall collision: check the tile before moving
- Camera that follows the player (offset all drawing by player position)
- A larger map that scrolls
- HUD: show player position

**Lesson 13 — Dungeon v2: Enemies**
- Enemy class with position, health, speed, color
- Zombie: wanders randomly (picks random direction each N frames)
- Skeleton: chases the player (move one step closer each tick using simple distance)
- Multiple enemies stored in a list
- Enemies can't walk through walls (same collision check as player)
- Touching an enemy hurts the player (damage on collision)
- Health bar drawn on screen (red bar that shrinks)
- Player death → game over screen

**Lesson 14 — Dungeon v3: Combat**
- Press Space to attack (sword swing)
- Attack affects tiles in front of player based on facing direction
- Attack has a cooldown timer (can't spam, shown as a small bar)
- Enemies take damage: flash white when hit
- Enemies have health, die when health reaches 0
- Death animation: enemy flashes and disappears
- Player attack animation: brief colored rectangle in attack direction
- Kill counter on HUD

**Lesson 15 — Dungeon v4: Loot & Items**
- Defeated enemies sometimes drop items (random chance)
- Item types: health potion (restores HP), speed boost (temporary), power sword (more damage)
- Items sit on the ground as colored squares, picked up by walking over them
- Inventory: a list shown at bottom of screen
- Press number keys (1-5) to use items from inventory
- Treasure chests placed in the map (new tile type), open by walking into them
- Chests contain random loot

**Lesson 16 — Dungeon v5: Multiple Rooms**
- The dungeon is now multiple rooms connected by corridors/doors
- Each room is its own 2D map with its own enemy list
- Doors: walk into a door tile → transition to the next room
- Room transition effect (brief fade or flash)
- Enemies spawn when entering a room for the first time
- Minimap in corner showing rooms explored (simple rectangles)
- Current room highlighted on minimap

**Lesson 17 — Dungeon v6: The Boss**
- Final room contains a boss enemy (larger, different color, more health)
- Boss has phases/patterns using a state machine:
  - Phase 1: Chase player slowly
  - Phase 2: Charge attack (move fast in one direction)
  - Phase 3: Spawn minions (create small enemies)
  - Rest period between phases
- Big health bar at top of screen for boss
- Victory screen when boss dies: "YOU WIN!" with stats (time, kills, items collected)
- Option to restart the whole game

**Lesson 18 — Dungeon v7: Sprites & Art**
- Replace colored squares with images
- `pygame.image.load()` for loading PNGs
- Create simple pixel art (or provide pre-made assets)
- Player sprite with facing directions (4 images or flip)
- Enemy sprites
- Tile sprites (stone floor, brick wall, door)
- Item sprites
- How sprite sheets work (optional/stretch)

**Lesson 19 — Dungeon v8: Sound & Music**
- `pygame.mixer` for sound effects and music
- Sound effects: sword swing, enemy hit, enemy death, item pickup, chest open, player hurt
- Background music: different track for dungeon vs boss fight
- Volume control
- Provide or create simple sound assets (or use free ones from OpenGameArt)

**Lesson 20 — Dungeon v9: Procedural Generation**
- Instead of hand-designed rooms, generate them randomly
- Simple algorithm: place rooms as rectangles, connect with corridors
- Random enemy placement per room
- Random chest placement
- Every playthrough is different
- Seed-based generation (same seed = same dungeon, for sharing with friends)

**Lesson 21 — Dungeon v10: Second Level & Polish**
- After beating the boss, a staircase appears → Level 2
- Level 2: harder enemies (more health, faster, new types)
- New enemy type: Creeper (explodes near player after countdown)
- Difficulty scaling: enemies get stronger each level
- Start screen with title art
- Pause menu (press Escape)
- Settings: music volume, SFX volume
- Save/load high scores to a file
- Polish: screen shake on hit, particle effects (simple colored dots), smoother animations

**Lesson 22 — Dungeon v11: Co-op Mode (Stretch)**
- Second player on same keyboard (WASD + different attack key)
- Player 2 class (reuse Player but different controls and color/sprite)
- Shared screen (camera follows midpoint between players)
- Cooperative: both players fight enemies together
- Shared inventory or separate inventories
- If one player dies, the other can continue

## Lesson Format

Each lesson should be a markdown file with:
1. **Title & Goal** — one sentence: what are we building/learning today
2. **New Concepts** — brief list of new things introduced
3. **Explanation** — clear, conversational explanation. Written for an 11-year-old. No jargon without explanation. Use analogies.
4. **Step-by-step build** — walk through the code piece by piece. Show code snippets, explain each part, then show the full file.
5. **Run it!** — "Save this as `game.py` and run `python game.py`"
6. **Experiments** — "Try changing X to Y. What happens?" (3-5 quick experiments)
7. **Challenge** — a small modification or addition to try on their own
8. **What's Next** — one-line teaser for the next lesson

## File Structure

```
roberts-coding-course/
├── README.md              # Course overview, setup instructions
├── COURSE_SPEC.md         # This file
├── reference/             # Daniel's original reference files
├── lessons/
│   ├── 01-the-basics/
│   │   ├── lesson.md
│   │   └── guessing_game.py  (complete reference solution)
│   ├── 02-conditions/
│   │   ├── lesson.md
│   │   └── conditions.py
│   ├── 03-loops/
│   │   ├── lesson.md
│   │   └── loops.py
│   ├── 04-lists/
│   │   ├── lesson.md
│   │   └── lists.py
│   ├── 05-connect4-v1/
│   │   ├── lesson.md
│   │   └── connect4.py
│   ├── 06-connect4-v2-functions/
│   │   ├── lesson.md
│   │   └── connect4.py
│   ├── ... etc for all 22 lessons
│   └── 22-dungeon-v11-coop/
│       ├── lesson.md
│       └── dungeon.py
└── assets/               # Any images, sounds, or sprites needed
    └── README.md         # Notes on where assets came from
```

## Style Guidelines
- Write like you're talking to a smart 11-year-old, not a college student
- Use "you" and "we" — conversational
- Short paragraphs, lots of code examples
- Bold key terms when first introduced
- Use emoji sparingly but naturally
- Analogies are great: "A variable is like a labeled box — you put something in it and can check what's inside later"
- Don't over-explain. If something is obvious, move on.
- Code comments should be helpful but not excessive
- Reference Daniel's teaching style from the reference files: practical, direct, no fluff

## Technical Notes
- Python 3.10+ assumed
- Pygame 2.x
- numpy only for Connect 4 (to match Daniel's reference code)
- All dungeon crawler code should use pure Python lists (no numpy)
- Keep code simple — no advanced patterns unless earned through the lesson progression
- Each lesson's .py file should be runnable standalone
- Use `time.sleep()` for frame rate (matches Daniel's reference style) rather than `pygame.time.Clock()` — simpler to understand. Can mention Clock as an improvement in later lessons.
