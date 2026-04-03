# Lists

!!! success "🎯 Mission"
    Learn how to store collections of items in a list — creating, reading, changing, adding, removing, and searching.

In Minecraft, your hotbar is a list of 9 items. Your inventory is a bigger list. The list of players on a Fortnite server? That's a list too. Whenever a game needs to keep track of *multiple things* in order, it uses a list.

## What's a List?

A variable holds one thing. A **list** holds a bunch of things in order. Create `lists.py`:

```python
fruits = ["apple", "banana", "cherry"]
print(fruits)
```

Square brackets `[]` make a list. Commas separate the items.

## Accessing Items by Index

Each item has a position number called an **index**, starting at 0:

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])    # apple
print(fruits[1])    # banana
print(fruits[2])    # cherry
```

!!! info "🎮 Fun Fact"
    Your Minecraft hotbar slots are actually numbered 0-8 internally, even though the game shows them as 1-9 on screen. Programmers start counting at zero everywhere!

You can count from the end with negative numbers:

```python
print(fruits[-1])    # cherry (last item)
print(fruits[-2])    # banana (second to last)
```

## Changing Items

Just assign to an index:

```python
fruits[1] = "mango"
print(fruits)    # ['apple', 'mango', 'cherry']
```

## How Long Is It?

`len()` tells you how many items are in a list:

```python
print(len(fruits))    # 3
```

## Adding Items with append()

`append()` sticks a new item on the end. Think about picking up items in Zelda — every time you grab a Hylian Shroom, the game *appends* it to your inventory.

```python
backpack = ["sword", "shield"]
backpack.append("potion")
print(backpack)    # ['sword', 'shield', 'potion']
```

## Removing Items

**`pop()`** removes by position and gives you the item back:

```python
items = ["apple", "banana", "cherry"]
removed = items.pop(1)
print(removed)    # banana
print(items)      # ['apple', 'cherry']
```

**`remove()`** removes by value — it finds the item and deletes it:

```python
pets = ["cat", "dog", "fish", "dog"]
pets.remove("dog")
print(pets)    # ['cat', 'fish', 'dog'] — only removes the first one!
```

## Checking If Something Is in a List

The `in` keyword checks if an item exists:

```python
fruits = ["apple", "banana", "cherry"]

if "banana" in fruits:
    print("We have bananas!")

if "mango" not in fruits:
    print("No mangos :(")
```

## Looping Through a List

Use a `for` loop to go through every item:

```python
colors = ["red", "green", "blue"]
for color in colors:
    print(f"I like {color}!")
```

## Build: Shopping List

Create `shopping.py` — a mini app that lets you add and remove items:

```python
shopping = []

while True:
    print(f"\nShopping list: {shopping}")
    print("1. Add item")
    print("2. Remove item")
    print("3. Quit")

    choice = input("Pick 1, 2, or 3: ")

    if choice == "1":
        item = input("What to add? ")
        shopping.append(item)
        print(f"Added {item}!")
    elif choice == "2":
        item = input("What to remove? ")
        if item in shopping:
            shopping.remove(item)
            print(f"Removed {item}!")
        else:
            print("That's not on the list!")
    elif choice == "3":
        print("Bye!")
        break
    else:
        print("Pick 1, 2, or 3!")
```

## What's Next?

👉 [Next: Build: Guessing Game](../11-build-guessing-game/lesson.md)