# Lesson 1: The Basics

**Goal:** Learn how Python works and build a number guessing game.

---

## Your Very First Program

Okay, let's write some code. For real. Right now.

### Opening VS Code

1. Press **Cmd + Space** to open Spotlight
2. Type **Visual Studio Code** and hit **Enter**

VS Code should open up. If it's your first time, you might see some welcome stuff -- just close those tabs.

### Creating a New File

1. Go to **File > New File** at the top menu (or press **Cmd + N**)
2. You'll see a blank file. Now save it right away: press **Cmd + S**
3. A save window will pop up. Navigate to the `coding-course` folder on your Desktop
4. Name the file **hello.py** (the `.py` at the end tells your computer this is a Python file)
5. Click **Save**

### Writing Your First Line of Code

In that empty file, type this one line:

```python
print("hello world")
```

That's it. One line. Let's run it and see what happens.

### Running Your Code

We need to open the Terminal inside VS Code. Go to **View > Terminal** at the top menu (or press **Ctrl + `** -- that's the backtick key, the one right above Tab on your keyboard).

A terminal panel will slide up at the bottom of VS Code. First, let's navigate to your coding folder. Type this and hit Enter:

```bash
cd ~/Desktop/coding-course
```

Now run your program by typing this and hitting Enter:

```bash
python3 hello.py
```

You should see:

```
hello world
```

That's it. You just wrote a program and ran it. Your computer read your instruction and did exactly what you told it to do -- it printed "hello world" on the screen.

---

## Making It Say More

Now let's make it do more. Go back to your `hello.py` file and change it to this:

```python
print("hello world")
print("my name is Robert")
print("I am learning Python!")
```

Save the file (Cmd + S), then go back to the terminal and run it again:

```bash
python3 hello.py
```

Now you should see all three lines, one after the other:

```
hello world
my name is Robert
I am learning Python!
```

See how Python reads your code from top to bottom? It does the first `print`, then the second, then the third. A program is just a list of instructions, and Python follows them in order. That's really all there is to it.

Try changing what's inside the quotes to whatever you want. Save and run it again. Go ahead, I'll wait.

---

## Talking to the Screen with `print()`

`print()` is how your program talks to you. Whatever you put inside the parentheses shows up on screen.

You can print words (they need to be in quotes):

```python
print("This is some text")
```

You can also print numbers (no quotes needed for numbers):

```python
print(42)
print(3.14)
```

Try adding some of these to your `hello.py` file and running it again to see what happens.

---

## Variables -- Giving Names to Things

You know how in math class you might write `x = 5`? Python has something like that, called **variables**. A variable is like a labeled box -- you put something in the box, and later you can use the label to get it back.

Create a new file. Go to **File > New File** (or Cmd + N), then **Cmd + S** to save it in your `coding-course` folder. Name it **variables.py**.

Type this:

```python
name = "Robert"
print(name)
```

Save it (Cmd + S) and run it:

```bash
python3 variables.py
```

It prints `Robert`. See what happened? You stored the word "Robert" inside a variable called `name`, and then you told Python to print whatever is inside `name`.

Let's add more variables:

```python
name = "Robert"
age = 11
height = 4.9
likes_minecraft = True

print(name)
print(age)
print(height)
print(likes_minecraft)
```

Save and run it. You'll see each value printed on its own line.

Here's what's going on with each one:

- `name` holds **text** (programmers call this a "string"). Text always goes inside quotes.
- `age` holds a **whole number** (programmers call this an "integer"). No quotes needed.
- `height` holds a **decimal number** (programmers call this a "float"). Also no quotes.
- `likes_minecraft` holds either `True` or `False` (programmers call this a "boolean"). Think of it like a yes/no switch.

You don't need to memorize those programmer words right now. Just know that Python can store text, numbers, and true/false values.

---

## f-strings -- Mixing Text and Variables

What if you want to print something like "Robert is 11 years old"? You could do this:

```python
print("Robert is 11 years old")
```

But that's boring -- what if you want to change the name or the age? That's where **f-strings** come in. They let you plug variables right into text. Think of it like filling in blanks on a form.

Update your `variables.py` file to look like this:

```python
name = "Robert"
age = 11
print(f"{name} is {age} years old")
```

Save and run it:

```bash
python3 variables.py
```

It prints: `Robert is 11 years old`

Here's how it works:

- The `f` before the opening quote tells Python "hey, there are variables inside this text"
- The `{name}` part gets replaced with whatever is stored in the `name` variable
- The `{age}` part gets replaced with whatever is stored in `age`

Try changing `name` to your friend's name and `age` to their age. Save and run it again. See how the output changes?

---

## Asking the User a Question with `input()`

So far, your programs just talk AT the screen. But what if you want your program to ask the user a question and wait for an answer? That's what `input()` does.

Create a new file called **questions.py** (Cmd + N, then Cmd + S, save in your `coding-course` folder).

Type this:

```python
favorite_color = input("What's your favorite color? ")
print(f"Cool, {favorite_color} is a great color!")
```

Save and run it:

```bash
python3 questions.py
```

The program will print "What's your favorite color?" and then wait. It's waiting for YOU to type something. Type a color and hit Enter. Then it'll respond using whatever you typed.

Pretty cool, right? Your program is having a conversation with you.

### Turning Text into Numbers

Here's something tricky that catches everyone at first. When you use `input()`, Python always gives you **text**, even if the person types a number. If someone types `11`, Python sees the text `"11"`, not the number `11`.

Why does this matter? Because you can't do math with text. Try adding this to your `questions.py` file:

```python
age = input("How old are you? ")
age = int(age)
next_year = age + 1
print(f"Next year you'll be {next_year}!")
```

See that `int(age)` line? That converts the text into an actual number. `int` is short for "integer" (a whole number). After that conversion, you can do math with it -- like adding 1.

Save and run it. Type your age when it asks, and it'll tell you how old you'll be next year.

---

## Let's Build: Number Guessing Game

Alright, you've learned enough to build something fun. We're going to make a game where:

1. The computer picks a secret random number between 1 and 100
2. You try to guess it
3. The computer tells you if your guess is too high or too low
4. You keep guessing until you get it

This is going to be the biggest thing you've written so far, so we'll build it step by step. Create a new file called **guessing_game.py**.

### Step 1: Pick a Random Number

Python has a built-in tool called `random` that can pick numbers for you. You just need to tell Python you want to use it by writing `import random` at the top of your file. Think of it like grabbing a tool out of a toolbox.

Type this in your `guessing_game.py` file:

```python
import random

secret = random.randint(1, 100)
```

`random.randint(1, 100)` picks a random whole number from 1 to 100 and stores it in a variable called `secret`. Every time you run the program, it'll pick a different number.

### Step 2: Set Up the Game

Add this below what you already have:

```python
print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print("Can you guess it?")
print()

guesses = 0
```

The `print()` with nothing inside it just prints a blank line -- it adds a little space so things look nicer. And `guesses` is a variable that will count how many tries you take.

### Step 3: The Guessing Loop

Now here's the big part. We need the game to keep asking "What's your guess?" over and over until you get it right. To repeat something in Python, you use a **while loop**.

Think of it like this: you know how in a board game, you keep taking turns until someone wins? A `while` loop is like that -- it keeps running the code inside it until you tell it to stop.

Add this below your existing code:

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

There's a lot going on here, so let's break it down:

- `while True:` means "keep doing this forever." But don't worry, we have an escape plan.
- Everything that's **indented** (pushed to the right with spaces) is inside the loop. Python uses indentation to know what's inside what.
- `if answer < secret:` checks if your guess is too low
- `elif answer > secret:` checks if your guess is too high ("elif" is short for "else if")
- `else:` means "if it's not too low and not too high, it must be exactly right!"
- `break` is the escape plan -- it breaks out of the loop and the game ends

### The Full Game

Here's what your complete `guessing_game.py` file should look like:

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

### Run It!

Save the file (Cmd + S) and run it in the terminal:

```bash
python3 guessing_game.py
```

Play a few rounds! Here's a tip: always guess the middle of the range. If the number is between 1 and 100, guess 50. If it says "too high," guess 25 (the middle of 1-50). If it says "too low," guess 75 (the middle of 50-100). Keep cutting the range in half. This trick is actually called **binary search** and it's a real strategy programmers use.

---

## Experiments

Now it's time to play around. Try these changes to your guessing game (make a change, save, run it, and see what happens):

1. **Make it easier.** Change `random.randint(1, 100)` to `random.randint(1, 10)`. Way easier to guess, right?

2. **Show how far off you are.** After the "Too low!" or "Too high!" message, add this line: `print(f"You were off by {abs(secret - answer)}")`. The `abs()` part makes sure the number is never negative.

3. **Limit the guesses.** What if you only get 7 tries? After the line `guesses = guesses + 1`, add these two lines (with the right indentation):
    ```python
        if guesses >= 7:
            print(f"Game over! The number was {secret}.")
            break
    ```

4. **Make the hints sillier.** Instead of just "Too low!" try making it say "WAAAY too low!!!" if you're off by more than 30, and "Ooh, so close!" if you're within 5.

5. **Ask for their name.** Before the `while` loop, add `player = input("What's your name? ")` and use it in the win message.

---

## Challenge

Here's a harder one: add a **play again** feature. After the player wins (or loses), ask them "Play again? (y/n)". If they type "y", pick a new secret number and start over. If they type "n", print "Thanks for playing!" and end.

Hint: you'll need another `while True:` loop that wraps around the whole game. The outer loop handles "play again," and the inner loop handles guessing.

Don't worry if this one takes a while. It's supposed to be hard. Give it a real try before you ask for help.

---

## What's Next

In Lesson 2, we'll learn about loops and lists -- and build a quiz game that keeps score. See you there!
