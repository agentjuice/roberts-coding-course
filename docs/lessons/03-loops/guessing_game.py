import random

secret = random.randint(1, 100)

print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")
print("Can you guess it?")
print()

guesses = 0

while True:
    answer = input("Your guess: ")
    answer = int(answer)
    guesses = guesses + 1

    if answer < secret:
        print("Too low! Try higher.")
    elif answer > secret:
        print("Too high! Try lower.")
    else:
        print(f"You got it! The number was {secret}.")
        print(f"It took you {guesses} guesses.")
        break
