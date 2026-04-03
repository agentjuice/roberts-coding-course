# Dropping Chips

!!! success "🎯 Mission"
    Make chips fall down the board one row at a time, like a real Connect 4 game.


![Chips dropping in Connect 4](/images/connect4_drop.gif)

*Watch the chips fall into place!*

## What's Wrong with the Old Version?

In the last lesson, chips just appeared in place -- poof! That works, but it doesn't look like a real Connect 4 game. In the real game, you drop a chip in the top and it *falls* down to the bottom. Let's make that happen.

## Thinking in Frames

You know how our game loop runs over and over? Each time through is one **frame**, like one frame in a movie. Right now our loop runs about 10 times per second. If we want a chip to fall, we don't move it all the way down at once. Instead, we move it **one row per frame**.

Frame 1: chip is at row 0
Frame 2: chip is at row 1
Frame 3: chip is at row 2
...and so on until it hits the bottom or another chip.

This is how ALL animation works in games -- small movements, many times per second, that look smooth when you watch them.

!!! tip "💡 Pro Tip"
    If your animation looks choppy, try increasing the frame rate (smaller `time.sleep` value). If it's too fast to see, slow it down. Finding the right speed is all about experimenting!

## State Variables

To make the animation work, we need to remember some things between frames:

- **`chip_falling`** -- is a chip currently dropping? (`True` or `False`)
- **`chip_x`** -- which column is it falling in?
- **`chip_y`** -- which row is it currently at?

These are called **state variables** because they track the *state* of the animation. Think of it like a bookmark -- they remember where we are in the middle of the falling process.

## Frame Rate

We'll change `time.sleep(0.1)` to `time.sleep(1/20)`. That means our game runs at **20 frames per second** (FPS). `1/20` is 0.05 seconds per frame. This makes the animation smoother and the chip falls at a nice speed.

!!! info "🎮 Fun Fact"
    Most movies run at 24 frames per second, TV shows at 30 FPS, and modern games at 60 FPS or higher. The human eye can notice the difference up to about 120 FPS!

## The Tricky Part

The animation code needs to be careful about order. Here's what happens each frame when a chip is falling:

1. Place the chip at its current position on the grid
2. Erase it from the position above (so it doesn't leave a trail)
3. Check if it's landed (hit the bottom or another chip)
4. If it landed, check for a winner and switch players
5. If not, move it down one row for the next frame

The key insight: we only check for the winner and process player input *after* the chip finishes falling. While it's falling, we ignore new key presses.

## Step-by-Step Build

### Step 1: Setup

Almost the same as before, but we add `chip_falling` and change the window size:

```python
import pygame
import time
import numpy

world = numpy.zeros((6, 6))
player = 1
winner = 0

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Connect 4')
font = pygame.font.Font(None, 25)
chip_falling = False
```

### Step 2: Event Handling

```python
while True:
    i = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            else:
                if event.unicode.isnumeric():
                    i = int(event.unicode)
                    chip_x = i - 1
```

Notice something new here: `event.unicode.isnumeric()`. This checks if the key pressed is actually a number before we try to convert it. Without this, pressing a letter key would crash the program! We also save `chip_x` (the column, zero-indexed) right away.

### Step 3: The Animation Logic

This is the big new piece. If a chip is currently falling, we handle it:

```python
    if chip_falling:
        world[chip_y][chip_x] = player
        if chip_y > 0:
            world[chip_y - 1][chip_x] = 0
```

First, we place the chip at its current row (`chip_y`). Then we erase it from the row above -- but only if it's not at row 0 (because there's no row -1!).

```python
        if chip_y == 5 or world[chip_y + 1][chip_x] > 0:
            chip_falling = False
```

Has it landed? It's landed if we're at the bottom row (5) or if there's already a chip in the row below.

```python
            for y in range(6):
                for x in range(6):
                    if world[y][x] != player:
                        continue
                    if x <= 2 and world[y][x + 1] == player and world[y][x + 2] == player and world[y][x + 3] == player:
                        winner = player
                    if y <= 2 and world[y + 1][x] == player and world[y + 2][x] == player and world[y + 3][x] == player:
                        winner = player
                    if x <= 2 and y <= 2 and world[y + 1][x + 1] == player and world[y + 2][x + 2] == player and world[y + 3][x + 3] == player:
                        winner = player
                    if x <= 2 and y > 2 and world[y - 1][x + 1] == player and world[y - 2][x + 2] == player and world[y - 3][x + 3] == player:
                        winner = player
```

Only when the chip has landed do we check for a winner. Same four-direction check as before.

```python
            if world[0][0] > 0 and world[0][1] > 0 and world[0][2] > 0 and world[0][3] > 0 and world[0][4] > 0 and world[0][5] > 0:
                winner = -1
            if player == 1:
                player = 2
            else:
                player = 1
        chip_y = chip_y + 1
```

After landing, check for draw and switch players. Then move `chip_y` down by 1 for the next frame (this only matters if the chip is still falling).

### Step 4: Start a New Chip Falling

```python
    if i > 0 and winner == 0:
        chip_falling = True
        chip_y = 0
```

If the player pressed a number and the game isn't over, start a new chip at the top. Notice this comes *after* the animation code -- that way the chip starts at row 0 and the animation picks it up on the *next* frame.

### Step 5: Drawing (Same as Before)

```python
    screen.fill('Blue')
    for x in range(6):
        text = font.render(str(x + 1), True, 'Green')
        screen.blit(text, ((x * 30 + 45, 10)))
    for y in range(6):
        for x in range(6):
            if world[y][x] == 0:
                pygame.draw.circle(screen, 'Black', (x * 30 + 50, y * 30 + 50), 10)
            elif world[y][x] == 1:
                pygame.draw.circle(screen, 'Red', (x * 30 + 50, y * 30 + 50), 10)
            elif world[y][x] == 2:
                pygame.draw.circle(screen, 'Yellow', (x * 30 + 50, y * 30 + 50), 10)
    if winner < 0:
        text = font.render('DRAW', True, 'Green')
        screen.blit(text, ((10, 350)))
    elif winner > 0:
        text = font.render("WINNER - PLAYER: %d" % winner, True, 'Green')
        screen.blit(text, ((10, 350)))
    pygame.display.update()
    time.sleep(1 / 20)
```

The drawing code is exactly the same. The magic is that because `world` gets updated each frame with the chip in a new position, the circle *appears* to fall when we redraw.

## The Full Code

You can see the complete file in [`connect4.py`](connect4.py).

## Run It!

1. Make sure you have Pygame and numpy installed:
   ```
   pip3 install pygame numpy
   ```
2. Run it:
   ```
   python3 connect4.py
   ```
3. Press 1-6 to drop chips and watch them fall!

!!! example "🧪 Experiments"
    1. **Slow-motion mode** -- Change `time.sleep(1 / 20)` to `time.sleep(0.5)`. Now the chip falls in slow motion -- you can see each step clearly.

    2. **Speed mode** -- Change it to `time.sleep(1 / 60)`. Super fast! This is 60 FPS, which is what most real games run at.

    3. **Change the window size** -- Make it `(400, 400)` or `(600, 600)`. See how the board looks at different sizes.

    4. **Add a falling sound** -- This is tricky but fun. Look up `pygame.mixer.Sound` and play a short sound each time `chip_falling` is set to `True`.

    5. **Trail effect** -- What happens if you comment out the line `world[chip_y - 1][chip_x] = 0`? The chip leaves a trail as it falls!

!!! abstract "🏆 Challenge"
    Right now, you can drop a chip into a full column and it just overwrites what's there. Add a check: if `world[0][chip_x]` is already taken (greater than 0), don't start the chip falling. This prevents stacking chips on a full column.

## What's Next

👉 [Next: The Final Version](../17-connect4-v5-pygame-functions/lesson.md)