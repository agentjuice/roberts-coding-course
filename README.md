# Robert's Coding Course

Welcome to your Python coding course! By the end, you'll have built four real projects — from simple terminal games all the way to a dungeon crawler with graphics and sound.

## What You Need

### Python 3.10 or newer

Check if you already have it:

```bash
python --version
```

If you see something like `Python 3.10.x` or higher, you're good. If not, download it from [python.org](https://www.python.org/downloads/).

### Install libraries

We'll need two extra libraries later in the course. Let's install them now so we're ready:

```bash
pip install pygame
pip install numpy
```

### Running lessons

Each lesson lives in its own folder. To run a lesson's project:

```bash
cd lessons/01-the-basics
python guessing_game.py
```

## Course Overview

### Warm-up (Lessons 1–6)
Get comfortable with Python basics by building small terminal programs.

| Lesson | Topic | Project |
|--------|-------|---------|
| 01 | The Basics | Number guessing game |
| 02 | Conditions | Decision-making programs |
| 03 | Loops | Repeating actions |
| 04 | Lists | Working with collections |
| 05 | Functions & Dictionaries | Contact book |
| 06 | Files & Error Handling | Save/load high scores |

### Connect 4 (Lessons 7–11)
Build a full Connect 4 game, step by step.

| Lesson | Topic | Project |
|--------|-------|---------|
| 07 | 2D Lists & Game Boards | Draw the board |
| 08 | Game Logic | Drop pieces & check wins |
| 09 | Intro to Pygame | Connect 4 with graphics |
| 10 | Polish & AI Opponent | Simple computer player |
| 11 | Growing the Snake | Full snake mechanics |

### Snake (Lessons 10–13)
The classic Snake game, from scratch.

| Lesson | Topic | Project |
|--------|-------|---------|
| 10 | Game Loop & Movement | Moving square |
| 11 | Collision Detection | Snake eats food |
| 12 | Growing the Snake | Full snake mechanics |
| 13 | Score & Speed | Difficulty scaling |

### Dungeon Crawler (Lessons 14–22)
A top-down dungeon crawler — the big finale.

| Lesson | Topic | Project |
|--------|-------|---------|
| 14 | Tile Maps | Drawing a dungeon |
| 15 | Player Movement & Cameras | Scrolling world |
| 16 | Sprites & Animation | Animated characters |
| 17 | Sound & Music | Audio effects |
| 18 | Enemies & Combat | Fighting system |
| 19 | Items & Inventory | Loot and upgrades |
| 20 | Procedural Generation | Random dungeons |
| 21 | Second Level & Polish | Complete game |
| 22 | Co-op Mode | Two-player mode |

## Folder Structure

```
roberts-coding-course/
├── README.md          ← you are here
├── assets/            ← game art & sounds (lessons 18+)
├── lessons/
│   ├── 01-the-basics/
│   ├── 02-conditions/
│   ├── 03-loops/
│   ├── 04-lists/
│   └── ...
└── reference/         ← cheat sheets & extras
```

Let's get started! Open up `lessons/01-the-basics/lesson.md` and dive in.
