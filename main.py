import os
import math
import asyncio
import generate_sentence

llm = generate_sentence.CodeGenerator()
score = 0
paragraph_list = []
paragraph_sentence_list = []
random_paragraph = ""
paragraph_length = ""

print("Hold On, Generating paragraphs...")
for pos in range(1):
    paragraph_list.append(llm.generate_response())
    
async def add_new_paragraph():
    paragraph_list.append(llm.generate_response())
    
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
    line_length = terminal_column_num - 18
    while len(random_paragraph) > 0:
        break_point = random_paragraph.find(" ", line_length - 10, line_length)
        paragraph_sentence_list.append(random_paragraph[:break_point])
        random_paragraph = random_paragraph.replace(random_paragraph[:break_point], "")
        # print(f"--> {random_paragraph}")
    # number_of_lines = math.ceil(len(random_paragraph)/line_length)
    # for line in range(number_of_lines):
    #     paragraph_sentence_list.append(random_paragraph[((line) * line_length):((line + 1) * line_length)])
    #     # print("|\t", end="")
    #     # print(random_paragraph[((line) * line_length):((line + 1) * line_length)], end="")
    #     # print("\t\t|")
    # for line in paragraph_sentence_list:
    #     print(line + "\n")
    # for line in paragraph_sentence_list:
    #     print(line)
        
        
def print_bottom_border(terminal_column_num, terminal_row_num):
    for col in range(round((terminal_column_num - paragraph_length)/2)):
        print(" ", end="") 
    print("|", end="")
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
    #print(f"\n{random_paragraph}", end="")
    print_paragraph(terminal_column_num)
    #print_bottom_border(terminal_column_num, 4)


print("If you do not reach 50wpm, a random file on your computer will be deleted... Good Luck! Are you ready? Hit enter to begin.")
while True:
    input("")
    random_paragraph = paragraph_list[0] 
    play_game()
    player_input = input("")
    if player_input == random_paragraph:
        score += 1
        print(f"Matches! Score: {score}. Hit Enter to Play Again!")
        paragraph_list.remove[0]
    else: 
        print(f"FAIL. Score: {score}. A file has been deleted...")
        break