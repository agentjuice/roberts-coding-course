# Hello World

!!! success "🎯 Mission"
    Write your very first Python program and make your computer say something.

Every game, app, and website you've ever used started with someone writing their first line of code — just like you're about to. Minecraft? Started as a simple Java program. Fortnite? Somebody had to write the very first line. This is where it all begins.

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

!!! info "🎮 Fun Fact"
    Every video game uses `print()` (or something like it) behind the scenes. When Minecraft shows "Respawn?" on screen, or when Fortnite shows your elimination count — that's the game printing text to the display.

## Print More Stuff

You can use `print()` as many times as you want:

```python
print("Hello, world!")
print("My name is Robert.")
print("I am learning Python!")
```

Each `print()` shows up on its own line.

## Comments

Sometimes you want to write a note **just for yourself** that Python completely ignores. Use a `#`:

```python
# This is a note to myself — Python skips this completely
print("But this line runs!")

print("Hi")  # You can put notes at the end of a line too
```

Comments are **only for you**. They're like sticky notes on your code. Python doesn't read them, doesn't care about them — they're just there so you can remind yourself what your code does when you come back to it later.

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

👉 [Next: Variables](../02-variables/lesson.md)