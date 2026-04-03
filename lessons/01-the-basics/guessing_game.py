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

    # How far off is the guess?
    difference = abs(secret - answer)

    if answer < secret:
        if difference > 30:
            print("Way too low!")
        elif difference > 10:
            print("Too low! Try higher.")
        else:
            print("A little too low. You're close!")
    elif answer > secret:
        if difference > 30:
            print("Way too high!")
        elif difference > 10:
            print("Too high! Try lower.")
        else:
            print("A little too high. You're close!")
    else:
        print(f"You got it! The number was {secret}.")
        print(f"It took you {guesses} guesses.")
        break
