# Lesson 9: Connect 4 v5 -- Pygame with Functions

!!! success "🎯 Mission"
    Clean up our Pygame Connect 4 by organizing the code into functions -- the same trick we used in Lesson 6, but now with graphics.


![Connect 4 with Pygame functions](/images/connect4_functions.png)

## Here We Go Again

Remember Lesson 6? We took the messy terminal Connect 4 and broke it into functions like `draw_world()`, `get_input()`, and `check_winner()`. The code got way easier to read.

Then in Lessons 7 and 8, we switched to Pygame and things got messy again. All the event handling, animation, drawing, and win-checking are tangled together in one giant loop. Sound familiar?

This is the **second time** you've felt the pain of messy code. And this time, you already know the fix: **functions**.

## The Plan

We're going to split our code into five functions:

| Function | What it does |
|---|---|
| `draw_world()` | Fills the screen, draws all circles and text |
| `get_input()` | Checks Pygame events, returns which key was pressed |
| `check_winner()` | Scans the board for four in a row |
| `switch()` | Swaps between player 1 and player 2 |
| `animate_chip()` | Moves the falling chip down one row |

After this, our main loop will be super short and easy to read:

```python
while True:
    i = get_input()
    # start chip falling if needed
    if chip_falling:
        animate_chip()
        # check if landed
    draw_world()
    time.sleep(0.1)
```

See how clean that is? You can read it like English.

## The `global` Keyword

Here's one tricky thing with functions in Python. When you create a variable outside a function (like `winner = 0`), the function can *read* it just fine. But if you want the function to *change* it, you need to use the **`global`** keyword.

```python
winner = 0

def check_winner():
    global winner    # "I want to change the REAL winner, not make a new one"
    winner = player
```

Without `global`, Python would create a brand-new `winner` variable that only lives inside the function, and the real one would never change. Think of it like the difference between writing on the class whiteboard (global) vs. writing on a sticky note that you throw away (local).

You don't need `global` to *read* a variable or to *modify* something inside a list or array (like `world[y][x] = player`). You only need it when you're assigning a completely new value to the variable with `=`.

!!! warning "⚠️ Watch Out"
    Forgetting `global` inside a function that changes a variable is a sneaky bug. Python won't give you an error -- it'll just create a new local variable with the same name, and your changes will vanish when the function ends.

## Why This Matters

Right now, Connect 4 is maybe 80 lines of code. That's manageable. But the Snake game we're building next will be bigger, and the dungeon game after that will be even bigger. If you don't organize your code into functions, you'll spend more time *finding* code than *writing* code.

Think of it like labeled drawers in a toolbox. You don't dump all your tools in one pile -- you sort them so you can find what you need.

!!! tip "Pro Tip"
    When your main loop reads like English -- `get_input()`, `animate_chip()`, `check_winner()`, `draw_world()` -- you know your code is well organized. If you can't tell what the main loop does at a glance, your functions probably need better names.

## Step-by-Step Build

### Step 1: Imports and Global Variables

```python
import pygame
import time
import numpy

world = numpy.zeros((6, 6))
player = 1
winner = 0
chip_falling = False
chip_falling_xpos = 0
chip_falling_ypos = 0

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Connect 4')
font = pygame.font.Font(None, 25)
```

All the variables live at the top, outside any function. We renamed `chip_x` and `chip_y` to `chip_falling_xpos` and `chip_falling_ypos` to make them clearer.

### Step 2: The `draw_world()` Function

```python
def draw_world():
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
```

This is *exactly* the same drawing code as before -- we just wrapped it in a function. Now instead of 15 lines in the main loop, we just call `draw_world()`. Notice we don't need `global` here because we're only *reading* `world`, `winner`, `screen`, and `font` -- not changing them.

### Step 3: The `get_input()` Function

```python
def get_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            else:
                return int(event.unicode)
    return 0
```

This function checks all events and **returns** the key that was pressed (as a number). If no key was pressed, it returns 0. The main loop can just say `i = get_input()` and it either gets a column number or 0.

### Step 4: The `check_winner()` Function

```python
def check_winner():
    global winner
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
    if world[0][0] > 0 and world[0][1] > 0 and world[0][2] > 0 and world[0][3] > 0 and world[0][4] > 0 and world[0][5] > 0:
        winner = -1
```

Here we DO need `global winner` because we're assigning to it with `winner = player`. Without that line, Python would think we're creating a local variable and the real `winner` would stay at 0 forever.

### Step 5: The `switch()` Function

```python
def switch():
    global player
    if player == 1:
        player = 2
    else:
        player = 1
```

Short and sweet. Needs `global player` because it changes `player`.

### Step 6: The `animate_chip()` Function

```python
def animate_chip():
    if chip_falling_ypos > 0:
        world[chip_falling_ypos - 1][chip_falling_xpos - 1] = 0
    world[chip_falling_ypos][chip_falling_xpos - 1] = player
```

This erases the chip from its old position and places it in the new one. Notice we DON'T need `global` for `world` -- we're modifying what's *inside* the array, not replacing the array itself.

### Step 7: The Main Loop

Here's the payoff -- look how clean this is:

```python
while True:
    i = get_input()
    if not chip_falling and i > 0 and winner == 0:
        chip_falling = True
        chip_falling_xpos = i
        chip_falling_ypos = 0
    if chip_falling:
        animate_chip()
        if chip_falling_ypos == 5 or world[chip_falling_ypos + 1][chip_falling_xpos - 1] > 0:
            chip_falling = False
            check_winner()
            switch()
        else:
            chip_falling_ypos = chip_falling_ypos + 1
    draw_world()
    time.sleep(0.1)
```

That's the ENTIRE main loop. Compare this to the 50+ lines we had before. You can read it top to bottom and understand what the game does:

1. Get input
2. If someone pressed a key, start a chip falling
3. If a chip is falling, animate it
4. If it landed, check for winner and switch players
5. Draw the board
6. Wait a bit

## The Full Code

You can see the complete file in `connect4.py` right next to this lesson.

## Run It!

1. Make sure you have Pygame and numpy installed:
   ```
   pip3 install pygame numpy
   ```
2. Run it:
   ```
   python3 connect4.py
   ```
3. It looks and plays the same as the last version -- but the code is SO much cleaner.

!!! example "🧪 Experiments"
    1. **Add a `reset_game()` function** -- Write a function that sets `world` back to zeros, `winner` to 0, and `player` to 1. Call it when someone presses R after the game ends.

    2. **Change `draw_world()` to use rectangles** -- Replace `pygame.draw.circle()` with `pygame.draw.rect()`. A rect takes a position AND a size: `pygame.draw.rect(screen, 'Red', (x, y, width, height))`.

    3. **Add a `draw_status()` function** -- Pull the winner/draw text into its own function. Now `draw_world()` only draws the board, and `draw_status()` handles the text.

    4. **Make `check_winner()` return True/False** -- Instead of using `global`, have it return `True` if someone won. The main loop checks the return value.

    5. **Add a move counter** -- Create a `moves` variable, increment it in `switch()`, and display it in `draw_world()`.

!!! abstract "🏆 Challenge"
    Add a **column highlight**. Track which column the mouse is hovering over (look up `pygame.mouse.get_pos()`) and draw that column's circles slightly brighter or with a different border. You'll want to do this inside `draw_world()`.

## What's Next

Connect 4 is done! Next up: we're building **Snake** -- the classic game where you eat food and grow longer. Get ready to learn about lists in a whole new way.
