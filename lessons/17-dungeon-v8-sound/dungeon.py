import pygame
import sys
import random
import time

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# Tile types
FLOOR = 0
WALL = 1
DOOR = 2
CHEST = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
DARK_GRAY = (50, 50, 50)
BROWN = (100, 60, 20)
ORANGE = (255, 165, 0)
PURPLE = (150, 0, 200)
DARK_RED = (150, 0, 0)
GOLD = (255, 215, 0)


# ============================================================
# SPRITE CREATION FUNCTIONS
# ============================================================

def create_player_sprite(facing_right=True):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(surf, (0, 100, 220), (8, 14, 16, 12))
    pygame.draw.circle(surf, (240, 200, 160), (16, 10), 7)
    eye_x = 18 if facing_right else 12
    pygame.draw.circle(surf, BLACK, (eye_x, 9), 2)
    pygame.draw.rect(surf, (120, 120, 140), (9, 3, 14, 5))
    pygame.draw.rect(surf, (60, 60, 80), (10, 26, 5, 5))
    pygame.draw.rect(surf, (60, 60, 80), (17, 26, 5, 5))
    if facing_right:
        pygame.draw.rect(surf, (200, 200, 220), (26, 8, 3, 14))
        pygame.draw.rect(surf, (180, 160, 60), (24, 18, 7, 3))
    else:
        pygame.draw.rect(surf, (200, 200, 220), (3, 8, 3, 14))
        pygame.draw.rect(surf, (180, 160, 60), (1, 18, 7, 3))
    return surf


def create_enemy_sprite(enemy_type):
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    if enemy_type == "zombie":
        pygame.draw.rect(surf, (60, 140, 50), (8, 12, 16, 14))
        pygame.draw.circle(surf, (80, 160, 60), (16, 9), 7)
        pygame.draw.circle(surf, RED, (13, 8), 2)
        pygame.draw.circle(surf, RED, (19, 8), 2)
        pygame.draw.rect(surf, (60, 140, 50), (2, 14, 6, 4))
        pygame.draw.rect(surf, (60, 140, 50), (24, 14, 6, 4))
        pygame.draw.rect(surf, (50, 100, 40), (10, 26, 5, 5))
        pygame.draw.rect(surf, (50, 100, 40), (17, 26, 5, 5))
    else:
        pygame.draw.circle(surf, WHITE, (16, 9), 7)
        pygame.draw.circle(surf, BLACK, (13, 8), 2)
        pygame.draw.circle(surf, BLACK, (19, 8), 2)
        pygame.draw.rect(surf, BLACK, (13, 12, 6, 2))
        pygame.draw.rect(surf, (200, 200, 200), (11, 16, 10, 2))
        pygame.draw.rect(surf, (200, 200, 200), (11, 20, 10, 2))
        pygame.draw.rect(surf, (200, 200, 200), (11, 24, 10, 2))
        pygame.draw.rect(surf, WHITE, (15, 16, 2, 12))
        pygame.draw.rect(surf, WHITE, (11, 28, 3, 3))
        pygame.draw.rect(surf, WHITE, (18, 28, 3, 3))
    return surf


def create_boss_sprite():
    size = TILE_SIZE * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (160, 30, 30), (12, 24, 40, 30))
    pygame.draw.circle(surf, (180, 40, 40), (32, 18), 14)
    pygame.draw.polygon(surf, (80, 20, 20), [(20, 10), (24, 0), (28, 10)])
    pygame.draw.polygon(surf, (80, 20, 20), [(36, 10), (40, 0), (44, 10)])
    pygame.draw.circle(surf, YELLOW, (27, 16), 4)
    pygame.draw.circle(surf, YELLOW, (37, 16), 4)
    pygame.draw.circle(surf, BLACK, (27, 16), 2)
    pygame.draw.circle(surf, BLACK, (37, 16), 2)
    pygame.draw.rect(surf, BLACK, (26, 24, 12, 4))
    pygame.draw.rect(surf, WHITE, (28, 24, 3, 3))
    pygame.draw.rect(surf, WHITE, (33, 24, 3, 3))
    pygame.draw.rect(surf, (160, 30, 30), (2, 28, 10, 8))
    pygame.draw.rect(surf, (160, 30, 30), (52, 28, 10, 8))
    pygame.draw.rect(surf, (120, 20, 20), (16, 54, 10, 8))
    pygame.draw.rect(surf, (120, 20, 20), (38, 54, 10, 8))
    return surf


def create_tile_sprites():
    sprites = {}
    floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
    floor.fill((55, 55, 60))
    pygame.draw.line(floor, (65, 65, 70), (0, 0), (TILE_SIZE, 0), 1)
    pygame.draw.line(floor, (65, 65, 70), (0, 0), (0, TILE_SIZE), 1)
    for _ in range(4):
        x = random.randint(4, TILE_SIZE - 4)
        y = random.randint(4, TILE_SIZE - 4)
        pygame.draw.circle(floor, (45, 45, 50), (x, y), 1)
    sprites[FLOOR] = floor

    wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall.fill((110, 65, 25))
    pygame.draw.line(wall, (80, 50, 20), (0, 8), (TILE_SIZE, 8), 1)
    pygame.draw.line(wall, (80, 50, 20), (0, 16), (TILE_SIZE, 16), 1)
    pygame.draw.line(wall, (80, 50, 20), (0, 24), (TILE_SIZE, 24), 1)
    pygame.draw.line(wall, (80, 50, 20), (16, 0), (16, 8), 1)
    pygame.draw.line(wall, (80, 50, 20), (8, 8), (8, 16), 1)
    pygame.draw.line(wall, (80, 50, 20), (24, 8), (24, 16), 1)
    pygame.draw.line(wall, (80, 50, 20), (16, 16), (16, 24), 1)
    pygame.draw.line(wall, (80, 50, 20), (8, 24), (8, 32), 1)
    pygame.draw.line(wall, (80, 50, 20), (24, 24), (24, 32), 1)
    pygame.draw.line(wall, (70, 40, 15), (0, 0), (TILE_SIZE, 0), 2)
    sprites[WALL] = wall

    door = pygame.Surface((TILE_SIZE, TILE_SIZE))
    door.fill((80, 50, 30))
    pygame.draw.rect(door, (60, 35, 15), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4), 2)
    pygame.draw.line(door, (60, 35, 15), (16, 2), (16, 30), 1)
    pygame.draw.circle(door, GOLD, (22, 16), 3)
    sprites[DOOR] = door

    chest = pygame.Surface((TILE_SIZE, TILE_SIZE))
    chest.fill((55, 55, 60))
    pygame.draw.rect(chest, (139, 90, 43), (4, 10, 24, 16))
    pygame.draw.rect(chest, (160, 110, 50), (4, 6, 24, 6))
    pygame.draw.circle(chest, GOLD, (16, 18), 3)
    pygame.draw.rect(chest, GOLD, (15, 18, 2, 4))
    pygame.draw.rect(chest, (100, 70, 30), (4, 12, 24, 2))
    sprites[CHEST] = chest

    return sprites


def create_item_sprites():
    sprites = {}
    hp = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(hp, (200, 30, 30), (10, 12, 12, 14), border_radius=3)
    pygame.draw.rect(hp, (180, 180, 180), (13, 6, 6, 8))
    pygame.draw.rect(hp, (220, 60, 60), (12, 16, 8, 6))
    sprites["health_potion"] = hp

    sp = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.polygon(sp, (50, 150, 255), [
        (18, 4), (10, 16), (15, 16), (12, 28), (22, 14), (17, 14)
    ])
    sprites["speed_boost"] = sp

    sw = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(sw, (220, 200, 60), (14, 2, 4, 18))
    pygame.draw.rect(sw, (160, 120, 40), (8, 20, 16, 3))
    pygame.draw.rect(sw, (120, 80, 30), (14, 23, 4, 6))
    sprites["power_sword"] = sw

    return sprites


def try_load_sprite(filename, fallback_surface):
    try:
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.scale(img, (fallback_surface.get_width(), fallback_surface.get_height()))
        print(f"Loaded sprite: {filename}")
        return img
    except (pygame.error, FileNotFoundError):
        return fallback_surface


# ============================================================
# SOUND MANAGER
# ============================================================

class SoundManager:
    """Tries to load sound files from assets/ folder.
    If files don't exist, the game runs silently -- no crash."""

    def __init__(self):
        self.sounds = {}
        self.music_playing = None
        self.volume = 0.7
        self.enabled = True

        # Initialize the mixer
        try:
            pygame.mixer.init()
            print("Sound system initialized!")
        except pygame.error:
            print("Could not initialize sound system. Running silent.")
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
                print(f"  No sound file found: {filepath} (running silent for this effect)")

        # Try to load music tracks
        self.music_files = {
            "dungeon": "assets/dungeon_music.wav",
            "boss": "assets/boss_music.wav",
        }

    def play(self, sound_name):
        """Play a sound effect by name. Does nothing if sound is missing."""
        if not self.enabled:
            return
        sound = self.sounds.get(sound_name)
        if sound:
            sound.play()

    def play_music(self, track_name):
        """Play background music. Does nothing if file is missing."""
        if not self.enabled:
            return
        if self.music_playing == track_name:
            return  # Already playing this track

        filepath = self.music_files.get(track_name)
        if filepath:
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.volume * 0.5)
                pygame.mixer.music.play(-1)  # -1 means loop forever
                self.music_playing = track_name
                print(f"  Playing music: {filepath}")
            except (pygame.error, FileNotFoundError):
                print(f"  No music file found: {filepath}")
                self.music_playing = None

    def stop_music(self):
        """Stop background music."""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass
            self.music_playing = None

    def set_volume(self, vol):
        """Set volume for all sounds (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, vol))
        if not self.enabled:
            return
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.volume)
        try:
            pygame.mixer.music.set_volume(self.volume * 0.5)
        except pygame.error:
            pass

    def volume_up(self):
        self.set_volume(self.volume + 0.1)

    def volume_down(self):
        self.set_volume(self.volume - 0.1)


# ============================================================
# ROOM DATA
# ============================================================

def make_room_maps():
    room0_map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    room0_enemies = [("zombie", 8, 5), ("zombie", 15, 10), ("skeleton", 20, 3)]

    room1_map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,3,0,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    room1_enemies = [("zombie", 3, 3), ("skeleton", 10, 6), ("zombie", 20, 10), ("skeleton", 15, 14)]

    room2_map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    room2_enemies = [("skeleton", 5, 5), ("skeleton", 18, 5), ("zombie", 5, 12), ("zombie", 18, 12), ("skeleton", 12, 9)]

    room3_map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    room3_enemies = [("zombie", 6, 6), ("zombie", 18, 6), ("skeleton", 12, 12)]

    room4_map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    room4_enemies = []

    rooms_data = [
        (room0_map, room0_enemies, [], (2, 2)),
        (room1_map, room1_enemies, [], (12, 1)),
        (room2_map, room2_enemies, [], (12, 1)),
        (room3_map, room3_enemies, [], (12, 1)),
        (room4_map, room4_enemies, [], (12, 1)),
    ]
    return rooms_data


# ============================================================
# GAME CLASSES
# ============================================================

class Player:
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.health = 10
        self.max_health = 10
        self.attack_power = 2
        self.facing = "right"
        self.speed = 1
        self.inventory = []
        self.attack_cooldown = 0
        self.attacking = False
        self.attack_timer = 0
        self.hurt_timer = 0
        self.kills = 0
        self.speed_boost_timer = 0
        self.sprite_right = sprites["player_right"]
        self.sprite_left = sprites["player_left"]

    def move(self, dx, dy, tile_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
            tile = tile_map[new_y][new_x]
            if tile != WALL:
                self.x = new_x
                self.y = new_y
        if dx > 0:
            self.facing = "right"
        elif dx < 0:
            self.facing = "left"
        elif dy < 0:
            self.facing = "up"
        elif dy > 0:
            self.facing = "down"

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = 8
            self.attack_cooldown = 20

    def get_attack_tile(self):
        if self.facing == "right":
            return (self.x + 1, self.y)
        elif self.facing == "left":
            return (self.x - 1, self.y)
        elif self.facing == "up":
            return (self.x, self.y - 1)
        elif self.facing == "down":
            return (self.x, self.y + 1)
        return (self.x + 1, self.y)

    def use_item(self, index):
        if 0 <= index < len(self.inventory):
            item_type = self.inventory.pop(index)
            if item_type == "health_potion":
                self.health = min(self.health + 5, self.max_health)
            elif item_type == "speed_boost":
                self.speed_boost_timer = 300
            elif item_type == "power_sword":
                self.attack_power = 4

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attacking = False
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if self.facing == "left":
            sprite = self.sprite_left
        else:
            sprite = self.sprite_right

        if self.hurt_timer > 0 and self.hurt_timer % 4 < 2:
            flash = sprite.copy()
            flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
            screen.blit(flash, (px, py))
        else:
            screen.blit(sprite, (px, py))

        if self.attacking:
            ax, ay = self.get_attack_tile()
            apx = ax * TILE_SIZE - camera_x
            apy = ay * TILE_SIZE - camera_y
            attack_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.arc(attack_surf, (255, 255, 200, 180), (0, 0, TILE_SIZE, TILE_SIZE), 0, 3.14, 4)
            screen.blit(attack_surf, (apx, apy))


class Enemy:
    def __init__(self, enemy_type, x, y, sprites):
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.health = 4 if enemy_type == "zombie" else 3
        self.max_health = self.health
        self.move_timer = 0
        self.move_delay = 20 if enemy_type == "zombie" else 15
        self.alive = True
        self.hit_flash = 0
        self.death_timer = 0
        self.sprite = sprites.get(enemy_type, sprites.get("zombie"))

    def update(self, player, tile_map):
        if not self.alive:
            self.death_timer -= 1
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            if self.enemy_type == "zombie":
                dx = random.choice([-1, 0, 0, 1])
                dy = random.choice([-1, 0, 0, 1]) if dx == 0 else 0
            else:
                dx = 0
                dy = 0
                if abs(player.x - self.x) > abs(player.y - self.y):
                    dx = 1 if player.x > self.x else -1
                else:
                    dy = 1 if player.y > self.y else -1
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_y < len(tile_map) and 0 <= new_x < len(tile_map[0]):
                if tile_map[new_y][new_x] == FLOOR:
                    self.x = new_x
                    self.y = new_y

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 10
        if self.health <= 0:
            self.alive = False
            self.death_timer = 15

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if not self.alive:
            if self.death_timer > 0:
                alpha = int(255 * (self.death_timer / 15))
                death_surf = self.sprite.copy()
                death_surf.set_alpha(alpha)
                screen.blit(death_surf, (px, py))
            return
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            flash = self.sprite.copy()
            flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
            screen.blit(flash, (px, py))
        else:
            screen.blit(self.sprite, (px, py))
        if self.health < self.max_health:
            bar_width = TILE_SIZE - 4
            bar_height = 3
            fill = int(bar_width * self.health / self.max_health)
            pygame.draw.rect(screen, RED, (px + 2, py - 5, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (px + 2, py - 5, fill, bar_height))


class Boss:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.health = 50
        self.max_health = 50
        self.alive = True
        self.phase = "chase"
        self.phase_timer = 0
        self.move_timer = 0
        self.hit_flash = 0
        self.charge_dx = 0
        self.charge_dy = 0
        self.death_timer = 0
        self.summon_count = 0
        self.sprite = sprite

    def update(self, player, tile_map, enemies, enemy_sprites):
        if not self.alive:
            self.death_timer -= 1
            return
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.phase_timer += 1
        self.move_timer += 1

        if self.phase == "chase":
            if self.move_timer >= 12:
                self.move_timer = 0
                dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
                dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_y < len(tile_map) - 1 and 0 <= new_x < len(tile_map[0]) - 1:
                    if tile_map[new_y][new_x] != WALL:
                        self.x = new_x
                        self.y = new_y
            if self.phase_timer > 120:
                self.phase = "charge"
                self.phase_timer = 0
                self.charge_dx = 1 if player.x > self.x else -1
                self.charge_dy = 1 if player.y > self.y else -1

        elif self.phase == "charge":
            if self.move_timer >= 3:
                self.move_timer = 0
                new_x = self.x + self.charge_dx
                new_y = self.y + self.charge_dy
                if 0 <= new_y < len(tile_map) - 1 and 0 <= new_x < len(tile_map[0]) - 1:
                    if tile_map[new_y][new_x] != WALL:
                        self.x = new_x
                        self.y = new_y
                    else:
                        self.phase = "summon"
                        self.phase_timer = 0
                        self.summon_count = 0
                else:
                    self.phase = "summon"
                    self.phase_timer = 0
                    self.summon_count = 0
            if self.phase_timer > 60:
                self.phase = "summon"
                self.phase_timer = 0
                self.summon_count = 0

        elif self.phase == "summon":
            if self.phase_timer == 30 and self.summon_count < 2:
                spawn_x = self.x + random.choice([-2, 2])
                spawn_y = self.y + random.choice([-2, 2])
                spawn_x = max(1, min(spawn_x, len(tile_map[0]) - 2))
                spawn_y = max(1, min(spawn_y, len(tile_map) - 2))
                if tile_map[spawn_y][spawn_x] != WALL:
                    enemies.append(Enemy("skeleton", spawn_x, spawn_y, enemy_sprites))
                    self.summon_count += 1
            if self.phase_timer > 90:
                self.phase = "rest"
                self.phase_timer = 0

        elif self.phase == "rest":
            if self.phase_timer > 60:
                self.phase = "chase"
                self.phase_timer = 0

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash = 10
        if self.health <= 0:
            self.alive = False
            self.death_timer = 60

    def touches_player(self, player):
        return (self.x <= player.x <= self.x + 1 and
                self.y <= player.y <= self.y + 1)

    def draw(self, screen, camera_x, camera_y):
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if not self.alive:
            if self.death_timer > 0:
                alpha = int(255 * (self.death_timer / 60))
                death_surf = self.sprite.copy()
                death_surf.set_alpha(alpha)
                screen.blit(death_surf, (px, py))
            return
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            flash = self.sprite.copy()
            flash.fill(WHITE, special_flags=pygame.BLEND_ADD)
            screen.blit(flash, (px, py))
        else:
            screen.blit(self.sprite, (px, py))


class Item:
    def __init__(self, item_type, x, y, sprites):
        self.item_type = item_type
        self.x = x
        self.y = y
        self.collected = False
        self.sprite = sprites.get(item_type)

    def draw(self, screen, camera_x, camera_y):
        if self.collected:
            return
        px = self.x * TILE_SIZE - camera_x
        py = self.y * TILE_SIZE - camera_y
        if self.sprite:
            screen.blit(self.sprite, (px, py))
        else:
            color = RED if self.item_type == "health_potion" else BLUE if self.item_type == "speed_boost" else GOLD
            pygame.draw.rect(screen, color, (px + 8, py + 8, TILE_SIZE - 16, TILE_SIZE - 16))


class Room:
    def __init__(self, tile_map, enemies, items, doors_to, room_index):
        self.tile_map = tile_map
        self.enemies = enemies
        self.items = items
        self.doors_to = doors_to
        self.room_index = room_index
        self.visited = False
        self.boss = None

    def get_door_positions(self):
        doors = []
        for row in range(len(self.tile_map)):
            for col in range(len(self.tile_map[row])):
                if self.tile_map[row][col] == DOOR:
                    doors.append((col, row))
        return doors


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robert's Dungeons v8 - Sound!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 22)

        # Initialize sound manager
        self.sound = SoundManager()

        # Create sprites
        self.sprites = {}
        self.sprites["player_right"] = create_player_sprite(facing_right=True)
        self.sprites["player_left"] = create_player_sprite(facing_right=False)
        self.sprites["zombie"] = create_enemy_sprite("zombie")
        self.sprites["skeleton"] = create_enemy_sprite("skeleton")
        self.sprites["boss"] = create_boss_sprite()
        self.sprites["tiles"] = create_tile_sprites()
        self.sprites["items"] = create_item_sprites()

        self.sprites["player_right"] = try_load_sprite("assets/player_right.png", self.sprites["player_right"])
        self.sprites["player_left"] = try_load_sprite("assets/player_left.png", self.sprites["player_left"])
        self.sprites["zombie"] = try_load_sprite("assets/zombie.png", self.sprites["zombie"])
        self.sprites["skeleton"] = try_load_sprite("assets/skeleton.png", self.sprites["skeleton"])
        self.sprites["boss"] = try_load_sprite("assets/boss.png", self.sprites["boss"])

        # Build rooms
        rooms_data = make_room_maps()
        self.rooms = []
        for i, (tmap, edata, idata, pstart) in enumerate(rooms_data):
            enemy_sprites = {"zombie": self.sprites["zombie"], "skeleton": self.sprites["skeleton"]}
            enemies = [Enemy(etype, ex, ey, enemy_sprites) for etype, ex, ey in edata]
            items = [Item(itype, ix, iy, self.sprites["items"]) for itype, ix, iy in idata]
            doors_to = {}
            if i > 0:
                doors_to["top"] = i - 1
            if i < len(rooms_data) - 1:
                doors_to["bottom"] = i + 1
            room = Room(tmap, enemies, items, doors_to, i)
            self.rooms.append(room)

        self.rooms[-1].boss = Boss(12, 8, self.sprites["boss"])

        self.current_room = 0
        start_pos = rooms_data[0][3]
        player_sprites = {"player_right": self.sprites["player_right"], "player_left": self.sprites["player_left"]}
        self.player = Player(start_pos[0], start_pos[1], player_sprites)

        self.camera_x = 0
        self.camera_y = 0
        self.running = True
        self.game_over = False
        self.victory = False
        self.transition_timer = 0
        self.start_time = time.time()
        self.rooms[0].visited = True

        # Start dungeon music
        self.sound.play_music("dungeon")

    def get_room(self):
        return self.rooms[self.current_room]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over or self.victory:
                    if event.key == pygame.K_r:
                        self.sound.stop_music()
                        self.__init__()
                    return

                if event.key == pygame.K_UP:
                    self.player.move(0, -1, self.get_room().tile_map)
                elif event.key == pygame.K_DOWN:
                    self.player.move(0, 1, self.get_room().tile_map)
                elif event.key == pygame.K_LEFT:
                    self.player.move(-1, 0, self.get_room().tile_map)
                elif event.key == pygame.K_RIGHT:
                    self.player.move(1, 0, self.get_room().tile_map)
                elif event.key == pygame.K_SPACE:
                    self.player.attack()
                    self.sound.play("sword_swing")
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    idx = event.key - pygame.K_1
                    if idx < len(self.player.inventory):
                        self.player.use_item(idx)
                        self.sound.play("item_pickup")
                # Volume controls
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    self.sound.volume_up()
                elif event.key == pygame.K_MINUS:
                    self.sound.volume_down()

    def check_door_transition(self):
        room = self.get_room()
        tile = room.tile_map[self.player.y][self.player.x]
        if tile == DOOR:
            door_positions = room.get_door_positions()
            for dx, dy in door_positions:
                if dx == self.player.x and dy == self.player.y:
                    old_room = self.current_room
                    if dy == 0 and "top" in room.doors_to:
                        self.current_room = room.doors_to["top"]
                        self.player.y = len(self.get_room().tile_map) - 2
                        self.transition_timer = 15
                    elif dy == len(room.tile_map) - 1 and "bottom" in room.doors_to:
                        self.current_room = room.doors_to["bottom"]
                        self.player.y = 1
                        self.transition_timer = 15
                    if self.current_room != old_room:
                        self.sound.play("door_open")
                        self.rooms[self.current_room].visited = True
                        # Switch to boss music if entering boss room
                        if self.current_room == len(self.rooms) - 1:
                            self.sound.play_music("boss")
                        else:
                            self.sound.play_music("dungeon")
                    break

    def check_chest(self):
        room = self.get_room()
        if room.tile_map[self.player.y][self.player.x] == CHEST:
            room.tile_map[self.player.y][self.player.x] = FLOOR
            loot = random.choice(["health_potion", "speed_boost", "power_sword"])
            if len(self.player.inventory) < 5:
                self.player.inventory.append(loot)
                self.sound.play("chest_open")

    def update(self):
        if self.game_over or self.victory:
            return
        if self.transition_timer > 0:
            self.transition_timer -= 1
            return

        self.player.update()
        room = self.get_room()
        enemy_sprites = {"zombie": self.sprites["zombie"], "skeleton": self.sprites["skeleton"]}

        for enemy in room.enemies:
            enemy.update(self.player, room.tile_map)
            if enemy.alive and enemy.x == self.player.x and enemy.y == self.player.y:
                if self.player.hurt_timer <= 0:
                    self.player.health -= 1
                    self.player.hurt_timer = 30
                    self.sound.play("player_hurt")

        if self.player.attacking and self.player.attack_timer == 7:
            ax, ay = self.player.get_attack_tile()
            for enemy in room.enemies:
                if enemy.alive and enemy.x == ax and enemy.y == ay:
                    enemy.take_damage(self.player.attack_power)
                    self.sound.play("enemy_hit")
                    if not enemy.alive:
                        self.player.kills += 1
                        self.sound.play("enemy_death")
                        if random.random() < 0.4:
                            loot = random.choice(["health_potion", "speed_boost", "power_sword"])
                            room.items.append(Item(loot, enemy.x, enemy.y, self.sprites["items"]))

            if room.boss and room.boss.alive:
                boss = room.boss
                if (boss.x <= ax <= boss.x + 1) and (boss.y <= ay <= boss.y + 1):
                    boss.take_damage(self.player.attack_power)
                    self.sound.play("enemy_hit")
                    if not boss.alive:
                        self.victory = True
                        self.player.kills += 1
                        self.sound.play("enemy_death")
                        self.sound.stop_music()

        if room.boss and room.boss.alive:
            room.boss.update(self.player, room.tile_map, room.enemies, enemy_sprites)
            if room.boss.touches_player(self.player):
                if self.player.hurt_timer <= 0:
                    self.player.health -= 2
                    self.player.hurt_timer = 30
                    self.sound.play("player_hurt")

        room.enemies = [e for e in room.enemies if e.alive or e.death_timer > 0]

        for item in room.items:
            if not item.collected and item.x == self.player.x and item.y == self.player.y:
                if len(self.player.inventory) < 5:
                    self.player.inventory.append(item.item_type)
                    item.collected = True
                    self.sound.play("item_pickup")

        self.check_door_transition()
        self.check_chest()

        self.camera_x = self.player.x * TILE_SIZE - SCREEN_WIDTH // 2 + TILE_SIZE // 2
        self.camera_y = self.player.y * TILE_SIZE - SCREEN_HEIGHT // 2 + TILE_SIZE // 2

        if self.player.health <= 0:
            self.game_over = True
            self.sound.stop_music()

    def draw(self):
        self.screen.fill(BLACK)
        room = self.get_room()
        tile_sprites = self.sprites["tiles"]

        for row in range(len(room.tile_map)):
            for col in range(len(room.tile_map[row])):
                sx = col * TILE_SIZE - self.camera_x
                sy = row * TILE_SIZE - self.camera_y
                if -TILE_SIZE < sx < SCREEN_WIDTH and -TILE_SIZE < sy < SCREEN_HEIGHT:
                    tile_type = room.tile_map[row][col]
                    if tile_type in tile_sprites:
                        self.screen.blit(tile_sprites[tile_type], (sx, sy))
                    else:
                        self.screen.blit(tile_sprites[FLOOR], (sx, sy))

        for item in room.items:
            item.draw(self.screen, self.camera_x, self.camera_y)
        for enemy in room.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        if room.boss:
            room.boss.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        if self.transition_timer > 0:
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash.fill(WHITE)
            alpha = int(255 * (self.transition_timer / 15))
            flash.set_alpha(alpha)
            self.screen.blit(flash, (0, 0))

        self.draw_hud(room)

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            text = self.big_font.render("GAME OVER", True, RED)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))
            restart = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 300))

        if self.victory:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))
            text = self.big_font.render("YOU WIN!", True, GOLD)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150))
            elapsed = int(time.time() - self.start_time)
            stats = [
                f"Time: {elapsed // 60}m {elapsed % 60}s",
                f"Kills: {self.player.kills}",
                f"Items collected: {5 - len(self.player.inventory)} used",
                "Press R to play again",
            ]
            for i, line in enumerate(stats):
                t = self.font.render(line, True, WHITE)
                self.screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 240 + i * 35))

        pygame.display.flip()

    def draw_hud(self, room):
        # Health bar
        bar_x, bar_y = 10, 10
        bar_width, bar_height = 200, 20
        fill = int(bar_width * self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, DARK_RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        hp_text = self.small_font.render(f"HP: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(hp_text, (bar_x + 5, bar_y + 2))

        # Kill counter
        kill_text = self.font.render(f"Kills: {self.player.kills}", True, WHITE)
        self.screen.blit(kill_text, (bar_x, bar_y + 28))

        # Attack cooldown
        if self.player.attack_cooldown > 0:
            cd_fill = int(60 * (1 - self.player.attack_cooldown / 20))
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y + 52, 60, 8))
            pygame.draw.rect(self.screen, YELLOW, (bar_x, bar_y + 52, cd_fill, 8))

        # Volume indicator
        vol_text = self.small_font.render(f"Vol: {int(self.sound.volume * 100)}%  (+/-)", True, WHITE)
        self.screen.blit(vol_text, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 25))

        # Inventory
        inv_y = SCREEN_HEIGHT - 50
        inv_text = self.small_font.render("Inventory (1-5):", True, WHITE)
        self.screen.blit(inv_text, (10, inv_y - 18))
        for i in range(5):
            slot_x = 10 + i * 40
            pygame.draw.rect(self.screen, (60, 60, 60), (slot_x, inv_y, 34, 34))
            pygame.draw.rect(self.screen, WHITE, (slot_x, inv_y, 34, 34), 1)
            if i < len(self.player.inventory):
                item_type = self.player.inventory[i]
                item_sprite = self.sprites["items"].get(item_type)
                if item_sprite:
                    self.screen.blit(item_sprite, (slot_x + 1, inv_y + 1))

        # Room indicator
        room_text = self.small_font.render(f"Room {self.current_room + 1}/5", True, WHITE)
        self.screen.blit(room_text, (SCREEN_WIDTH - 100, 10))

        # Speed boost
        if self.player.speed_boost_timer > 0:
            boost_text = self.small_font.render("SPEED BOOST!", True, BLUE)
            self.screen.blit(boost_text, (SCREEN_WIDTH // 2 - 50, 10))

        # Boss health bar
        if room.boss and room.boss.alive:
            boss_bar_w = 400
            boss_bar_x = SCREEN_WIDTH // 2 - boss_bar_w // 2
            boss_bar_y = 50
            boss_fill = int(boss_bar_w * room.boss.health / room.boss.max_health)
            pygame.draw.rect(self.screen, (80, 0, 0), (boss_bar_x, boss_bar_y, boss_bar_w, 24))
            pygame.draw.rect(self.screen, (200, 30, 30), (boss_bar_x, boss_bar_y, boss_fill, 24))
            pygame.draw.rect(self.screen, WHITE, (boss_bar_x, boss_bar_y, boss_bar_w, 24), 2)
            boss_name = self.font.render("DEMON KING", True, WHITE)
            self.screen.blit(boss_name, (SCREEN_WIDTH // 2 - boss_name.get_width() // 2, boss_bar_y + 28))

        # Minimap
        mm_x = SCREEN_WIDTH - 70
        mm_y = 30
        for i, r in enumerate(self.rooms):
            rx = mm_x
            ry = mm_y + i * 14
            color = (100, 100, 100)
            if r.visited:
                color = (80, 80, 120)
            if i == self.current_room:
                color = GREEN
            pygame.draw.rect(self.screen, color, (rx, ry, 12, 10))
            pygame.draw.rect(self.screen, WHITE, (rx, ry, 12, 10), 1)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


# ============================================================
# START THE GAME
# ============================================================
if __name__ == "__main__":
    game = Game()
    game.run()
