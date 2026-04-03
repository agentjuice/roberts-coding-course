import random

print("🎲 Dice Roller 🎲")
print()

while True:
    input("Press Enter to roll... ")
    
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    total = die1 + die2
    
    print(f"  Die 1: {die1}")
    print(f"  Die 2: {die2}")
    print(f"  Total: {total}")
    
    if total == 12:
        print("  🎉 DOUBLE SIXES!")
    elif total == 2:
        print("  💀 Snake eyes!")
    
    print()
