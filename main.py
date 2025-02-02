import os
import math
import asyncio
import random
import time
import generate_sentence
import printing_functions
import delete_functions
import pygame_game

llm = generate_sentence.CodeGenerator()
score = 0
paragraph_list = []
paragraph_sentence_list = []
random_paragraph = ""
paragraph_length = ""
start = end = 0
 
while True:   
    game_type = input("Would you like to play through the terminal [1] or through pygame [2]? Please enter a number: ")
    if game_type == "1":
        print("Terminal Selected!\n")
        print("Hold On, Generating paragraphs...")
        break
    elif game_type == "2":
        print("PyGame Selected!")
        pygame_game.start_game()
        break
    else:
        print("Invalid input! ", end="")

for p in range(3):
    paragraph_list.append(llm.generate_paragraph())
    
async def add_new_paragraph():
    paragraph_list.append(llm.generate_paragraph())
    
def delete():
    delete_functions.initaite_deletion()
    
def play_game():
    global start_time
    start_time = time.time()
    asyncio.run(add_new_paragraph())
    terminal_column_num = os.get_terminal_size().columns
    terminal_row_num = 4
    
    #print borders 
    printing_functions.print_top_border(terminal_column_num, 4)
    printing_functions.print_paragraph(random_paragraph, paragraph_sentence_list, terminal_column_num)
    printing_functions.print_bottom_border(terminal_column_num, 4)

if game_type == "1":
    print("If you do not reach 50wpm, a random file on your computer will be deleted... Good Luck! Are you ready? Hit enter to begin.")
while True and game_type == "1":
    random_paragraph = paragraph_list[score]
    paragraph_sentence_list = []
    input("")
    play_game()
    player_input = input("")
    
    end_time = time.time()
    time_taken = end_time - start_time
    wpm = round(((len(random_paragraph.split()) / time_taken) * 60), 2)
    print(f"\nWPM: {wpm:.2f}")
    
    if (wpm >= 50 and player_input == random_paragraph):
        score += 1
        print(f"Match! Score: {score}. Hit Enter to Play Again!")
        print("Generating new sentence...")
    elif (wpm < 50 and player_input == random_paragraph):
        print(f"Sentence matches, but wpm was {50 - wpm} too slow! \nScore: {score}. \nA random file has been deleted...")
        delete()
        break
    elif (wpm >= 50 and player_input != random_paragraph):
        print(f"WPM was {wpm - 50} over the minimum, however sentences do not match! \nScore: {score}. \nA random file has been deleted...")
        delete()
        break
    else: 
        print(f"FAIL. Score: {score}. A random file has been deleted...")
        delete()
        break