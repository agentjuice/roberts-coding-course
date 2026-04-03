import os, re, glob

LESSONS = [
    ("01-hello-world", "02-variables", "#2 — Variables"),
    ("02-variables", "03-types", "#3 — Types"),
    ("03-types", "04-fstrings", "#4 — f-strings"),
    ("04-fstrings", "05-input", "#5 — Input"),
    ("05-input", "06-if-else", "#6 — If / Else"),
    ("06-if-else", "07-comparisons", "#7 — Comparisons"),
    ("07-comparisons", "08-while-loops", "#8 — While Loops"),
    ("08-while-loops", "09-for-loops", "#9 — For Loops"),
    ("09-for-loops", "10-lists-basics", "#10 — Lists: Basics"),
    ("10-lists-basics", "11-lists-operations", "#11 — Lists: Operations"),
    ("11-lists-operations", "12-build-guessing-game", "#12 — Build: Guessing Game"),
    ("12-build-guessing-game", "13-connect4-v1", "#13 — Connect 4: Terminal Version"),
    ("13-connect4-v1", "14-connect4-v2-functions", "#14 — Connect 4: Functions"),
    ("14-connect4-v2-functions", "15-connect4-v3-pygame", "#15 — Connect 4: Pygame"),
    ("15-connect4-v3-pygame", "16-connect4-v4-animation", "#16 — Connect 4: Animation"),
    ("16-connect4-v4-animation", "17-connect4-v5-pygame-functions", "#17 — Connect 4: Pygame + Functions"),
    ("17-connect4-v5-pygame-functions", "18-snake-v1", "#18 — Snake Game"),
    ("18-snake-v1", "19-snake-v2-classes", "#19 — Classes & OOP"),
    ("19-snake-v2-classes", "20-dungeon-v1-hero", "#20 — Dungeon: The Hero"),
    ("20-dungeon-v1-hero", "21-dungeon-v2-enemies", "#21 — Dungeon: Enemies"),
    ("21-dungeon-v2-enemies", "22-dungeon-v3-combat", "#22 — Dungeon: Combat"),
    ("22-dungeon-v3-combat", "23-dungeon-v4-loot", "#23 — Dungeon: Loot & Items"),
    ("23-dungeon-v4-loot", "24-dungeon-v5-rooms", "#24 — Dungeon: Multiple Rooms"),
    ("24-dungeon-v5-rooms", "25-dungeon-v6-boss", "#25 — Dungeon: The Boss"),
    ("25-dungeon-v6-boss", "26-dungeon-v7-sprites", "#26 — Dungeon: Sprites & Art"),
    ("26-dungeon-v7-sprites", "27-dungeon-v8-sound", "#27 — Dungeon: Sound & Music"),
    ("27-dungeon-v8-sound", "28-dungeon-v9-procgen", "#28 — Dungeon: Procedural Generation"),
    ("28-dungeon-v9-procgen", "29-dungeon-v10-polish", "#29 — Dungeon: Polish & Second Level"),
    ("29-dungeon-v10-polish", "30-dungeon-v11-coop", "#30 — Dungeon: Co-op Mode"),
]

for current, next_dir, next_title in LESSONS:
    filepath = f"lessons/{current}/lesson.md"
    if not os.path.exists(filepath):
        print(f"SKIP: {filepath}")
        continue
    
    with open(filepath) as f:
        content = f.read()
    
    # Find the What's Next section and replace everything after it
    pattern = r"(## What's Next\??\n).*"
    link = f"../{ next_dir}/lesson.md"
    replacement = f"\\1\n👉 [Go to {next_title}]({link})"
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed: {current} -> {next_title}")

# Last lesson gets a special ending
last = "lessons/30-dungeon-v11-coop/lesson.md"
if os.path.exists(last):
    with open(last) as f:
        content = f.read()
    pattern = r"(## What's Next\??\n).*"
    replacement = "\\1\n🎉 **You finished the entire course!** You built a dungeon crawler from scratch. That's incredible. Now go build something of your own!"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(last, 'w') as f:
        f.write(new_content)
    print("Fixed: 30 (final lesson)")

print("Done!")
