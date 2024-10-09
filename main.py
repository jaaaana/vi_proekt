import nltk
from nltk.corpus import words
import random
import pygame

# Ensure you have the NLTK word corpus installed
# nltk.download('words')

# Filter out only five-letter words
word_list = [word.lower() for word in words.words() if len(word) == 5]

# Initialize an empty 5x5 grid with empty spaces (' ')
grid = [[' ' for _ in range(5)] for _ in range(5)]


# Function to get a list of words starting with a specific letter
def get_words_starting_with(letter, word_list):
    return [word for word in word_list if word[0] == letter]


# Function to get words with specific letter at a given position
def get_words_with_letter_at(letter, position, word_list):
    return [word for word in word_list if word[position] == letter]


# Function to assign a word to a row or column
def assign_word_to_grid(word, grid, index, is_horizontal):
    if is_horizontal:
        grid[index] = list(word)  # Assign word horizontally
    else:
        for i in range(5):
            grid[i][index] = word[i]  # Assign word vertically


# Backtracking function to fill the grid based on constraints
def fill_grid_with_constraints(grid, word_list):
    # Step 1: Choose the first random horizontal word (row 0)
    h1 = random.choice(word_list)
    assign_word_to_grid(h1, grid, 0, is_horizontal=True)

    # Step 2: Choose the first vertical word (column 0), starting with h1[0]
    v1_candidates = get_words_starting_with(grid[0][0], word_list)
    for v1 in v1_candidates:
        assign_word_to_grid(v1, grid, 0, is_horizontal=False)

        # Step 3: Choose the second horizontal word (row 2), starting with v1[2]
        h2_candidates = get_words_starting_with(grid[2][0], word_list)
        for h2 in h2_candidates:
            assign_word_to_grid(h2, grid, 2, is_horizontal=True)

            # Step 4: Choose the second vertical word (column 2), starting with h1[2] and matching h2[2]
            v2_candidates = get_words_with_letter_at(grid[0][2], 0, word_list)
            v2_candidates = [w for w in v2_candidates if w[2] == grid[2][2]]
            for v2 in v2_candidates:
                assign_word_to_grid(v2, grid, 2, is_horizontal=False)

                # Step 5: Choose the third horizontal word (row 4), starting with v1[4]
                h3_candidates = get_words_starting_with(grid[4][0], word_list)
                for h3 in h3_candidates:
                    assign_word_to_grid(h3, grid, 4, is_horizontal=True)

                    # Step 6: Choose the third vertical word (column 4), starting with h1[4] and matching h3[2]
                    v3_candidates = get_words_with_letter_at(grid[0][4], 0, word_list)
                    v3_candidates = [w for w in v3_candidates if w[2] == grid[2][4] and w[4] == grid[4][4]]
                    for v3 in v3_candidates:
                        assign_word_to_grid(v3, grid, 4, is_horizontal=False)

                        # If all constraints are satisfied, return the grid
                        return grid

    # If no solution is found, return None (backtracking will trigger)
    return None


# Main function to generate the Waffle puzzle grid
def generate_waffle_grid():
    while True:
        solution = fill_grid_with_constraints(grid, word_list)
        if solution:
            break

    # Print the final grid
    for row in solution:
        print(' '.join(row))


# Generate and print the waffle grid
generate_waffle_grid()

pygame.init()

# Set up the display
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waffle Game")

# Get the filtered word list
word_list = [word.lower() for word in words.words() if len(word) == 5]

# Generate the solution grid using constraint satisfaction (from previous step)
solution_grid = [[' ' for _ in range(5)] for _ in range(5)]  # Placeholder for the solution grid


def generate_solution():
    while True:
        solution = fill_grid_with_constraints(solution_grid, word_list)
        if solution:
            break
        for row in solution:
            print(' '.join(row))
    return solution


# A 5x5 solution grid generated earlier
solution_grid = generate_solution()


# Function to draw the grid
def draw_grid(grid):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)
            letter = grid[row][col]
            if letter != ' ':
                font = pygame.font.Font(None, 74)
                text = font.render(letter.upper(), True, BLACK)
                screen.blit(text, (x + SQUARE_SIZE // 3, y + SQUARE_SIZE // 5))


# Function to color the squares based on correctness
def color_grid(grid, solution_grid):
    for row in range(ROWS):
        for col in range(COLS):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            if grid[row][col] == solution_grid[row][col]:
                color = GREEN  # Correct letter and correct position
            elif grid[row][col] in [solution_grid[row][i] for i in range(5)] or grid[row][col] in [solution_grid[i][col]
                                                                                                   for i in range(5)]:
                color = YELLOW  # Correct letter in the wrong position
            else:
                color = GRAY  # Letter not in the word
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))


# Create the moveable grid by shuffling letters but leaving some in place for hints
def create_movable_grid(solution_grid, num_fixed_letters=5):
    movable_grid = [row[:] for row in solution_grid]  # Deep copy of the solution grid
    fixed_positions = set()

    # Choose a few letters to remain in fixed positions (e.g., 5 random letters)
    while len(fixed_positions) < num_fixed_letters:
        row = random.randint(0, 4)
        col = random.randint(0, 4)
        fixed_positions.add((row, col))

    # Collect letters that are not in fixed positions
    movable_letters = [solution_grid[row][col] for row in range(ROWS) for col in range(COLS) if
                       (row, col) not in fixed_positions]
    random.shuffle(movable_letters)

    # Fill the movable grid with shuffled letters, skipping the fixed positions
    idx = 0
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) not in fixed_positions:
                movable_grid[row][col] = movable_letters[idx]
                idx += 1

    return movable_grid, fixed_positions


# Main game loop
def main():
    movable_grid, fixed_positions = create_movable_grid(solution_grid)
    selected = None  # Tracks the selected square for dragging

    running = True
    while running:
        screen.fill(WHITE)

        # Draw the colored grid based on correctness
        color_grid(movable_grid, solution_grid)
        draw_grid(movable_grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle dragging and dropping of grid squares
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                if (row, col) not in fixed_positions and movable_grid[row][col] != ' ':
                    selected = (row, col)

            if event.type == pygame.MOUSEBUTTONUP:
                if selected:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // SQUARE_SIZE
                    row = pos[1] // SQUARE_SIZE

                    # Swap the letters in the selected and target positions if target is not fixed
                    if (row, col) not in fixed_positions:
                        movable_grid[row][col], movable_grid[selected[0]][selected[1]] = movable_grid[selected[0]][
                            selected[1]], movable_grid[row][col]
                    selected = None

        pygame.display.flip()


# Generate and print the waffle grid
main()
pygame.quit()
