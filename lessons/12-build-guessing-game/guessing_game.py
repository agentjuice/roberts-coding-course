import random

secret = random.randint(1, 100)
guesses = 0
all_guesses = []

print("I'm thinking of a number between 1 and 100.")
print()

while True:
    answer = int(input("Your guess: "))
    guesses = guesses + 1
    all_guesses.append(answer)

    if answer == secret:
        print(f"You got it in {guesses} guesses!")
        break
    elif answer > secret:
        print("Too high!")
    else:
        print("Too low!")

    # Difficulty feedback
    diff = abs(answer - secret)
    if diff > 30:
        print("Way off!")
    elif diff > 10:
        print("Getting warmer...")
    else:
        print("So close!")

    print(f"Guesses so far: {all_guesses}")
    print()
