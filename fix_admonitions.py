import re, os, glob

FIXES = {
    '!!! tip\n': '!!! tip "💡 Pro Tip"\n',
    '!!! tip "Pro Tip"\n': '!!! tip "💡 Pro Tip"\n',
    '!!! warning\n': '!!! warning "⚠️ Watch Out"\n',
    '!!! warning "Watch Out"\n': '!!! warning "⚠️ Watch Out"\n',
    '!!! info\n': '!!! info "🎮 Fun Fact"\n',
    '!!! info "Did You Know?"\n': '!!! info "🎮 Did You Know?"\n',
    '!!! example\n': '!!! example "🧪 Experiment"\n',
    '!!! example "Experiments"\n': '!!! example "🧪 Experiments"\n',
    '!!! abstract\n': '!!! abstract "🏆 Challenge"\n',
}

for f in sorted(glob.glob('lessons/*/lesson.md')):
    with open(f) as fh:
        content = fh.read()
    changed = False
    for old, new in FIXES.items():
        if old in content:
            content = content.replace(old, new)
            changed = True
    if changed:
        with open(f, 'w') as fh:
            fh.write(content)
        print(f'Fixed: {f}')

print('Done')
