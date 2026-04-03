# Lesson 17: Dungeon v8 -- Sound & Music

**Goal:** Add sound effects and background music to the dungeon, and learn how to handle errors gracefully when files are missing.

## Why Sound Matters

Play any game with the sound off, then turn it on. Night and day, right? Sound effects give your brain feedback -- you *feel* the sword hit, you *hear* the enemy die, you *know* you picked up an item. Music sets the mood. A dungeon should feel tense; a boss fight should feel intense.

Pygame has a built-in sound system called **pygame.mixer**. It can play short sound effects (like a sword swing) and longer background music (like a dungeon theme) at the same time.

## The Problem: We Don't Have Sound Files

Here's a real-world problem you'll run into all the time. We want to play sounds, but we don't have any .wav files on disk yet. If we just wrote `pygame.mixer.Sound("sword.wav")` and the file doesn't exist, the program would crash.

This is where **try/except** comes in -- honestly one of the most important things in all of programming. Think of it like this: you're telling Python "hey, try this thing, and if it blows up, do this other thing instead of crashing."

```python
try:
    sound = pygame.mixer.Sound("assets/sword_swing.wav")
    print("Loaded sword sound!")
except (pygame.error, FileNotFoundError):
    sound = None
    print("No sword sound file found, running silent")
```

If the file exists, great -- we load it. If not, we set `sound` to `None` and move on. The game works either way.

This pattern is used ALL the time in real software. Video players try to load subtitles -- if the file's not there, no subtitles. Web browsers try to load images -- if the server's down, show a placeholder. Same idea everywhere.

## The Sound Manager

Rather than scattering try/except blocks all over the place, we'll build a **SoundManager** class that handles all the sound stuff in one place:

```python
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.volume = 0.7
        self.enabled = True

        try:
            pygame.mixer.init()
            print("Sound system initialized!")
        except pygame.error:
            print("Could not initialize sound. Running silent.")
            self.enabled = False
            return

        # Try to load each sound effect
        sound_files = {
            "sword_swing": "assets/sword_swing.wav",
            "enemy_hit": "assets/enemy_hit.wav",
            "enemy_death": "assets/enemy_death.wav",
            "item_pickup": "assets/item_pickup.wav",
            "chest_open": "assets/chest_open.wav",
            "player_hurt": "assets/player_hurt.wav",
            "door_open": "assets/door_open.wav",
        }

        for name, filepath in sound_files.items():
            try:
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
                print(f"  Loaded sound: {filepath}")
            except (pygame.error, FileNotFoundError):
                self.sounds[name] = None
                print(f"  No sound file: {filepath} (silent)")
```

The `play` method checks if the sound exists before playing:

```python
def play(self, sound_name):
    if not self.enabled:
        return
    sound = self.sounds.get(sound_name)
    if sound:
        sound.play()
```

If the sound is `None` (because the file wasn't found), nothing happens. No crash. That's the beauty of it.

## Sound Effects vs Music

You know how in games there are two kinds of audio? Short clips that play when stuff happens (sword swing, enemy grunt, item pickup) and then a longer track that loops in the background? Pygame treats these differently.

**Sound effects** are those short clips. Pygame can play a bunch of them at the same time on separate "channels."

**Background music** is the longer track that loops continuously. Pygame has a special system for it: `pygame.mixer.music`. Only one music track can play at a time.

```python
def play_music(self, track_name):
    filepath = self.music_files.get(track_name)
    if filepath:
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.volume * 0.5)
            pygame.mixer.music.play(-1)  # -1 means loop forever
        except (pygame.error, FileNotFoundError):
            print(f"No music file: {filepath}")
```

The `-1` argument to `play()` means "loop forever." You could pass `0` for "play once" or `3` for "play 3 times."

We play dungeon music in normal rooms and switch to boss music when entering the boss room.

## Volume Control

We let the player adjust volume with the **+** and **-** keys:

```python
def volume_up(self):
    self.set_volume(self.volume + 0.1)

def volume_down(self):
    self.set_volume(self.volume - 0.1)

def set_volume(self, vol):
    self.volume = max(0.0, min(1.0, vol))  # Clamp between 0 and 1
    for sound in self.sounds.values():
        if sound:
            sound.set_volume(self.volume)
    pygame.mixer.music.set_volume(self.volume * 0.5)
```

That `max(0.0, min(1.0, vol))` trick **clamps** the value between 0 and 1. Volume can't go below 0 or above 1. We set music a bit quieter (times 0.5) so it doesn't drown out the sound effects.

## Where to Get Free Sounds

When you're ready to add real sound files, here are great free sources:

- **OpenGameArt.org** -- free game assets, tons of sounds
- **freesound.org** -- huge library of free sounds (need a free account)
- **sfxr** (or its web version **jfxr**) -- generates retro game sounds. Perfect for a dungeon crawler!

Download .wav files and put them in an `assets/` folder next to your game. The SoundManager will automatically find and load them.

## Step-by-Step Build

### Step 1: The SoundManager class

Add the `SoundManager` class after the sprite functions. It handles initialization, loading, playing, and volume.

### Step 2: Create sound manager in Game.__init__

```python
self.sound = SoundManager()
```

This goes right at the top of `__init__`, before building rooms.

### Step 3: Play sounds at the right moments

Sprinkle `self.sound.play(...)` calls throughout the game logic:

```python
# When player attacks
self.sound.play("sword_swing")

# When enemy takes damage
self.sound.play("enemy_hit")

# When enemy dies
self.sound.play("enemy_death")

# When player gets hurt
self.sound.play("player_hurt")

# When picking up an item
self.sound.play("item_pickup")

# When opening a chest
self.sound.play("chest_open")

# When going through a door
self.sound.play("door_open")
```

### Step 4: Music switching

Start dungeon music in `__init__`, switch to boss music when entering the boss room:

```python
# In __init__
self.sound.play_music("dungeon")

# When entering boss room
if self.current_room == len(self.rooms) - 1:
    self.sound.play_music("boss")

# When boss dies or game over
self.sound.stop_music()
```

### Step 5: Volume controls in handle_input

```python
elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
    self.sound.volume_up()
elif event.key == pygame.K_MINUS:
    self.sound.volume_down()
```

### Step 6: Volume display in HUD

Show the current volume so the player knows what level they're at:

```python
vol_text = self.small_font.render(f"Vol: {int(self.sound.volume * 100)}%  (+/-)", True, WHITE)
self.screen.blit(vol_text, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 25))
```

### The Full Game

The complete file is `dungeon.py` in this folder. It includes everything from lesson 16 (sprites) plus the full sound system.

## Run It!

```bash
python3 dungeon.py
```

When you run it, look at the terminal output. You'll see messages like:

```
Sound system initialized!
  No sound file found: assets/sword_swing.wav (running silent for this effect)
  No sound file found: assets/enemy_hit.wav (running silent for this effect)
  ...
```

The game runs perfectly fine without sound files. But if you download some .wav files and put them in an `assets/` folder, those messages will change to "Loaded sound!" and you'll hear them in-game.

Use arrow keys to move, Space to attack, 1-5 for items, +/- for volume.

## Experiments

1. **Try the jfxr sound generator.** Go to https://jfxr.frozenfractal.com in your browser. Generate a "hit" sound, export it as a .wav file, and save it as `assets/sword_swing.wav`. Run the game -- you should hear it!

2. **Change the volume step.** Instead of `self.volume + 0.1`, try `0.05` for finer control or `0.25` for bigger jumps.

3. **Add a new sound event.** Add a "level_up" sound that plays when you enter a new room for the first time.

4. **Make boss music switch back.** Right now, once boss music starts, it stays. Make it switch back to dungeon music if you leave the boss room.

## Challenge

Add a **mute toggle**. When the player presses **M**, all sound is muted. Press M again to unmute. Show "MUTED" on the HUD when sound is off. Hint: you'll need a `self.muted` variable in the SoundManager, and check it in the `play()` method.

## What's Next

In Lesson 18, we'll make every playthrough different with procedural generation -- the dungeon builds itself randomly each time you play!
