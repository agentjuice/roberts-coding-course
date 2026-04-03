questions = [
    {
        "question": "What planet is closest to the Sun?",
        "choices": ["A) Venus", "B) Mercury", "C) Mars", "D) Earth"],
        "answer": "B"
    },
    {
        "question": "What language is this course teaching?",
        "choices": ["A) JavaScript", "B) Scratch", "C) Python", "D) Java"],
        "answer": "C"
    },
    {
        "question": "What does the print() function do?",
        "choices": ["A) Prints on paper", "B) Shows text on screen", "C) Deletes text", "D) Saves a file"],
        "answer": "B"
    },
    {
        "question": "What symbol do you use for 'equals' in a comparison?",
        "choices": ["A) =", "B) =>", "C) ==", "D) !="],
        "answer": "C"
    },
    {
        "question": "In Python, what index is the FIRST item in a list?",
        "choices": ["A) 1", "B) 0", "C) -1", "D) 2"],
        "answer": "B"
    },
    {
        "question": "What does 'elif' stand for?",
        "choices": ["A) else figure", "B) elephant if", "C) else if", "D) element if"],
        "answer": "C"
    },
    {
        "question": "Which of these is a BOOLEAN value?",
        "choices": ["A) \"hello\"", "B) 42", "C) 3.14", "D) True"],
        "answer": "D"
    },
]

print("=== Robert's Quiz Game ===")
print(f"Answer {len(questions)} questions. Let's see how you do!\n")

score = 0

for i in range(len(questions)):
    q = questions[i]
    print(f"Question {i + 1} of {len(questions)}: {q['question']}")

    for choice in q["choices"]:
        print(f"  {choice}")

    player_answer = input("Your answer (A/B/C/D): ").upper()

    if player_answer == q["answer"]:
        print("Correct!\n")
        score = score + 1
    else:
        # Find the full text of the correct answer
        correct_text = ""
        for choice in q["choices"]:
            if choice.startswith(q["answer"]):
                correct_text = choice
        print(f"Wrong! The answer was {correct_text}.\n")

print("=== Results ===")
print(f"You got {score} out of {len(questions)} right!")

percentage = int(score / len(questions) * 100)

if percentage == 100:
    print("PERFECT SCORE! You're a genius!")
elif percentage >= 80:
    print("Great job!")
elif percentage >= 60:
    print("Not bad! Study up and try again.")
else:
    print("Keep learning — you'll get there!")
