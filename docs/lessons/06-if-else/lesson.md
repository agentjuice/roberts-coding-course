# Lesson 6: If-Else

!!! success "🎯 Mission"
    Make your program choose what to do based on a condition.


## Making Decisions

Up until now, Python runs every line top to bottom, no exceptions. But what if you want it to do something *only* when a condition is true? That's what `if` does. Create `decisions.py`:

```python
age = int(input("How old are you? "))

if age >= 13:
    print("You're a teenager!")
```

If the age is 13 or more, it prints the message. Otherwise, it does nothing and moves on.

**Important:** the indented line (4 spaces) is the code that runs *only* when the condition is true. Indentation matters in Python!

## Adding Else

What if you want to handle *both* cases?

```python
age = int(input("How old are you? "))

if age >= 13:
    print("You're a teenager!")
else:
    print("You're not a teenager yet!")
```

`else` catches everything that the `if` didn't.

## Multiple Paths with Elif

Sometimes there are more than two options. Use `elif` (short for "else if"):

```python
age = int(input("How old are you? "))

if age >= 18:
    print("You're an adult!")
elif age >= 13:
    print("You're a teenager!")
else:
    print("You're a kid!")
```

Python checks each condition from top to bottom and runs the **first** one that's true. Then it skips the rest.

## You Can Have Multiple Lines Inside

Everything indented under an `if` runs together:

```python
score = 95

if score >= 90:
    print("Amazing!")
    print("You got an A!")
    print("Keep it up!")
```

All three lines run because they're all indented under the `if`.

## Build: Age Checker

Create `age_checker.py`:

```python
name = input("What's your name? ")
age = int(input("How old are you? "))

print(f"\nHello, {name}!")

if age >= 16:
    print("You can drive!")
elif age >= 13:
    print("You can watch PG-13 movies!")
elif age >= 10:
    print("You're in double digits!")
else:
    print("You're still young — enjoy it!")

print(f"\nYou'll be {age + 1} next year!")
```

Try running it with different ages to see all the paths!

## What's Next?

In Lesson 7, you'll learn about all the **comparison operators** — more ways to write conditions.
