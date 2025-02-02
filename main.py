import os
import math
import asyncio
import generate_sentence
import random

llm = generate_sentence.CodeGenerator()
score = 0
paragraph_list = []
paragraph_sentence_list = []
random_paragraph = ""
paragraph_length = ""
    
print("Hold On, Generating paragraphs...")

for p in range(3):
    paragraph_list.append(llm.generate_paragraph())
    
async def add_new_paragraph():
    paragraph_list.append(llm.generate_paragraph())
    
def print_top_border(terminal_column_num, terminal_row_num):
    for col in range(terminal_column_num):
        print("-", end="")
    print("")
    for row in range(round(terminal_row_num / 2)):
        print("|", end="")
        for col in range(terminal_column_num - 2):
            print(" ", end="")
        print("|")
    
def print_paragraph(terminal_column_num):
    paragraph = random_paragraph
    line_length = terminal_column_num - 18
    while len(paragraph) > line_length:
        break_point = paragraph.find(" ", line_length - 10, line_length)
        paragraph_sentence_list.append(paragraph[:(break_point + 1)])
        paragraph = paragraph.replace(paragraph[:(break_point + 1)], "")
    paragraph_sentence_list.append(paragraph)
    for line in paragraph_sentence_list:
        sentence_to_print = ""
        sentence_to_print += "|        "
        sentence_to_print += line
        spaces = (terminal_column_num - (len(sentence_to_print) + 1))
        for pos in range(int(spaces)):
            sentence_to_print += " "
        sentence_to_print += "|"
        print(sentence_to_print)
        
def print_bottom_border(terminal_column_num, terminal_row_num):
    for row in range(round(terminal_row_num / 2)):
        print("|", end="")
        for col in range(terminal_column_num - 2):
            print(" ", end="")
        print("|")
    for col in range(terminal_column_num):
        print("-", end="")
    print("")
    
def play_game():
    
    asyncio.run(add_new_paragraph())
    terminal_column_num = os.get_terminal_size().columns
    terminal_row_num = 4
    
    #print borders 
    print_top_border(terminal_column_num, 4)
    print_paragraph(terminal_column_num)
    print_bottom_border(terminal_column_num, 4)

print("If you do not reach 50wpm, a random file on your computer will be deleted... Good Luck! Are you ready? Hit enter to begin.")
while True:
    random_paragraph = paragraph_list[score]
    paragraph_sentence_list = []
    input("")
    play_game()
    player_input = input("")
    if player_input == random_paragraph:
        score += 1
        print(f"Matches! Score: {score}. Hit Enter to Play Again!")
        print("Generating new sentence...")
    else: 
        print(f"FAIL. Score: {score}. A file has been deleted...")
        break