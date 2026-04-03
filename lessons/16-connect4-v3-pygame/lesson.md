# Adding Graphics

!!! success "🎯 Mission"
    Rebuild Connect 4 with real graphics using Pygame -- a window, colors, and circles instead of terminal text.


![Here is what your Connect 4 game will look like when we are done with this lesson!](/images/connect4_pygame.png)

## Why Pygame?

Up to now, our Connect 4 game runs in the terminal. It works, but it looks pretty plain -- just numbers in a grid. Wouldn't it be cooler to have an actual window with colored circles?

That's what **Pygame** does. It's a Python library that lets you create windows, draw shapes, play sounds, and handle keyboard/mouse input. Basically, it turns Python into a game engine.

This is similar to what Unreal Engine does for Fortnite or what Unity does for tons of indie games — they handle the graphics so the developer can focus on making the game fun.

!!! info "🎮 Fun Fact"
    Pygame was created in the year 2000 and is one of the most popular game libraries for Python. Thousands of games have been made with it, including some that have been sold on Steam!

## Installing Pygame

Before we can use it, we need to install it. Open your terminal and run:

```bash
pip3 install pygame
```

That's it. Now you can `import pygame` in any Python file.

## The Coordinate System

Here's something important that trips people up. In Pygame, the **top-left corner** of the window is position `(0, 0)`. The x-axis goes right (like normal), but the **y-axis goes DOWN**, not up. So `(100, 200)` means 100 pixels to the right and 200 pixels *down* from the top-left.

Think of it like reading a book -- you start at the top-left and go right and down.

!!! warning "⚠️ Watch Out"
    The y-axis going DOWN instead of UP trips up almost everyone at first. If your game object is moving the wrong direction vertically, check if you're adding when you should be subtracting (or vice versa).

## The Game Loop

You know how in the terminal version, we used `input()` to pause and wait for the player? Pygame doesn't work that way. Instead, we have a **game loop** that runs over and over, super fast:

1. **Check for events** (did someone press a key? click the X button?)
2. **Update** the game state (place a chip, check for winner)
3. **Draw** everything to the screen
4. **Flip the display** (`pygame.display.update()`)
5. **Sleep** a tiny bit (`time.sleep(0.1)`) so we don't burn your CPU

This loop runs maybe 10 times per second. Every time through, it redraws the entire screen from scratch. Think of it like a flipbook -- each "page" is a complete picture, and flipping through them fast makes it look smooth.

## Colors

Pygame understands color names like `'Red'`, `'Blue'`, `'Black'`, `'Yellow'`, and `'Green'`. You can also use RGB tuples like `(255, 0, 0)` for red, but the names are easier to read.

## Events Instead of input()

In the terminal, `input()` stopped everything and waited for you to type. In Pygame, the game loop keeps running and we check for **events** each time through. A keyboard press creates a `pygame.KEYDOWN` event, and we can read which key was pressed from `event.unicode`.

## Back to Messy (On Purpose!)

You might notice this code is all jammed into one big loop again -- no functions. That's on purpose! We cleaned things up with functions in Lesson 14, but now we're learning a completely new library (Pygame), so we're keeping it simple. We'll add functions back later.

## Step-by-Step Build

### Step 1: Imports and Setup

```python
import pygame
import time
import numpy

world = numpy.zeros((6, 6))
player = 1
winner = 0
```

Same grid and variables as before. Nothing new here.

### Step 2: Initialize Pygame

```python
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Connect 4')
font = pygame.font.Font(None, 25)
```

- `pygame.init()` starts up Pygame's systems
- `set_mode((800, 400))` creates a window that's 800 pixels wide and 400 tall
- `set_caption()` sets the text in the title bar
- `pygame.font.Font(None, 25)` creates a font for drawing text (size 25, default font)

### Step 3: The Main Loop -- Events

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
                i = int(event.unicode)
```

Every frame, we check all events:
- `pygame.QUIT` happens when someone clicks the X button on the window
- `pygame.KEYDOWN` happens when a key is pressed
- Escape key quits the game
- Any other key -- we grab its character with `event.unicode` and convert to a number

### Step 4: Place the Chip

```python
    if i > 0 and winner == 0:
        for y in range(6):
            if y == 5 or world[y + 1][i - 1] > 0:
                world[y][i - 1] = player
                break
```

If the player pressed a number key and the game isn't over, we drop a chip. We scan from the top down and place it in the first row where either we hit the bottom (`y == 5`) or there's already a chip below.

No animation yet -- the chip just appears instantly. We'll add animation in the next lesson!

### Step 5: Check for a Winner

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

Same win-checking logic as before -- horizontal, vertical, and both diagonals.

### Step 6: Check for Draw and Switch Players

```python
        if world[0][0] > 0 and world[0][1] > 0 and world[0][2] > 0 and world[0][3] > 0 and world[0][4] > 0 and world[0][5] > 0:
            winner = -1
        if player == 1:
            player = 2
        else:
            player = 1
```

### Step 7: Draw Everything

Now the fun part -- actually drawing the board!

```python
    screen.fill('Blue')
    for x in range(6):
        text = font.render(str(x + 1), True, 'Green')
        screen.blit(text, ((x * 30 + 45, 10)))
```

- `screen.fill('Blue')` paints the whole window blue (like a Connect 4 board)
- We render column numbers (1-6) as green text across the top
- `font.render()` turns text into an image, and `screen.blit()` puts that image on screen

```python
    for y in range(6):
        for x in range(6):
            if world[y][x] == 0:
                pygame.draw.circle(screen, 'Black', (x * 30 + 50, y * 30 + 50), 10)
            elif world[y][x] == 1:
                pygame.draw.circle(screen, 'Red', (x * 30 + 50, y * 30 + 50), 10)
            elif world[y][x] == 2:
                pygame.draw.circle(screen, 'Yellow', (x * 30 + 50, y * 30 + 50), 10)
```

For every cell on the grid, we draw a circle:
- Empty = black circle (looks like a hole)
- Player 1 = red circle
- Player 2 = yellow circle

The `(x * 30 + 50, y * 30 + 50)` figures out where each circle goes. The `10` at the end is the radius.

### Step 8: Show Winner Text and Update Display

```python
    if winner < 0:
        text = font.render('DRAW', True, 'Green')
        screen.blit(text, ((10, 350)))
    elif winner > 0:
        text = font.render("WINNER - PLAYER: %d" % winner, True, 'Green')
        screen.blit(text, ((10, 350)))
    pygame.display.update()
    time.sleep(0.1)
```

- If there's a winner or draw, show a message at the bottom
- `pygame.display.update()` actually pushes everything to the screen (nothing shows until you call this!)
- `time.sleep(0.1)` waits a tenth of a second before the next loop

## The Full Code

You can see the complete file in [`connect4.py`](connect4.py). It puts all the steps above together into one runnable file.

## Run It!

1. Make sure you have Pygame and numpy installed:
   ```
   pip3 install pygame numpy
   ```
2. Run it:
   ```
   python3 connect4.py
   ```
3. Press number keys 1-6 to drop chips. Press Escape or click the X to quit.

!!! example "🧪 Experiments"
    1. **Change the window size** -- Try `pygame.display.set_mode((600, 600))`. What happens? Does the board still fit?

    2. **Change the colors** -- Swap `'Red'` and `'Yellow'` for other colors like `'Orange'`, `'Purple'`, or `'White'`. Pick your favorites!

    3. **Make the circles bigger** -- Change the radius from `10` to `15` or `20`. You'll also need to adjust the spacing (the `30` in `x * 30`).

    4. **Change the background** -- Try `screen.fill('DarkGreen')` or `screen.fill((50, 50, 50))` for dark gray. The RGB tuple lets you pick any color!

    5. **Add a player indicator** -- Before `pygame.display.update()`, render some text that says whose turn it is, like `"Player 1's turn"`.

!!! abstract "🏆 Challenge"
    Add a **restart** feature. When someone wins (or it's a draw), if the player presses the R key, reset `world` to all zeros, set `winner = 0`, and set `player = 1`. Now you can play again without restarting the program!

    Hint: check for `event.key == pygame.K_r` in your event loop.

## What's Next

👉 [Next: Dropping Chips](../17-connect4-v4-animation/lesson.md)