import random

player_attack = 15
enemy_armor = 4

bonus = random.randint(0, 5)
damage = player_attack - enemy_armor + bonus

print(f"Attack power: {player_attack}")
print(f"Enemy armor: {enemy_armor}")
print(f"Random bonus: {bonus}")
print(f"Total damage: {damage}")

if random.random() < 0.2:
    damage = damage * 2
    print(f"CRITICAL HIT! Double damage: {damage}")
