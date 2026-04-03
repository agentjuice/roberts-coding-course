# Lesson 7: Comparisons

!!! success "🎯 Mission"
    Learn all the comparison operators and how to combine them with `and`, `or`, and `not`.


## The Comparison Operators

You already used `>=` in Lesson 6. Here's the full set. Create `comparisons.py`:

```python
x = 10

print(x == 10)    # True  — "is equal to"
print(x != 5)     # True  — "is NOT equal to"
print(x > 5)      # True  — "greater than"
print(x < 20)     # True  — "less than"
print(x >= 10)    # True  — "greater than or equal to"
print(x <= 9)     # False — "less than or equal to"
```

Each one gives back `True` or `False` — a boolean.

**Watch out:** `==` (two equals signs) *checks* if things are equal. `=` (one equals sign) *stores* a value. Mixing them up is a super common mistake.

## Combining with `and`

`and` means **both** conditions must be true:

```python
age = 15
has_ticket = True

if age >= 13 and has_ticket:
    print("You can enter!")
```

## Combining with `or`

`or` means **at least one** condition must be true:

```python
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")
```

## Flipping with `not`

`not` flips `True` to `False` and `False` to `True`:

```python
is_raining = False

if not is_raining:
    print("Let's go outside!")
```

## Strings Can Be Compared Too

```python
answer = input("What's the password? ")

if answer == "secret123":
    print("Access granted!")
else:
    print("Wrong password!")
```

## Build: Quiz Game

Create `quiz.py`:

```python
score = 0

answer = input("What planet is closest to the sun? ")
if answer == "Mercury" or answer == "mercury":
    print("Correct!")
    score = score + 1
else:
    print("Nope — it's Mercury!")

answer = int(input("What is 7 * 8? "))
if answer == 56:
    print("Correct!")
    score = score + 1
else:
    print("Nope — it's 56!")

answer = input("True or False: Python is named after a snake. ")
if answer == "False" or answer == "false":
    print("Correct! It's named after Monty Python.")
    score = score + 1
else:
    print("Nope — it's named after the comedy show Monty Python!")

print(f"\nYou got {score} out of 3!")

if score == 3:
    print("Perfect score!")
elif score >= 2:
    print("Nice job!")
else:
    print("Better luck next time!")
```

## What's Next?

In Lesson 8, you'll learn about **while loops** — how to make code repeat over and over.
