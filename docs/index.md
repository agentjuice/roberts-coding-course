# Robert's Coding Course

!!! success "🎯 Mission"
    Learn Python. Build games. Go from zero to building your own dungeon crawler.

---

## Hey Robert!

Welcome to your coding course. By the end of this, you're going to build a dungeon crawler game -- like Minecraft Dungeons, but one you made yourself. Pretty cool, right?

But we're not starting there. We're starting small, building up, and every single lesson ends with something you can actually play. Here's the plan:

### The Journey

| Project | What You're Building |
|---------|----------------------|
| **Getting Started** | Your first programs — printing, variables, loops, lists, and a guessing game |
| **Connect 4** | A full Connect 4 game — terminal, then graphics, then animation |
| **Snake** | The classic Snake game, then rebuilt with classes |
| **Dungeon Crawler** | A Minecraft Dungeons-style game with enemies, combat, loot, bosses, and co-op |

### How This Course Works

- **You build real games, not boring examples.** Every lesson makes something you can actually play.
- **It's okay to be messy at first.** You'll write code that works, then later learn cleaner ways to do it. That's how real programmers learn too.
- **Nothing is hidden.** You'll see how everything works under the hood.

---

## Setting Up Your Computer

Before you can write code, we need to install a couple of things. This only takes about 10 minutes, and you only have to do it once.

### Step 1: Install Python

Python is the programming language you're going to learn. Think of it like the language your computer speaks -- you'll write instructions in Python, and your computer will follow them.

Here's how to install it:

1. Open your web browser (Safari, Chrome, whatever you use)
2. Go to [python.org/downloads](https://www.python.org/downloads/)
3. You'll see a big yellow button that says something like **"Download Python 3.x.x"** -- click it
4. A `.pkg` file will download. Find it in your Downloads folder and double-click it
5. An installer window will pop up. Just click **Continue** through each step, then click **Install**
6. It might ask for your password -- that's your Mac's password (ask your dad if you need help)
7. When it says "The installation was successful," click **Close**

Nice! Python is installed.

### Step 2: Make Sure Python Works

Let's check that it actually installed. We're going to open something called the **Terminal**. Think of Terminal like a text message conversation with your computer -- you type a command, hit Enter, and your computer responds.

1. Press **Cmd + Space** on your keyboard (that opens Spotlight search)
2. Type **Terminal**
3. Hit **Enter**

A window will pop up with a blinking cursor. This is the Terminal. Type this and hit Enter:

```bash
python3 --version
```

You should see something like `Python 3.12.0` (the exact number doesn't matter, as long as it starts with 3). If you see that, Python is working!

If you get an error, ask your dad to help troubleshoot -- sometimes Macs need an extra step.

### Step 3: Install VS Code

VS Code is where you'll actually write your code. Think of it like Google Docs, but for code instead of essays.

1. Go to [code.visualstudio.com](https://code.visualstudio.com)
2. Click the big blue **"Download for Mac"** button
3. A `.zip` file will download. Find it in your Downloads folder and double-click it to unzip
4. You'll see an app called **Visual Studio Code** -- drag it into your **Applications** folder
5. Open it from Applications (or press Cmd + Space, type "Visual Studio Code", hit Enter)

When VS Code opens for the first time, it might show you some welcome tabs. You can close those.

Now let's add one helpful thing to VS Code:

1. Look at the left sidebar -- there's an icon that looks like four squares (one is floating away). Click it. That's the **Extensions** panel.
2. In the search box at the top, type **Python**
3. The first result should be "Python" by Microsoft. Click the blue **Install** button.

That's it! VS Code is ready.

### Step 4: Install Some Extra Tools

Later in the course, you'll need a couple of extra tools for making games with graphics. Let's install them now so you don't have to worry about it later.

Open Terminal again (Cmd + Space, type Terminal, hit Enter) and type this command, then hit Enter:

```bash
pip3 install pygame numpy
```

You'll see a bunch of text scroll by -- that's normal. It's downloading and installing the tools. Think of `pip3` like an app store for Python -- it lets you install extra tools that other people have made.

If you see any red error text, ask your dad to help with this.

### Step 5: Create Your Coding Folder

You need a place to save all your code. Let's make a folder on your Desktop. In Terminal, type this and hit Enter:

```bash
mkdir ~/Desktop/coding-course
```

That just created a folder called `coding-course` on your Desktop. You should be able to see it there! Every file you make during this course will go in that folder.

---

## How to Use This Course

Here's the deal:

1. **Read each lesson** on this site, step by step
2. **Type the code yourself** -- seriously, don't copy and paste! I know it's tempting, but typing it yourself helps your brain learn it way faster. It's like how you remember a phone number better if you dial it yourself instead of tapping a contact.
3. **Run your code** after every step to see what happens. Don't wait until the end!
4. **Try the experiments** -- change things, break things on purpose, see what happens. You won't hurt anything, I promise.
5. **Try the challenge** at the end before moving on

Go at your own speed. Some lessons might take 20 minutes, some might take a couple of days. There's no timer, no grade, no rush. If you get stuck, take a break and come back to it. Sometimes your brain needs time to chew on things.

---

## Ready?

Let's go write your first line of code.

[Start Lesson 1 -- Hello World](lessons/01-hello-world/lesson.md)
