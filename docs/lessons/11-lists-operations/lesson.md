# Lesson 11: Lists -- Operations

!!! success "🎯 Mission"
    Learn how to add, remove, and search for items in lists.


## Adding Items with append()

`append()` sticks a new item on the end of the list. Create `list_ops.py`:

```python
backpack = ["sword", "shield"]
print(backpack)

backpack.append("potion")
print(backpack)    # ['sword', 'shield', 'potion']
```

## Removing Items

There are two ways to remove things:

**`pop()`** removes by position and gives you the item back:

```python
items = ["apple", "banana", "cherry"]
removed = items.pop(1)
print(removed)    # banana
print(items)      # ['apple', 'cherry']

# With no number, pop() removes the last item
last = items.pop()
print(last)       # cherry
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

## Looping and Building

A common pattern — start empty and build up a list:

```python
favorites = []

while True:
    food = input("Enter a favorite food (or 'done'): ")
    if food == "done":
        break
    favorites.append(food)

print(f"\nYour favorites: {favorites}")
print(f"You listed {len(favorites)} foods!")
```

## Build: Shopping List

Create `shopping.py`:

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

In Lesson 12, you'll combine **everything** you've learned into a real project — a number guessing game!
