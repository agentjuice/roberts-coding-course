# Input

!!! success "🎯 Mission"
    Make your programs interactive by asking the user to type stuff in.

Without input, a program just does the same thing every time — boring! Input is what makes programs *interactive*. When Minecraft asks you to name an enchanted sword, or when you type your username to log in to Fortnite — that's input. Your program is about to start listening.

## Getting Text from the User

The `input()` function pauses your program and waits for the user to type something. Create `asking.py`:

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

Run it with `python3 asking.py`. It waits for you to type, then uses what you typed.

Here's the flow:

1. **Ask** — `input("question")` shows the question and waits
2. **Store** — the answer goes into a variable
3. **Use** — you do something with it

## Numbers Need Converting

Here's a gotcha: `input()` **always** gives you a string, even if the user types a number:

```python
age = input("How old are you? ")
print(type(age))    # <class 'str'> — it's text, not a number!
```

If you want to do math with it, wrap it in `int()`:

```python
age = int(input("How old are you? "))
next_year = age + 1
print(f"Next year you'll be {next_year}!")
```

`int()` converts the text `"11"` into the number `11`. Without it, `age + 1` would crash because Python can't add a string and a number.

## Build: Mad Libs

Create `mad_libs.py`:

```python
print("=== MAD LIBS ===")
print()

animal = input("Give me an animal: ")
food = input("Give me a food: ")
number = input("Give me a number: ")
verb = input("Give me a verb (like 'run' or 'dance'): ")
place = input("Give me a place: ")

print()
print("=== YOUR STORY ===")
print(f"One day, a {animal} walked into {place}.")
print(f"It ordered {number} plates of {food}.")
print(f'The waiter said "That\'s a lot of {food}!"')
print(f"So the {animal} started to {verb} on the table.")
print("The end.")
```

Try it with the silliest words you can think of!

## What's Next?

👉 [Next: If / Else](../07-if-else/lesson.md)