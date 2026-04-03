# Lesson 1: Hello, World!

!!! success "🎯 Mission"
    Write your very first Python program and make your computer say something.


## Setting Up

First, open **VS Code**. If you don't have it yet, download it from [code.visualstudio.com](https://code.visualstudio.com).

1. Open VS Code
2. Click **File → Open Folder** and pick a folder for your coding projects (like a folder called `python-projects` on your Desktop)
3. In the left sidebar, click the **New File** icon and name it `hello.py` — the `.py` ending tells your computer it's a Python file
4. Now open the **Terminal** by clicking **Terminal → New Terminal** at the top menu (or press **Ctrl + `**)

You should see a dark panel at the bottom of VS Code. That's your terminal — it's where you'll run your code.

## Your First Program

Type this in `hello.py`:

```python
print("Hello, world!")
```

Now run it! In your terminal, type:

```bash
python3 hello.py
```

You should see:

```
Hello, world!
```

That's it. You just wrote a program. `print()` tells Python to display whatever you put inside the parentheses.

## Print More Stuff

You can use `print()` as many times as you want:

```python
print("Hello, world!")
print("My name is Robert.")
print("I am learning Python!")
```

Each `print()` shows up on its own line.

## Comments

Sometimes you want to write a note to yourself that Python ignores. Use a `#`:

```python
# This is a comment — Python skips it
print("But this line runs!")

print("Hi")  # You can also put comments at the end of a line
```

Comments are great for reminding yourself what your code does.

## Build: ASCII Art

Make a new file called `ascii_art.py`. Use `print()` to draw something cool:

```python
# My awesome ASCII art
print("  /\\_/\\  ")
print(" ( o.o ) ")
print("  > ^ <  ")
print(" /|   |\\")
print("(_|   |_)")
```

Run it with `python3 ascii_art.py`. Try making your own design — a rocket, a house, your name in big letters, whatever you want!

## What's Next?

In Lesson 2, you'll learn about **variables** — how to make Python remember things.
