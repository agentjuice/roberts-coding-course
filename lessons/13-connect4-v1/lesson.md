# Your First Game

!!! success "🎯 Mission"
    Build a working two-player Connect 4 game that runs right in your terminal.


![Connect 4 terminal game in action](/images/connect4_terminal.gif)

*This is what your terminal game will look like — players taking turns and a winner!*

Alright, this is a big one -- we're building an actual game! Connect 4 is the one where you drop colored chips into a grid and try to get four in a row. By the end of this lesson, you'll have a playable version running in your terminal. Let's break down how it works.

### The Board Is a Grid

Remember lists from Lesson 10? A list is like a row of boxes. But a Connect 4 board isn't just one row -- it's a **grid** with rows *and* columns. That's called a **2D array** (two-dimensional array). Think of it like a spreadsheet, or better yet, like graph paper where each square can hold a value.

Minecraft uses the same concept — the world is a giant 3D array of blocks. Each position holds a block type (stone, dirt, air). Our Connect 4 board is a smaller, 2D version of the same idea.

!!! tip "🧮 Math Moment: 2D Arrays"
    The Connect 4 board is a **2D array** — a grid of rows and columns. To access a cell, you use two indices: `board[row][col]`. Checking for 4 in a row means checking neighbors: `board[y][x+1]`, `board[y][x+2]`, `board[y][x+3]`. This is the same math that Minecraft uses to check if 4 blocks are connected, or how chess programs check for valid moves.

We're going to use a library called **numpy** to create our grid. A library is code that someone else wrote that we can use -- no need to reinvent the wheel. numpy is great at working with grids of numbers.

```python
import numpy
world = numpy.zeros((6, 6))
```

This creates a 6-by-6 grid filled with zeros. Each `0` means "empty." When player 1 drops a chip, we put a `1` there. Player 2 gets a `2`.

!!! info "🎮 Fun Fact"
    Connect 4 was first sold in 1974 by Milton Bradley. Mathematicians later proved that if both players play perfectly, the first player can always win! It took until 1988 for a computer to figure that out.

### The Game Loop

Our whole game lives inside a `while True:` loop. You know how games keep running frame after frame until you quit? That's exactly what this does. Every time through the loop, we:

1. **Draw** the board
2. **Get input** from the current player
3. **Place** the chip in the lowest empty row
4. **Check** if someone won (or if it's a draw)
5. **Switch** to the other player

### Clearing the Screen

Every time we redraw the board, we want a clean screen. `os.system('clear')` tells your Mac to clear the terminal. It's like erasing a whiteboard before drawing the board again.

### Win Detection

This is the trickiest part. After a chip lands, we need to check if there are four in a row. But "in a row" can mean four directions:

- **Horizontal** (left to right) -->
- **Vertical** (top to bottom) |
- **Diagonal down-right** \
- **Diagonal up-right** /

We loop through every cell on the board. For each cell that belongs to the current player, we check if the next three cells in each direction also belong to that player. If they do -- winner!

!!! warning "⚠️ Watch Out"
    When checking for wins near the edges of the board, you need to make sure you don't look "off the edge." That's what the `x <= 2` and `y <= 2` checks are for -- they make sure there are enough cells in that direction to check.

### Draw Detection

If the entire top row is full and nobody has won, it's a **draw**. No more chips can be dropped.

## Step-by-Step Build

### Step 1: Imports and Setup

We need three libraries:

```python
import os       # for clearing the screen
import numpy    # for our 2D grid
```

And our game variables:

```python
world = numpy.zeros((6, 6))  # the board -- all zeros means all empty
player = 1                    # player 1 goes first
winner = 0                    # no winner yet (0 = nobody)
```

### Step 2: Draw the Board

At the top of our `while True:` loop, we clear the screen and print the board:

```python
while True:
    os.system('clear')
    print("  1  2  3  4  5  6")
    print("---------------------")
    print(world)
```

numpy's `print(world)` shows the grid nicely. The numbers on top help players pick a column.

### Step 3: Check for Game Over

Right after drawing, we check if the game is already over:

```python
    if winner < 0:
        print("DRAW")
        exit()
    elif winner > 0:
        print("WINNER - PLAYER: %d" % winner)
        exit()
```

The `%d` is a placeholder that gets replaced with the winner's number. `exit()` stops the whole program.

### Step 4: Get Player Input and Place the Chip

We ask the player for a column, then find the lowest empty row and place the chip there:

```python
    input_text = input("Enter your move player %d: " % player)
    if not str.isnumeric(input_text):
        continue
    i = int(input_text)
    if i == 0:
        exit()
    if i > 6:
        continue
    if world[0][i - 1] > 0:
        continue

    # Find the lowest empty row in this column
    for y in range(5, -1, -1):
        if world[y][i - 1] == 0:
            world[y][i - 1] = player
            break
```

There's a lot of checking here! We make sure:
- The input is actually a number (`str.isnumeric`)
- Entering `0` quits the game
- The column isn't bigger than 6
- The column isn't already full (`world[0][i - 1] > 0` checks the top cell)

Then we scan from the bottom row up (`range(5, -1, -1)`) to find the first empty spot and place the chip there.

### Step 5: Check for a Winner

After a chip lands, we scan the whole board:

```python
    for y in range(6):
            for x in range(6):
                if world[y][x] != player:
                    continue
                # horizontal
                if x <= 2 and world[y][x + 1] == player and world[y][x + 2] == player and world[y][x + 3] == player:
                    winner = player
                # vertical
                if y <= 2 and world[y + 1][x] == player and world[y + 2][x] == player and world[y + 3][x] == player:
                    winner = player
                # diagonal down-right
                if x <= 2 and y <= 2 and world[y + 1][x + 1] == player and world[y + 2][x + 2] == player and world[y + 3][x + 3] == player:
                    winner = player
                # diagonal up-right
                if x <= 2 and y > 2 and world[y - 1][x + 1] == player and world[y - 2][x + 2] == player and world[y - 3][x + 3] == player:
                    winner = player
```

The `x <= 2` and `y <= 2` checks stop us from looking off the edge of the board. For example, if `x` is 4, there aren't three more cells to the right, so we don't check horizontal.

### Step 6: Check for Draw and Switch Players

```python
    if world[0][0] > 0 and world[0][1] > 0 and world[0][2] > 0 and world[0][3] > 0 and world[0][4] > 0 and world[0][5] > 0:
        winner = -1

    if player == 1:
        player = 2
    else:
        player = 1
```

If every cell in the top row is taken, the board is full -- it's a draw (we set `winner` to -1). Then we swap who's playing next.

## The Full Code

You can see the complete file in [`connect4.py`](connect4.py). It puts all of the steps above together into one file.

## Run It!

First, make sure you have numpy installed. Open your terminal and run:

```bash
pip3 install numpy
```

Then save your file (Cmd+S) and run it:

```bash
python3 connect4.py
```

Enter column numbers (1-6) to drop chips. Enter 0 to quit.

!!! example "🧪 Experiments"
    1. **Change the board size** -- Try making it `numpy.zeros((8, 8))` and update the column numbers and range checks. Can you make a bigger board work?

    2. **Change the win condition** -- What if you only needed 3 in a row instead of 4? (Hint: remove one of the checks in each direction.)

    3. **Change the player symbols** -- Right now players are `1.0` and `2.0`. Can you think of a way to show something different?

!!! abstract "🏆 Challenge"
    Add a **move counter** that shows how many total moves have been made. Print it next to the board each turn. (Hint: create a variable, add 1 to it each time a chip lands.)

## What's Next

👉 [Next: Cleaning Up](../14-connect4-v2-functions/lesson.md)

