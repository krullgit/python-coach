# --------------------------------------------------------
# Pyhton bootcamp
# Licensed under The GPL2 License [see LICENSE for details]
# Written by Matthes Krull
# ------------------------------------------------------

import time
import random
import matplotlib.pyplot as plt
import os 

# parameter
PATH_ART_1 = "docs/art1.txt"
PATH_ART_2 = "docs/art2.txt"
DURATION = 300

def open_text_file(path):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    return lines

def print_waiting_animation():
    animation = "|/-\\"
    idx = 0
    time_start = time.time()
    while (time.time() - time_start) < 1:
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)
    print("", end="\n")

def print_as_typewriter(text, speed):
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(random.random()*speed)
    
def print_ascii_art_from_file(path):
    f = open (path,'r')
    for line in f:
        print(line, end="")
        time.sleep(0.08)
    print("\n\n")



# welcome the user
msg_welcome = "Welcome to the python drill camp."
msg_instructions = "If a variable, class, or function is required for a task, you have to create them on your own, that's part of the challenge."
print_ascii_art_from_file(PATH_ART_1)
print_waiting_animation()
print_as_typewriter(msg_welcome, 0.1)
print("", end="\n\n")
print_waiting_animation()
# print_as_typewriter(msg_instructions, 0.05)
# print("", end="\n\n")

# ask for the topic
tmp_topic_invalid = True 
questions_topic = ""
while tmp_topic_invalid:
    try:
        print("Choose the topic of your questions. The following question files are available:")
        filesnames = os.listdir(os.getcwd())
        tmp_counter = 0
        tmp_filesnames = []
        for filename in filesnames:
            if not filename.startswith("python_questions_"): continue
            tmp_filesnames.append(filename)
            print(f"[{tmp_counter}]: {filename}")
            tmp_counter += 1
        topic_number = input("Choose your topic (number):")
        topic_number = int(topic_number)
        questions_topic = tmp_filesnames[topic_number]
        tmp_topic_invalid = False
    except ValueError:
        print("Please enter valid number. You failed the python training already haha")
    except IndexError:
        print("Please enter valid number. You failed the python training already haha")

# open the file with the questions and parse them
question_type = []
question_difficulty = []
questions = []
tmp_question_type = ""
questions_raw = open_text_file(questions_topic)
for line in questions_raw:
    if line == '\n': # filter out the new lines
        continue
    elif line.startswith("#"): # spot the question type
        tmp_question_type = line[2:] # save the type, but crop the "# "
        continue
    elif line.startswith("-1 "): # this question is not in the test
        continue
    else: # these are the questions
        question_type.append(tmp_question_type) # append the same question type as before
        question_difficulty.append(int(line[0]))
        questions.append(line[2:].strip())
assert(len(questions) == len(question_type)), "question types and questions must have the same length"

# ask for the difficulty
tmp_difficulty_invalid = True
difficulty = 0
while tmp_difficulty_invalid:
    try:
        difficulty = input("Choose difficulty from 1 to 5 and press enter:")
        difficulty = int(difficulty) 
        tmp_difficulty_invalid = False
    except ValueError:
        print("Please enter valid number. You failed the python training already haha")

print_ascii_art_from_file(PATH_ART_2)
input(f"Press Enter to start. You have {DURATION} seconds.")
print()

file_question_log = open("logs/questions_log.txt", "w")

question_counter = 0

time_start = time.time()
question_counter = 0
questions_done = []
while (time.time() - time_start) < DURATION:
    
    random_choise = random.choice(list(range(len(questions))))
    
    if question_difficulty[random_choise] > difficulty:
        continue
    question_topic = "("+str(question_counter)+") "+"["+str(question_difficulty[random_choise])+"] "+"TOPIC: " + question_type[random_choise].title()
    print(question_topic, end="")
    
    question_current = questions[random_choise][0].upper() + questions[random_choise][1:]  + "."
    print(question_current,end="")
    
    file_question_log.write(question_topic)
    file_question_log.write(question_current)
    file_question_log.write("\n")
    file_question_log.write("\n")
    file_question_log.flush()
    
    print("\n")
    input("press enter if done ...")
    print("\n")
    
    question_counter += 1
    questions_done.append(random_choise)
    

print(f"Your time is up. You did {question_counter} questions in {round(time.time() - time_start,2)} seconds.")

# calculate score according to difficulty the time needed
score = 0
for idx in questions_done:
    difficulty = int(question_difficulty[idx])
    score += difficulty + (difficulty ** 2) * 0.3
score = round(score/(time.time() - time_start),2)
print(f"Your score is {score}")
file_question_log.close()

# get the scores log filename according to the topic
path_log_scores = questions_topic.replace("python_questions_","")
path_log_scores = "logs/scores_log_" + path_log_scores

# just save the scores
file_question_scores = open(path_log_scores, "a")
file_question_scores.write(str(score)+"\n")
file_question_scores.close()

scores = open_text_file(path_log_scores)
scores = [float(x) for x in scores]

# make histogram with progress
plt.plot(list(range(len(scores))),scores)
plt.show()
# plt.pause(3)
plt.close()