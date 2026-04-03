# Multiple Rooms

!!! success "🎯 Mission"
    Create a dungeon with 5 connected rooms, door transitions, and a minimap to track where you've been.


!!! example "🎮 Play It! — Multiple Rooms Demo"
    By the end of this section, you'll be building a playable game just like this one. **Arrow keys to move, Space to attack!**

<iframe src="/games/dungeon_v5.html" width="100%" height="450" style="border: 5px solid #ffcc00; border-radius: 16px; box-shadow: 6px 6px 0px #ff00ff; background: #0b0b13;"></iframe>


## Why Multiple Rooms?

Right now our dungeon is one big open area. But real dungeon crawlers have rooms you move between — each room is its own mini-challenge. Think of it like floors in Minecraft Dungeons, except we're using doors instead of staircases.

Here's the plan:
- 5 rooms, each with its own tile map and enemies
- Doors (tile type 2) connect the rooms
- Walk into a door and you teleport to the next room
- A minimap shows which rooms you've visited

## The Room Class

Each room is basically a self-contained little world:

```python
class Room:
    def __init__(self, tile_map, enemy_spawns, chest_positions, player_start, door_connections):
        self.tile_map = [row[:] for row in tile_map]  # deep copy
        self.enemies = []
        self.items = []
        self.enemy_spawns = enemy_spawns
        self.chest_positions = chest_positions
        self.player_start = player_start
        self.door_connections = door_connections
        self.visited = False
        self.chests_opened = set()
```

The big new thing here is **door_connections**. It's a dictionary that maps a door's position to where it leads:

```python
door_connections = {
    (9, 7): (1, 1, 7),   # door at (9,7) leads to room 1, spawn at (1,7)
}
```

So when the player walks into the door at column 9, row 7, we switch to room index 1 and place the player at (1, 7) in that room. It's kind of like a teleporter — you step on this spot, and boom, you're somewhere else.

## Room Transitions

When you step on a door tile, the game does three things:

1. **Looks up** where this door leads in the `door_connections` dict
2. **Flashes** the screen white for a few frames (transition effect)
3. **Loads** the new room and places the player at the spawn point

```python
if tile == 2:
    door_pos = (new_x, new_y)
    connections = current_room.door_connections
    if door_pos in connections:
        room_idx, spawn_x, spawn_y = connections[door_pos]
        self.transition_to_room(room_idx, spawn_x, spawn_y)
```

The transition effect is simple — we just fill the screen white for a few frames:

```python
def transition_to_room(self, room_idx, spawn_x, spawn_y):
    self.flash_timer = 8  # white flash for 8 frames
    self.current_room_idx = room_idx
    room = self.rooms[room_idx]
    if not room.visited:
        room.visited = True
        room.spawn_enemies()
    self.player.x = spawn_x
    self.player.y = spawn_y
```

That white flash is a classic game trick. Without it, the room switch would feel instant and jarring. With it, your brain goes "oh, I'm transitioning somewhere" and it feels smooth.

## Spawning Enemies Per Room

Each room only spawns enemies the **first time** you enter. After that, whatever enemies you killed stay dead, and any items stay on the ground. This is tracked by `room.visited`.

```python
def spawn_enemies(self):
    for x, y, enemy_type in self.enemy_spawns:
        self.enemies.append(Enemy(x, y, enemy_type))
```

This is nice because it means you can clear a room, leave, and come back to grab items you left behind without getting ambushed again.

## The Room Layouts

We create 5 rooms. Each one is about 20 columns by 15 rows:

- **Room 0** (Start): A simple room with a couple zombies. Door on the right.
- **Room 1** (Corridor): A narrow hallway-like room. Doors on left and right.
- **Room 2** (Arena): Open room with several enemies and chests. Door on left and bottom.
- **Room 3** (Maze): Twisty corridors with skeletons. Door on top and right.
- **Room 4** (Boss Room): Big empty room. No enemies yet — this is where the boss will go in Lesson 25!

## The Minimap

The minimap sits in the top-right corner. It's just small rectangles showing which rooms you've found:

```python
def draw_minimap(self):
    base_x = SCREEN_WIDTH - 120
    base_y = 10
    # Room positions on minimap (hand-placed to look like a map)
    positions = [(0, 1), (1, 1), (2, 1), (2, 2), (3, 1)]
    for i, (mx, my) in enumerate(positions):
        rx = base_x + mx * 25
        ry = base_y + my * 20
        if i == self.current_room_idx:
            color = WHITE
        elif self.rooms[i].visited:
            color = GRAY
        else:
            continue  # don't show unvisited rooms
        pygame.draw.rect(self.screen, color, (rx, ry, 20, 15))
```

Visited rooms are gray, the current room is white, and rooms you haven't found yet are invisible. It's a small detail but it makes exploring feel way more satisfying — you can see your progress!

## Step-by-Step Build

This lesson builds on everything from Lesson 23:

1. Create the `Room` class to hold maps, enemies, items, and door connections
2. Define 5 room layouts as 2D lists
3. Set up door connections between rooms
4. Add transition logic (flash + room switch)
5. Update the game loop to work with `current_room` instead of a single map
6. Draw the minimap
7. Player HP and inventory carry between rooms

The full code is in `dungeon.py`.

## Run It!

```bash
python3 dungeon.py
```

Move with arrow keys, attack with Space, 1-5 for items. Walk into the dark brown doors to move between rooms. Check the minimap in the top-right to see where you've been.

## Experiments

1. **Add a 6th room** — copy one of the room maps, add it to the rooms list, and connect it with doors.
2. **Change room colors** — give each room a different floor color to make them feel distinct.
3. **More enemies** — double the enemy spawns in Room 2 to make it a real challenge.
4. **Locked doors** — make a door that only opens if you have a "key" item in your inventory.
5. **Room names** — display the room name at the top of the screen when you enter (like "The Crypt" or "Skeleton Hall").

## Challenge

Add a **room clear bonus**: when all enemies in a room are defeated, spawn a special chest in the center of the room. This rewards the player for fighting instead of running past enemies.

## What's Next

👉 [Next: The Boss](../26-dungeon-v6-boss/lesson.md)