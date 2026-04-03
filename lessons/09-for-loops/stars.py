# Triangle pattern
size = int(input("How big? "))

for row in range(1, size + 1):
    for col in range(row):
        print("*", end="")
    print()

# Upside-down triangle
print()
for row in range(size, 0, -1):
    for col in range(row):
        print("*", end="")
    print()
