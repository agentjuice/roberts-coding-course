inventory = ["sword", "shield", "potion", "map", "torch"]

print("=== YOUR INVENTORY ===")
print(f"You have {len(inventory)} items:")
print()

for i in range(len(inventory)):
    print(f"  {i + 1}. {inventory[i]}")

print()
print(f"First item: {inventory[0]}")
print(f"Last item: {inventory[-1]}")
