# While Loops

!!! success "🎯 Mission"
    Learn how to make code repeat with `while` loops — including the powerful `while True` + `break` pattern.

Think about Minecraft — the game is constantly checking: Is it daytime? Are there mobs nearby? Is the player moving? That's a loop running 20 times per second, checking everything over and over. Every game you've ever played is powered by a loop that never stops running until you quit.

## Why Loops?

Imagine you want a password checker that keeps asking until you get it right. Without loops, you'd have to copy-paste the same code a hundred times and *hope* the user gets it within that many tries. Loops let you repeat code as many times as needed.

## while True + break

This is the most common loop pattern in games. Create `password.py`:

```python
while True:
    guess = input("Enter the password: ")
    if guess == "secret":
        print("Access granted!")
        break
    print("Wrong! Try again.")
```

Here's how it works:

- `while True:` means "keep looping forever"
- `break` means "stop the loop right now"
- So it keeps asking until you type "secret", then `break` escapes the loop

This is the exact same pattern every game uses for its **game loop**. The game runs `while True:` to keep going forever, and when you press Escape or choose "Quit to Menu," that's a `break`.

## while with a Condition

You can also loop while something is true:

```python
countdown = 5
while countdown > 0:
    print(countdown)
    countdown = countdown - 1
print("Blastoff!")
```

When `countdown` reaches 0, the condition `countdown > 0` becomes `False` and the loop stops.

## Counters

A **counter** is a variable that keeps track of how many times something happened:

```python
attempts = 0

while True:
    guess = input("Guess the password: ")
    attempts = attempts + 1

    if guess == "python":
        print(f"Got it in {attempts} tries!")
        break
    print("Nope!")
```

## Build: Countdown Timer

Create `countdown.py`:

```python
import time

number = int(input("Count down from what number? "))

while number > 0:
    print(number)
    time.sleep(1)
    number = number - 1

print("BLASTOFF! 🚀")
```

The `time.sleep(1)` pauses for 1 second between each number. Run it and watch it count down in real time!

## What's Next?

👉 [Next: For Loops](../10-for-loops/lesson.md)