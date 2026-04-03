import re

def move_admonition(filepath, admonition_start, insert_after):
    """Remove admonition from bottom, insert after a specific line."""
    with open(filepath) as f:
        lines = f.readlines()
    
    # Find and extract the admonition block
    adm_lines = []
    adm_start = -1
    for i, line in enumerate(lines):
        if admonition_start in line:
            adm_start = i
        if adm_start >= 0:
            adm_lines.append(line)
            # Admonition ends when we hit a non-indented, non-empty line after the title
            if i > adm_start and not line.startswith('    ') and not line.startswith('!!!') and line.strip() == '':
                break
    
    if adm_start == -1:
        print(f"  SKIP: admonition not found")
        return
    
    # Remove admonition from original position
    for line in adm_lines:
        lines.remove(line)
    
    # Find insert point
    insert_idx = -1
    for i, line in enumerate(lines):
        if insert_after in line:
            insert_idx = i + 1
    
    if insert_idx == -1:
        print(f"  SKIP: insert point not found")
        return
    
    # Skip to end of current paragraph/block
    while insert_idx < len(lines) and lines[insert_idx].strip() != '':
        insert_idx += 1
    
    # Insert admonition
    lines.insert(insert_idx, '\n')
    for j, adm_line in enumerate(adm_lines):
        lines.insert(insert_idx + 1 + j, adm_line)
    
    with open(filepath, 'w') as f:
        f.writelines(lines)
    print(f"  Moved!")

# 1. Game Loop - coordinates near "bouncing ball" or coordinate system mention
print("Game Loop (15):")
move_admonition('lessons/15-the-game-loop/lesson.md', 'Math Moment: Coordinates', 'bouncing ball')

# 2. Connect 4 (13) - 2D arrays near the numpy grid explanation  
print("Connect 4 (13):")
move_admonition('lessons/13-connect4-v1/lesson.md', 'Math Moment: 2D Arrays', 'smaller, 2D version')

# 3. Adding Graphics (16) - velocity near coordinate system explanation
print("Adding Graphics (16):")
move_admonition('lessons/16-connect4-v3-pygame/lesson.md', 'Math Moment: Position + Speed', 'y-axis goes DOWN')

# 4. Snake (19) - collision near the collision detection section
print("Snake (19):")
move_admonition('lessons/19-snake-v1/lesson.md', 'Math Moment: Collision', 'Self collision')

# 5. Enemies (22) - pythagorean near skeleton chase logic
print("Enemies (22):")
move_admonition('lessons/22-dungeon-v2-enemies/lesson.md', 'Math Moment: The Pythagorean', 'Skeletons hunt you down')

# 6. Loot (24) - probability near the drop rate explanation
print("Loot (24):")
move_admonition('lessons/24-dungeon-v4-loot/lesson.md', 'Math Moment: Probability', "40% chance")

# 7. Isometric (32) - transforms near the formula
print("Isometric (32):")
move_admonition('lessons/32-isometric-basics/lesson.md', 'Math Moment: Coordinate', 'diamond')
