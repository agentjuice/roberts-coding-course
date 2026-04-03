import time

number = int(input("Count down from what number? "))

while number > 0:
    print(number)
    time.sleep(1)
    number = number - 1

print("BLASTOFF!")
