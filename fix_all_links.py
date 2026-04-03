import os, re, glob

LINKS = [
    ("01-hello-world", "02-variables", "Variables"),
    ("02-variables", "03-types", "Types"),
    ("03-types", "04-fstrings", "f-strings"),
    ("04-fstrings", "05-input", "Input"),
    ("05-input", "06-if-else", "If / Else"),
    ("06-if-else", "07-comparisons", "Comparisons"),
    ("07-comparisons", "08-while-loops", "While Loops"),
    ("08-while-loops", "09-for-loops", "For Loops"),
    ("09-for-loops", "10-lists", "Lists"),
    ("10-lists", "11-build-guessing-game", "Build: Guessing Game"),
    ("11-build-guessing-game", "12-connect4-v1", "Your First Game"),
    ("12-connect4-v1", "13-connect4-v2-functions", "Cleaning Up"),
    ("13-connect4-v2-functions", "14-the-game-loop", "The Game Loop"),
    ("14-the-game-loop", "15-connect4-v3-pygame", "Adding Graphics"),
    ("15-connect4-v3-pygame", "16-connect4-v4-animation", "Dropping Chips"),
    ("16-connect4-v4-animation", "17-connect4-v5-pygame-functions", "The Final Version"),
    ("17-connect4-v5-pygame-functions", "18-snake-v1", "Snake Game"),
    ("18-snake-v1", "19-snake-v2-classes", "Classes"),
    ("19-snake-v2-classes", "20-dungeon-v1-hero", "The Hero"),
    ("20-dungeon-v1-hero", "21-dungeon-v2-enemies", "Enemies"),
    ("21-dungeon-v2-enemies", "22-dungeon-v3-combat", "Combat"),
    ("22-dungeon-v3-combat", "23-dungeon-v4-loot", "Loot & Items"),
    ("23-dungeon-v4-loot", "24-dungeon-v5-rooms", "Multiple Rooms"),
    ("24-dungeon-v5-rooms", "25-dungeon-v6-boss", "The Boss"),
    ("25-dungeon-v6-boss", "26-dungeon-v7-sprites", "Sprites & Art"),
    ("26-dungeon-v7-sprites", "27-dungeon-v8-sound", "Sound & Music"),
    ("27-dungeon-v8-sound", "28-dungeon-v9-procgen", "Procedural Generation"),
    ("28-dungeon-v9-procgen", "29-dungeon-v10-polish", "Polish & Second Level"),
    ("29-dungeon-v10-polish", "30-dungeon-v11-coop", "Co-op Mode"),
    ("30-dungeon-v11-coop", "31-isometric-basics", "Isometric Basics"),
    ("31-isometric-basics", "32-isometric-dungeon", "Isometric Dungeon"),
    ("32-isometric-dungeon", "33-depth-sorting", "Depth Sorting"),
    ("33-depth-sorting", "34-isometric-game", "The Full Game"),
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
