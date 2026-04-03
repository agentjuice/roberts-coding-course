import os
import numpy

world = numpy.zeros((6, 6))
player = 1
winner = 0

while True:
    os.system('clear')
    print("  1  2  3  4  5  6")
    print("---------------------")
    print(world)

    if winner < 0:
        print("DRAW")
        exit()
    elif winner > 0:
        print("WINNER - PLAYER: %d" % winner)
        exit()

    input_text = input("Enter your move player %d: " % player)

    if not str.isnumeric(input_text):
        continue

    i = int(input_text)

    if i == 0:
        exit()

    if i > 6:
        continue

    if world[0][i - 1] > 0:
        continue

    # Find the lowest empty row
    for y in range(5, -1, -1):
        if world[y][i - 1] == 0:
            world[y][i - 1] = player
            break

    # Check for winner
    for y in range(6):
        for x in range(6):
            if world[y][x] != player:
                continue

            if x <= 2 and world[y][x + 1] == player and world[y][x + 2] == player and world[y][x + 3] == player:
                winner = player

            if y <= 2 and world[y + 1][x] == player and world[y + 2][x] == player and world[y + 3][x] == player:
                winner = player

            if x <= 2 and y <= 2 and world[y + 1][x + 1] == player and world[y + 2][x + 2] == player and world[y + 3][x + 3] == player:
                winner = player

            if x <= 2 and y > 2 and world[y - 1][x + 1] == player and world[y - 2][x + 2] == player and world[y - 3][x + 3] == player:
                winner = player

    if world[0][0] > 0 and world[0][1] > 0 and world[0][2] > 0 and world[0][3] > 0 and world[0][4] > 0 and world[0][5] > 0:
        winner = -1

    if player == 1:
        player = 2
    else:
        player = 1
