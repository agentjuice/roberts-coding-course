# Variables

!!! success "🎯 Mission"
    Learn how to store information in variables so Python can remember things.

Every game you've ever played uses variables. In Minecraft, your health is a variable. Your hunger bar is a variable. The number of diamonds in your inventory? Variable. When a Creeper explodes near you and your health drops from 20 to 8 — that's a variable being updated.

## What's a Variable?

A variable is like a labeled box. You put something in it, give it a name, and use that name later to get the thing back.

Create a new file called `variables.py` and type this:

```python
name = "Robert"
print(name)
```

Run it with `python3 variables.py`. Python prints `Robert` — it remembered what you stored!

The `=` sign doesn't mean "equals" like in math. It means **"store this value."** So `name = "Robert"` means "put Robert into the box labeled name."

## Naming Rules

Variable names can use letters, numbers, and underscores. They **can't** start with a number and they **can't** have spaces:

```python
player_name = "Robert"    # Good — use underscores for spaces
player1 = "Alice"         # Good — numbers are fine (just not first)
my_score = 100            # Good
# 1st_place = "Bob"      # Bad — can't start with a number
```

Use names that describe what's inside. `score` is better than `x`. `player_name` is better than `n`.

## Storing Different Things

Variables can hold text (in quotes) or numbers (no quotes):

```python
player = "Robert"
health = 100
level = 3
```

## Updating Variables

You can change what's in a variable anytime:

```python
score = 0
print(score)    # 0

score = 10
print(score)    # 10

score = score + 5
print(score)    # 15
```

That last line looks weird, but read it right to left: "take what's in `score`, add 5, and store the result back in `score`."

This is exactly what happens in Fortnite when you pick up shield potions — the game runs something like `shield = shield + 50`.

## Build: Character Stats Card

Create `character.py`:

```python
# My RPG Character
name = "Shadow Knight"
health = 100
attack = 25
defense = 15
level = 1

print("=== CHARACTER STATS ===")
print(name)
print(health)
print(attack)
print(defense)
print(level)
print("=======================")
```

Try changing the values to make your own character!

## What's Next?

👉 [Next: Math](../03-math/lesson.md)