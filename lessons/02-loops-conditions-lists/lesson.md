# Lesson 2: Loops, Conditions & Lists

**Goal:** Master the building blocks of logic and build a multiple-choice quiz game.

## New Concepts

- `if` / `elif` / `else` — making decisions
- Comparison operators — `==`, `!=`, `<`, `>`, `<=`, `>=`
- `while True:` and `break`
- `for` loops and `range()`
- **Lists** — storing multiple items in one place
- List operations — `append()`, `pop()`, `len()`, `in`

## Making Decisions with `if`

Programs need to make choices. "If the player's score is above 90, print 'Amazing!' — otherwise, print 'Keep trying!'"

```python
score = 95

if score > 90:
    print("Amazing!")
else:
    print("Keep trying!")
```

The indented code under `if` only runs when the condition is `True`. The code under `else` only runs when it's `False`.

What if you need more than two options? Use `elif` (short for "else if"):

```python
score = 75

if score >= 90:
    print("A — Amazing!")
elif score >= 80:
    print("B — Great job!")
elif score >= 70:
    print("C — Not bad!")
elif score >= 60:
    print("D — You passed... barely.")
else:
    print("F — Try again.")
```

Python checks each condition from top to bottom and runs the **first** one that's true, then skips the rest.

## Comparison Operators

Here are all the ways to compare things:

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | equals | `5 == 5` is `True` |
| `!=` | not equals | `5 != 3` is `True` |
| `<` | less than | `3 < 5` is `True` |
| `>` | greater than | `5 > 3` is `True` |
| `<=` | less than or equal | `5 <= 5` is `True` |
| `>=` | greater than or equal | `7 >= 3` is `True` |

**Watch out:** `=` is for putting something in a variable. `==` is for checking if two things are equal. Mixing them up is a super common mistake.

## Loops — Doing Things More Than Once

### `while` loops

A `while` loop keeps running as long as its condition is true.

```python
count = 0
while count < 5:
    print(f"Count is {count}")
    count = count + 1
```

This prints 0, 1, 2, 3, 4 — then stops because `count` hits 5 and the condition `count < 5` becomes `False`.

### `while True` and `break`

Sometimes you don't know ahead of time when to stop. Use `while True:` to loop forever, and `break` to escape:

```python
while True:
    command = input("Type 'quit' to exit: ")
    if command == "quit":
        print("Bye!")
        break
    print(f"You typed: {command}")
```

### `for` loops

A `for` loop goes through a collection of items, one at a time.

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")
```

### `range()` — Counting with `for`

`range()` gives you a sequence of numbers. Super useful with `for`:

```python
for i in range(5):
    print(i)
# Prints: 0, 1, 2, 3, 4
```

You can also set a start and end:

```python
for i in range(1, 6):
    print(i)
# Prints: 1, 2, 3, 4, 5
```

Notice: `range(1, 6)` goes up to but **doesn't include** 6. Yeah, it's weird. You get used to it.

## Lists — Storing Multiple Things

A **list** is like a row of labeled boxes. Instead of making a separate variable for each item, you put them all in one place.

```python
colors = ["red", "green", "blue", "yellow"]
```

### Getting items by index

Each item has a position number called an **index**, starting at 0:

```python
print(colors[0])   # "red"
print(colors[1])   # "green"
print(colors[3])   # "yellow"
```

Yes, counting starts at 0, not 1. Every programmer finds this annoying at first.

### Useful list operations

```python
colors = ["red", "green", "blue"]

# How many items?
print(len(colors))          # 3

# Add to the end
colors.append("purple")     # ["red", "green", "blue", "purple"]

# Remove the last item
last = colors.pop()         # last = "purple", list is back to 3 items

# Check if something is in the list
if "red" in colors:
    print("Red is here!")

# Loop through the list
for color in colors:
    print(color)
```

### Lists can hold anything

```python
numbers = [10, 20, 30, 40]
mixed = ["hello", 42, True, 3.14]
empty = []
```

## Let's Build: Quiz Game

We're going to build a quiz game that:

1. Stores questions, answer choices, and correct answers
2. Asks each question one at a time
3. Checks if the player got it right
4. Tracks and displays the final score

### Step 1: Store the questions

We'll use a **list of dictionaries**. A dictionary (we'll cover these more later) is like a mini form — it stores labeled pieces of information.

```python
questions = [
    {
        "question": "What planet is closest to the Sun?",
        "choices": ["A) Venus", "B) Mercury", "C) Mars", "D) Earth"],
        "answer": "B"
    },
    {
        "question": "What language is this course teaching?",
        "choices": ["A) JavaScript", "B) Scratch", "C) Python", "D) Java"],
        "answer": "C"
    },
]
```

Each question has three parts: the question text, a list of choices, and the correct answer letter.

### Step 2: Loop through the questions

```python
score = 0

for i in range(len(questions)):
    q = questions[i]
    print(f"\nQuestion {i + 1}: {q['question']}")

    for choice in q["choices"]:
        print(f"  {choice}")

    player_answer = input("Your answer (A/B/C/D): ").upper()

    if player_answer == q["answer"]:
        print("Correct!")
        score = score + 1
    else:
        print(f"Wrong! The answer was {q['answer']}.")
```

- `range(len(questions))` gives us 0, 1, 2, ... for each question
- `.upper()` converts the player's input to uppercase, so "b" and "B" both work
- We check their answer against the stored correct answer

### Step 3: Show the results

```python
print(f"\n=== Results ===")
print(f"You got {score} out of {len(questions)} right!")

percentage = int(score / len(questions) * 100)

if percentage == 100:
    print("PERFECT SCORE! You're a genius!")
elif percentage >= 80:
    print("Great job!")
elif percentage >= 60:
    print("Not bad! Study up and try again.")
else:
    print("Keep learning — you'll get there!")
```

### The Full Game

Here's the complete file. This is saved as `quiz_game.py` in this folder.

```python
questions = [
    {
        "question": "What planet is closest to the Sun?",
        "choices": ["A) Venus", "B) Mercury", "C) Mars", "D) Earth"],
        "answer": "B"
    },
    {
        "question": "What language is this course teaching?",
        "choices": ["A) JavaScript", "B) Scratch", "C) Python", "D) Java"],
        "answer": "C"
    },
    {
        "question": "What does the print() function do?",
        "choices": ["A) Prints on paper", "B) Shows text on screen", "C) Deletes text", "D) Saves a file"],
        "answer": "B"
    },
    {
        "question": "What symbol do you use for 'equals' in a comparison?",
        "choices": ["A) =", "B) =>", "C) ==", "D) !="],
        "answer": "C"
    },
    {
        "question": "In Python, what index is the FIRST item in a list?",
        "choices": ["A) 1", "B) 0", "C) -1", "D) 2"],
        "answer": "B"
    },
]

print("=== Robert's Quiz Game ===")
print(f"Answer {len(questions)} questions. Let's see how you do!\n")

score = 0

for i in range(len(questions)):
    q = questions[i]
    print(f"Question {i + 1}: {q['question']}")

    for choice in q["choices"]:
        print(f"  {choice}")

    player_answer = input("Your answer (A/B/C/D): ").upper()

    if player_answer == q["answer"]:
        print("Correct!\n")
        score = score + 1
    else:
        print(f"Wrong! The answer was {q['answer']}.\n")

print("=== Results ===")
print(f"You got {score} out of {len(questions)} right!")

percentage = int(score / len(questions) * 100)

if percentage == 100:
    print("PERFECT SCORE! You're a genius!")
elif percentage >= 80:
    print("Great job!")
elif percentage >= 60:
    print("Not bad! Study up and try again.")
else:
    print("Keep learning — you'll get there!")
```

## Run It!

Save this as `quiz_game.py` and run:

```bash
python quiz_game.py
```

## Experiments

1. **Add a question.** Copy one of the existing question dictionaries and change it to your own question. Does it show up in the game?

2. **Shuffle the questions.** Add `import random` at the top and `random.shuffle(questions)` before the loop. Now the order is different every time.

3. **Show the question number differently.** Instead of "Question 1", try "Question 1 of 5". Hint: use `len(questions)` in the f-string.

4. **Add a timer.** Can you figure out how to show how long the whole quiz took? Look up `import time` and `time.time()`.

5. **Wrong answer feedback.** When the player gets one wrong, show what the correct answer actually said (not just the letter). You'll need to find the right choice from the list.

## Challenge

Add a **category** field to each question (like "Science", "Python", "Math"). After the quiz, show a breakdown: "Science: 1/2 correct, Python: 2/3 correct." You'll need to track scores per category — try using a dictionary.

## What's Next

In Lesson 3, we'll learn about functions (reusable blocks of code) and dictionaries (like lists, but with named keys instead of numbers) — and build a contact book app.
