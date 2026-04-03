# Lesson 1: The Basics

**Goal:** Learn how Python works and build a number guessing game.

## New Concepts

- What a program is
- `print()` — showing text on screen
- **Variables** — storing values
- **Types** — strings, integers, floats, booleans
- `input()` — getting info from the user
- `int()` — converting text to a number
- **f-strings** — putting variables inside text
- `import random` — using Python's built-in tools

## What Is a Program?

A program is just a list of instructions for your computer. Python reads your instructions from top to bottom, one line at a time, and does exactly what you tell it.

Create a file called `hello.py` and type this:

```python
print("Hello, world!")
print("My name is Robert.")
print("I am learning Python!")
```

Run it:

```bash
python hello.py
```

You should see all three lines printed out, in order. That's it — you just wrote a program.

## Talking to the Screen with `print()`

`print()` is how your program talks to you. Whatever you put inside the parentheses shows up on screen.

```python
print("This is a string — text inside quotes.")
print(42)
print(3.14)
```

## Variables — Labeled Boxes

A **variable** is like a labeled box. You put something in the box, and later you can look inside by using the label.

```python
name = "Robert"
age = 11
height = 4.9
likes_python = True
```

Here's what's going on:

- `name` holds a **string** (text, always in quotes)
- `age` holds an **integer** (a whole number)
- `height` holds a **float** (a number with a decimal point)
- `likes_python` holds a **boolean** (`True` or `False`)

You can use variables in `print()`:

```python
print(name)
print(age)
```

## f-strings — Mixing Text and Variables

What if you want to say "Robert is 11 years old"? You could do this:

```python
print("Robert is 11 years old")
```

But that's boring — it only works for one person. **f-strings** let you plug variables right into text. Put an `f` before the opening quote, then use `{}` around your variables:

```python
name = "Robert"
age = 11
print(f"{name} is {age} years old")
```

That prints: `Robert is 11 years old`

The `f` stands for "format." You'll use f-strings constantly.

## Asking the User with `input()`

`input()` pauses your program and waits for the user to type something.

```python
favorite_color = input("What's your favorite color? ")
print(f"Cool, {favorite_color} is a great color!")
```

**Important:** `input()` always gives you a string, even if the user types a number. If someone types `42`, Python sees it as the text `"42"`, not the number `42`.

To turn it into a real number, wrap it with `int()`:

```python
age = input("How old are you? ")
age = int(age)           # now it's a real number
next_year = age + 1
print(f"Next year you'll be {next_year}!")
```

## Let's Build: Number Guessing Game

Time to put it all together. We're going to build a game where:

1. The computer picks a random number between 1 and 100
2. You guess the number
3. The computer tells you if you're too high or too low
4. You keep guessing until you get it

### Step 1: Pick a random number

Python has a built-in tool called `random` that can pick numbers for us. We need to **import** it — that just means "hey Python, I want to use this tool."

```python
import random

secret = random.randint(1, 100)
```

`random.randint(1, 100)` picks a random whole number from 1 to 100 and stores it in `secret`.

### Step 2: Set up the game

```python
print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print("Can you guess it?")
print()

guesses = 0
```

We use `guesses` to count how many tries it takes.

### Step 3: The guessing loop

We need the game to keep asking until the player gets it right. That's a **while loop** — it repeats a block of code as long as something is true.

```python
while True:
    answer = input("Your guess: ")
    answer = int(answer)
    guesses = guesses + 1

    if answer < secret:
        print("Too low! Try higher.")
    elif answer > secret:
        print("Too high! Try lower.")
    else:
        print(f"You got it! The number was {secret}.")
        print(f"It took you {guesses} guesses.")
        break
```

- `while True:` means "keep going forever" (until we say `break`)
- `if`/`elif`/`else` checks the three possibilities
- `break` escapes the loop when the player wins

### The Full Game

Here's the complete file. This is saved as `guessing_game.py` in this folder.

```python
import random

secret = random.randint(1, 100)

print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print("Can you guess it?")
print()

guesses = 0

while True:
    answer = input("Your guess: ")
    answer = int(answer)
    guesses = guesses + 1

    if answer < secret:
        print("Too low! Try higher.")
    elif answer > secret:
        print("Too high! Try lower.")
    else:
        print(f"You got it! The number was {secret}.")
        print(f"It took you {guesses} guesses.")
        break
```

## Run It!

Save this as `guessing_game.py` and run:

```bash
python guessing_game.py
```

Try to guess the number in as few tries as possible. A good strategy: always guess the middle of the remaining range. (That's called **binary search** — you'll learn more about it later.)

## Experiments

1. **Change the range.** Replace `random.randint(1, 100)` with `random.randint(1, 10)`. Way easier, right?

2. **Add hot/cold hints.** After "Too low!" or "Too high!", can you also print how far off the guess was? Try `print(f"You were off by {abs(secret - answer)}")`.

3. **Limit the guesses.** What if the player only gets 7 tries? You'll need to check `if guesses >= 7:` and print "Game over!" then `break`.

4. **Change the messages.** Make the hints sillier — "WAAAY too high!" if they're off by more than 30, "So close!" if they're within 5.

5. **Ask for their name.** Use `input()` at the start to ask the player's name, then use it in the victory message.

## Challenge

Add a **play again** feature. After the player wins (or loses), ask "Play again? (y/n)". If they say "y", pick a new number and start over. If "n", print "Thanks for playing!" and end the program.

Hint: you'll need another `while True:` loop that wraps around the whole game.

## What's Next

In Lesson 2, we'll go deeper into loops, conditions, and lists — and build a quiz game that tracks your score.
