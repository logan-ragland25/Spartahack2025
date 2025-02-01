import os


sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "A watched pot never boils.",
    "She sells seashells by the seashore.",
    "Pack my box with five dozen liquor jugs.",
    "How razorback-jumping frogs can level six piqued gymnasts!",
    "I have never seen a purple cow.",
    "The five boxing wizards jump quickly.",
    "Sphinx of black quartz, judge my vow.",
    "Grumpy wizards make toxic brew for the evil queen and jack.",
    "Jackdaws love my big sphinx of quartz.",
    "Crazy Fredrick bought many very exquisite opal jewels.",
    "Waltz, bad nymph, for quick jigs vex.",
    "Jinxed wizards pluck ivy from the big quilt.",
    "The jay, pig, fox, zebra, and my wolves quack!",
    "My girl wove six dozen plaid jackets before breakfast.",
    "Brawny gods just flocked up to quiz and vex him.",
    "Fredrick jumped over the lazy sphinx with zest.",
    "Just keep examining every low bid quoted for zinc etchings.",
    "The wizard quickly jinxed the gnomes before they vanished.",
    "The fog was thick, and the night was dark and silent.",
    "She whispered a secret only the wind could hear.",
    "Lightning flashed, and thunder roared across the valley.",
    "His footsteps echoed in the empty hallway.",
    "The clock ticked, marking the seconds as they passed.",
    "A cat sat on the windowsill, watching the world outside.",
    "The detective found a single clue hidden under the rug.",
    "The river flowed gently, carrying leaves downstream.",
    "A distant train whistle broke the early morning silence.",
    "She traced patterns in the sand with her fingertips.",
    "A book lay open, its pages fluttering in the breeze.",
]

score = 0
random_sentence = ""
sentence_length = ""

def play_game():
    terminal_column_num = os.get_terminal_size().columns
    terminal_row_num = 4
    for col in range(terminal_column_num):
        print("-", end="")
    print("")
    for row in range(round(terminal_row_num / 2)):
        print("|", end="")
        for col in range(terminal_column_num - 2):
            print(" ", end="")
        print("|")
    print("|", end="")
    for col in range(round((terminal_column_num - sentence_length)/2) - 2):
            print(" ", end="")
    print(random_sentence, end="")
    for col in range(round((terminal_column_num - sentence_length)/2)):
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


print("If you do not reach 50wpm, a random file on your computer will be deleted... Good Luck! Are you ready? Hit enter to begin.")
while True:
    input("")
    random_sentence = sentences[0]    
    sentence_length = len(random_sentence)
    play_game()
    player_input = input("")
    if player_input == random_sentence:
        score += 1
        print(f"Matches! Score: {score}. Hit Enter to Play Again!")
    else: 
        print(f"FAIL. Score: {score}. A file has been deleted...")
        break

