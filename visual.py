import pygame
from yellow_tile_script import *
from grids import grids
from solutions import solutions
import time
from best_version import main


def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(list(string[i * 5:i * 5 + 5]))
    return grid


pygame.init()

WIDTH, HEIGHT = 500, 500
TILE_SIZE = 80
MARGIN = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waffle Game")

GREEN = (0, 200, 0)
YELLOW = (255, 200, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.Font(None, 60)
number = 10
GRID = read_grid(grids[number])
SOLUTION = read_grid(solutions[number])
total, green = create_dictionaries(SOLUTION)
COLORS, green = initial_colors(GRID, SOLUTION, total, green)

IMMUTABLE_TILES = {(1, 1), (1, 3), (3, 1), (3, 3)}

selected_tile = None


def draw_grid():
    for i, row in enumerate(COLORS):
        for j, c in enumerate(row):
            x = j * (TILE_SIZE + MARGIN) + MARGIN
            y = i * (TILE_SIZE + MARGIN) + MARGIN

            if (i, j) in IMMUTABLE_TILES:
                color = WHITE
            elif c == 0:
                color = GREEN
            elif c == 1:
                color = YELLOW
            else:
                color = GRAY

            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
            letter = GRID[i][j]
            if letter:
                text = FONT.render(letter, True, BLACK)
                text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                screen.blit(text, text_rect)


def swap_tiles(pos1, pos2):
    i1, j1 = pos1
    i2, j2 = pos2

    GRID[i1][j1], GRID[i2][j2] = GRID[i2][j2], GRID[i1][j1]
    global COLORS, green
    COLORS, green = refresh_colors(GRID, SOLUTION, total, green, COLORS)


def grid_to_screen_coordinates(row, col):
    x = col * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2
    y = row * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2
    return x, y


def perform_swap_action(swap_list):
    for command in swap_list:
        _, pos1_str, pos2_str = command.split('_')
        pos1 = (int(pos1_str[0]), int(pos1_str[1]))
        pos2 = (int(pos2_str[0]), int(pos2_str[1]))

        pos1_screen = grid_to_screen_coordinates(*pos1)
        pos2_screen = grid_to_screen_coordinates(*pos2)

        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos1_screen, "button": 1})
        mouse_up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": pos1_screen, "button": 1})
        pygame.event.post(mouse_down_event)
        pygame.event.post(mouse_up_event)

        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": pos2_screen, "button": 1})
        mouse_up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": pos2_screen, "button": 1})
        pygame.event.post(mouse_down_event)
        pygame.event.post(mouse_up_event)

        swap_tiles(pos1, pos2)

        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()

        time.sleep(1)


def v_main():
    global selected_tile
    print(COLORS)
    running = True

    swap_list = main(number)

    perform_swap_action(swap_list)
    FPS = 30
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    v_main()
