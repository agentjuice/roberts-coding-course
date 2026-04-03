import os, re

LINKS = [
    ("01-hello-world", "02-variables", "Variables"),
    ("02-variables", "03-math", "Math & Numbers"),
    ("03-math", "04-types", "Types"),
    ("04-types", "05-fstrings", "f-strings"),
    ("05-fstrings", "06-input", "Input"),
    ("06-input", "07-if-else", "If / Else"),
    ("07-if-else", "08-comparisons", "Comparisons"),
    ("08-comparisons", "09-while-loops", "While Loops"),
    ("09-while-loops", "10-for-loops", "For Loops"),
    ("10-for-loops", "11-lists", "Lists"),
    ("11-lists", "12-build-guessing-game", "Guessing Game"),
    ("12-build-guessing-game", "13-connect4-v1", "Your First Game"),
    ("13-connect4-v1", "14-connect4-v2-functions", "Cleaning Up"),
    ("14-connect4-v2-functions", "15-the-game-loop", "The Game Loop"),
    ("15-the-game-loop", "16-connect4-v3-pygame", "Adding Graphics"),
    ("16-connect4-v3-pygame", "17-connect4-v4-animation", "Dropping Chips"),
    ("17-connect4-v4-animation", "18-connect4-v5-pygame-functions", "The Final Version"),
    ("18-connect4-v5-pygame-functions", "19-snake-v1", "Snake Game"),
    ("19-snake-v1", "20-snake-v2-classes", "Classes"),
    ("20-snake-v2-classes", "21-dungeon-v1-hero", "The Hero"),
    ("21-dungeon-v1-hero", "22-dungeon-v2-enemies", "Enemies"),
    ("22-dungeon-v2-enemies", "23-dungeon-v3-combat", "Combat"),
    ("23-dungeon-v3-combat", "24-dungeon-v4-loot", "Loot & Items"),
    ("24-dungeon-v4-loot", "25-dungeon-v5-rooms", "Multiple Rooms"),
    ("25-dungeon-v5-rooms", "26-dungeon-v6-boss", "The Boss"),
    ("26-dungeon-v6-boss", "27-dungeon-v7-sprites", "Sprites & Art"),
    ("27-dungeon-v7-sprites", "28-dungeon-v8-sound", "Sound & Music"),
    ("28-dungeon-v8-sound", "29-dungeon-v9-procgen", "Procedural Generation"),
    ("29-dungeon-v9-procgen", "30-dungeon-v10-polish", "Polish & Second Level"),
    ("30-dungeon-v10-polish", "31-dungeon-v11-coop", "Co-op Mode"),
    ("31-dungeon-v11-coop", "32-isometric-basics", "Isometric Basics"),
    ("32-isometric-basics", "33-isometric-dungeon", "Isometric Dungeon"),
    ("33-isometric-dungeon", "34-depth-sorting", "Depth Sorting"),
    ("34-depth-sorting", "35-isometric-game", "The Full Game"),
]

for current, next_dir, next_name in LINKS:
    filepath = f"lessons/{current}/lesson.md"
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath}")
        continue
    with open(filepath) as f:
        content = f.read()
    pattern = r"(## What's Next\??)\n.*$"
    replacement = f"\\1\n\n👉 [Next: {next_name}](../{next_dir}/lesson.md)"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {current} -> {next_name}")

print("Done!")
