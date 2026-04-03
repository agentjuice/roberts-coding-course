import random

playlist = []

print("=== Playlist Manager ===")
print()

while True:
    print("What do you want to do?")
    print("  1. Add a song")
    print("  2. Remove a song")
    print("  3. Show playlist")
    print("  4. Shuffle playlist")
    print("  5. Quit")
    print()

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        song = input("Enter the song name: ")
        playlist.append(song)
        print(song + " added!")

    elif choice == "2":
        if len(playlist) == 0:
            print("Your playlist is empty! Nothing to remove.")
        else:
            song = input("Enter the song to remove: ")
            if song in playlist:
                playlist.remove(song)
                print(song + " removed!")
            else:
                print("Couldn't find " + song + " in your playlist.")

    elif choice == "3":
        if len(playlist) == 0:
            print("Your playlist is empty.")
        else:
            print("Your playlist:")
            for i, song in enumerate(playlist, 1):
                print("  " + str(i) + ". " + song)

    elif choice == "4":
        if len(playlist) == 0:
            print("Your playlist is empty! Nothing to shuffle.")
        else:
            random.shuffle(playlist)
            print("Playlist shuffled!")

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("That's not a valid choice. Pick 1-5.")

    print()
