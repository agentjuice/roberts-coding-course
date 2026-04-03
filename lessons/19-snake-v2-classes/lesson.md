# Lesson 19: Snake v2 -- Classes and Objects

!!! success "🎯 Mission"
    Rebuild Snake using **classes** to organize the code like a real game developer would.


![Same Snake game, rebuilt with classes](/images/snake_classes.png)


## Why Classes?

Look at the Snake code from last lesson. The snake's data (`snake`, `snake_direction`) and the snake's behavior (movement, collision checking, drawing) are scattered all over the place. The apple's stuff is mixed in too. It works, but it's messy.

What if we could bundle the snake's data *and* its behavior into one neat package? That's exactly what a **class** does.

Think of it like this: a class is a **blueprint**. If you had a blueprint for "Snake," it would say "a Snake has a body and a direction, and it can move, draw itself, and change direction." Then you can build an actual snake from that blueprint -- that's called an **object**.

In Minecraft, every Creeper is an *object* built from the same Creeper *class*. Each one has its own position and health, but they all share the same behavior: walk toward player, hiss, explode. One blueprint, thousands of creepers.

## The `self` Keyword

Here's the part that confuses everyone at first. When you write a method (a function inside a class), the first parameter is always `self`. It means "the object I'm talking about."

```python
class Snake:
    def __init__(self):
        self.body = [(0, 0)]
        self.direction = 'right'
```

`self.body` means "MY body" -- the body that belongs to THIS particular snake. `self.direction` means "MY direction." If you had two snakes, each one would have its own `self.body` and `self.direction`.

## `__init__()` -- The Constructor

**`__init__()`** is a special method that runs automatically when you create a new object. It's where you set up the starting values. The double underscores are Python's way of saying "this is special."

```python
my_snake = Snake()  # This calls __init__() automatically!
```

When you write `Snake()`, Python creates a new Snake object and immediately calls `__init__()` on it. You don't call `__init__()` yourself -- Python handles it.

## Methods -- Functions That Belong to an Object

A **method** is just a function that lives inside a class. The difference from a regular function is that it always gets `self` as the first parameter, so it can access the object's data.

```python
class Snake:
    def score(self):
        return len(self.body) - 1
```

You call it like this:

```python
my_snake = Snake()
print(my_snake.score())  # prints 0 (body has 1 segment, minus 1)
```

Notice you don't pass `self` when calling -- Python fills that in for you. You just write `my_snake.score()` and Python knows that `self` is `my_snake`.

## The Three Classes

We'll split our game into three classes:

- **`Snake`** -- has a body and direction. Can draw itself, update its position, change direction, and report its score.
- **`Apple`** -- has a position. Can regenerate in a random spot and draw itself.
- **`World`** -- has the screen, font, snake, apple, and game state. Handles input, updates everything, and draws the whole scene.

The `World` is the boss -- it owns a Snake and an Apple and coordinates everything.

## Step-by-Step Build

### Step 1: Imports

Same three libraries as before:

```python
import pygame
import time
import random
```

### Step 2: The Snake Class

```python
class Snake:
    def __init__(self):
        self.body = [(0, 0)]
        self.direction = 'right'
```

Instead of two separate variables floating around, the snake's data lives right here inside the class. Clean!

Now the draw method:

```python
    def draw(self, screen):
        for i in self.body:
            pygame.draw.rect(screen, 'Yellow', (i[0] * 21 + 25, i[1] * 21 + 25, 20, 20))
```

The snake knows how to draw itself. We pass in the screen so it knows *where* to draw. It loops through `self.body` and draws a yellow square for each segment.

The update method handles movement and collision:

```python
    def update(self, apple):
        last_snake_position = self.body[0]
        new_snake_position = None
        if self.direction == 'up':
            new_snake_position = (last_snake_position[0], last_snake_position[1] - 1)
        elif self.direction == 'down':
            new_snake_position = (last_snake_position[0], last_snake_position[1] + 1)
        elif self.direction == 'left':
            new_snake_position = (last_snake_position[0] - 1, last_snake_position[1])
        elif self.direction == 'right':
            new_snake_position = (last_snake_position[0] + 1, last_snake_position[1])
        if new_snake_position[0] < 0 or new_snake_position[0] >= 20 or new_snake_position[1] < 0 or new_snake_position[1] >= 15:
            return True
        for i in self.body:
            if new_snake_position == i:
                return True
        self.body.insert(0, new_snake_position)
        if new_snake_position == apple.position:
            apple.regen()
        else:
            self.body.pop()
        return False
```

This is the same logic as before, but now it **returns** `True` if the snake died and `False` if it's still alive. Notice how it directly tells the apple to `regen()` when it gets eaten -- objects talking to each other!

The direction-changing method:

```python
    def change_direction(self, key):
        if key == pygame.K_UP:
            if self.direction != 'down':
                self.direction = 'up'
        elif key == pygame.K_DOWN:
            if self.direction != 'up':
                self.direction = 'down'
        elif key == pygame.K_LEFT:
            if self.direction != 'right':
                self.direction = 'left'
        elif key == pygame.K_RIGHT:
            if self.direction != 'left':
                self.direction = 'right'
```

And the score:

```python
    def score(self):
        return len(self.body) - 1
```

We subtract 1 because the snake starts with one segment, so score starts at 0.

### Step 3: The Apple Class

```python
class Apple:
    def __init__(self):
        self.position = None

    def regen(self):
        self.position = (random.randint(0, 19), random.randint(0, 14))

    def draw(self, screen):
        if self.position:
            pygame.draw.rect(screen, 'Red', (self.position[0] * 21 + 25, self.position[1] * 21 + 25, 20, 20))
```

Short and sweet. The apple knows its position, can regenerate somewhere random, and can draw itself. That's it.

### Step 4: The World Class

The World ties everything together:

```python
class World:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 25)
        self.screen = pygame.display.set_mode((800, 400))
        self.regen()

    def regen(self):
        self.snake = Snake()
        self.apple = Apple()
        self.game_over = False
```

The `__init__()` sets up Pygame and then calls `self.regen()` to create a fresh snake and apple. The `regen()` method is also used when you press Space to restart -- it creates brand new Snake and Apple objects.

Input handling:

```python
    def get_input(self, input_events):
        for event in input_events:
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                elif event.key == pygame.K_SPACE:
                    self.regen()
                else:
                    self.snake.change_direction(event.key)
```

See how clean this is? For direction keys, we just pass the key to the snake and let *it* figure out what to do. The World doesn't need to know the details of how direction-changing works.

Updating the game state:

```python
    def update_state(self):
        if not self.apple.position:
            self.apple.regen()
        if not self.game_over:
            self.game_over = self.snake.update(self.apple)
```

Two lines. If there's no apple, make one. If the game isn't over, update the snake (and store whether it died).

Drawing:

```python
    def draw(self):
        self.screen.fill('Blue')
        for x in range(20):
            for y in range(15):
                pygame.draw.rect(self.screen, 'Black', (x * 21 + 25, y * 21 + 25, 20, 20))
        self.draw_text("SCORE: %d" % self.snake.score(), "Green", 500, 25)
        if self.game_over:
            self.draw_text("GAME OVER", "Green", 25, 360)
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)
        pygame.display.update()
```

The World draws the background grid, then tells the apple and snake to draw themselves. Each object handles its own drawing.

A little helper for text:

```python
    def draw_text(self, text, color, x, y):
        text_image = self.font.render(text, True, color)
        self.screen.blit(text_image, ((x, y)))

    def quit(self):
        pygame.quit()
        exit()
```

### Step 5: The Main Loop

Here's the payoff. After all that class setup, the main game loop is beautifully simple:

```python
world = World()
while True:
    world.get_input(pygame.event.get())
    world.update_state()
    world.draw()
    time.sleep(1 / 4)
```

Four lines! Create a world, then every frame: get input, update, draw, wait. That's the **game loop pattern**, and it's how real games are structured. Every game you've ever played does basically this.

Compare that to the tangled mess of Lesson 18. Same game, way cleaner code.

## The Full Code

You can see the complete file in [`snake.py`](snake.py). It puts all of the steps above together into one file.

## Run It!

```
pip3 install pygame
python3 snake.py
```

Same controls as before -- arrow keys to move, Space to restart, Escape to quit.

You'll notice this version runs a bit slower (`time.sleep(1 / 4)` instead of `1 / 10`). You can change that speed in the last line.

## Experiments

1. **Speed it up** -- Change `time.sleep(1 / 4)` to `time.sleep(1 / 10)` to match the old version's speed. Try `1 / 15` for a real challenge.

2. **Add a method** -- Add a `length()` method to the Snake class that returns `len(self.body)`. Use it somewhere in the World.

3. **Color the head differently** -- In `Snake.draw()`, draw the first segment (index 0) in a different color from the rest. Maybe a green head with a yellow body?

4. **Make the apple blink** -- In `Apple.draw()`, use `time.time()` to check the time and only draw the apple every other half-second. (Hint: `int(time.time() * 2) % 2 == 0`)

5. **Add a speed boost** -- Make the game get faster as the score goes up. Instead of a fixed `time.sleep(1 / 4)`, calculate the delay based on `world.snake.score()`.

## Challenge

Add a **Poison Apple** class. It works like a regular Apple but it's colored purple and makes the snake *shorter* by one segment when eaten (use `self.body.pop()` an extra time). The World should have both a regular Apple and a Poison Apple on screen at the same time.

## What's Next

👉 [Go to #20 — Dungeon: The Hero](../20-dungeon-v1-hero/lesson.md)