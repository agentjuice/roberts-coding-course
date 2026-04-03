name = input("What's your name? ")
age = int(input("How old are you? "))

print(f"\nHello, {name}!")

if age >= 16:
    print("You can drive!")
elif age >= 13:
    print("You can watch PG-13 movies!")
elif age >= 10:
    print("You're in double digits!")
else:
    print("You're still young — enjoy it!")

print(f"\nYou'll be {age + 1} next year!")
