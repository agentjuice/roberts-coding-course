# The Game Loop

!!! success "🎯 Mission"
    Understand the **game loop** -- the single most important concept in game programming. Every game ever made uses one, and after this lesson, you'll know exactly how it works.

## The Heartbeat of Every Game

Right now, on your computer, Minecraft runs a loop about 20 times per second. Every single tick, it does the same three things: check what the player is doing (input), update the world (physics, mobs moving, blocks breaking), and draw everything on screen (render). Then it does it again. And again. Forever.

**That's the game loop.**

Every game you've ever played -- Zelda, Mario Kart, F1 games, Fortnite -- they ALL have this exact same structure at their core.

Here's the pattern:

```python
while game_is_running:
    handle_input()    # What is the player doing?
    update_state()    # What changed in the world?
    draw_screen()     # Show everything on screen
    tick()            # Wait a tiny bit, then do it all again
```

That's it. Four steps, repeating forever. Let's break each one down.

## 1. Handle Input

This is where the game checks: **what is the player doing right now?**

- In Minecraft: did they press W to walk forward? Did they click to break a block?
- In Mario Kart: are they holding the accelerator? Did they press the drift button?
- In our demo below: did they press Escape to quit?

The game doesn't wait for you to do something. It just checks, really fast, every single frame. If you're not pressing anything, it moves on.

## 2. Update State

This is where the game **figures out what changed** since the last frame.

- In Minecraft: mobs move, gravity pulls falling blocks, crops grow, redstone circuits fire.
- In Fortnite: bullets travel, the storm circle shrinks, players take damage.
- In our demo: the ball moves a little bit and bounces off walls.

This is the "brain" of the game. All the rules and physics live here.

## 3. Draw Screen

This is where the game **shows you everything**.

It redraws the ENTIRE screen from scratch, every single frame. It doesn't move things around -- it erases everything and redraws it all in the new positions. This happens so fast (60+ times per second) that it looks like smooth motion.

Think of it like a flipbook. Each page is drawn fresh, but flip through them fast and you see animation.

## 4. Tick

The game waits just a tiny bit before doing it all again. This controls how fast the loop runs -- the **frame rate**.

Without this pause, the game would run as fast as your computer can go, which would be different on every machine. The tick keeps everything consistent.

!!! info "🎮 Fun Fact"
    Minecraft runs its game logic at **20 ticks per second**. Most console and PC games target **60 frames per second**. Competitive games like CS2 and Valorant run at **144+ fps** because pro players need every millisecond of responsiveness. The higher the frame rate, the smoother everything feels.

## Let's Build One

Time to see the game loop in action. We'll make the simplest possible visual demo: **a ball bouncing around a window**.

- **Input:** press Escape to quit
- **Update:** move the ball, bounce off walls
- **Draw:** fill the screen, draw the ball
- **Tick:** control frame rate

Here's the complete code:

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Bouncing Ball")
clock = pygame.time.Clock()

# Ball state
x, y = 300, 200       # Starting position (center of window)
dx, dy = 4, 3         # Speed: 4 pixels right, 3 pixels down per frame

running = True
while running:
    # 1. INPUT -- check what the player is doing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # 2. UPDATE -- move the ball and bounce off walls
    x += dx
    y += dy
    if x <= 15 or x >= 585:   # Hit left or right wall
        dx = -dx
    if y <= 15 or y >= 385:   # Hit top or bottom wall
        dy = -dy

    # 3. DRAW -- clear screen and draw ball in new position
    screen.fill('Black')
    pygame.draw.circle(screen, 'Cyan', (x, y), 15)
    pygame.display.flip()

    # 4. TICK -- run at 60 frames per second
    clock.tick(60)

pygame.quit()
```

That's under 35 lines, and it's a complete game loop with real graphics. Every game you'll build from here follows this exact same pattern.

## Run It!

Save the file and run:

```bash
python3 bouncing_ball.py
```

You should see a cyan ball bouncing around a black window. Press Escape (or close the window) to quit.

!!! example "🧪 Experiments"
    1. **Change the speed** -- Try setting `dx, dy = 8, 6`. What happens? Try `1, 1` for slow motion.

    2. **Change the frame rate** -- Change `clock.tick(60)` to `clock.tick(10)`. Now try `clock.tick(144)`. See how the frame rate changes the feel?

    3. **Add a second ball** -- Create `x2, y2, dx2, dy2` variables and draw a second circle with a different color. Each ball bounces independently!

    4. **Change the color on bounce** -- Make the ball change color every time it hits a wall. (Hint: store the color in a variable and change it when you flip `dx` or `dy`.)

    5. **Make it leave a trail** -- What happens if you remove the `screen.fill('Black')` line? The ball draws over itself without erasing!

!!! abstract "🏆 Challenge"
    Add keyboard controls: use the arrow keys to change the ball's direction while it's moving. You'll need to check for `pygame.K_UP`, `pygame.K_DOWN`, `pygame.K_LEFT`, and `pygame.K_RIGHT` in the input section and modify `dx` and `dy` accordingly.

## What's Next

👉 [Go to #16 — Connect 4: Pygame](../16-connect4-v3-pygame/lesson.md)
