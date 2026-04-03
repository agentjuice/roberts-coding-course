import random

player_attack = 15
enemy_armor = 4
bonus = random.randint(0, 5)

damage = player_attack - enemy_armor + bonus

enemy_health = 50
enemy_health = enemy_health - damage

print("Attack power:", player_attack)
print("Enemy armor:", enemy_armor)
print("Random bonus: +" + str(bonus))
print("Damage dealt:", damage)
print("Enemy health remaining:", enemy_health)
