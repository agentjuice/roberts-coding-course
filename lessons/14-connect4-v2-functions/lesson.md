# Lesson 14: Connect 4 v2 -- Functions

!!! success "🎯 Mission"
    Refactor our Connect 4 game by organizing the messy code into clean, reusable **functions**.


So remember the Connect 4 code from last lesson? It works, but it's one giant `while True:` loop with everything jammed together. Imagine you wanted to change how the board draws, or fix a bug in the win checker -- you'd have to hunt through the whole file to find the right lines. It's like having all your clothes, books, and games in one huge pile on the floor. It works (you can find stuff eventually), but it's a mess.

We're going to fix that by learning about **functions**.

### What Are Functions?

A function is a named block of code that does one specific job. Think of it like a recipe card. Instead of memorizing every step every time, you just say "follow the pancake recipe" and all the steps happen.

In Python, you create a function with the **`def`** keyword:

```python
def say_hello():
    print("Hello!")
```

Now whenever you write `say_hello()`, Python runs that code. The parentheses `()` are important -- they tell Python "run this function."

### Functions Can Return Things

Some functions do their job and then **hand something back** to you. That's called a **return value**.

```python
def add(a, b):
    return a + b

result = add(3, 4)  # result is now 7
```

The `return` keyword sends a value back to wherever the function was called. It's like asking someone a question -- the return value is their answer.

### The `global` Keyword

Here's something a little weird. Variables you create outside a function are called **global variables**. Functions can *read* them just fine, but if a function wants to *change* a global variable, you have to tell Python that's what you mean by using the **`global`** keyword:

```python
score = 0

def add_point():
    global score
    score = score + 1
```

Without `global score`, Python would think you're trying to create a brand new variable called `score` inside the function, and it would get confused.

Fair warning: using `global` a lot isn't great practice. In a later lesson, we'll learn about **classes**, which are a much cleaner way to share data. But for now, `global` gets the job done.

!!! info "🎮 Fun Fact"
    Professional programmers almost never use `global` variables. Instead, they use techniques like classes (which you'll learn soon!) or pass data through function parameters. But `global` is a great starting point for understanding how data flows between functions.

### The Plan

We're going to take the big messy loop from Lesson 13 and break it into five functions:

| Function | Job |
|---|---|
| `draw_world()` | Clear screen, print the board, check game over |
| `get_input()` | Ask the player for a column, return it |
| `check_winner()` | Scan the board for four in a row |
| `switch()` | Swap from player 1 to player 2 (or back) |
| `animate_chip()` | Move the chip down one row |

!!! tip "💡 Pro Tip"
    A good function does **one thing** and has a name that describes what it does. If you can't describe what a function does in one sentence, it's probably doing too much and should be split up.

After this, our main loop will read almost like English:

```python
while True:
    draw_world()
    if not chip_falling:
        i = get_input()
        ...
    else:
        animate_chip()
        ...
    if not chip_falling:
        check_winner()
        switch()
```

That's *so* much easier to understand. You can look at the main loop and immediately know what's going on without reading every single line of code.

## Step-by-Step Build

### Step 1: Same Setup as Before

The imports and variables stay the same:

```python
import os
import numpy
import time

world = numpy.zeros((6, 6))
player = 1
winner = 0
chip_falling = False
chip_falling_ypos = 0
```

### Step 2: The `draw_world()` Function

We pull out all the drawing code into its own function:

```python
def draw_world():
    os.system('clear')
    print("  1  2  3  4  5  6")
    print("---------------------")
    print(world)
    if winner < 0:
        print("DRAW")
        exit()
    elif winner > 0:
        print("WINNER - PLAYER: %d" % winner)
        exit()
```

Notice that `draw_world()` can read `world` and `winner` without needing `global` -- it's only *reading* them, not changing them.

### Step 3: The `get_input()` Function

This function asks for input and **returns** the column number. If the input is bad, it returns `-1`:

```python
def get_input():
    input_text = input()
    if not str.isnumeric(input_text):
        return -1
    i = int(input_text)
    if i == 0:
        exit()
    if i > 6:
        return -1
    if world[0][i - 1] > 0:
        return -1
    return i
```

Returning `-1` for bad input is a common trick. The main loop can check: if the result is negative, skip this turn.

### Step 4: The `check_winner()` Function

This is the big win-checking code, now in its own function. It needs `global winner` because it might *change* the winner variable:

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

### Step 5: The `switch()` Function

Short and sweet:

```python
def switch():
    global player
    if player == 1:
        player = 2
    else:
        player = 1
```

Again, `global player` is needed because we're *changing* `player`.

### Step 6: The `animate_chip()` Function

Moves the chip down one row:

```python
def animate_chip():
    if chip_falling_ypos > 0:
        world[chip_falling_ypos - 1][i - 1] = 0
    world[chip_falling_ypos][i - 1] = player
```

This one modifies `world` directly through numpy indexing (assigning to specific cells), which works without `global` because we're changing the *contents* of `world`, not replacing the whole variable. Think of it like this: you're rearranging furniture inside a house, not replacing the house itself. Python only cares if you try to swap out the whole house.

### Step 7: The Clean Main Loop

Now look how much nicer the main loop is:

```python
while True:
    draw_world()
    if not chip_falling:
        i = get_input()
        if i < 0:
            continue
        chip_falling = True
        chip_falling_ypos = 0
    else:
        animate_chip()
        if chip_falling_ypos == 5 or world[chip_falling_ypos + 1][i - 1] > 0:
            chip_falling = False
        else:
            chip_falling_ypos = chip_falling_ypos + 1
            time.sleep(0.05)
    if not chip_falling:
        check_winner()
        switch()
```

You can read this and immediately understand the flow: draw, get input (or animate), check winner, switch. That's the power of functions.

## The Full Code

Check out `connect4.py` next to this lesson for the complete, runnable file.

## Run It!

Make sure numpy is installed (`pip3 install numpy` if you haven't already), then save your file (Cmd+S) and run:

```bash
python3 connect4.py
```

It plays exactly the same as v1 -- but the code is way more organized. Same game, cleaner code.

!!! example "🧪 Experiments"
    1. **Add a print inside a function** -- Put `print("Drawing the world!")` at the top of `draw_world()`. See how it runs every time the function is called?

    2. **Make `get_input()` print the prompt** -- Change it so `get_input()` also prints "Enter your move player X:" before calling `input()`. (Hint: you'll need to read the `player` variable.)

    3. **Create a new function** -- Write a function called `is_board_full()` that returns `True` if the top row is full and `False` otherwise. Use it inside `check_winner()`.

    4. **Rename functions** -- Try renaming `switch()` to `next_player()`. Make sure you change it everywhere it's called!

    5. **Comment the functions** -- Add a comment at the top of each function explaining what it does. This is called **documentation** and it's a great habit.

!!! abstract "🏆 Challenge"
    Create a function called `print_prompt()` that prints "Enter your move player X:" (with the right player number) and call it from the main loop before `get_input()`. This separates the prompt from the input logic -- each function does one job.

## What's Next

👉 [Go to #15 — The Game Loop](../15-the-game-loop/lesson.md)