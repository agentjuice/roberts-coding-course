# Lesson 9: For Loops

!!! success "🎯 Mission"
    Learn `for` loops with `range()` and build patterns with nested loops.


## for i in range()

A `for` loop runs a specific number of times. Create `forloops.py`:

```python
for i in range(5):
    print(i)
```

Output: `0, 1, 2, 3, 4` (each on its own line). It starts at 0 and stops *before* 5.

## range() Variations

```python
# Start at 1, stop before 6
for i in range(1, 6):
    print(i)    # 1, 2, 3, 4, 5

# Count by 2s
for i in range(0, 10, 2):
    print(i)    # 0, 2, 4, 6, 8

# Count backwards
for i in range(5, 0, -1):
    print(i)    # 5, 4, 3, 2, 1
```

The three numbers are: **start**, **stop**, **step**.

## for with Strings

You can loop through the characters of a string:

```python
name = "Robert"
for letter in name:
    print(letter)
```

This prints each letter on its own line: R, o, b, e, r, t.

## Nested Loops

A loop inside a loop. The inner loop runs completely for each step of the outer loop:

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

The `end=""` tells `print` not to make a new line — so all the stars in one row stay on the same line. The `print()` at the end of each row makes a new line.

## Build: Star Patterns

Create `stars.py`:

```python
# Triangle
size = int(input("How big? "))

for row in range(1, size + 1):
    for col in range(row):
        print("*", end="")
    print()
```

If you enter `5`, you get:
```
*
**
***
****
*****
```

**Challenge:** Can you make it print upside-down? (Hint: start `row` at `size` and count down.)

## What's Next?

In Lesson 10, you'll learn about **lists** — how to store a whole collection of things in one variable.
