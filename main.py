import pygame
from grids import grids
from solutions import solutions
import random


def original_grid(number):
    grid = []
    string = grids[number]
    for i in range(5):
        grid.append(list(string[i * 5:i * 5 + 5]))
    print(grid)
    return grid


def solution_grid(number):
    grid = []
    string = solutions[number]
    for i in range(5):
        grid.append(list(string[i * 5:i * 5 + 5]))
    print(grid)
    return grid


def get_fixed_positions(original, solved):
    fixed_pos = []
    for i in range(5):
        for j in range(5):
            if original[i][j] == solved[i][j]:
                fixed_pos.append((i, j))
    return tuple(fixed_pos)


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


# Main game loop
def main():
    random_grid = random.randint(0, 100)
    solved_grid = solution_grid(random_grid)
    movable_grid, fixed_positions = original_grid(random_grid), get_fixed_positions(original_grid(random_grid),
                                                                                    solved_grid)
    selected = None  # Tracks the selected square for dragging

    running = True
    while running:
        screen.fill(WHITE)

        # Draw the colored grid based on correctness
        color_grid(movable_grid, solved_grid)
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
