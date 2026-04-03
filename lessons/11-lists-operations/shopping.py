shopping = []

while True:
    print(f"\nShopping list: {shopping}")
    print("1. Add item")
    print("2. Remove item")
    print("3. Quit")

    choice = input("Pick 1, 2, or 3: ")

    if choice == "1":
        item = input("What to add? ")
        shopping.append(item)
        print(f"Added {item}!")
    elif choice == "2":
        item = input("What to remove? ")
        if item in shopping:
            shopping.remove(item)
            print(f"Removed {item}!")
        else:
            print("That's not on the list!")
    elif choice == "3":
        print("Bye!")
        break
    else:
        print("Pick 1, 2, or 3!")
