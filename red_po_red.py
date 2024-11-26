from grids import grids
from solutions import solutions
from yellow_tile_script import *


def read_grid(string):
    grid = []
    for i in range(5):
        grid.append(list(string[i * 5:i * 5 + 5]))
    return grid


if __name__ == '__main__':
    yellow = 1
    gray = 2
    number = 10
    grid = grids[number]
    solution = solutions[number]
    original_grid = read_grid(grid)
    solution_grid = read_grid(solution)

    total, green = create_dictionaries(solution_grid)
    colors, green = initial_colors(original_grid, solution_grid, total, green)

    swaps = []

    for i in range(5):
        for j in range(5):
            if original_grid[i][j] == solution_grid[i][j]:
                continue
            letter = solution_grid[i][j]
            possible_swaps = []
            for k in range(5):
                for l in range(5):
                    if original_grid[k][l] == letter and colors[k][l] != 0:
                        possible_swaps.append((k, l))
            flag = False
            for k, l in possible_swaps:
                if original_grid[i][j] == solution_grid[k][l]:
                    swaps.append((i, j, k, l))
                    original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
                    colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)
                    flag = True
                    break
            if flag:
                continue

            for k, l in possible_swaps:
                if original_grid[k][l] == solution_grid[i][j] and colors[k][l] != 0:
                    original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
                    if check_yellow(k, l, original_grid, solution_grid, total, green):
                        colors, green = refresh_colors(original_grid, solution_grid, total, green, colors)
                        swaps.append((i, j, k, l))
                        flag = True
                        break
                    else:
                        original_grid[i][j], original_grid[k][l] = original_grid[k][l], original_grid[i][j]
            if flag:
                continue

            swaps.append((i, j) + possible_swaps[0])

    print(swaps)
    print(len(swaps))
