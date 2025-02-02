def print_top_border(terminal_column_num, terminal_row_num):
    for col in range(terminal_column_num):
        print("-", end="")
    print("")
    for row in range(round(terminal_row_num / 2)):
        print("|", end="")
        for col in range(terminal_column_num - 2):
            print(" ", end="")
        print("|")
    
def print_paragraph(random_paragraph, paragraph_sentence_list, terminal_column_num):
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