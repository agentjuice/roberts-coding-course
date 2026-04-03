# Snake Game

!!! success "🎯 Mission"
    Build a fully playable Snake game with Pygame -- movement, apples, growing, collision, score, and game over.


!!! example "🎮 Play It! — Snake Demo"
    By the end of this section, you'll be building a playable game just like this one. **Use arrow keys to move** (or swipe on mobile). Press **Space** to restart!

<iframe src="/games/snake.html" width="100%" height="450" style="border: 5px solid #ffcc00; border-radius: 16px; box-shadow: 6px 6px 0px #ff00ff; background: #0000ff;"></iframe>

## Tuples: Coordinates in a Pair

You know how a position on a grid always has two numbers -- an x and a y? Python has a special thing called a **tuple** that's perfect for that. It looks like a list, but with parentheses instead of square brackets:

```python
position = (3, 7)
```

That's an `(x, y)` pair. You get the pieces out with `position[0]` (the x) and `position[1]` (the y).

So why not just use a list? Think of it like this: a coordinate is always exactly two numbers. You'd never want to `.append()` a third number to a coordinate -- that doesn't even make sense. A tuple is Python's way of saying "these things go together as a unit, and that's that." Python also handles tuples a little more efficiently behind the scenes.

## The Snake Is a List of Tuples

Here's where it gets cool. The snake's body is a **list of tuples**:

```python
snake = [(3, 2), (2, 2), (1, 2), (0, 2)]
```

Each tuple is one segment's position. The first one in the list is the head. When the snake moves, we stick a new head at the front and chop off the tail at the back. When it eats an apple, we skip the chop -- so the snake grows by one!

!!! info "🎮 Fun Fact"
    The original Snake game was created in 1976 for arcade machines. It became hugely famous when Nokia put it on their phones in 1998. Over 400 million people have played Snake on a Nokia phone!

## Movement and Direction

We keep a `snake_direction` variable that's one of `'up'`, `'down'`, `'left'`, or `'right'`. Each frame, we look at the head's position and figure out the new head position based on the direction.

One important rule: the snake can't do a 180-degree turn. If you're going right, pressing left would make you crash into yourself instantly. So we block opposite-direction changes.

## Collision Detection

Two things end the game:

1. **Wall collision** -- the new head is outside the grid bounds
2. **Self collision** -- the new head lands on a segment that's already part of the snake's body

We check both before actually adding the new head to the snake.

## Step-by-Step Build

### Step 1: Imports and Variables

We need three libraries, plus some starting variables:

```python
import pygame
import time
import random

snake = [(0, 0)]
snake_direction = 'right'
apple_position = None
game_over = False
```

The snake starts as a single segment at `(0, 0)` -- the top-left corner. The apple starts as `None` because we'll place it randomly once the game starts.

### Step 2: Set Up Pygame

```python
pygame.init()
font = pygame.font.Font(None, 25)
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Snake')
```

We've done this before in Connect 4. The window is 800 by 400 pixels. We also create a font for the score text.

### Step 3: The Main Loop and Input

```python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                snake = [(0, 0)]
                snake_direction = 'right'
                apple_position = None
                game_over = False
            elif event.key == pygame.K_UP:
                if snake_direction != 'down':
                    snake_direction = 'up'
            elif event.key == pygame.K_DOWN:
                if snake_direction != 'up':
                    snake_direction = 'down'
            elif event.key == pygame.K_LEFT:
                if snake_direction != 'right':
                    snake_direction = 'left'
            elif event.key == pygame.K_RIGHT:
                if snake_direction != 'left':
                    snake_direction = 'right'
```

Notice the 180-degree turn prevention. If you're going `'down'`, pressing up does nothing. If you're going `'right'`, pressing left does nothing. Each direction blocks its opposite.

!!! tip "💡 Pro Tip"
    Blocking 180-degree turns is a classic game design pattern. Without it, the snake would instantly crash into itself when you press the opposite direction. Always think about what happens when a player mashes buttons!

Pressing **Space** resets the whole game -- it puts the snake back at `(0, 0)`, resets the direction, removes the apple, and clears the game over flag.

### Step 4: Spawn the Apple

```python
    if not apple_position:
        apple_position = (random.randint(0, 19), random.randint(0, 14))
```

If there's no apple on the board (because the game just started or the snake ate it), we pick a random position. The grid is 20 cells wide and 15 cells tall, so x goes from 0 to 19 and y goes from 0 to 14.

### Step 5: Move the Snake

This is the heart of the game:

```python
    if not game_over:
        last_snake_position = snake[0]
        new_snake_position = None
        if snake_direction == 'up':
            new_snake_position = (last_snake_position[0], last_snake_position[1] - 1)
        elif snake_direction == 'down':
            new_snake_position = (last_snake_position[0], last_snake_position[1] + 1)
        elif snake_direction == 'left':
            new_snake_position = (last_snake_position[0] - 1, last_snake_position[1])
        elif snake_direction == 'right':
            new_snake_position = (last_snake_position[0] + 1, last_snake_position[1])
```

We take the current head position (`snake[0]`) and create a new position one step in the current direction. Up means y gets smaller (remember, y=0 is the top of the screen). Down means y gets bigger.

### Step 6: Check for Collisions

```python
        if new_snake_position[0] < 0 or new_snake_position[0] >= 20 or new_snake_position[1] < 0 or new_snake_position[1] >= 15:
            game_over = True
        for i in snake:
            if new_snake_position == i:
                game_over = True
```

First we check walls: if the new head would be outside the grid (x less than 0, x 20 or more, y less than 0, y 15 or more), it's game over.

Then we check self-collision: we loop through every segment in the snake's body. If the new head would land on any of them, game over.

### Step 7: Grow or Move

```python
        if not game_over:
            snake.insert(0, new_snake_position)
        if new_snake_position == apple_position:
            apple_position = None
        elif not game_over:
            snake.pop()
```

If the game isn't over, we insert the new head at position 0 (the front of the list).

Then: if the new head is on the apple, we set `apple_position = None` so a new apple spawns next frame -- and we *don't* pop the tail, so the snake grows by one segment.

If the head isn't on the apple (and the game isn't over), we `pop()` the last element off the list. That's the tail disappearing -- so the snake stays the same length and appears to move forward.

### Step 8: Draw Everything

```python
    screen.fill('Blue')
    for x in range(20):
        for y in range(15):
            pygame.draw.rect(screen, 'Black', (x * 21 + 25, y * 21 + 25, 20, 20))
    if apple_position:
        pygame.draw.rect(screen, 'Red', (apple_position[0] * 21 + 25, apple_position[1] * 21 + 25, 20, 20))
    for t in snake:
        pygame.draw.rect(screen, 'Yellow', (t[0] * 21 + 25, t[1] * 21 + 25, 20, 20))
```

First we fill the background blue. Then we draw a 20x15 grid of black squares -- each one is 20 pixels with a 1-pixel gap (that's why we multiply by 21 instead of 20). The `+ 25` adds a margin around the edges.

Then we draw the apple as a red square and each snake segment as a yellow square, using the same grid math.

### Step 9: Score and Game Over Text

```python
    score_text = font.render("SCORE: %d" % len(snake), True, 'Green')
    screen.blit(score_text, ((500, 25)))
    if game_over:
        game_over_text = font.render("GAME OVER", True, 'Green')
        screen.blit(game_over_text, ((25, 360)))
    pygame.display.update()
    time.sleep(1 / 10)
```

The score is just the length of the snake list. We render text to an image, then `blit` (paste) it onto the screen. If the game is over, we also show "GAME OVER" at the bottom.

`time.sleep(1 / 10)` makes the game run at about 10 frames per second -- that's the snake's speed.

## The Full Code

You can see the complete file in [`snake.py`](snake.py). It puts all of the steps above together into one file.

## Run It!

```
pip3 install pygame
python3 snake.py
```

Use the **arrow keys** to steer the snake. Eat red apples to grow. Don't hit the walls or yourself! Press **Space** to restart after game over. Press **Escape** to quit.

## Experiments

1. **Change the speed** -- Try `time.sleep(1 / 5)` for a slower game or `time.sleep(1 / 20)` for a faster one. What feels best?

2. **Make a bigger grid** -- Change the 20 and 15 to bigger numbers (and update the `randint` ranges and bounds checks to match). Can you fill the whole window?

3. **Change the colors** -- Make the snake green, the apple yellow, and the background dark gray. Look up Pygame color names or use `(r, g, b)` tuples like `(255, 128, 0)` for orange.

4. **Start the snake longer** -- Change the starting snake to `[(2, 0), (1, 0), (0, 0)]` so it starts with three segments. Does the game feel different?

5. **Remove wall death** -- Instead of game over when hitting a wall, make the snake wrap around to the other side. (Hint: use `%` -- the modulo operator -- on the coordinates.)

## Challenge

Add a **high score** that persists across restarts. Create a `high_score` variable that starts at 0. When the game ends, if `len(snake)` is higher than `high_score`, update it. Display the high score next to the regular score. (It won't save when you close the program -- that's fine for now.)

## What's Next

👉 [Next: Classes](../19-snake-v2-classes/lesson.md)