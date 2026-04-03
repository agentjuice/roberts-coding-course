import re
import os

COURSE = os.path.dirname(os.path.abspath(__file__))

LESSONS = {
    "07-connect4-v3-pygame": ("connect4_pygame.png", "Here's what your Connect 4 game will look like when you're done with this lesson!"),
    "08-connect4-v4-animation": ("connect4_anim.png", "Connect 4 with chip-dropping animation"),
    "09-connect4-v5-pygame-functions": ("connect4_functions.png", "Same game, but with clean organized code"),
    "10-snake-v1": ("snake.png", "The Snake game you're about to build!"),
    "11-snake-v2-classes": ("snake_classes.png", "Same Snake game, rebuilt with classes"),
    "12-dungeon-v1-hero": ("dungeon_v1.png", "Your first dungeon — you're the blue square!"),
    "13-dungeon-v2-enemies": ("dungeon_v2.png", "Now with enemies roaming the dungeon!"),
    "14-dungeon-v3-combat": ("dungeon_v3.png", "Combat system in action!"),
    "15-dungeon-v4-loot": ("dungeon_v4.png", "Loot drops and an inventory bar!"),
    "16-dungeon-v5-rooms": ("dungeon_v5.png", "Multiple rooms connected with a minimap!"),
    "17-dungeon-v6-boss": ("dungeon_v6.png", "The boss fight — can you beat it?"),
}

for lesson, (img, caption) in LESSONS.items():
    filepath = os.path.join(COURSE, "lessons", lesson, "lesson.md")
    if not os.path.exists(filepath):
        print(f"SKIP: {lesson}")
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Skip if image already added
    if img in content:
        print(f"SKIP (already has image): {lesson}")
        continue
    
    # Insert after the **Goal:** line
    pattern = r'(\*\*Goal:\*\*[^\n]*\n)'
    img_block = f'\\1\n![{caption}](../../images/{img})\n\n'
    new_content = re.sub(pattern, img_block, content, count=1)
    
    if new_content == content:
        # Try inserting after first heading instead
        pattern = r'(# [^\n]+\n)'
        img_block = f'\\1\n![{caption}](../../images/{img})\n\n'
        new_content = re.sub(pattern, img_block, content, count=1)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Added {img} to {lesson}")

print("\nDone! Now copy lessons to docs/lessons")
