# Lesson 8: While Loops

!!! success "🎯 Mission"
    Learn how to make code repeat with `while` loops — including the powerful `while True` + `break` pattern.


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

In Lesson 9, you'll learn about **for loops** — a different kind of loop that's great when you know exactly how many times to repeat.
