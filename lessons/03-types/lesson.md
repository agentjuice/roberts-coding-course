# Types

!!! success "🎯 Mission"
    Understand the four basic types of data in Python: strings, integers, floats, and booleans.

Games need to keep track of different *kinds* of information. Your player name is text, your health is a whole number, your exact position is a decimal, and whether you're alive is true/false. Python calls these different **types**, and understanding them is how you stop your code from doing weird things — like trying to subtract "hello" from 42.

## Every Value Has a Type

Python keeps track of what *kind* of data each value is. Create a file called `types.py`:

```python
print(type("hello"))    # <class 'str'>
print(type(42))         # <class 'int'>
print(type(3.14))       # <class 'float'>
print(type(True))       # <class 'bool'>
```

The `type()` function tells you what kind of thing you're looking at.

## Strings (str)

A **string** is text. Always in quotes — single or double, doesn't matter:

```python
greeting = "Hello!"
name = 'Robert'
```

You can stick strings together with `+`:

```python
first = "Shadow"
last = "Knight"
full = first + " " + last
print(full)    # Shadow Knight
```

## Integers (int)

An **integer** is a whole number — no decimal point:

```python
health = 100
score = 0
lives = 3
```

You can do math with them:

```python
print(10 + 3)     # 13
print(10 - 3)     # 7
print(10 * 3)     # 30
print(10 // 3)    # 3 (division, rounded down)
print(10 % 3)     # 1 (remainder — "modulo")
```

## Floats (float)

A **float** is a number with a decimal point:

```python
temperature = 98.6
pi = 3.14159
price = 4.99
```

## Booleans (bool)

A **boolean** is either `True` or `False`. That's it — only two options:

```python
is_alive = True
game_over = False
```

In Minecraft, the game is constantly tracking booleans: `is_raining = True`, `is_player_sneaking = False`, `has_elytra_equipped = True`. Every on/off state in a game is a boolean.

These become super important when we get to if-statements (Lesson 6).

## Watch Out: Strings vs Numbers

This trips everyone up:

```python
print(5 + 3)       # 8 — math!
print("5" + "3")   # "53" — glued two strings together!
```

`"5"` (with quotes) is text. `5` (no quotes) is a number. They're completely different.

## Build: Type Detective

Create `type_detective.py`:

```python
a = "100"
b = 100
c = 100.0
d = True

print(a, "is", type(a))
print(b, "is", type(b))
print(c, "is", type(c))
print(d, "is", type(d))

# Can you predict these?
print(type(a + "hello"))
print(type(b + 50))
print(type(b + c))
```

Run it and see if your predictions were right!

## What's Next?

👉 [Next: f-strings](../04-fstrings/lesson.md)