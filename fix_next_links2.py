import os, re, glob

LINKS = {
    "01-hello-world": ("02-variables", "Variables"),
    "02-variables": ("03-types", "Types"),
    "03-types": ("04-fstrings", "f-strings"),
    "04-fstrings": ("05-input", "Input"),
    "05-input": ("06-if-else", "If / Else"),
    "06-if-else": ("07-comparisons", "Comparisons"),
    "07-comparisons": ("08-while-loops", "While Loops"),
    "08-while-loops": ("09-for-loops", "For Loops"),
    "09-for-loops": ("10-lists-basics", "Lists: Basics"),
    "10-lists-basics": ("11-lists-operations", "Lists: Operations"),
    "11-lists-operations": ("12-build-guessing-game", "Build: Guessing Game"),
    "12-build-guessing-game": ("13-connect4-v1", "Your First Game"),
    "13-connect4-v1": ("14-connect4-v2-functions", "Cleaning Up"),
    "14-connect4-v2-functions": ("15-the-game-loop", "The Game Loop"),
    "15-the-game-loop": ("16-connect4-v3-pygame", "Adding Graphics"),
    "16-connect4-v3-pygame": ("17-connect4-v4-animation", "Dropping Chips"),
    "17-connect4-v4-animation": ("18-connect4-v5-pygame-functions", "The Final Version"),
    "18-connect4-v5-pygame-functions": ("19-snake-v1", "Snake Game"),
    "19-snake-v1": ("20-snake-v2-classes", "Classes"),
    "20-snake-v2-classes": ("21-dungeon-v1-hero", "The Hero"),
    "21-dungeon-v1-hero": ("22-dungeon-v2-enemies", "Enemies"),
    "22-dungeon-v2-enemies": ("23-dungeon-v3-combat", "Combat"),
    "23-dungeon-v3-combat": ("24-dungeon-v4-loot", "Loot & Items"),
    "24-dungeon-v4-loot": ("25-dungeon-v5-rooms", "Multiple Rooms"),
    "25-dungeon-v5-rooms": ("26-dungeon-v6-boss", "The Boss"),
    "26-dungeon-v6-boss": ("27-dungeon-v7-sprites", "Sprites & Art"),
    "27-dungeon-v7-sprites": ("28-dungeon-v8-sound", "Sound & Music"),
    "28-dungeon-v8-sound": ("29-dungeon-v9-procgen", "Procedural Generation"),
    "29-dungeon-v9-procgen": ("30-dungeon-v10-polish", "Polish & Second Level"),
    "30-dungeon-v10-polish": ("31-dungeon-v11-coop", "Co-op Mode"),
    "31-dungeon-v11-coop": ("32-isometric-basics", "Isometric Basics"),
    "32-isometric-basics": ("33-isometric-dungeon", "Isometric Dungeon"),
    "33-isometric-dungeon": ("34-depth-sorting", "Depth Sorting"),
    "34-depth-sorting": ("35-isometric-game", "The Full Game"),
}

for current, (next_dir, next_name) in LINKS.items():
    filepath = f"lessons/{current}/lesson.md"
    if not os.path.exists(filepath):
        continue
    
    with open(filepath) as f:
        content = f.read()
    
    # Replace everything after "## What's Next" with consistent format
    pattern = r"(## What's Next\??)\n.*$"
    replacement = f"\\1\n\n👉 [Next: {next_name}](../{next_dir}/lesson.md)"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {current} -> {next_name}")

print("Done!")
