# Lesson 3: Loops -- Repeating Things

!!! success "🎯 Mission"
    Learn how to make code repeat, and build a number guessing game.


---

## Why Loops?

Imagine you wanted to print "hello" 100 times. You *could* write this:

```python
print("hello")
print("hello")
print("hello")
print("hello")
# ... 96 more times
```

That would be awful. Nobody wants to do that. And what if you wanted to change it to 200 times? Or 1,000? You'd lose your mind.

Loops let you tell Python: "Hey, do this thing over and over." One line of loop code can replace hundreds of copy-pasted lines. Loops are one of the most powerful ideas in programming.

---

## `while True` with `break`

The simplest kind of loop is one that runs forever -- until you tell it to stop. It looks like this:

```python
while True:
    print("This runs forever!")
```

!!! warning
    If you run that code, it will literally print "This runs forever!" nonstop until you close the terminal. To stop a runaway program, press **Ctrl + C** in the terminal. That's your emergency stop button.

Okay, so a loop that runs forever isn't very useful by itself. But add a `break` statement and now you've got something useful. `break` means "stop the loop right now and move on."

Here's a real example -- a password checker:

```python
while True:
    password = input("Enter the password: ")
    if password == "python123":
        print("Access granted!")
        break
    else:
        print("Wrong password. Try again.")
```

This keeps asking for the password forever. But the moment someone types "python123", it prints "Access granted!" and `break` escapes the loop. Try it! Create a new file called **password.py**, paste that in, save with **Cmd + S**, and run it:

```bash
python3 password.py
```

Type the wrong password a few times, then type the right one. See how it works?

---

## `while` with a Condition

You don't always need `while True`. You can put any condition after `while`, and the loop will keep going as long as that condition is true.

Here's a countdown:

```python
count = 10
while count > 0:
    print(count)
    count = count - 1
print("Liftoff!")
```

Let's walk through it:

- `count` starts at 10
- The loop checks: is `count > 0`? Yes (10 is greater than 0), so it runs the code inside
- It prints 10, then subtracts 1 so `count` becomes 9
- Back to the top: is 9 > 0? Yes. Print 9, subtract 1, count becomes 8
- This keeps going... 7, 6, 5, 4, 3, 2, 1
- Now `count` is 0. Is 0 > 0? Nope! The loop stops.
- Python moves on to `print("Liftoff!")`

Here's another one -- counting UP to a number the user picks:

```python
target = int(input("Count up to what number? "))
number = 1
while number <= target:
    print(number)
    number = number + 1
```

---

## Counters

You just saw the **counter pattern** -- it's one of the most common things in programming. The idea is:

1. Start a variable at some number
2. Use it inside the loop
3. Add 1 (or subtract 1) each time through

```python
i = 0
while i < 5:
    print(f"i is {i}")
    i = i + 1
```

This prints:

```
i is 0
i is 1
i is 2
i is 3
i is 4
```

Notice it prints 0 through 4 -- that's five numbers total, but it stops *before* reaching 5. That's because the condition is `i < 5`, not `i <= 5`.

The line `i = i + 1` looks weird at first. In math class, `i = i + 1` makes no sense. But in Python, `=` means "set this variable to..." So it means "take the current value of `i`, add 1, and store the result back in `i`." It's just bumping the number up by one.

You can count down too:

```python
i = 5
while i > 0:
    print(f"i is {i}")
    i = i - 1
```

---

## `for i in range()`

Python has a shortcut for counting loops called `for` with `range()`. Instead of setting up a counter variable yourself, `range()` does it for you.

```python
for i in range(5):
    print(i)
```

This prints 0, 1, 2, 3, 4. That's the same thing as the `while` counter loop we wrote above, but way shorter.

Here's what `range()` can do:

**`range(5)`** -- gives you 0, 1, 2, 3, 4 (five numbers, starting at 0)

```python
for i in range(5):
    print(i)
# 0 1 2 3 4
```

**`range(1, 11)`** -- gives you 1 through 10 (starts at 1, stops *before* 11)

```python
for i in range(1, 11):
    print(i)
# 1 2 3 4 5 6 7 8 9 10
```

**`range(0, 20, 2)`** -- gives you even numbers from 0 to 18 (the 2 means "count by twos")

```python
for i in range(0, 20, 2):
    print(i)
# 0 2 4 6 8 10 12 14 16 18
```

**`range(10, 0, -1)`** -- countdown from 10 to 1 (the -1 means "count backwards")

```python
for i in range(10, 0, -1):
    print(i)
print("Liftoff!")
# 10 9 8 7 6 5 4 3 2 1 Liftoff!
```

!!! tip
    The `range()` function always stops *before* the second number. So `range(1, 11)` gives you 1 through 10, not 1 through 11. It's a little weird, but you get used to it.

---

## `for` Loops with Strings

You can also use `for` to loop through each character in a string, one at a time:

```python
name = "Robert"
for letter in name:
    print(letter)
```

This prints:

```
R
o
b
e
r
t
```

Each time through the loop, `letter` holds the next character. Here's a fun one -- a spy encoder that adds a dash between every letter:

```python
word = input("Enter a word: ")
coded = ""
for letter in word:
    coded = coded + letter + "-"
print(coded)
```

If you type "hello", it prints `h-e-l-l-o-`. (Don't worry about the extra dash at the end -- we'll learn how to fix that kind of thing later.)

---

## Nested Loops

What happens if you put a loop *inside* another loop? You get a **nested loop**. The inner loop runs all the way through for *each* time the outer loop runs once.

Here's an example that prints a rectangle of stars:

```python
for row in range(3):
    for col in range(5):
        print("*", end="")
    print()
```

Output:

```
*****
*****
*****
```

The `end=""` part tells `print` not to go to a new line after each star. Then the `print()` at the end of each row adds the newline.

Let's walk through it:

- Outer loop: `row` is 0. Inner loop prints 5 stars. Then `print()` makes a new line.
- Outer loop: `row` is 1. Inner loop prints 5 stars again. New line.
- Outer loop: `row` is 2. Inner loop prints 5 more stars. New line.

Here's a multiplication table using nested loops:

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i * j:4}", end="")
    print()
```

Output:

```
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
```

The `{i * j:4}` part means "print the number, but pad it so it takes up 4 spaces." That's what makes the columns line up nice and neat.

---

## Common Loop Patterns

Here are some patterns you'll use ALL the time. These are worth remembering.

### Summing Numbers

Add up all the numbers from 1 to 100:

```python
total = 0
for i in range(1, 101):
    total = total + i
print(f"The sum of 1 to 100 is {total}")
```

The answer is 5050. (A mathematician named Gauss figured out a shortcut for this when he was a kid, but loops work just fine too.)

### Finding Things

Find the first even number greater than 17:

```python
for i in range(18, 100):
    if i % 2 == 0:
        print(f"Found it: {i}")
        break
```

The `%` operator gives you the remainder after division. If `i % 2 == 0`, that means `i` divides evenly by 2, so it's even.

### Repeating Until Valid Input

Keep asking until the user types an actual number:

```python
while True:
    text = input("Enter a number: ")
    if text.isdigit():
        number = int(text)
        print(f"Thanks! You entered {number}.")
        break
    else:
        print("That's not a number. Try again.")
```

The `.isdigit()` method returns `True` if the text is all digits. This is great for making your programs crash-proof.

### Building Up a String

Build a string character by character:

```python
result = ""
for i in range(1, 6):
    result = result + str(i) + " "
print(result)
```

Output: `1 2 3 4 5 `

The `str(i)` part converts the number `i` into text so you can glue it onto the string.

---

## Build Project: Number Guessing Game

Alright, let's put this all together and build something fun. We're going to make a number guessing game where:

1. The computer picks a secret random number between 1 and 100
2. You guess, and it tells you "Too high!" or "Too low!"
3. It counts your guesses
4. When you get it right, it tells you how many guesses it took

Create a new file called **guessing_game.py** (Cmd + N, then Cmd + S, save in your `coding-course` folder).

### Step 1: Pick a Random Number

```python
import random

secret = random.randint(1, 100)
```

`import random` tells Python you want to use the `random` toolbox. `random.randint(1, 100)` picks a random whole number from 1 to 100.

### Step 2: Welcome the Player

```python
print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print("Can you guess it?")
print()
```

### Step 3: Set Up a Guess Counter

```python
guesses = 0
```

This variable will keep track of how many tries the player takes.

### Step 4: The Game Loop

Here's where the loop comes in. We use `while True` so the game keeps asking for guesses, and `break` when they get it right:

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

### The Full Game

Here's the complete file all together:

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

---

## Run It!

Save the file (Cmd + S) and run it in the terminal:

```bash
python3 guessing_game.py
```

Play a few rounds! Try to guess the number in as few tries as possible. If you use the strategy of always guessing the middle of the remaining range, you can get any number in 7 guesses or fewer.

---

!!! example "🧪 Experiments"
    Try these changes to your guessing game. Make a change, save, run, see what happens:

    1. **Limit to 7 guesses.** After the line `guesses = guesses + 1`, add this:
        ```python
            if guesses >= 7:
                print(f"Out of guesses! The number was {secret}.")
                break
        ```
        Now the player only gets 7 tries. Can you still win?

    2. **Add difficulty levels.** Before the game loop, ask the player to pick easy (1-10), medium (1-100), or hard (1-1000). Use their choice to set the range for `random.randint()`.

    3. **Give a hint about even or odd.** At the start of the game, add:
        ```python
        if secret % 2 == 0:
            print("Hint: the number is even.")
        else:
            print("Hint: the number is odd.")
        ```

    4. **Show how far off they are.** After "Too low!" or "Too high!", add: `print(f"You were off by {abs(secret - answer)}")`

    5. **Add a play again feature.** Wrap the whole game in another `while True:` loop. After the player wins (or runs out of guesses), ask `"Play again? (y/n) "`. If they type "y", pick a new `secret` and reset `guesses` to 0. If not, `break` out of the outer loop.

---

!!! abstract "🏆 Challenge"
    Here's a tough one: flip the game around. Instead of YOU guessing the computer's number, make the **computer guess YOUR number**.

    Here's how it works:

    1. You think of a number between 1 and 100 (don't tell the computer!)
    2. The computer guesses
    3. You type "h" if the guess is too high, "l" if it's too low, or "c" if it's correct
    4. The computer uses your feedback to make a smarter guess next time

    The trick is called **binary search** -- the computer should always guess the middle of the remaining range. If you say "too high," it throws away everything above its guess. If you say "too low," it throws away everything below. Each guess cuts the possibilities in half.

    With this strategy, the computer can ALWAYS guess your number in 7 tries or fewer. Every single time. That's the power of binary search.

    Hint: you'll need two variables, `low` and `high`, that start at 1 and 100. The computer's guess is `(low + high) // 2` (the `//` means divide and round down). If you say "too high," set `high = guess - 1`. If "too low," set `low = guess + 1`.

---

## What's Next

In Lesson 4, we'll learn about **lists** -- storing collections of things -- and build a playlist manager. See you there!
