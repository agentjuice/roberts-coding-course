# Lesson 4: Lists -- Storing Collections

**Goal:** Learn how to store and work with collections of data, and build a playlist manager.

---

## Your First List

Up until now, every variable you've made holds one thing. One number. One string. One answer. But what if you want to store a bunch of things together -- like a list of your favorite games, or all the scores from a quiz?

That's what **lists** are for. A list is like a row of boxes sitting next to each other, and each box can hold something.

```python
games = ["Minecraft", "Fortnite", "Zelda", "Mario Kart"]
print(games)
```

Save that in a file called `lists.py`, hit **Cmd + S**, open your terminal, and run it:

```bash
python3 lists.py
```

You'll see:

```
['Minecraft', 'Fortnite', 'Zelda', 'Mario Kart']
```

That's a list. Square brackets `[ ]` on the outside, items separated by commas. Done.

## Creating Lists

You can make lists with all kinds of stuff:

```python
# A list of strings
colors = ["red", "blue", "green", "yellow"]

# A list of numbers
scores = [98, 85, 72, 100, 91]

# An empty list (nothing in it yet)
empty = []

# You can even mix types (but you usually won't)
weird = ["hello", 42, True, 3.14]
```

Most of the time, your lists will have all the same type of thing in them -- all strings, or all numbers. But Python won't stop you from mixing.

## Accessing Items by Index

Every item in a list has a number called an **index**. Here's the thing that trips everyone up: **the first item is index 0, not 1.**

```python
fruits = ["apple", "banana", "cherry", "date"]
#          index 0   index 1   index 2   index 3

print(fruits[0])   # apple
print(fruits[1])   # banana
print(fruits[2])   # cherry
print(fruits[3])   # date
```

Why does it start at 0? It goes back to the early days of programming. The very first popular language, called C, stored lists as a spot in your computer's memory. The index was how far to jump from the start. The first item is zero jumps away -- it's already right there. The second item is one jump away. And so on. Every major language since then has kept the tradition, including Python.

It feels weird at first, but you'll get used to it fast. Just remember: **first item = index 0**.

### Negative Indexing

Here's a cool trick. You can use negative numbers to count from the **end** of the list:

```python
fruits = ["apple", "banana", "cherry", "date"]

print(fruits[-1])   # date (last item)
print(fruits[-2])   # cherry (second to last)
```

This is super handy when you want the last item but you don't know how long the list is.

## Changing Items

You can replace any item by assigning to its index:

```python
colors = ["red", "blue", "green"]
print(colors)

colors[0] = "purple"
print(colors)
```

```
['red', 'blue', 'green']
['purple', 'blue', 'green']
```

The first item changed from `"red"` to `"purple"`. The rest stayed the same.

## How Many Items? Use `len()`

The `len()` function tells you how many items are in a list:

```python
animals = ["cat", "dog", "hamster", "parrot"]
print(len(animals))   # 4
```

Notice that `len()` gives you 4, but the last index is 3. That's because indexes start at 0. The last index is always `len(list) - 1`. This will make more sense the more you use it.

## Adding Items with `append()`

`append()` sticks a new item onto the **end** of the list:

```python
snacks = ["chips", "popcorn"]
print(snacks)

snacks.append("cookies")
print(snacks)

snacks.append("pretzels")
print(snacks)
```

```
['chips', 'popcorn']
['chips', 'popcorn', 'cookies']
['chips', 'popcorn', 'cookies', 'pretzels']
```

You can even start with an empty list and build it up:

```python
my_list = []
my_list.append("first")
my_list.append("second")
my_list.append("third")
print(my_list)   # ['first', 'second', 'third']
```

This is actually how a lot of real programs work -- start empty, add things as the user does stuff.

## Removing Items with `pop()`

`pop()` removes the **last** item from the list and gives it back to you:

```python
tasks = ["homework", "dishes", "laundry", "gaming"]
print(tasks)

done = tasks.pop()
print(done)     # gaming
print(tasks)    # ['homework', 'dishes', 'laundry']
```

You can also pop a specific index:

```python
tasks = ["homework", "dishes", "laundry", "gaming"]
removed = tasks.pop(1)
print(removed)   # dishes
print(tasks)     # ['homework', 'laundry', 'gaming']
```

!!! warning "⚠️ Watch Out"
    If you try to pop from an empty list, Python will crash with an `IndexError`. Always make sure the list has items before you pop.

## Removing Items with `remove()`

`remove()` finds an item **by its value** and removes the first one it finds:

```python
pets = ["cat", "dog", "cat", "hamster"]
pets.remove("cat")
print(pets)   # ['dog', 'cat', 'hamster']
```

Notice it only removed the **first** `"cat"`, not both of them.

!!! warning "⚠️ Watch Out"
    If the value isn't in the list, `remove()` crashes with a `ValueError`. You should check if the item is in the list before removing it -- and we're about to learn exactly how to do that.

## The `in` Keyword

The `in` keyword checks whether something exists in a list. It gives back `True` or `False`:

```python
foods = ["pizza", "tacos", "sushi", "burgers"]

print("pizza" in foods)     # True
print("broccoli" in foods)  # False
```

This is really useful with `if` statements:

```python
foods = ["pizza", "tacos", "sushi", "burgers"]

search = input("What food are you looking for? ")

if search in foods:
    print("Yes! We have " + search)
else:
    print("Sorry, no " + search + " here.")
```

And now we can safely remove things:

```python
pets = ["cat", "dog", "hamster"]
to_remove = "fish"

if to_remove in pets:
    pets.remove(to_remove)
    print("Removed " + to_remove)
else:
    print(to_remove + " is not in the list!")
```

## Looping Through Lists with `for`

You've used `while` loops before. Now meet the `for` loop -- it's perfect for going through every item in a list:

```python
colors = ["red", "blue", "green", "yellow"]

for color in colors:
    print(color)
```

```
red
blue
green
yellow
```

The variable `color` takes on each value in the list, one at a time. You can name it whatever makes sense -- if your list is called `games`, you might write `for game in games:`.

You can do more than just print:

```python
names = ["Alice", "Bob", "Charlie"]

for name in names:
    print("Hello, " + name + "!")
```

```
Hello, Alice!
Hello, Bob!
Hello, Charlie!
```

### Looping with Numbers (enumerate)

Sometimes you need the index AND the value. Use `enumerate()`:

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(str(i) + ": " + fruit)
```

```
0: apple
1: banana
2: cherry
```

If you want to start counting from 1 instead of 0 (which looks nicer for humans), you can do:

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits, 1):
    print(str(i) + ": " + fruit)
```

```
1: apple
2: banana
3: cherry
```

## Working with Lists of Numbers

Lists of numbers are super useful. Let's say you have a list of test scores and want to find the highest one:

```python
scores = [85, 92, 78, 95, 88]

highest = scores[0]

for score in scores:
    if score > highest:
        highest = score

print("The highest score is: " + str(highest))
```

We start by assuming the first score is the highest. Then we check each score -- if it's higher, it becomes the new highest. By the end, we've found the biggest one.

You can do the same thing to find the lowest:

```python
scores = [85, 92, 78, 95, 88]

lowest = scores[0]

for score in scores:
    if score < lowest:
        lowest = score

print("The lowest score is: " + str(lowest))
```

And to add them all up:

```python
scores = [85, 92, 78, 95, 88]

total = 0

for score in scores:
    total = total + score

average = total / len(scores)
print("Average: " + str(average))
```

!!! tip "💡 Built-in Shortcuts"
    Python actually has built-in functions for these: `max(scores)`, `min(scores)`, and `sum(scores)`. They do exactly what our loops did, but in one line. It's great to know both ways -- understanding the loop version helps you think like a programmer, and the built-in versions save you time.

## Putting It All Together

Let's combine a bunch of what we learned in one little program:

```python
# Start with some items
inventory = ["sword", "shield", "potion"]

# Add a new item
inventory.append("bow")

# Check if we have something
if "potion" in inventory:
    print("You have a potion! Using it...")
    inventory.remove("potion")

# Show what's left
print("Your inventory:")
for i, item in enumerate(inventory, 1):
    print("  " + str(i) + ". " + item)

print("Total items: " + str(len(inventory)))
```

```
You have a potion! Using it...
Your inventory:
  1. sword
  2. shield
  3. bow
Total items: 3
```

See how all these pieces fit together? Lists, `in`, `remove()`, `for` loops, `len()` -- they're all tools that work together.

## Build Project: Playlist Manager

Time to build something real. We're going to make a program that lets you manage a playlist of songs -- add songs, remove songs, see your playlist, shuffle it, and quit. It uses everything we've learned about lists plus a `while True` loop for the menu.

Create a new file called `playlist.py` in VS Code. Here's the full thing:

```python
import random

playlist = []

print("=== Playlist Manager ===")
print()

while True:
    print("What do you want to do?")
    print("  1. Add a song")
    print("  2. Remove a song")
    print("  3. Show playlist")
    print("  4. Shuffle playlist")
    print("  5. Quit")
    print()

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        song = input("Enter the song name: ")
        playlist.append(song)
        print(song + " added!")

    elif choice == "2":
        if len(playlist) == 0:
            print("Your playlist is empty! Nothing to remove.")
        else:
            song = input("Enter the song to remove: ")
            if song in playlist:
                playlist.remove(song)
                print(song + " removed!")
            else:
                print("Couldn't find " + song + " in your playlist.")

    elif choice == "3":
        if len(playlist) == 0:
            print("Your playlist is empty.")
        else:
            print("Your playlist:")
            for i, song in enumerate(playlist, 1):
                print("  " + str(i) + ". " + song)

    elif choice == "4":
        if len(playlist) == 0:
            print("Your playlist is empty! Nothing to shuffle.")
        else:
            random.shuffle(playlist)
            print("Playlist shuffled!")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("That's not a valid choice. Pick 1-5.")

    print()
```

Let's break down the important parts:

- **`import random`** at the top gives us access to `random.shuffle()`, which rearranges a list in random order
- **`playlist = []`** starts with an empty list -- the user will add songs
- **`while True`** keeps the menu running forever until the user picks Quit
- **`break`** exits the `while True` loop when the user chooses to quit
- We check `len(playlist) == 0` before removing, showing, or shuffling -- you can't do those on an empty list
- **`enumerate(playlist, 1)`** gives us nice numbered output starting from 1

## Run It!

Save the file (**Cmd + S**), open your terminal, and run:

```bash
python3 playlist.py
```

Try adding a few songs, showing the playlist, shuffling it, and removing one. Try removing a song that doesn't exist. Try shuffling when the playlist is empty. See what happens!

!!! example "🧪 Experiments"
    - Add a "Play" option (choice 6) that picks a random song from the playlist and prints "Now playing: [song name]". Hint: use `random.choice(playlist)`.
    - Add the artist name along with the song. Instead of just `"Bohemian Rhapsody"`, let the user type `"Bohemian Rhapsody - Queen"`.
    - When the user quits, save the playlist to a file. When the program starts, load it back. (This is tricky -- you'll need to look up how to read and write files in Python!)

!!! abstract "🏆 Challenge"
    Add a **search** feature (choice 6 or 7) that asks the user for a search term and shows all songs that contain that term. For example, if your playlist has "Bohemian Rhapsody", "Rap God", and "Rapture", searching for "rap" should show "Bohemian Rhapsody" and "Rapture" (because `in` is case-sensitive... or is it? Try using `.lower()` to make it case-insensitive!).

## What's Next

In Lesson 5, we'll use everything we've learned to build Connect 4 -- a real game you can play in the terminal!
