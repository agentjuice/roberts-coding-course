# Lesson 2: Conditions -- Making Decisions

**Goal:** Learn how to make your programs choose what to do, and build a choose-your-own-adventure story.

---

## Your First `if` Statement

Up until now, every line of your code runs no matter what. Top to bottom, every single time. But real programs need to make **decisions**. Think about it -- when you check the weather, you decide whether to bring an umbrella. Your brain does an `if` check without you even thinking about it.

Let's teach Python to do the same thing. Open VS Code, create a new file called **weather.py** in your `coding-course` folder, and type this:

```python
raining = True

if raining:
    print("Bring an umbrella!")
```

Save it with **Cmd + S**, open your terminal, and run it:

```bash
cd ~/Desktop/coding-course
python3 weather.py
```

You should see:

```
Bring an umbrella!
```

Now change `True` to `False` and run it again. Nothing prints! The code inside the `if` only runs when the condition is `True`.

### Indentation Matters

See how `print("Bring an umbrella!")` is pushed to the right with **4 spaces**? That's called **indentation**, and in Python it's not optional -- it's how Python knows which code belongs inside the `if`. If you forget the spaces, Python will yell at you with an error.

!!! warning
    Python is very picky about indentation. Always use **4 spaces** (not a tab, not 2 spaces -- 4 spaces). VS Code usually handles this for you when you press Tab, but double-check if you get weird errors.

---

## `if` / `else` -- Two Paths

What if you want something to happen when the condition is `False` too? That's where `else` comes in. Create a new file called **even_odd.py**:

```python
number = int(input("Pick a number: "))

if number % 2 == 0:
    print("That's an even number!")
else:
    print("That's an odd number!")
```

Run it:

```bash
python3 even_odd.py
```

The `%` symbol is called **modulo** -- it gives you the remainder after division. So `number % 2` divides by 2 and checks the remainder. If the remainder is 0, the number is even. Otherwise, it's odd.

Try it with a few numbers: 7, 10, 0, -3. See how it always picks one path or the other? With `if`/`else`, your code is guaranteed to do *something* -- it can never just skip everything.

---

## `elif` -- More Than Two Paths

Sometimes two paths aren't enough. What if you want 5 paths? You could nest a bunch of `if`/`else` blocks, but that gets ugly fast. Instead, use `elif` (short for "else if"). Create a file called **grades.py**:

```python
score = int(input("Enter your test score (0-100): "))

if score >= 90:
    print("A -- Amazing!")
elif score >= 80:
    print("B -- Nice work!")
elif score >= 70:
    print("C -- Not bad!")
elif score >= 60:
    print("D -- You passed... barely.")
else:
    print("F -- Time to study more!")
```

Run it:

```bash
python3 grades.py
```

Try entering 95, 85, 72, 61, and 45. Notice how Python checks each condition **from top to bottom** and stops at the first one that's `True`. That's important! If you entered 95, it matches `score >= 90` and never even looks at the rest.

!!! tip
    The order of your `elif` conditions matters. Put the most specific (or highest) conditions first, and work your way down. If you put `score >= 60` at the top, *every* passing score would match it and you'd never see A, B, or C.

---

## Comparison Operators

You've already seen `>=` and `==`, but here's the full list of ways to compare things in Python:

| Operator | Meaning                  | Example         | Result  |
|----------|--------------------------|-----------------|---------|
| `==`     | Equal to                 | `5 == 5`        | `True`  |
| `!=`     | Not equal to             | `5 != 3`        | `True`  |
| `<`      | Less than                | `3 < 10`        | `True`  |
| `>`      | Greater than             | `10 > 3`        | `True`  |
| `<=`     | Less than or equal to    | `5 <= 5`        | `True`  |
| `>=`     | Greater than or equal to | `7 >= 10`       | `False` |

You can try these out in the terminal interactively. Type `python3` by itself to open the Python shell, then type comparisons:

```python
>>> 10 > 3
True
>>> "hello" == "hello"
True
>>> 5 != 5
False
>>> 100 <= 99
False
```

Type `exit()` to leave the Python shell when you're done experimenting.

!!! warning
    The most common mistake beginners make is using `=` when they mean `==`. One equals sign (`=`) **assigns** a value to a variable. Two equals signs (`==`) **compares** two values. If you write `if score = 90:` Python will give you an error. You want `if score == 90:`.

---

## Boolean Values

Those `True` and `False` results you've been seeing? They're called **booleans** (named after a mathematician called George Boole). They're a type in Python, just like strings and integers.

You can store comparisons in variables:

```python
age = 11
is_teenager = age >= 13
print(is_teenager)
```

This prints `False` because 11 is not greater than or equal to 13. The variable `is_teenager` holds a boolean value.

You can also use booleans directly:

```python
game_over = False

if game_over:
    print("Thanks for playing!")
else:
    print("Keep going!")
```

This is really useful in games -- you'll see `game_over` flags like this all the time.

---

## Boolean Logic -- `and`, `or`, `not`

Sometimes one condition isn't enough. What if you need to check two things at once?

### `and` -- Both Must Be True

```python
height = 140
age = 11

if height >= 130 and age >= 10:
    print("You can ride the rollercoaster!")
else:
    print("Sorry, not this time.")
```

With `and`, **both** conditions must be `True` for the whole thing to be `True`.

| A     | B     | A `and` B |
|-------|-------|-----------|
| True  | True  | **True**  |
| True  | False | False     |
| False | True  | False     |
| False | False | False     |

### `or` -- At Least One Must Be True

```python
day = input("What day is it? ")

if day == "Saturday" or day == "Sunday":
    print("It's the weekend! No school!")
else:
    print("It's a school day.")
```

With `or`, only **one** of the conditions needs to be `True`.

| A     | B     | A `or` B  |
|-------|-------|-----------|
| True  | True  | **True**  |
| True  | False | **True**  |
| False | True  | **True**  |
| False | False | False     |

### `not` -- Flip It

```python
raining = False

if not raining:
    print("Leave the umbrella at home!")
```

`not` simply flips `True` to `False` and `False` to `True`. That's it.

---

## Nested `if` Statements

You can put `if` statements *inside* other `if` statements. This is called **nesting**. Create a file called **school_day.py**:

```python
import datetime

today = datetime.datetime.now()
day = today.strftime("%A")
hour = today.hour

if day == "Saturday" or day == "Sunday":
    print("It's the weekend! Relax!")
else:
    print(f"It's {day} -- a school day.")
    if hour < 12:
        print("Good morning! Time for class.")
    elif hour < 15:
        print("It's the afternoon. Almost done!")
    else:
        print("School's out! Free time!")
```

Run it:

```bash
python3 school_day.py
```

See how the second `if`/`elif`/`else` is indented inside the first `else`? That means it only runs if it's a school day. Python uses indentation to know what's inside what.

!!! tip
    Don't go too crazy with nesting. If you're more than 3 levels deep, your code is getting hard to read. There are usually cleaner ways to write it (like using `and`/`or` to combine conditions).

---

## More Practice

Let's do a few more quick examples to lock this in.

### Temperature Advice

Create **temperature.py**:

```python
temp = int(input("What's the temperature in Fahrenheit? "))

if temp >= 90:
    print("It's scorching! Stay inside and drink water.")
elif temp >= 75:
    print("Nice and warm. Great day to go outside!")
elif temp >= 55:
    print("A bit cool. Grab a light jacket.")
elif temp >= 32:
    print("It's cold! Bundle up.")
else:
    print("It's freezing! Stay inside if you can.")
```

### Can You Vote?

Create **voting.py**:

```python
age = int(input("How old are you? "))

if age >= 18:
    print("You can vote!")
else:
    years_left = 18 - age
    print(f"Not yet! You have to wait {years_left} more year(s).")
```

### Simple Calculator

Create **calculator.py**:

```python
num1 = float(input("First number: "))
operator = input("Operator (+, -, *, /): ")
num2 = float(input("Second number: "))

if operator == "+":
    result = num1 + num2
elif operator == "-":
    result = num1 - num2
elif operator == "*":
    result = num1 * num2
elif operator == "/":
    if num2 == 0:
        print("You can't divide by zero!")
        result = None
    else:
        result = num1 / num2
else:
    print("I don't know that operator!")
    result = None

if result is not None:
    print(f"{num1} {operator} {num2} = {result}")
```

Notice how the calculator uses nested `if` inside the division case to check for dividing by zero. That would crash your program without the check!

---

## Build Project: Choose-Your-Own-Adventure Story

Time to put it all together. You're going to build an interactive story where the player makes choices and each choice leads somewhere different. This is basically how text adventure games work -- and they're all built on `if` statements.

Create a new file called **adventure.py** and type this:

```python
print("=" * 50)
print("   THE CAVE OF SHADOWS")
print("=" * 50)
print()
print("You stand at the entrance of a dark cave.")
print("A cold wind blows from inside, carrying")
print("the faint sound of dripping water.")
print("Torchlight flickers on the stone walls.")
print()

choice1 = input("Do you (enter) the cave or (leave)? ")

if choice1 == "enter":
    print()
    print("You step inside. The air gets colder.")
    print("After a few steps, the tunnel splits in two.")
    print("The LEFT path glows faintly blue.")
    print("The RIGHT path smells like smoke.")
    print()

    choice2 = input("Go (left) or (right)? ")

    if choice2 == "left":
        print()
        print("You follow the blue glow and find an")
        print("underground lake. The water shimmers")
        print("with a strange light.")
        print("There's a small boat by the shore,")
        print("and something glittering at the bottom")
        print("of the lake.")
        print()

        choice3 = input("Take the (boat) or (dive) into the water? ")

        if choice3 == "boat":
            print()
            print("You row the boat to the center of the lake.")
            print("A treasure chest rises from the water!")
            print("Inside: a golden crown and ancient coins.")
            print()
            print("*** You found the treasure! You win! ***")
        elif choice3 == "dive":
            print()
            print("You dive into the glowing water.")
            print("It's warm! You swim deeper and find")
            print("an underwater tunnel that leads to")
            print("a hidden garden full of crystals.")
            print()
            print("*** You discovered the Crystal Garden! ***")
        else:
            print()
            print("You stand there, unsure. The glow fades.")
            print("You wander back out of the cave, empty-handed.")

    elif choice2 == "right":
        print()
        print("You follow the smoky path and find a")
        print("sleeping dragon curled around a pile of gold!")
        print("Its scales shimmer red and orange.")
        print()

        choice3 = input("Try to (sneak) past or (wake) the dragon? ")

        if choice3 == "sneak":
            print()
            print("You tiptoe past the dragon...")
            print("...and grab a handful of gold coins!")
            print("You make it out without waking it.")
            print()
            print("*** You escaped with dragon gold! ***")
        elif choice3 == "wake":
            print()
            print("The dragon opens one enormous eye.")
            print("'A visitor? How bold.'")
            print("It turns out this dragon loves riddles.")
            print("You spend the evening trading jokes")
            print("and it gives you a magic scale as a gift.")
            print()
            print("*** You befriended the dragon! ***")
        else:
            print()
            print("You freeze in fear. The dragon snores.")
            print("Eventually you back away slowly and leave.")

    else:
        print()
        print("You bump into a wall in the dark.")
        print("Ouch. You stumble back outside.")

elif choice1 == "leave":
    print()
    print("You decide the cave is too scary.")
    print("You walk back to town and buy a sandwich.")
    print("It's a really good sandwich, honestly.")
    print()
    print("*** The End (Sandwich Ending) ***")

else:
    print()
    print("You stand there, confused by your own choices.")
    print("A bat flies out of the cave and startles you.")
    print("You run away screaming.")
```

This is a big one! Take your time typing it. Pay close attention to the indentation -- each level of `if` goes 4 more spaces to the right.

---

## Run It!

Save your file (**Cmd + S**) and run it in the terminal:

```bash
python3 adventure.py
```

Play through it a few times and try every path. There are **at least 7 different endings** hidden in there. Can you find them all?

!!! example "🧪 Experiments"
    - Add a **fourth decision point** inside one of the paths -- maybe the dragon asks you a riddle and you have to pick the right answer
    - Add a **secret ending** -- if the player types a secret word at any prompt, something unexpected happens
    - Add a **health variable** at the top (`health = 100`) and make some choices reduce it -- if health hits 0, the game ends early
    - Add `print()` calls with more atmospheric descriptions -- sounds, smells, what things look like

!!! abstract "🏆 Challenge"
    Add an **inventory system** to your adventure. Start with an empty list: `inventory = []`. Let the player pick up items along the way (like a key, a torch, or a magic gem). Then later in the story, check if they have the right item to unlock a special path. For example: `if "key" in inventory:` could open a locked door that leads to a bonus ending.

---

## What's Next

You now know how to make your programs **think** and **choose**. That's a huge deal -- almost every interesting program in the world uses conditions. Games, apps, websites -- they're all making decisions constantly.

In **Lesson 3**, we'll learn about **loops** -- making code repeat itself -- and build a number guessing game. Instead of your program running once and stopping, it'll keep going until something happens. Combined with conditions, that's where things start to get really powerful.
