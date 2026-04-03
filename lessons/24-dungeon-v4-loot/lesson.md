# Lesson 24: Dungeon v4 — Loot & Items

!!! success "🎯 Mission"
    Add an item and inventory system so defeated enemies drop loot, and you can collect and use items.


![Loot drops and an inventory bar!](/images/dungeon_v4.png)


## How Loot Works in Games

You know how in Minecraft Dungeons, when you beat a mob it might drop an item? Maybe a sword, maybe a potion, maybe nothing at all. You pick it up, it goes in your inventory, and you use it when you need it.

We're going to build exactly that system. Here's the plan:

1. When an enemy dies, there's a 40% chance it drops a random item
2. Items sit on the ground as little colored squares
3. Walk over an item to pick it up (goes into your inventory)
4. Press 1-5 to use an item from your inventory
5. Treasure chests on the map give you loot too

## The Item Class

Items are pretty simple. They just need a position, a type, and a color:

```python
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        if item_type == "health_potion":
            self.color = (255, 50, 50)       # Red
        elif item_type == "speed_boost":
            self.color = (0, 255, 255)        # Cyan
        elif item_type == "power_sword":
            self.color = (255, 165, 0)        # Orange
```

Items get drawn as small squares — half the tile size — so they look like little pickups sitting on the floor:

```python
def draw(self, screen, cam_x, cam_y):
    sx = self.x * TILE_SIZE - cam_x + TILE_SIZE // 4
    sy = self.y * TILE_SIZE - cam_y + TILE_SIZE // 4
    pygame.draw.rect(screen, self.color, (sx, sy, TILE_SIZE // 2, TILE_SIZE // 2))
```

## Enemy Drops

When an enemy dies, we roll the dice. `random.random()` gives a number between 0 and 1. If it's less than 0.4, that's a 40% chance — the enemy drops something:

```python
if random.random() < 0.4:
    item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
    self.items.append(Item(enemy.x, enemy.y, item_type))
```

Think of it like a loot table. Every time an enemy goes down, the game basically flips a coin (well, a weighted coin) to decide if you get anything.

## Picking Up Items

When the player walks onto a tile that has an item, we add it to the inventory (if there's room):

```python
for item in self.items[:]:
    if item.x == self.player.x and item.y == self.player.y:
        if len(self.player.inventory) < 5:
            self.player.inventory.append(item.item_type)
            self.items.remove(item)
```

The `[:]` makes a copy of the list so we can safely remove items while looping. That's a handy Python trick you'll use a lot — if you try to remove things from a list while you're looping over it without making a copy first, weird things happen.

## Using Items

Press number keys 1 through 5 to use items from your inventory:

```python
if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
    slot = event.key - pygame.K_1  # Converts to 0-4
    if slot < len(self.player.inventory):
        item_type = self.player.inventory.pop(slot)
        if item_type == "health_potion":
            self.player.health = min(self.player.health + 5, self.player.max_health)
        elif item_type == "speed_boost":
            self.player.speed_boost_timer = 150  # ~5 seconds at 30fps
        elif item_type == "power_sword":
            self.player.damage_boost_timer = 150
```

The **speed boost** makes the player move every frame instead of having a movement delay. The **power sword** doubles your damage. Both last about 5 seconds. That `event.key - pygame.K_1` line is a neat trick — it converts the key code into a 0-4 index so we know which inventory slot was pressed.

## Treasure Chests

We add a new tile type: `3` means chest. On the map it looks like a brown/yellow square. When you walk into it, it opens (turns into floor) and spawns a random item:

```python
if self.tile_map[new_y][new_x] == 3:
    self.tile_map[new_y][new_x] = 0  # Open the chest (becomes floor)
    item_type = random.choice(["health_potion", "speed_boost", "power_sword"])
    self.items.append(Item(new_x, new_y, item_type))
```

## Drawing the Inventory

At the bottom of the screen, we show colored squares for each item in the inventory, with number labels:

```python
for i, item_type in enumerate(self.player.inventory):
    color = {"health_potion": (255, 50, 50), "speed_boost": (0, 255, 255),
             "power_sword": (255, 165, 0)}[item_type]
    x = 10 + i * 50
    y = 560
    pygame.draw.rect(screen, color, (x, y, 32, 32))
    label = self.font.render(str(i + 1), True, (255, 255, 255))
    screen.blit(label, (x + 12, y - 18))
```

## The HUD

The heads-up display now shows:
- Health bar (top-left)
- Kill count
- Active effects (speed/power icons when active)
- Inventory bar (bottom)

## Step-by-Step Build

The full file builds on everything from lessons 12-14 (player, enemies, combat) and adds:

1. The `Item` class
2. Inventory on the `Player` class (a list, plus boost timers)
3. Random drops from dead enemies
4. Pickup logic in the game update
5. Number key handling for using items
6. Treasure chests on the map
7. Updated HUD drawing

The complete code is in `dungeon.py` — save it and run it!

## Run It!

```bash
python3 dungeon.py
```

Move with arrow keys, attack with Space, and press 1-5 to use items. Walk over items to pick them up, and walk into the brown/yellow chests to open them.

## Experiments

1. **Change the drop rate** — find `0.4` and change it to `1.0` so every enemy drops something. Or try `0.1` for rare drops.
2. **Super potions** — change the health potion to restore 20 HP instead of 5. Now they feel powerful.
3. **Longer boosts** — change `150` frames to `300` for speed and power boosts. Double the fun!
4. **More inventory slots** — change the max from 5 to 10. Update the drawing too.
5. **New item type** — try adding a "shield" item that sets a `shield_timer` and reduces damage taken.

## Challenge

Add a **gold coin** item type (yellow color). Instead of going to inventory, coins add to a score counter displayed on the HUD. Make enemies drop coins 30% of the time (separately from the 40% item drop). Show "Gold: X" on screen.

## What's Next

👉 [Go to #25 — Dungeon: Multiple Rooms](../25-dungeon-v5-rooms/lesson.md)