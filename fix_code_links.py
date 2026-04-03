import os, glob, re

for lesson_dir in sorted(glob.glob('lessons/*')):
    lesson_md = os.path.join(lesson_dir, 'lesson.md')
    if not os.path.exists(lesson_md):
        continue
    
    # Find .py files in the lesson dir
    py_files = [f for f in os.listdir(lesson_dir) if f.endswith('.py')]
    if not py_files:
        continue
    
    with open(lesson_md) as f:
        content = f.read()
    
    changed = False
    for py_file in py_files:
        # Replace references like "in connect4.py right next to this lesson" or similar
        # with a proper link
        old_phrases = [
            f"in `{py_file}` right next to this lesson",
            f"in {py_file} right next to this lesson",
            f"the complete file in {py_file}",
            f"the complete file in `{py_file}`",
        ]
        for phrase in old_phrases:
            if phrase in content:
                content = content.replace(phrase, f"in [`{py_file}`]({py_file})")
                changed = True
    
    if changed:
        with open(lesson_md, 'w') as f:
            f.write(content)
        print(f"Fixed links: {lesson_dir}")

print("Done")
