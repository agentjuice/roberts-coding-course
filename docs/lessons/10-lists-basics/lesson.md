# Lists: Basics

!!! success "🎯 Mission"
    Learn how to store a collection of items in a list — creating, reading, changing, and measuring.

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

Why start at 0? It's a computer science tradition — you'll get used to it!

!!! info "🎮 Fun Fact"
    Your Minecraft hotbar slots are actually numbered 0-8 internally, even though the game shows them as 1-9 on screen. Programmers start counting at zero everywhere!

## Negative Indexing

You can count from the end with negative numbers:

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[-1])    # cherry (last item)
print(fruits[-2])    # banana (second to last)
```

## Changing Items

Just assign to an index:

```python
fruits = ["apple", "banana", "cherry"]
fruits[1] = "mango"
print(fruits)    # ['apple', 'mango', 'cherry']
```

## How Long Is It?

`len()` tells you how many items are in a list:

```python
fruits = ["apple", "banana", "cherry"]
print(len(fruits))    # 3
```

## Different Types of Lists

Lists can hold numbers, strings, booleans — even a mix:

```python
scores = [95, 87, 100, 72]
names = ["Alice", "Bob", "Charlie"]
mixed = ["hello", 42, True, 3.14]
empty = []
```

## Looping Through a List

You can use a `for` loop to go through every item:

```python
colors = ["red", "green", "blue"]
for color in colors:
    print(f"I like {color}!")
```

## Build: Inventory Viewer

Create `inventory.py`:

```python
inventory = ["sword", "shield", "potion", "map", "torch"]

print("=== YOUR INVENTORY ===")
print(f"You have {len(inventory)} items:")
print()

for i in range(len(inventory)):
    print(f"  {i + 1}. {inventory[i]}")

print()
print(f"First item: {inventory[0]}")
print(f"Last item: {inventory[-1]}")
```

## What's Next?

👉 [Next: Lists: Operations](../11-lists-operations/lesson.md)