score = 0

answer = input("What planet is closest to the sun? ")
if answer == "Mercury" or answer == "mercury":
    print("Correct!")
    score = score + 1
else:
    print("Nope — it's Mercury!")

answer = int(input("What is 7 * 8? "))
if answer == 56:
    print("Correct!")
    score = score + 1
else:
    print("Nope — it's 56!")

answer = input("True or False: Python is named after a snake. ")
if answer == "False" or answer == "false":
    print("Correct! It's named after Monty Python.")
    score = score + 1
else:
    print("Nope — it's named after the comedy show Monty Python!")

print(f"\nYou got {score} out of 3!")

if score == 3:
    print("Perfect score!")
elif score >= 2:
    print("Nice job!")
else:
    print("Better luck next time!")
