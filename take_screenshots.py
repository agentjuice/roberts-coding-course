"""Run each Pygame game for a few frames and save a screenshot."""
import subprocess
import sys
import os

COURSE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(COURSE_DIR, "docs", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# For each game, create a wrapper that imports the game, runs a few frames, saves screenshot
GAMES = [
    ("lessons/07-connect4-v3-pygame/connect4.py", "connect4_pygame.png", 5),
    ("lessons/08-connect4-v4-animation/connect4.py", "connect4_anim.png", 5),
    ("lessons/09-connect4-v5-pygame-functions/connect4.py", "connect4_functions.png", 5),
    ("lessons/10-snake-v1/snake.py", "snake.png", 30),
    ("lessons/11-snake-v2-classes/snake.py", "snake_classes.png", 30),
    ("lessons/12-dungeon-v1-hero/dungeon.py", "dungeon_v1.png", 10),
    ("lessons/13-dungeon-v2-enemies/dungeon.py", "dungeon_v2.png", 10),
    ("lessons/14-dungeon-v3-combat/dungeon.py", "dungeon_v3.png", 10),
    ("lessons/15-dungeon-v4-loot/dungeon.py", "dungeon_v4.png", 10),
    ("lessons/16-dungeon-v5-rooms/dungeon.py", "dungeon_v5.png", 10),
    ("lessons/17-dungeon-v6-boss/dungeon.py", "dungeon_v6.png", 10),
]

WRAPPER = '''
import pygame
import sys
import os

# Patch time.sleep to be instant
import time
original_sleep = time.sleep
time.sleep = lambda x: original_sleep(0.01)

# Patch pygame.event.get to inject fake events after N frames
frame_count = 0
max_frames = {max_frames}
original_event_get = pygame.event.get

def patched_event_get(*args, **kwargs):
    global frame_count
    frame_count += 1
    if frame_count >= max_frames:
        # Save screenshot and quit
        pygame.image.save(pygame.display.get_surface(), "{output_path}")
        print("Screenshot saved: {output_path}")
        pygame.quit()
        sys.exit(0)
    events = original_event_get(*args, **kwargs)
    # Filter out QUIT events so game keeps running
    return [e for e in events if e.type != pygame.QUIT]

pygame.event.get = patched_event_get

# Run the game
os.chdir("{game_dir}")
exec(open("{game_file}").read())
'''

for game_path, output_name, max_frames in GAMES:
    full_game_path = os.path.join(COURSE_DIR, game_path)
    output_path = os.path.join(IMAGES_DIR, output_name)
    game_dir = os.path.dirname(full_game_path)
    game_file = os.path.basename(full_game_path)

    if not os.path.exists(full_game_path):
        print(f"SKIP (not found): {game_path}")
        continue

    wrapper_code = WRAPPER.format(
        max_frames=max_frames,
        output_path=output_path.replace("\\", "\\\\"),
        game_dir=game_dir.replace("\\", "\\\\"),
        game_file=game_file,
    )

    print(f"Running: {game_path} → {output_name}")
    try:
        result = subprocess.run(
            [sys.executable, "-c", wrapper_code],
            timeout=15,
            capture_output=True,
            text=True,
            env={**os.environ, "SDL_VIDEODRIVER": "cocoa"},
        )
        if result.returncode == 0:
            print(f"  ✓ {output_name}")
        else:
            print(f"  ✗ Exit code {result.returncode}")
            if result.stderr:
                print(f"    {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout")
    except Exception as e:
        print(f"  ✗ Error: {e}")
