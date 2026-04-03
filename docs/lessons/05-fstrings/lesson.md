# f-strings

!!! success "🎯 Mission"
    Learn how to mix variables into text with f-strings so your output looks clean.

Think about any game's HUD (heads-up display). In Minecraft, it shows "Health: 20" and in Mario Kart it shows "Lap 2/3". That text mixes words with changing numbers — and f-strings are exactly how programmers do that.

## The Problem

In Lesson 2, our character card just printed raw values with no labels. We *could* glue strings together with `+`, but it gets ugly fast:

```python
name = "Robert"
score = 42
print("Player: " + name + " | Score: " + str(score))
```

You have to convert numbers to strings with `str()`, and all those `+` signs and quotes are confusing. There's a better way.

## f-Strings to the Rescue

Put an `f` before the opening quote, then use `{}` to drop variables right into the text. Create `fstrings.py`:

```python
name = "Robert"
score = 42
print(f"Player: {name} | Score: {score}")
```

Output: `Player: Robert | Score: 42`

That's it. The `f` stands for "format." Python sees the curly braces and swaps in the variable values.

## You Can Do Math Inside the Braces

```python
price = 4.99
quantity = 3
print(f"Total: ${price * quantity}")
```

Output: `Total: $14.97`

Anything inside `{}` gets evaluated as Python code first, then turned into text.

!!! info "🎮 Fun Fact"
    F1 racing games display things like "LAP 23/57 — Gap: 1.234s" on screen. Behind the scenes, that's built with something very similar to f-strings: `f"LAP {current_lap}/{total_laps} — Gap: {gap}s"`.

## Build: Better Character Card

Create `character_card.py`:

```python
name = "Shadow Knight"
health = 100
attack = 25
defense = 15
level = 1

print(f"╔══════════════════════╗")
print(f"║  {name:^18}  ║")
print(f"╠══════════════════════╣")
print(f"║  Health:  {health:>10}  ║")
print(f"║  Attack:  {attack:>10}  ║")
print(f"║  Defense: {defense:>10}  ║")
print(f"║  Level:   {level:>10}  ║")
print(f"╚══════════════════════╝")
```

The `>10` means "right-align in a space 10 characters wide." The `^18` means "center in 18 characters." These are optional formatting tricks — the basic `{variable}` is all you really need.

Run it with `python3 character_card.py` and admire your fancy output!

## What's Next?

👉 [Next: Input](../06-input/lesson.md)