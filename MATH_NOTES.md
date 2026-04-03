# Math Integration Notes

## Where math naturally fits in existing lessons:

### Coordinates (Lesson 15 - Game Loop / Lesson 16 - Pygame)
- The coordinate system: (0,0) is top-left, y goes DOWN
- Why y goes down (screens draw top to bottom)
- Pixels as coordinates on a grid
- Moving right = x increases, moving down = y increases

### Distance Formula (Lesson 22 - Enemies)
- Skeleton chases player: how do you know which direction to move?
- Distance = sqrt((x2-x1)² + (y2-y1)²) — that's Pythagoras!
- "If the skeleton is at (3,4) and you're at (6,8), how far apart are you?"
- Connect to Pythagorean theorem: a² + b² = c²
- Real use: deciding if an enemy is "close enough" to attack

### Grid Math (Lesson 13 - Your First Game / Connect 4)
- 2D arrays: row and column = (y, x)
- Converting between grid position and screen position: x * tile_size
- Index math: checking neighbors (x+1, x-1, y+1, y-1)

### Collision Detection (Lesson 18 - Snake / Lesson 22 - Enemies)
- Bounding box: is point inside rectangle?
- if x >= left and x <= right and y >= top and y <= bottom
- Circle collision: distance between centers < sum of radii (Pythagoras again!)

### Angles & Direction (Lesson 23 - Combat)
- Facing direction as a concept (up/down/left/right)
- For advanced: atan2(dy, dx) gives you the angle to something
- Trigonometry preview: sin/cos for circular motion

### Velocity & Speed (Lesson 15 - Game Loop)
- position = position + speed (each frame)
- Speed × time = distance (the bouncing ball)
- Frame rate: why 60fps means 60 updates per second

### Randomness & Probability (Lesson 24 - Loot)
- random.randint() — uniform distribution
- Drop rates: "30% chance to drop a health potion"
- if random.random() < 0.3: drop_item()

### Isometric Math (Lessons 32-35)
- Coordinate transformation: 2D → isometric
- screen_x = (grid_x - grid_y) × (tile_width / 2)  
- screen_y = (grid_x + grid_y) × (tile_height / 2)
- This is matrix multiplication (don't say that, just show it)
- Reverse: screen → grid (for mouse clicks)

## How to integrate:
- Don't make separate "math lessons" — weave into game lessons
- Use "🧮 Math Moment" admonition boxes
- Keep it visual: "here's the triangle, here's why it works"
- Always show the game use case FIRST, then the math behind it
- "You just used the Pythagorean theorem and didn't even know it!"
