import os
import numpy
import time

world = numpy.zeros((6, 6))
player = 1
winner = 0
chip_falling = False
chip_falling_ypos = 0

def draw_world():
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

def get_input():
    input_text = input()
    if not str.isnumeric(input_text):
        return -1
    i = int(input_text)
    if i == 0:
        exit()
    if i > 6:
        return -1
    if world[0][i - 1] > 0:
        return -1
    return i

def check_winner():
    global winner
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

def switch():
    global player
    if player == 1:
        player = 2
    else:
        player = 1

def animate_chip():
    if chip_falling_ypos > 0:
        world[chip_falling_ypos - 1][i - 1] = 0
    world[chip_falling_ypos][i - 1] = player

while True:
    draw_world()
    if not chip_falling:
        i = get_input()
        if i < 0:
            continue
        chip_falling = True
        chip_falling_ypos = 0
    else:
        animate_chip()
        if chip_falling_ypos == 5 or world[chip_falling_ypos + 1][i - 1] > 0:
            chip_falling = False
        else:
            chip_falling_ypos = chip_falling_ypos + 1
            time.sleep(0.05)
    if not chip_falling:
        check_winner()
        switch()
