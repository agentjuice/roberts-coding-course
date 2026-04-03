# Lesson 12: Build -- Number Guessing Game

!!! success "🎯 Mission"
    Combine everything you've learned — variables, input, if-else, comparisons, loops, and lists — to build a real number guessing game.


## The Plan

The computer picks a random number between 1 and 100. You guess, and it tells you "too high" or "too low" until you get it right.

This uses:

- **Variables** to store the secret number and guess count
- **Input** to get guesses from the player
- **If-elif-else** to check if the guess is right, too high, or too low
- **While loop** to keep the game going
- **f-strings** to show feedback

## The Code

Create `guessing_game.py`:

```python
import random

secret = random.randint(1, 100)
guesses = 0

print("I'm thinking of a number between 1 and 100.")
print()

while True:
    answer = int(input("Your guess: "))
    guesses = guesses + 1

    if answer == secret:
        print(f"You got it in {guesses} guesses!")
        break
    elif answer > secret:
        print("Too high!")
    else:
        print("Too low!")
```

Run it with `python3 guessing_game.py` and try to beat it!

## How It Works

1. `random.randint(1, 100)` picks a random number and stores it in `secret`
2. The `while True` loop keeps asking for guesses
3. Each guess increases the counter
4. If the guess matches, we print the score and `break` out of the loop
5. Otherwise, we give a hint and loop again

## Make It Better

Try adding these features:

**Difficulty feedback** — tell the player how far off they are:

```python
diff = abs(answer - secret)
if diff > 30:
    print("Way off!")
elif diff > 10:
    print("Getting warmer...")
else:
    print("So close!")
```

**Limit the guesses** — give them only 7 tries:

```python
max_guesses = 7

while guesses < max_guesses:
    answer = int(input(f"Guess ({guesses + 1}/{max_guesses}): "))
    guesses = guesses + 1

    if answer == secret:
        print(f"You got it in {guesses} guesses!")
        break
    elif answer > secret:
        print("Too high!")
    else:
        print("Too low!")
else:
    print(f"Out of guesses! The number was {secret}.")
```

**Track all guesses** with a list:

```python
all_guesses = []

# Inside the loop, after each guess:
all_guesses.append(answer)
print(f"Your guesses so far: {all_guesses}")
```

## What's Next?

👉 [Go to #13 — Connect 4: Terminal Version](../13-connect4-v1/lesson.md)