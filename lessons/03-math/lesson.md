# Math & Numbers

!!! success "🎯 Mission"
    Learn how to do math in Python, combine it with variables, and use randomness — a key ingredient in every game.

Games are full of math. When a Creeper explodes in Minecraft, the game calculates the distance to every nearby block and figures out the damage. When you boost in Mario Kart, the game multiplies your speed by 1.5. When loot drops in Zelda, the game rolls a random number to decide what you get. Let's learn how Python does math.

## Basic Operators

Create `math_stuff.py`:

```python
print(10 + 3)    # 13  (addition)
print(10 - 3)    # 7   (subtraction)
print(10 * 3)    # 30  (multiplication)
print(10 / 3)    # 3.333...  (division)
print(10 // 3)   # 3   (division, rounded down)
print(10 ** 3)   # 1000 (power — 10 × 10 × 10)
print(10 % 3)    # 1   (remainder — "modulo")
```

That last one, `%` (modulo), is surprisingly useful in games. Want to check if a number is even or odd? `number % 2` gives you `0` for even, `1` for odd. Want something to happen every 10th frame? `frame % 10 == 0`.

## Math with Variables

Here's where it gets powerful — combine math with variables:

```python
health = 100
damage = 25

health = health - damage
print(health)    # 75

health = health - damage
print(health)    # 50
```

!!! warning "⚠️ Watch Out"
    Remember: `=` does NOT mean "equals" in Python. It means **"store this value."** When you write `health = health - damage`, you're saying: "take the current health, subtract the damage, and store the result back in health." It's like updating a scoreboard, not solving a math equation.

There's a shorthand for this that you'll see a lot:

```python
score = 0
score += 10    # same as: score = score + 10
score += 10    # score is now 20
score -= 5     # same as: score = score - 5, score is now 15
score *= 2     # same as: score = score * 2, score is now 30
```

## Randomness

Here's something every game needs: **random numbers**. When a zombie spawns in Minecraft, its position is random. When you open a chest in Zelda, the loot is random. When an F1 car has a mechanical failure, it's (simulated) random.

Python has a built-in tool for this called `random`:

```python
import random

# Random integer between 1 and 6 (like rolling a dice)
dice = random.randint(1, 6)
print(f"You rolled a {dice}!")

# Random integer between 1 and 100
number = random.randint(1, 100)
print(f"Secret number: {number}")
```

`import random` loads Python's random number toolkit. You only need to write it once at the top of your file.

!!! info "🎮 Fun Fact"
    Computers can't actually be truly random — they use complex math formulas that *look* random but are completely predictable if you know the starting number (called a "seed"). That's why Minecraft lets you enter a world seed — the same seed always generates the same world!

## Random Choices

You can also pick a random item from a list:

```python
import random

weapons = ["sword", "axe", "bow", "staff"]
drop = random.choice(weapons)
print(f"The enemy dropped a {drop}!")
```

And check random chances:

```python
import random

# 30% chance to drop loot
if random.random() < 0.3:
    print("The enemy dropped a health potion!")
else:
    print("No loot this time.")
```

`random.random()` gives you a decimal between 0 and 1. If it's less than 0.3, that happens about 30% of the time. This is exactly how loot drop rates work in real games.

## Build: Dice Roller

Create `dice.py`:

```python
import random

print("🎲 Dice Roller 🎲")
print()

while True:
    input("Press Enter to roll... ")
    
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1 + die2
    
    print(f"  Die 1: {die1}")
    print(f"  Die 2: {die2}")
    print(f"  Total: {total}")
    
    if total == 12:
        print("  🎉 DOUBLE SIXES!")
    elif total == 2:
        print("  💀 Snake eyes!")
    
    print()
```

## What's Next?

👉 [Next: Types](../04-types/lesson.md)